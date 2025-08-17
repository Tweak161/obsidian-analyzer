#!/usr/bin/env python3
"""Process all remaining batches and generate summaries"""
import json
from pathlib import Path

# Check which batches need processing
batch_dir = Path("ai_summary_batches")
total_batches = 9

processed = []
unprocessed = []

for i in range(1, total_batches + 1):
    prompt_file = batch_dir / f"batch_{i:03d}_prompt.txt"
    response_file = batch_dir / f"batch_{i:03d}_response.json"
    
    if prompt_file.exists():
        if response_file.exists():
            processed.append(i)
        else:
            unprocessed.append(i)

print(f"Status: {len(processed)} processed, {len(unprocessed)} remaining")
print(f"Processed batches: {processed}")
print(f"Unprocessed batches: {unprocessed}")

# Show next batch to process
if unprocessed:
    next_batch = unprocessed[0]
    prompt_file = batch_dir / f"batch_{next_batch:03d}_prompt.txt"
    print(f"\nNext batch to process: Batch {next_batch}")
    print(f"Prompt file: {prompt_file}")
    
    # Read and display prompt
    with open(prompt_file, 'r') as f:
        content = f.read()
    
    # Show summary of notes in batch
    lines = content.split('\n')
    notes_in_batch = []
    for i, line in enumerate(lines):
        if line.startswith("Note ") and "ID:" in line:
            path_line = lines[i+1] if i+1 < len(lines) else ""
            if "Path:" in path_line:
                path = path_line.split("Path: ")[1].strip()
                notes_in_batch.append(path)
    
    print(f"\nNotes in this batch ({len(notes_in_batch)}):")
    for note in notes_in_batch:
        print(f"  - {note}")