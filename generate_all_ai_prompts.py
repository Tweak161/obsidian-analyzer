#!/usr/bin/env python3
"""Generate all prompts for remaining AI summaries"""
import json
from pathlib import Path

def main():
    # Load vault data
    with open('vault_analysis.json', 'r') as f:
        vault_data = json.load(f)
    
    # Load remaining notes
    with open('remaining_notes.json', 'r') as f:
        remaining = json.load(f)
    
    notes_metadata = vault_data.get('notes_metadata', {})
    
    # Process all remaining notes
    all_summaries = []
    
    for i, note_info in enumerate(remaining):
        note_id = note_info['note_id']
        path = note_info['path']
        
        if note_id in notes_metadata:
            metadata = notes_metadata[note_id]
            
            # Read note content
            vault_path = Path("/home/thomas/Obsidian-PKM-Hero")
            file_path = vault_path / path
            
            content = ""
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8')[:3000]
                except:
                    content = f"[Unable to read file: {path}]"
            
            # Determine note type
            note_type = "note"
            if "MOC" in path or "Map of Content" in content[:500]:
                note_type = "Map of Content (MOC)"
            elif any(book_indicator in path.lower() for book_indicator in ["boap", "book", "fooled by", "models", "7 habits", "4000 weeks", "deep work"]):
                note_type = "book summary"
            elif "journal" in path.lower() or "tagebuch" in path.lower():
                note_type = "journal entry"
            
            # Create summary entry
            summary_entry = {
                "note_id": note_id,
                "path": path,
                "note_type": note_type,
                "content_preview": content[:500] + "..." if len(content) > 500 else content
            }
            
            all_summaries.append(summary_entry)
    
    # Generate the prompt
    print(f"I need to generate AI summaries for {len(all_summaries)} notes from my Obsidian vault.")
    print("\nPlease analyze these notes and provide for EACH note:")
    print("1. A 1-2 sentence summary")
    print("2. Up to 5 relevant hashtags (from: #book, #journal, #moc, #AI, #meditation, #spirituality, #philosophy, #productivity, #programming, #health, #finance, #psychology, #relationship, #career, #education, #travel, #creativity, #science, #technology, #business, #writing, #personal)")
    print("   - Use #book for book summaries or notes about books")
    print("   - Use #journal for personal journal entries or reflections") 
    print("   - Use #moc for 'Map of Content' notes that organize and link to other notes")
    print("3. 5-10 key concepts/keywords")
    print("\nHere are the notes grouped by type:\n")
    
    # Group by type
    by_type = {}
    for entry in all_summaries:
        note_type = entry['note_type']
        if note_type not in by_type:
            by_type[note_type] = []
        by_type[note_type].append(entry)
    
    # Print grouped notes
    for note_type, notes in by_type.items():
        print(f"\n=== {note_type.upper()} ({len(notes)} notes) ===")
        for note in notes[:5]:  # Show first 5 of each type
            print(f"\nNote ID: {note['note_id']}")
            print(f"Path: {note['path']}")
            print(f"Content preview: {note['content_preview'][:200]}...")
        
        if len(notes) > 5:
            print(f"\n... and {len(notes) - 5} more {note_type} notes")
    
    # Save note info for later processing
    with open('notes_to_summarize.json', 'w') as f:
        json.dump(all_summaries, f, indent=2)
    
    print(f"\n\nTotal notes to process: {len(all_summaries)}")
    print("Note information saved to notes_to_summarize.json")

if __name__ == "__main__":
    main()