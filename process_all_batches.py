#!/usr/bin/env python3
"""Process all remaining batches at once"""
import json
from pathlib import Path

# Import all processed responses
batch_files = [
    "batch_001_response.json",
    "batch_002_response.json"
]

all_summaries = []

for batch_file in batch_files:
    file_path = Path("ai_summary_batches") / batch_file
    if file_path.exists():
        with open(file_path, 'r') as f:
            data = json.load(f)
            all_summaries.extend(data["summaries"])

print(f"Collected {len(all_summaries)} summaries from {len(batch_files)} batches")

# Import them all at once
import sys
sys.path.append('..')
from manual_summary_helper import save_manual_summaries, load_vault_data

vault_data = load_vault_data()

# Create combined response
combined_response = json.dumps({"summaries": all_summaries}, indent=2)

# Save all summaries
if save_manual_summaries(combined_response, vault_data):
    print("All summaries imported successfully!")
else:
    print("Error importing summaries")