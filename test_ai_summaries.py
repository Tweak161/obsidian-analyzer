#!/usr/bin/env python3
import json

# Load the vault analysis data
with open('vault_analysis.json', 'r') as f:
    data = json.load(f)

notes_metadata = data.get('notes_metadata', {})

# Test with a specific note we know has AI summary
test_notes = [
    "800_Ressources/100_Philosophy/Albert Camus",
    "800_Ressources/100_Philosophy/Albert Camus.md",
    "800_Ressources/100_Philosophy/Buddha.excalidraw",
    "800_Ressources/100_Philosophy/Buddha.excalidraw.md"
]

print("=== Testing note lookup ===")
for test_note in test_notes:
    print(f"\nTrying key: '{test_note}'")
    if test_note in notes_metadata:
        metadata = notes_metadata[test_note]
        print(f"  ✓ Found in notes_metadata")
        print(f"  Path field: {metadata.get('path', 'NO PATH')}")
        print(f"  Has ai_summary: {bool(metadata.get('ai_summary'))}")
        if metadata.get('ai_summary'):
            print(f"  AI summary preview: {metadata['ai_summary'][:50]}...")
    else:
        print(f"  ✗ NOT found in notes_metadata")

# Show all 800_Ressources notes with AI summaries
print("\n\n=== All 800_Ressources notes with AI summaries ===")
count = 0
for note_id, metadata in notes_metadata.items():
    if '800_Ressources' in note_id and isinstance(metadata, dict) and metadata.get('ai_summary'):
        print(f"\nNote ID: {note_id}")
        print(f"Path: {metadata.get('path', 'NO PATH')}")
        print(f"AI Summary: {metadata['ai_summary'][:60]}...")
        count += 1
        if count >= 5:
            print(f"\n... and {sum(1 for k, v in notes_metadata.items() if '800_Ressources' in k and isinstance(v, dict) and v.get('ai_summary')) - 5} more")
            break