#!/usr/bin/env python3
"""Check if AI classifications are in dashboard data"""

import json

# Load the vault analysis data that feeds the dashboard
with open("vault_analysis.json", "r") as f:
    data = json.load(f)

# Check a few notes to see if they have AI data
print("Checking if AI classifications are in dashboard data...\n")

sample_notes = [
    "002_Input/Book List.md",
    "002_Input/MOC - Programming.md",
    "002_Input/Building Block Meals.md"
]

for note_path in sample_notes:
    # Find the note in metadata
    for note_id, metadata in data["notes_metadata"].items():
        if metadata.get("path") == note_path:
            print(f"{note_path}:")
            print(f"  Auto hashtags: {metadata.get('auto_hashtags', [])}")
            print(f"  Keywords: {metadata.get('keywords', [])[:5]}...")  # First 5
            print(f"  AI Summary: {metadata.get('ai_summary', 'No summary')[:80]}...")
            print()
            break

# Check hashtag counts
print("\nTop hashtags in dashboard:")
for hashtag_data in data["hashtags"][:10]:
    print(f"  {hashtag_data['hashtag']}: {hashtag_data['count']} notes")