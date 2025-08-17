#!/usr/bin/env python3
"""
Update existing vault analysis with comprehensive linked content data
"""
import json
import re
from pathlib import Path

print("Loading existing vault analysis...")
with open('vault_analysis_with_git.json', 'r') as f:
    data = json.load(f)

vault_path = Path("/mnt/c/Users/hess/Lokal/MyVault")
notes_metadata = data.get('notes_metadata', {})

# Regex patterns for link extraction
wikilink_pattern = re.compile(r'\[\[([^|\\]]+)(?:\|([^\\]]+))?\]\]')
image_pattern = re.compile(r'!\[\[([^\]]+)\]\]|!\[([^\]]*)\]\(([^\)]+)\)')
markdown_link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
pdf_pattern = re.compile(r'!\[\[([^]]+\.pdf)\]\]', re.IGNORECASE)

def extract_linked_content(file_path: Path, existing_links_out: list) -> dict:
    """Extract all linked content from a markdown file"""
    linked_content = {
        "notes": [],
        "images": [],
        "pdfs": [],
        "urls": [],
        "files": []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use existing links_out data for note links
        for link in existing_links_out:
            # Skip if it's an image, PDF, or other file extension
            if not any(ext in link.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.pdf', '.avif', '.webp', '.mp4', '.mp3']):
                # Also skip single characters or very short links
                if len(link) > 2:
                    linked_content["notes"].append({
                        "title": link,
                        "path": link
                    })
        
        # Extract images
        images = image_pattern.findall(content)
        for img in images:
            img_path = img[0] or img[2]
            if img_path:
                linked_content["images"].append({
                    "path": img_path,
                    "alt": img[1] if len(img) > 1 and img[1] else ""
                })
        
        # Extract standard markdown links
        markdown_links = markdown_link_pattern.findall(content)
        for link_text, link_url in markdown_links:
            # Categorize the link
            if link_url.startswith(('http://', 'https://', 'www.')):
                linked_content["urls"].append({
                    "text": link_text,
                    "url": link_url
                })
            elif link_url.lower().endswith('.pdf'):
                linked_content["pdfs"].append({
                    "text": link_text,
                    "path": link_url
                })
            elif any(link_url.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']):
                # Image link not captured by image pattern
                if link_url not in [img["path"] for img in linked_content["images"]]:
                    linked_content["images"].append({
                        "path": link_url,
                        "alt": link_text
                    })
            else:
                # Other file types
                linked_content["files"].append({
                    "text": link_text,
                    "path": link_url
                })
        
        # Extract embedded PDFs
        pdfs = pdf_pattern.findall(content)
        for pdf in pdfs:
            if pdf not in [p["path"] for p in linked_content["pdfs"]]:
                linked_content["pdfs"].append({
                    "text": pdf.split('/')[-1],
                    "path": pdf
                })
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    
    return linked_content

print(f"Updating linked content for {len(notes_metadata)} notes...")

# Process each note
updated_count = 0
for note_id, metadata in notes_metadata.items():
    if isinstance(metadata, dict) and metadata.get('path'):
        file_path = vault_path / metadata['path']
        if file_path.exists() and file_path.suffix == '.md':
            linked_content = extract_linked_content(file_path, metadata.get('links_out', []))
            metadata['linked_content'] = linked_content
            updated_count += 1
            
            if updated_count % 100 == 0:
                print(f"Processed {updated_count} notes...")

print(f"\nUpdated {updated_count} notes with linked content")

# Show some statistics
total_linked_notes = 0
total_linked_images = 0
total_linked_pdfs = 0
total_linked_urls = 0

for note_id, metadata in notes_metadata.items():
    if isinstance(metadata, dict) and 'linked_content' in metadata:
        lc = metadata['linked_content']
        total_linked_notes += len(lc.get('notes', []))
        total_linked_images += len(lc.get('images', []))
        total_linked_pdfs += len(lc.get('pdfs', []))
        total_linked_urls += len(lc.get('urls', []))

print(f"\nLinked content statistics:")
print(f"  Total linked notes: {total_linked_notes}")
print(f"  Total linked images: {total_linked_images}")
print(f"  Total linked PDFs: {total_linked_pdfs}")
print(f"  Total external URLs: {total_linked_urls}")

# Save updated analysis
print("\nSaving updated analysis...")
with open('vault_analysis_with_git.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)

print("✓ Analysis updated successfully!")
print("\nTo see the linked content in the dashboard, restart it:")
print("  pkill -f 'python3 dashboard.py' && python3 dashboard.py")