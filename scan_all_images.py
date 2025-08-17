#!/usr/bin/env python3
"""
Scan vault for ALL image files and add them to the analysis
"""
import json
import os
from pathlib import Path
from collections import defaultdict

# Load existing analysis
print("Loading existing vault analysis...")
with open('vault_analysis_with_git.json', 'r') as f:
    data = json.load(f)

vault_path = Path("/mnt/c/Users/hess/Lokal/MyVault")
if not vault_path.exists():
    print(f"Error: Vault path does not exist: {vault_path}")
    exit(1)

# Image extensions to look for
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico', '.tiff', '.tif'}

# Get all image files from the vault
print("Scanning for all image files...")
all_images = {}
image_count_by_extension = defaultdict(int)

for root, dirs, files in os.walk(vault_path):
    # Skip hidden directories
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    for file in files:
        file_path = Path(root) / file
        if file_path.suffix.lower() in IMAGE_EXTENSIONS:
            relative_path = file_path.relative_to(vault_path)
            image_path_str = str(relative_path).replace('\\', '/')
            
            # Get file stats
            try:
                stat = file_path.stat()
                all_images[image_path_str] = {
                    'path': image_path_str,
                    'absolute_path': str(file_path),
                    'format': file_path.suffix.lower()[1:],  # Remove the dot
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'filename': file_path.name
                }
                image_count_by_extension[file_path.suffix.lower()] += 1
            except OSError as e:
                print(f"Error accessing {file_path}: {e}")

print(f"\nFound {len(all_images)} total images in vault")
print("Images by format:")
for ext, count in sorted(image_count_by_extension.items()):
    print(f"  {ext}: {count}")

# Now check which images are referenced in notes
print("\nAnalyzing image usage in notes...")
notes_metadata = data.get('notes_metadata', {})
referenced_images = set()
image_usage = defaultdict(list)  # image -> list of notes using it

for note_id, metadata in notes_metadata.items():
    if isinstance(metadata, dict):
        images = metadata.get('images', [])
        for img in images:
            # Normalize the image path
            img_normalized = img.replace('\\', '/')
            referenced_images.add(img_normalized)
            image_usage[img_normalized].append({
                'note_id': note_id,
                'path': metadata.get('path', ''),
                'title': metadata.get('path', '').split('/')[-1]
            })

# Find orphaned images (in vault but not referenced)
orphaned_images = []
for img_path, img_data in all_images.items():
    if img_path not in referenced_images:
        orphaned_images.append(img_data)

# Sort orphaned images by size (largest first)
orphaned_images.sort(key=lambda x: x['size'], reverse=True)

print(f"\nImage usage statistics:")
print(f"  Total images in vault: {len(all_images)}")
print(f"  Referenced images: {len(referenced_images)}")
print(f"  Orphaned images: {len(orphaned_images)}")
print(f"  Total size of orphaned images: {sum(img['size'] for img in orphaned_images) / (1024*1024):.1f} MB")

# Add comprehensive image data to the analysis
data['all_images'] = all_images
data['image_usage'] = dict(image_usage)
data['orphaned_images'] = orphaned_images
data['image_stats'] = {
    'total_images': len(all_images),
    'referenced_images': len(referenced_images),
    'orphaned_images': len(orphaned_images),
    'formats': dict(image_count_by_extension),
    'total_size_mb': round(sum(img['size'] for img in all_images.values()) / (1024*1024), 2),
    'orphaned_size_mb': round(sum(img['size'] for img in orphaned_images) / (1024*1024), 2)
}

# Show top 10 largest orphaned images
if orphaned_images:
    print("\nTop 10 largest orphaned images:")
    for img in orphaned_images[:10]:
        print(f"  {img['filename']} ({img['size_mb']} MB) - {img['path']}")

# Save updated analysis
print("\nSaving updated analysis with comprehensive image data...")
with open('vault_analysis_with_git.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)

print("✓ Analysis updated successfully!")
print(f"\nTo see all images in the dashboard, restart it:")
print("  pkill -f 'python3 dashboard.py' && python3 dashboard.py")