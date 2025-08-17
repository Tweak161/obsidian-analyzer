#!/usr/bin/env python3
"""Process multiple batches of classifications efficiently"""

from ai_classifier import AIClassifier
from pathlib import Path
import json

vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
classifier = AIClassifier(vault_path)

# Get all unclassified files
unclassified_files = []
for file_path in Path(vault_path).rglob('*.md'):
    if '.trash' in str(file_path):
        continue
    
    relative_path = str(file_path.relative_to(vault_path))
    
    # Skip if already classified
    if relative_path in classifier.classifications:
        continue
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(1000)  # First 1000 chars for preview
        
        # Skip empty files
        if not content.strip():
            continue
            
        unclassified_files.append({
            'file_path': relative_path,
            'file_name': file_path.name,
            'content_preview': content[:500]  # Shorter preview
        })
        
    except Exception as e:
        continue

# Calculate how many more we need
current_count = len(classifier.classifications)
target_count = 100
needed = target_count - current_count

print(f"Current classifications: {current_count}")
print(f"Target: {target_count}")
print(f"Still need: {needed}")
print(f"Unclassified files available: {len(unclassified_files)}")

# Show the next files to classify
if needed > 0 and unclassified_files:
    next_batch = unclassified_files[:min(needed, 20)]  # Process up to 20 at a time
    
    print(f"\nNext {len(next_batch)} files to classify:")
    for i, file_info in enumerate(next_batch, 1):
        print(f"{i}. {file_info['file_name']}")
        if '/' in file_info['file_path']:
            print(f"   Path: {file_info['file_path']}")
    
    # Save batch for processing
    with open('next_batch_to_classify.json', 'w') as f:
        json.dump(next_batch, f, indent=2)
    
    print(f"\nBatch saved to next_batch_to_classify.json")
else:
    print("\nTarget reached or no more files to classify!")