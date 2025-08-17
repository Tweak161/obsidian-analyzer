#!/usr/bin/env python3
"""Fix the note IDs in remaining batches"""
import json
from pathlib import Path

# Load vault data to get correct IDs
with open("vault_analysis.json", "r") as f:
    vault_data = json.load(f)

# Create path to ID mapping
path_to_id = {}
for note_id, metadata in vault_data["notes_metadata"].items():
    path = metadata.get("path", "")
    if path:
        path_to_id[path] = note_id

# Fix batches 4-9
for batch_num in range(4, 10):
    response_file = f"ai_summary_batches/batch_{batch_num:03d}_response.json"
    
    try:
        with open(response_file, 'r') as f:
            data = json.load(f)
        
        # Fix note IDs
        fixed = False
        for summary in data["summaries"]:
            path = summary["path"]
            if path in path_to_id:
                correct_id = path_to_id[path]
                if summary["note_id"] != correct_id:
                    summary["note_id"] = correct_id
                    fixed = True
        
        if fixed:
            # Save fixed version
            with open(response_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Fixed batch {batch_num}")
        else:
            print(f"Batch {batch_num} already correct")
            
    except Exception as e:
        print(f"Error with batch {batch_num}: {e}")

print("\nNow re-import the fixed batches")