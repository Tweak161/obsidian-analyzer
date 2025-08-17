#!/usr/bin/env python3
"""Process all truly remaining notes that don't have AI summaries yet"""
import json
from pathlib import Path

# Load vault data
with open("vault_analysis.json", "r") as f:
    vault_data = json.load(f)

vault_path = Path("/mnt/c/Users/hess/OneDrive/Dokumente/MyVault")

# Get ONLY notes without AI summaries
remaining_notes = []
for note_id, metadata in vault_data["notes_metadata"].items():
    path = metadata.get("path", "")
    if path.startswith("800_Ressources/") and not metadata.get("ai_summary"):
        remaining_notes.append({
            "note_id": note_id,
            "path": path,
            "metadata": metadata
        })

# Sort by path
remaining_notes.sort(key=lambda x: x["path"])

print(f"Found {len(remaining_notes)} notes without AI summaries")

# Process in batches of 10
batch_size = 10
total_batches = (len(remaining_notes) + batch_size - 1) // batch_size

for batch_num in range(total_batches):
    start_idx = batch_num * batch_size
    end_idx = min(start_idx + batch_size, len(remaining_notes))
    batch = remaining_notes[start_idx:end_idx]
    
    print(f"\n{'='*60}")
    print(f"FINAL BATCH {batch_num + 1} of {total_batches} (Notes {start_idx + 1}-{end_idx})")
    print(f"{'='*60}")
    
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
    
    for i, note in enumerate(batch, 1):
        note_path = vault_path / note["path"]
        
        try:
            with open(note_path, 'r', encoding='utf-8') as f:
                content = f.read()[:1500]
        except Exception as e:
            content = f"[Error reading file: {str(e)}]"
        
        prompt += f"\n---\nNote {i} (ID: {note['note_id']})\n"
        prompt += f"Path: {note['path']}\n"
        prompt += f"Name: {Path(note['path']).name}\n\n"
        prompt += f"Content:\n{content}\n"
    
    # Save prompt
    filename = f"final_batch_{batch_num + 1:02d}_prompt.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    print(f"Saved prompt to: {filename}")
    print("Notes in this batch:")
    for note in batch:
        print(f"  - {note['note_id']}")

print(f"\n{'='*60}")
print("Summary:")
print(f"  Total remaining notes: {len(remaining_notes)}")
print(f"  Generated {total_batches} batch prompts")
print("\nThese prompts contain ONLY notes that don't have AI summaries yet.")