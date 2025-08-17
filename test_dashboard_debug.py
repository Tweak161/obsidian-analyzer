#!/usr/bin/env python3
"""Test the dashboard hashtag functionality"""
import json

# Load the data
with open('vault_analysis.json', 'r') as f:
    data = json.load(f)

notes_metadata = data.get('notes_metadata', {})
hashtags_data = data.get('hashtags', [])

# Find a hashtag that has notes with AI summaries
test_hashtag = None
for h in hashtags_data:
    hashtag = h['hashtag']
    # Check if any notes with this hashtag have AI summaries
    for note_id, metadata in notes_metadata.items():
        if hashtag in metadata.get('auto_hashtags', []) and metadata.get('ai_summary'):
            test_hashtag = hashtag
            print(f"Found test hashtag: {hashtag}")
            break
    if test_hashtag:
        break

# Simulate what update_notes does
current_notes_metadata = {}
filtered_notes = []

for note_id, metadata in notes_metadata.items():
    if test_hashtag in metadata.get('auto_hashtags', []):
        # This is what the dashboard does
        path = metadata.get('path', '')
        if path and '/' in path:
            top_folder = path.split('/')[0]
            # Assuming 800_Ressources is included
            if top_folder == '800_Ressources':
                current_notes_metadata[note_id] = metadata
                filtered_notes.append({
                    'path': metadata.get('path', ''),
                })
                
                if 'Albert Camus' in note_id:
                    print(f"\nDEBUG: Processing {note_id}")
                    print(f"  Path: {path}")
                    print(f"  Has AI summary: {bool(metadata.get('ai_summary'))}")

# Now simulate selection
if filtered_notes:
    # Take first note with AI summary
    for note_data in filtered_notes:
        selected_path = note_data['path']
        note_id = selected_path.rstrip('.md') if selected_path.endswith('.md') else selected_path
        
        print(f"\nSimulating selection:")
        print(f"  Selected path: {selected_path}")
        print(f"  Converted note_id: {note_id}")
        print(f"  In current_notes_metadata: {note_id in current_notes_metadata}")
        
        if note_id in current_notes_metadata:
            metadata = current_notes_metadata[note_id]
            ai_summary = metadata.get('ai_summary', None)
            print(f"  AI summary found: {bool(ai_summary)}")
            if ai_summary:
                print(f"  AI summary preview: {ai_summary[:50]}...")
                break