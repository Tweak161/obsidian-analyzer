#!/usr/bin/env python3
"""Process remaining notes in 800_Ressources"""
import json
from pathlib import Path

# Load vault data
with open("vault_analysis.json", "r") as f:
    vault_data = json.load(f)

# Find vault path
vault_path = Path("/mnt/c/Users/hess/OneDrive/Dokumente/MyVault")

# Get remaining notes without summaries
remaining_notes = []
for note_id, metadata in vault_data["notes_metadata"].items():
    path = metadata.get("path", "")
    if path.startswith("800_Ressources/") and not metadata.get("ai_summary"):
        remaining_notes.append((note_id, metadata))

# Sort by path
remaining_notes.sort(key=lambda x: x[1].get("path", ""))

print(f"Remaining notes to process: {len(remaining_notes)}")

# Save list of remaining notes
with open("remaining_notes.json", "w") as f:
    json.dump([{"note_id": n[0], "path": n[1].get("path")} for n in remaining_notes], f, indent=2)

print("List saved to remaining_notes.json")

# Generate next batch prompt
batch_size = 10
batch = remaining_notes[:batch_size]

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

print("\n" + "="*60)
print("NEXT BATCH PROMPT:")
print("="*60)
print(prompt)