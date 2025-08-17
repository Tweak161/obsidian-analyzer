#!/usr/bin/env python3
"""Git history analyzer for Obsidian vault files"""
import subprocess
import json
import os
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime
import concurrent.futures
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class GitHistoryAnalyzer:
    """Analyzes git history for files in the vault"""
    
    def __init__(self, vault_path: str, cache_file: str = "git_history_cache.json"):
        self.vault_path = Path(vault_path)
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.is_git_repo = self._check_git_repo()
        
    def _load_cache(self) -> Dict:
        """Load cached git history data"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def clear_cache(self):
        """Clear the git history cache"""
        self.cache = {}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
    
    def _check_git_repo(self) -> bool:
        """Check if the vault is a git repository"""
        try:
            result = subprocess.run(
                ["git", "-C", str(self.vault_path), "rev-parse", "--git-dir"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def get_file_commit_count(self, file_path: str, use_cache: bool = True) -> int:
        """Get the number of commits for a specific file"""
        if not self.is_git_repo:
            return 0
            
        # Check cache first (if enabled)
        if use_cache and file_path in self.cache:
            return self.cache[file_path].get('commit_count', 0)
        
        try:
            result = subprocess.run(
                ["git", "-C", str(self.vault_path), "rev-list", "--count", "HEAD", "--", file_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip():
                count = int(result.stdout.strip())
                self.cache[file_path] = {'commit_count': count}
                return count
        except Exception as e:
            logger.error(f"Error getting commit count for {file_path}: {e}")
        
        return 0
    
    def get_file_history_details(self, file_path: str, use_cache: bool = True) -> Dict:
        """Get detailed git history for a file"""
        if not self.is_git_repo:
            return {'commit_count': 0}
        
        # Check cache (if enabled)
        if use_cache and file_path in self.cache and 'first_commit' in self.cache[file_path]:
            return self.cache[file_path]
        
        details = {'commit_count': 0}
        
        try:
            # Get commit count
            count_result = subprocess.run(
                ["git", "-C", str(self.vault_path), "rev-list", "--count", "HEAD", "--", file_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if count_result.returncode == 0 and count_result.stdout.strip():
                details['commit_count'] = int(count_result.stdout.strip())
                
                # Get first and last commit dates
                if details['commit_count'] > 0:
                    # First commit
                    first_result = subprocess.run(
                        ["git", "-C", str(self.vault_path), "log", "--reverse", "--format=%ai", "-1", "--", file_path],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if first_result.returncode == 0 and first_result.stdout.strip():
                        details['first_commit'] = first_result.stdout.strip().split()[0]
                    
                    # Last commit
                    last_result = subprocess.run(
                        ["git", "-C", str(self.vault_path), "log", "--format=%ai", "-1", "--", file_path],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if last_result.returncode == 0 and last_result.stdout.strip():
                        details['last_commit'] = last_result.stdout.strip().split()[0]
                        
            self.cache[file_path] = details
            
        except Exception as e:
            logger.error(f"Error getting history details for {file_path}: {e}")
        
        return details
    
    def analyze_files_batch(self, file_paths: list, batch_size: int = 100, max_workers: int = 4) -> Dict[str, Dict]:
        """Analyze multiple files in parallel batches"""
        results = {}
        total = len(file_paths)
        processed = 0
        
        # Process in batches
        for i in range(0, total, batch_size):
            batch = file_paths[i:i + batch_size]
            
            # Use ThreadPoolExecutor for I/O bound git operations
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_file = {
                    executor.submit(self.get_file_history_details, file_path): file_path
                    for file_path in batch
                }
                
                for future in concurrent.futures.as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        result = future.result()
                        results[file_path] = result
                        processed += 1
                        
                        if processed % 50 == 0:
                            print(f"Progress: {processed}/{total} files processed")
                            
                    except Exception as e:
                        logger.error(f"Error processing {file_path}: {e}")
                        results[file_path] = {'commit_count': 0}
            
            # Save cache periodically
            if i % 500 == 0:
                self._save_cache()
        
        # Final cache save
        self._save_cache()
        
        return results
    
    def calculate_git_importance_score(self, commit_count: int) -> float:
        """Calculate importance score based on commit count"""
        # Since most files have 1 commit, adjust scoring to be more granular
        if commit_count == 0:
            return 0.0
        elif commit_count == 1:
            return 0.2  # Base score for tracked files
        elif commit_count == 2:
            return 0.5
        elif commit_count == 3:
            return 0.7
        elif commit_count <= 5:
            return 0.85
        else:  # 6+ commits
            return 1.0
    
    def get_vault_statistics(self, file_paths: list) -> Dict:
        """Get overall git statistics for the vault"""
        if not self.is_git_repo:
            return {
                'total_files': len(file_paths),
                'files_with_history': 0,
                'average_commits': 0,
                'max_commits': 0,
                'most_edited_files': []
            }
        
        # Analyze all files
        results = self.analyze_files_batch(file_paths)
        
        # Calculate statistics
        commit_counts = [r.get('commit_count', 0) for r in results.values()]
        files_with_history = sum(1 for c in commit_counts if c > 0)
        
        # Find most edited files
        file_commits = [(f, r.get('commit_count', 0)) for f, r in results.items()]
        file_commits.sort(key=lambda x: x[1], reverse=True)
        most_edited = file_commits[:10]
        
        stats = {
            'total_files': len(file_paths),
            'files_with_history': files_with_history,
            'average_commits': sum(commit_counts) / len(commit_counts) if commit_counts else 0,
            'max_commits': max(commit_counts) if commit_counts else 0,
            'most_edited_files': [
                {'file': f, 'commits': c} for f, c in most_edited if c > 1
            ]
        }
        
        return stats


def main():
    """Test the git history analyzer"""
    import sys
    
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        vault_path = "//mnt/c/Users/hess/OneDrive/Dokumente/MyVault"
    
    analyzer = GitHistoryAnalyzer(vault_path)
    
    if analyzer.is_git_repo:
        print(f"✓ Vault at {vault_path} is a git repository")
        
        # Test with a sample file
        test_file = "800_Ressources/100_Philosophy/Friedrich Nietzsche - Overview.excalidraw.md"
        details = analyzer.get_file_history_details(test_file)
        print(f"\nTest file: {test_file}")
        print(f"Details: {json.dumps(details, indent=2)}")
        
        # Calculate importance score
        score = analyzer.calculate_git_importance_score(details.get('commit_count', 0))
        print(f"Git importance score: {score}")
    else:
        print(f"✗ Vault at {vault_path} is not a git repository")


if __name__ == "__main__":
    main()