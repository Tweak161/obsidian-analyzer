#!/usr/bin/env python3
"""
Comprehensive script to process all remaining AI summaries in batches
Shows progress and allows continuation from where it left off
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

def load_vault_data():
    """Load the vault analysis data"""
    with open("vault_analysis.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_vault_data(vault_data):
    """Save the vault analysis data"""
    with open("vault_analysis.json", "w", encoding="utf-8") as f:
        json.dump(vault_data, f, indent=2, ensure_ascii=False)

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

def generate_progress_report(vault_data, folder_filter="800_Ressources"):
    """Generate a progress report"""
    total = 0
    completed = 0
    by_folder = {}
    
    for note_id, metadata in vault_data["notes_metadata"].items():
        path = metadata.get("path", "")
        if path.startswith(folder_filter):
            total += 1
            
            # Extract subfolder
            parts = path.split("/")
            if len(parts) > 1:
                subfolder = parts[1]
            else:
                subfolder = "root"
            
            if subfolder not in by_folder:
                by_folder[subfolder] = {"total": 0, "completed": 0}
            
            by_folder[subfolder]["total"] += 1
            
            if metadata.get("ai_summary"):
                completed += 1
                by_folder[subfolder]["completed"] += 1
    
    return {
        "total": total,
        "completed": completed,
        "remaining": total - completed,
        "by_folder": by_folder
    }

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
                content = f.read()[:1500]  # Limit content for efficiency
        except Exception as e:
            content = f"[Error reading file: {str(e)}]"
        
        prompt += f"\n---\nNote {i} (ID: {note['note_id']})\n"
        prompt += f"Path: {note['path']}\n"
        prompt += f"Name: {Path(note['path']).name}\n\n"
        prompt += f"Content:\n{content}\n"
    
    return prompt

def save_batch_prompt(prompt, batch_num):
    """Save a batch prompt to a file"""
    filename = f"batch_{batch_num}_prompt.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(prompt)
    return filename

def process_batch_response(json_response, vault_data):
    """Process a batch response and update vault data"""
    try:
        response_data = json.loads(json_response)
        updated = 0
        
        for summary in response_data.get("summaries", []):
            note_id = summary.get("note_id")
            if note_id and note_id in vault_data["notes_metadata"]:
                vault_data["notes_metadata"][note_id]["ai_summary"] = summary.get("ai_summary", "")
                vault_data["notes_metadata"][note_id]["ai_hashtags"] = summary.get("ai_hashtags", [])
                vault_data["notes_metadata"][note_id]["ai_keywords"] = summary.get("ai_keywords", [])
                updated += 1
        
        return updated
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return 0

def main():
    """Main processing function"""
    # Configuration
    BATCH_SIZE = 10
    VAULT_PATH = Path("/mnt/c/Users/hess/OneDrive/Dokumente/MyVault")
    
    print("AI Summary Batch Processor")
    print("=" * 60)
    
    # Load vault data
    print("Loading vault data...")
    vault_data = load_vault_data()
    
    # Generate initial progress report
    progress = generate_progress_report(vault_data)
    print(f"\nInitial Status:")
    print(f"  Total notes: {progress['total']}")
    print(f"  Completed: {progress['completed']} ({progress['completed']/progress['total']*100:.1f}%)")
    print(f"  Remaining: {progress['remaining']}")
    
    print("\nBy folder:")
    for folder, stats in sorted(progress['by_folder'].items()):
        pct = stats['completed']/stats['total']*100 if stats['total'] > 0 else 0
        print(f"  {folder}: {stats['completed']}/{stats['total']} ({pct:.1f}%)")
    
    # Get unprocessed notes
    unprocessed = get_all_unprocessed_notes(vault_data)
    
    if not unprocessed:
        print("\nAll notes have been processed!")
        return
    
    print(f"\nFound {len(unprocessed)} notes to process")
    print(f"Processing in batches of {BATCH_SIZE}")
    
    # Process in batches
    total_batches = (len(unprocessed) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(unprocessed))
        batch = unprocessed[start_idx:end_idx]
        
        print(f"\n{'='*60}")
        print(f"BATCH {batch_num + 1} of {total_batches}")
        print(f"Processing notes {start_idx + 1} to {end_idx}")
        print(f"{'='*60}")
        
        # Generate prompt
        prompt = create_batch_prompt(batch, VAULT_PATH)
        
        # Save prompt to file
        prompt_file = save_batch_prompt(prompt, batch_num + 1)
        print(f"\nPrompt saved to: {prompt_file}")
        
        # Show first few lines of the batch
        print("\nNotes in this batch:")
        for note in batch[:5]:
            print(f"  - {note['path']}")
        if len(batch) > 5:
            print(f"  ... and {len(batch) - 5} more")
        
        # Manual processing step
        print("\n" + "-"*60)
        print("MANUAL STEP REQUIRED:")
        print("1. Copy the prompt from the file above")
        print("2. Paste it into your Claude conversation")
        print("3. Save Claude's JSON response to a file")
        print("4. Run: python3 manual_summary_helper.py save <response_file.json>")
        print("-"*60)
        
        # Option to continue or pause
        if batch_num < total_batches - 1:
            user_input = input("\nPress Enter to prepare next batch, or 'q' to quit: ")
            if user_input.lower() == 'q':
                print("\nPausing batch processing. You can resume later.")
                break
    
    print("\n" + "="*60)
    print("Batch preparation complete!")
    print("Remember to import the responses using:")
    print("  python3 manual_summary_helper.py save <response_file.json>")
    
    # Final status
    print("\nTo check final progress after importing, run:")
    print("  python3 show_progress.py")

if __name__ == "__main__":
    main()