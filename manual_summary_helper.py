#!/usr/bin/env python3
"""
Manual Summary Helper - Generate summaries through Claude Code conversation
This script prepares prompts that you can paste into your Claude conversation
"""

import json
import sys
from pathlib import Path
from typing import List, Dict

def load_vault_analysis() -> dict:
    """Load the vault analysis data"""
    with open("vault_analysis.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_notes_for_folder(vault_data: dict, folder: str) -> List[Dict]:
    """Get notes from specific folder that need summaries"""
    # Try to find vault path - check common locations
    vault_path = None
    possible_paths = [
        Path.home() / "OneDrive" / "Dokumente" / "MyVault",
        Path.home() / "Documents" / "MyVault", 
        Path.home() / "MyVault",
        Path.home() / "Obsidian" / "MyVault",
        Path("/mnt/c/Users/hess/OneDrive/Dokumente/MyVault"),
        Path("/mnt/c/Users/thomas/OneDrive/Dokumente/MyVault"),
        Path.cwd().parent / "MyVault",
        Path.cwd().parent / "002_Slipbox"
    ]
    
    # Try to find a valid vault path by checking if a known note exists
    sample_note = None
    for _, metadata in vault_data["notes_metadata"].items():
        if metadata.get("path", "").startswith(folder):
            sample_note = metadata.get("path")
            break
    
    if sample_note:
        for possible_path in possible_paths:
            if (possible_path / sample_note).exists():
                vault_path = possible_path
                print(f"Found vault at: {vault_path}")
                break
    
    if not vault_path:
        # Fall back to current directory
        vault_path = Path.cwd()
        print(f"Warning: Could not find vault path, using current directory: {vault_path}")
    
    notes = []
    
    for note_id, metadata in vault_data["notes_metadata"].items():
        path = metadata.get("path", "")
        if path.startswith(folder) and not metadata.get("ai_summary"):
            full_path = vault_path / path
            if full_path.exists():
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    notes.append({
                        "path": path,
                        "name": Path(path).name,
                        "content": content[:3000],  # First 3000 chars
                        "note_id": note_id
                    })
                except Exception as e:
                    print(f"Error reading {path}: {e}")
    
    return notes

def generate_prompt_for_batch(notes: List[Dict]) -> str:
    """Generate a prompt for Claude to process multiple notes"""
    prompt = """Please analyze these Obsidian notes and provide for EACH note:
1. A 1-2 sentence summary
2. Up to 5 relevant hashtags (from: #book, #journal, #moc, #AI, #meditation, #spirituality, #philosophy, #productivity, #programming, #health, #finance, #psychology, #relationship, #career, #education, #travel, #creativity, #science, #technology, #business, #writing, #personal)
   - Use #book for book summaries or notes about books
   - Use #journal for personal journal entries or reflections
   - Use #moc for "Map of Content" notes that organize and link to other notes
3. 5-10 key concepts/keywords

Please respond in this exact JSON format:
```json
{
  "summaries": [
    {
      "note_id": "NOTE_ID_HERE",
      "path": "PATH_HERE",
      "ai_summary": "Brief summary here",
      "ai_hashtags": ["#tag1", "#tag2"],
      "ai_keywords": ["keyword1", "keyword2"]
    }
  ]
}
```

Here are the notes to analyze:

"""
    
    for i, note in enumerate(notes, 1):
        prompt += f"\n---\nNote {i} (ID: {note['note_id']})\nPath: {note['path']}\nName: {note['name']}\n\nContent:\n{note['content']}\n"
    
    return prompt

def save_manual_summaries(summaries_json: str, vault_data: dict):
    """Save manually generated summaries back to vault analysis"""
    try:
        summaries = json.loads(summaries_json)
        
        updated = 0
        for item in summaries.get("summaries", []):
            note_id = item.get("note_id")
            if note_id and note_id in vault_data["notes_metadata"]:
                vault_data["notes_metadata"][note_id]["ai_summary"] = item.get("ai_summary", "")
                vault_data["notes_metadata"][note_id]["ai_hashtags"] = item.get("ai_hashtags", [])
                vault_data["notes_metadata"][note_id]["ai_keywords"] = item.get("ai_keywords", [])
                updated += 1
        
        # Save updated vault analysis
        with open("vault_analysis.json", "w", encoding="utf-8") as f:
            json.dump(vault_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Successfully updated {updated} notes with AI summaries!")
        return True
        
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 manual_summary_helper.py <command> [args]")
        print("\nCommands:")
        print("  generate <folder> [batch_size]  - Generate prompts for manual summarization")
        print("  save <json_file>               - Save summaries from Claude's response")
        print("\nExample:")
        print("  python3 manual_summary_helper.py generate 800_Ressources 5")
        print("  python3 manual_summary_helper.py save summaries.json")
        return
    
    command = sys.argv[1]
    vault_data = load_vault_analysis()
    
    if command == "generate":
        folder = sys.argv[2] if len(sys.argv) > 2 else "800_Ressources"
        batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        
        notes = get_notes_for_folder(vault_data, folder)
        print(f"Found {len(notes)} notes in {folder} without AI summaries")
        
        if not notes:
            print("All notes already have summaries!")
            return
        
        # Process in batches
        for i in range(0, len(notes), batch_size):
            batch = notes[i:i+batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(notes) + batch_size - 1) // batch_size
            
            print(f"\n{'='*60}")
            print(f"BATCH {batch_num} of {total_batches}")
            print(f"{'='*60}")
            print("\nCopy the following prompt and paste it into your Claude conversation:")
            print("-" * 60)
            print(generate_prompt_for_batch(batch))
            print("-" * 60)
            
            if batch_num < total_batches:
                input("\nPress Enter to see the next batch...")
    
    elif command == "save":
        if len(sys.argv) < 3:
            print("Please provide the JSON file path")
            return
        
        json_file = sys.argv[2]
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                summaries_json = f.read()
            
            if save_manual_summaries(summaries_json, vault_data):
                print("Restart the dashboard to see the AI summaries!")
        except FileNotFoundError:
            print(f"File not found: {json_file}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()