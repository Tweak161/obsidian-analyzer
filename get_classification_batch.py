#!/usr/bin/env python3
"""Get batch of files for classification, excluding trash"""

from ai_classifier import AIClassifier
import json

vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
classifier = AIClassifier(vault_path)

# Get files excluding .trash
batch = []
count = 0
for file_path in classifier.vault_path.rglob('*.md'):
    if '.trash' in str(file_path) or count >= 10:
        continue
    
    relative_path = str(file_path.relative_to(classifier.vault_path))
    
    # Skip if already classified
    if relative_path in classifier.classifications:
        continue
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(3000)  # First 3000 chars
        
        # Skip empty files
        if not content.strip():
            continue
            
        batch.append({
            'file_path': relative_path,
            'file_name': file_path.name,
            'content_preview': content
        })
        count += 1
        
        if count >= 10:  # Get 10 files at a time
            break
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        continue

print(f'Found {len(batch)} files to classify (excluding .trash).')
print('\nFiles to classify:\n')

# Save batch
with open('current_batch.json', 'w') as f:
    json.dump(batch, f)

for i, item in enumerate(batch):
    print(f'{i+1}. {item["file_name"]}')
    if '/' in item["file_path"]:
        print(f'   Folder: {"/".join(item["file_path"].split("/")[:-1])}')
    print()