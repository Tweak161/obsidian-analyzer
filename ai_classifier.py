#!/usr/bin/env python3
"""
AI-powered classification system for Obsidian notes
Supports both manual classification and API-based classification
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import pickle

try:
    import anthropic
except ImportError:
    anthropic = None
    print("Note: anthropic package not installed. API classification will not be available.")


@dataclass
class NoteClassification:
    """Classification data for a single note"""
    file_path: str
    file_hash: str
    last_modified: str
    ai_hashtags: List[str]
    ai_keywords: List[str]
    ai_summary: str
    classification_date: str
    model_used: str = "claude-3-sonnet"


class AIClassifier:
    """AI-powered classifier for Obsidian notes"""
    
    def __init__(self, vault_path: str, api_key: Optional[str] = None):
        self.vault_path = Path(vault_path)
        self.api_key = api_key
        self.classifications_file = self.vault_path.parent / "ai_classifications.json"
        self.classifications = self._load_classifications()
        
        # Initialize API client if key provided
        self.client = None
        if api_key and anthropic:
            self.client = anthropic.Anthropic(api_key=api_key)
        elif api_key and not anthropic:
            print("Warning: anthropic package not installed. Install with: pip install anthropic")
    
    def _load_classifications(self) -> Dict[str, NoteClassification]:
        """Load existing classifications from file"""
        if self.classifications_file.exists():
            try:
                with open(self.classifications_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return {
                        path: NoteClassification(**item) 
                        for path, item in data.items()
                    }
            except Exception as e:
                print(f"Error loading classifications: {e}")
        return {}
    
    def _save_classifications(self):
        """Save classifications to file"""
        data = {
            path: asdict(classification)
            for path, classification in self.classifications.items()
        }
        with open(self.classifications_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate file hash"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def _prepare_prompt(self, content: str, file_name: str) -> str:
        """Prepare prompt for AI classification"""
        return f"""Please analyze this Obsidian note and provide:
1. Up to 5 relevant hashtags (from: #book, #AI, #meditation, #spirituality, #philosophy, #productivity, #programming, #health, #finance, #psychology, #relationship, #career, #education, #travel, #creativity, #science, #technology, #business, #writing, #personal, or suggest new ones if needed)
2. 5-10 key concepts/keywords (single words or short phrases)
3. A 1-2 sentence summary of the content

File name: {file_name}

Content (first 3000 characters):
{content[:3000]}

Please respond in this JSON format:
{{
    "hashtags": ["#tag1", "#tag2"],
    "keywords": ["keyword1", "keyword2"],
    "summary": "Brief summary of the note"
}}"""
    
    def classify_with_api(self, file_path: Path) -> Optional[NoteClassification]:
        """Classify a single file using the Claude API"""
        if not self.client:
            print("API client not initialized. Please provide API key.")
            return None
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Prepare prompt
            prompt = self._prepare_prompt(content, file_path.name)
            
            # Call Claude API
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse response
            result = json.loads(response.content[0].text)
            
            # Create classification
            classification = NoteClassification(
                file_path=str(file_path.relative_to(self.vault_path)),
                file_hash=self._get_file_hash(file_path),
                last_modified=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                ai_hashtags=result.get("hashtags", []),
                ai_keywords=result.get("keywords", []),
                ai_summary=result.get("summary", ""),
                classification_date=datetime.now().isoformat(),
                model_used="claude-3-sonnet-20240229"
            )
            
            return classification
            
        except Exception as e:
            print(f"Error classifying {file_path}: {e}")
            return None
    
    def prepare_batch_for_manual_classification(self, num_files: int = 10) -> List[Dict]:
        """Prepare a batch of files for manual classification"""
        batch = []
        
        # Find unclassified or changed files
        for file_path in self.vault_path.rglob("*.md"):
            if len(batch) >= num_files:
                break
                
            relative_path = str(file_path.relative_to(self.vault_path))
            current_hash = self._get_file_hash(file_path)
            
            # Check if needs classification
            if (relative_path not in self.classifications or 
                self.classifications[relative_path].file_hash != current_hash):
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    batch.append({
                        "file_path": relative_path,
                        "file_name": file_path.name,
                        "content_preview": content[:3000],
                        "prompt": self._prepare_prompt(content, file_path.name)
                    })
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
        
        return batch
    
    def add_manual_classification(self, file_path: str, hashtags: List[str], 
                                keywords: List[str], summary: str):
        """Add a manual classification"""
        full_path = self.vault_path / file_path
        
        classification = NoteClassification(
            file_path=file_path,
            file_hash=self._get_file_hash(full_path),
            last_modified=datetime.fromtimestamp(full_path.stat().st_mtime).isoformat(),
            ai_hashtags=hashtags,
            ai_keywords=keywords,
            ai_summary=summary,
            classification_date=datetime.now().isoformat(),
            model_used="manual"
        )
        
        self.classifications[file_path] = classification
        self._save_classifications()
    
    def classify_vault(self, limit: Optional[int] = None):
        """Classify all files in vault (requires API key)"""
        if not self.client:
            print("API client not initialized. Please provide API key.")
            return
        
        processed = 0
        for file_path in self.vault_path.rglob("*.md"):
            if limit and processed >= limit:
                break
                
            relative_path = str(file_path.relative_to(self.vault_path))
            current_hash = self._get_file_hash(file_path)
            
            # Skip if already classified and unchanged
            if (relative_path in self.classifications and 
                self.classifications[relative_path].file_hash == current_hash):
                continue
            
            print(f"Classifying: {relative_path}")
            classification = self.classify_with_api(file_path)
            
            if classification:
                self.classifications[relative_path] = classification
                processed += 1
                
                # Save periodically
                if processed % 10 == 0:
                    self._save_classifications()
        
        # Final save
        self._save_classifications()
        print(f"Classified {processed} files")
    
    def export_for_analyzer(self) -> Dict:
        """Export classifications in format compatible with obsidian_analyzer"""
        export_data = {}
        
        for file_path, classification in self.classifications.items():
            export_data[file_path] = {
                "ai_hashtags": classification.ai_hashtags,
                "ai_keywords": classification.ai_keywords,
                "ai_summary": classification.ai_summary
            }
        
        return export_data


def main():
    """Example usage"""
    vault_path = r"/mnt/c/Users/hess/OneDrive/Dokumente/MyVault"
    
    # For manual classification
    classifier = AIClassifier(vault_path)
    
    # Prepare batch for manual classification
    batch = classifier.prepare_batch_for_manual_classification(5)
    
    print("Files ready for manual classification:")
    for i, item in enumerate(batch):
        print(f"\n{i+1}. {item['file_name']}")
        print(f"Path: {item['file_path']}")
        print("\nPrompt to use with Claude:")
        print("-" * 80)
        print(item['prompt'])
        print("-" * 80)
    
    # Example: To use with API (uncomment and add your API key)
    # api_key = "your-api-key-here"
    # classifier = AIClassifier(vault_path, api_key)
    # classifier.classify_vault(limit=10)  # Classify first 10 files


if __name__ == "__main__":
    main()