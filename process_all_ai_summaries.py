#!/usr/bin/env python3
"""Process all AI summaries and update vault analysis"""
import json
import os
from pathlib import Path

def save_summaries(summaries_file):
    """Save AI summaries to vault analysis"""
    # Load summaries
    with open(summaries_file, 'r') as f:
        data = json.load(f)
    
    summaries = data.get('summaries', [])
    
    # Load vault analysis
    with open('vault_analysis.json', 'r') as f:
        vault_data = json.load(f)
    
    notes_metadata = vault_data.get('notes_metadata', {})
    
    # Update each note with AI summary
    updated_count = 0
    for summary in summaries:
        note_id = summary['note_id']
        if note_id in notes_metadata:
            notes_metadata[note_id]['ai_summary'] = summary['ai_summary']
            notes_metadata[note_id]['ai_hashtags'] = summary['ai_hashtags']
            notes_metadata[note_id]['ai_keywords'] = summary['ai_keywords']
            updated_count += 1
    
    # Save updated vault analysis
    with open('vault_analysis.json', 'w') as f:
        json.dump(vault_data, f, indent=2)
    
    print(f"Updated {updated_count} notes with AI summaries from {summaries_file}")
    return updated_count

def main():
    """Process all batch summary files"""
    total_updated = 0
    
    # Process all batch files
    batch_files = sorted([f for f in os.listdir('.') if f.startswith('batch_') and f.endswith('_summaries.json')])
    
    if not batch_files:
        print("No batch summary files found. Looking for individual files...")
        # Try batch_1_summaries.json format
        if os.path.exists('batch_1_summaries.json'):
            total_updated += save_summaries('batch_1_summaries.json')
    else:
        for batch_file in batch_files:
            if os.path.exists(batch_file):
                total_updated += save_summaries(batch_file)
    
    print(f"\nTotal notes updated: {total_updated}")
    
    # Update remaining notes list
    if os.path.exists('remaining_notes.json'):
        with open('vault_analysis.json', 'r') as f:
            vault_data = json.load(f)
        
        notes_metadata = vault_data.get('notes_metadata', {})
        
        # Find notes without AI summaries in 800_Ressources
        remaining = []
        for note_id, metadata in notes_metadata.items():
            if '800_Ressources' in note_id and not metadata.get('ai_summary'):
                remaining.append({
                    'note_id': note_id,
                    'path': metadata.get('path', '')
                })
        
        # Save updated remaining notes
        with open('remaining_notes.json', 'w') as f:
            json.dump(remaining, f, indent=2)
        
        print(f"Updated remaining_notes.json - {len(remaining)} notes left to process")

if __name__ == "__main__":
    main()