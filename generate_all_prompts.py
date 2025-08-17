#!/usr/bin/env python3
"""Generate all prompts for 800_Ressources folder"""
import json
from pathlib import Path

# Load vault data
with open("vault_analysis.json", "r") as f:
    vault_data = json.load(f)

# Find vault path
vault_path = Path("/mnt/c/Users/hess/OneDrive/Dokumente/MyVault")

# Get all notes without summaries
notes_to_process = []
for note_id, metadata in vault_data["notes_metadata"].items():
    path = metadata.get("path", "")
    if path.startswith("800_Ressources/") and not metadata.get("ai_summary"):
        notes_to_process.append((note_id, metadata))

# Sort by path for better organization
notes_to_process.sort(key=lambda x: x[1].get("path", ""))

print(f"Total notes to process: {len(notes_to_process)}")
print(f"Processing in batches of 10...\n")

# Process in batches of 10
batch_size = 10
for batch_num in range(0, len(notes_to_process), batch_size):
    batch = notes_to_process[batch_num:batch_num + batch_size]
    
    print(f"\n{'='*60}")
    print(f"BATCH {batch_num//batch_size + 1} ({batch_num + 1}-{min(batch_num + batch_size, len(notes_to_process))} of {len(notes_to_process)})")
    print(f"{'='*60}\n")
    
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
                content = f.read()[:2000]  # First 2000 chars
        except:
            content = "[Error reading file]"
        
        prompt += f"\n---\nNote {i} (ID: {note_id})\nPath: {path}\nName: {Path(path).name}\n\nContent:\n{content}\n"
    
    # Save prompt to file
    prompt_file = f"prompt_batch_{batch_num//batch_size + 1}.txt"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"Prompt saved to: {prompt_file}")
    
    if batch_num + batch_size < len(notes_to_process):
        input("\nPress Enter for next batch...")

print("\nAll prompts generated!")