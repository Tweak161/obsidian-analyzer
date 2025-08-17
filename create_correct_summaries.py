#!/usr/bin/env python3
"""Create correct summaries based on actual batch contents"""
import json
from pathlib import Path

# Read each batch prompt to get actual notes
for batch_num in range(4, 10):
    prompt_file = f"ai_summary_batches/batch_{batch_num:03d}_prompt.txt"
    
    with open(prompt_file, 'r') as f:
        content = f.read()
    
    # Extract notes from prompt
    lines = content.split('\n')
    notes = []
    
    i = 0
    while i < len(lines):
        if lines[i].startswith("Note ") and "ID:" in lines[i]:
            # Extract ID
            id_part = lines[i].split("ID: ")[1].strip()
            note_id = id_part.rstrip(")")
            
            # Extract path (next line)
            i += 1
            if i < len(lines) and "Path:" in lines[i]:
                path = lines[i].split("Path: ")[1].strip()
                
                # Extract name
                i += 1
                if i < len(lines) and "Name:" in lines[i]:
                    name = lines[i].split("Name: ")[1].strip()
                    
                    notes.append({
                        "note_id": note_id,
                        "path": path,
                        "name": name
                    })
        i += 1
    
    print(f"\nBatch {batch_num}: Found {len(notes)} notes")
    for note in notes[:3]:
        print(f"  - {note['note_id']}")

# Now check what's actually needed
print("\nChecking which notes still need summaries...")
with open("vault_analysis.json", "r") as f:
    vault_data = json.load(f)

remaining = []
for note_id, metadata in vault_data["notes_metadata"].items():
    path = metadata.get("path", "")
    if path.startswith("800_Ressources/") and not metadata.get("ai_summary"):
        remaining.append(note_id)

print(f"\nTotal remaining without summaries: {len(remaining)}")
print("First 10:")
for r in remaining[:10]:
    print(f"  - {r}")