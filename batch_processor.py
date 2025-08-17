#!/usr/bin/env python3
"""Batch processor for AI summaries"""
import json
import sys
from pathlib import Path

def get_next_batch(batch_size=10):
    """Get the next batch of notes to process"""
    # Load vault data
    with open("vault_analysis.json", "r") as f:
        vault_data = json.load(f)
    
    # Find vault path
    vault_path = Path("/mnt/c/Users/hess/OneDrive/Dokumente/MyVault")
    
    # Get remaining notes
    remaining = []
    for note_id, metadata in vault_data["notes_metadata"].items():
        path = metadata.get("path", "")
        if path.startswith("800_Ressources/") and not metadata.get("ai_summary"):
            remaining.append((note_id, metadata))
    
    # Sort and take batch
    remaining.sort(key=lambda x: x[1].get("path", ""))
    batch = remaining[:batch_size]
    
    if not batch:
        print("All notes have been processed!")
        return None
    
    # Generate prompt
    prompt = """Please analyze these Obsidian notes and provide for EACH note:
1. A 1-2 sentence summary
2. Up to 5 relevant hashtags (from: #book, #AI, #meditation, #spirituality, #philosophy, #productivity, #programming, #health, #finance, #psychology, #relationship, #career, #education, #travel, #creativity, #science, #technology, #business, #writing, #personal)
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
    
    for i, (note_id, metadata) in enumerate(batch, 1):
        path = metadata.get("path", "")
        full_path = vault_path / path
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()[:1500]  # Reduced size for efficiency
        except:
            content = "[Error reading file]"
        
        prompt += f"\n---\nNote {i} (ID: {note_id})\nPath: {path}\nName: {Path(path).name}\n\nContent:\n{content}\n"
    
    return prompt, len(remaining)

if __name__ == "__main__":
    batch_size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    result = get_next_batch(batch_size)
    
    if result:
        prompt, total_remaining = result
        print(f"Remaining notes: {total_remaining}")
        print(f"Processing batch of {min(batch_size, total_remaining)} notes")
        print("\n" + "="*60)
        print("COPY THIS PROMPT:")
        print("="*60)
        print(prompt)