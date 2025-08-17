#!/usr/bin/env python3
"""
Automated batch processor that generates all prompts at once
and saves them for sequential processing
"""

import json
import os
from pathlib import Path
from datetime import datetime

def load_vault_data():
    """Load the vault analysis data"""
    with open("vault_analysis.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_all_unprocessed_notes(vault_data, folder_filter="800_Ressources"):
    """Get all notes that need AI summaries"""
    unprocessed = []
    
    for note_id, metadata in vault_data["notes_metadata"].items():
        path = metadata.get("path", "")
        
        # Filter by folder
        if not path.startswith(folder_filter):
            continue
        
        # Skip if already has AI summary
        if metadata.get("ai_summary"):
            continue
            
        unprocessed.append({
            "note_id": note_id,
            "path": path,
            "metadata": metadata
        })
    
    # Sort by path for better organization
    unprocessed.sort(key=lambda x: x["path"])
    
    return unprocessed

def create_batch_prompt(notes_batch, vault_path):
    """Create a prompt for a batch of notes"""
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
    
    for i, note in enumerate(notes_batch, 1):
        note_path = Path(vault_path) / note["path"]
        
        try:
            with open(note_path, 'r', encoding='utf-8') as f:
                content = f.read()[:1200]  # Limit content for efficiency
        except Exception as e:
            content = f"[Error reading file: {str(e)}]"
        
        prompt += f"\n---\nNote {i} (ID: {note['note_id']})\n"
        prompt += f"Path: {note['path']}\n"
        prompt += f"Name: {Path(note['path']).name}\n\n"
        prompt += f"Content:\n{content}\n"
    
    return prompt

def main():
    """Main processing function"""
    # Configuration
    BATCH_SIZE = 10
    VAULT_PATH = Path("/mnt/c/Users/hess/OneDrive/Dokumente/MyVault")
    OUTPUT_DIR = Path("ai_summary_batches")
    
    print("Automated AI Summary Batch Generator")
    print("=" * 60)
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Load vault data
    print("Loading vault data...")
    vault_data = load_vault_data()
    
    # Get unprocessed notes
    unprocessed = get_all_unprocessed_notes(vault_data)
    
    if not unprocessed:
        print("\nAll notes have been processed!")
        return
    
    print(f"\nFound {len(unprocessed)} notes to process")
    
    # Generate progress by folder
    by_folder = {}
    for note in unprocessed:
        parts = note["path"].split("/")
        folder = parts[1] if len(parts) > 1 else "root"
        if folder not in by_folder:
            by_folder[folder] = 0
        by_folder[folder] += 1
    
    print("\nUnprocessed notes by folder:")
    for folder, count in sorted(by_folder.items()):
        print(f"  {folder}: {count}")
    
    print(f"\nGenerating batches of {BATCH_SIZE} notes each...")
    
    # Process in batches
    total_batches = (len(unprocessed) + BATCH_SIZE - 1) // BATCH_SIZE
    batch_info = []
    
    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(unprocessed))
        batch = unprocessed[start_idx:end_idx]
        
        # Generate prompt
        prompt = create_batch_prompt(batch, VAULT_PATH)
        
        # Save prompt to file
        batch_file = OUTPUT_DIR / f"batch_{batch_num + 1:03d}_prompt.txt"
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        # Save batch info
        batch_info.append({
            "batch_num": batch_num + 1,
            "prompt_file": str(batch_file),
            "notes_count": len(batch),
            "notes": [{"note_id": n["note_id"], "path": n["path"]} for n in batch]
        })
        
        print(f"  Batch {batch_num + 1}: {len(batch)} notes -> {batch_file.name}")
    
    # Save batch index
    index_file = OUTPUT_DIR / "batch_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump({
            "total_batches": total_batches,
            "total_notes": len(unprocessed),
            "batch_size": BATCH_SIZE,
            "created_at": datetime.now().isoformat(),
            "batches": batch_info
        }, f, indent=2)
    
    print(f"\n✓ Generated {total_batches} batch files in '{OUTPUT_DIR}' directory")
    print(f"✓ Batch index saved to: {index_file}")
    
    # Create processing script
    process_script = OUTPUT_DIR / "process_next_batch.sh"
    with open(process_script, 'w') as f:
        f.write("""#!/bin/bash
# Script to process the next unprocessed batch

# Find the next unprocessed batch
for i in {001..999}; do
    PROMPT_FILE="batch_${i}_prompt.txt"
    RESPONSE_FILE="batch_${i}_response.json"
    
    if [ -f "$PROMPT_FILE" ] && [ ! -f "$RESPONSE_FILE" ]; then
        echo "Next batch to process: $PROMPT_FILE"
        echo ""
        echo "Steps:"
        echo "1. Copy the content of $PROMPT_FILE"
        echo "2. Paste into Claude conversation"
        echo "3. Save response to $RESPONSE_FILE"
        echo "4. Run: python3 ../manual_summary_helper.py save $RESPONSE_FILE"
        echo ""
        echo "Opening prompt file..."
        cat "$PROMPT_FILE"
        break
    fi
done

if [ ! -f "$PROMPT_FILE" ]; then
    echo "All batches have been processed!"
fi
""")
    os.chmod(process_script, 0o755)
    
    print(f"\nNext steps:")
    print(f"1. cd {OUTPUT_DIR}")
    print(f"2. ./process_next_batch.sh")
    print(f"3. Copy prompt, paste to Claude, save response")
    print(f"4. Repeat until all batches are processed")
    
    print(f"\nAlternatively, I can process all batches now if you'd like.")

if __name__ == "__main__":
    main()