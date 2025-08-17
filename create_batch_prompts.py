#!/usr/bin/env python3
"""Create batch prompts for AI summaries with actual content"""
import json
from pathlib import Path

def read_note_content(vault_path, note_path, max_chars=2000):
    """Read note content safely"""
    file_path = vault_path / note_path
    try:
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            # For excalidraw files, try to extract text content
            if note_path.endswith('.excalidraw.md'):
                # Excalidraw files often have text in JSON format
                if len(content) > max_chars:
                    content = content[:max_chars]
            return content[:max_chars]
    except Exception as e:
        return f"[Error reading file: {e}]"
    return "[File not found]"

def create_batch_prompt(notes_batch, vault_path):
    """Create a prompt for a batch of notes"""
    prompt = """Please analyze these Obsidian notes and provide for EACH note:
1. A 1-2 sentence summary
2. Up to 5 relevant hashtags (from: #book, #journal, #moc, #AI, #meditation, #spirituality, #philosophy, #productivity, #programming, #health, #finance, #psychology, #relationship, #career, #education, #travel, #creativity, #science, #technology, #business, #writing, #personal)
   - Use #book for book summaries or notes about books
   - Use #journal for personal journal entries or reflections
   - Use #moc for "Map of Content" notes that organize and link to other notes
3. 5-10 key concepts/keywords

Respond in this JSON format:
```json
{
  "summaries": [
    {
      "note_id": "NOTE_ID",
      "ai_summary": "1-2 sentence summary",
      "ai_hashtags": ["#tag1", "#tag2"],
      "ai_keywords": ["keyword1", "keyword2", "keyword3"]
    }
  ]
}
```

Notes to analyze:

"""
    
    for note in notes_batch:
        content = read_note_content(vault_path, note['path'])
        prompt += f"---\nNote ID: {note['note_id']}\nPath: {note['path']}\nContent:\n{content}\n\n"
    
    return prompt

def main():
    vault_path = Path("//mnt/c/Users/hess/OneDrive/Dokumente/MyVault")
    
    # Load notes to summarize
    with open('notes_to_summarize.json', 'r') as f:
        all_notes = json.load(f)
    
    batch_size = 10
    num_batches = (len(all_notes) + batch_size - 1) // batch_size
    
    print(f"Creating {num_batches} batches of {batch_size} notes each...")
    
    for i in range(0, len(all_notes), batch_size):
        batch = all_notes[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        # Create prompt for this batch
        prompt = create_batch_prompt(batch, vault_path)
        
        # Save to file
        filename = f'batch_prompt_{batch_num}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"Created {filename} with {len(batch)} notes")
    
    print(f"\nCreated {num_batches} batch prompt files.")
    print("You can now process each batch by copying the content to Claude.")

if __name__ == "__main__":
    main()