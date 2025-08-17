#!/usr/bin/env python3
"""Get batch of files from 800_Ressources for AI classification"""

import json
from pathlib import Path

# Load vault analysis
with open("vault_analysis.json", "r") as f:
    vault_data = json.load(f)

vault_path = Path(r"/mnt/c/Users/hess/OneDrive/Dokumente/MyVault")

# Get all unclassified notes from 800_Ressources
batch = []
count = 0

for note_id, metadata in vault_data["notes_metadata"].items():
    path = metadata.get("path", "")
    
    # Check if in 800_Ressources and has no AI summary
    if path.startswith("800_Ressources/") and not metadata.get("ai_summary"):
        full_path = vault_path / path
        
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read(3000)  # First 3000 chars
                
                # Skip empty files
                if content.strip():
                    batch.append({
                        'file_path': path,
                        'file_name': full_path.name,
                        'content_preview': content
                    })
                    count += 1
                    
                    if count >= 10:  # Process 10 at a time
                        break
                        
            except Exception as e:
                print(f"Error reading {path}: {e}")
                continue

print(f'Found {len(batch)} unclassified files in 800_Ressources')
print('\nFiles to classify:\n')

for item in batch:
    print(f"- {item['file_path']}")

# Save batch
with open('800_ressources_batch.json', 'w', encoding='utf-8') as f:
    json.dump(batch, f, ensure_ascii=False, indent=2)

print(f"\nBatch saved to 800_ressources_batch.json")
print("\nNow you can manually create classifications or use the AI API if you have a key set.")