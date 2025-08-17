#!/usr/bin/env python3
import json

# Load vault analysis
with open('vault_analysis.json', 'r') as f:
    data = json.load(f)

notes_metadata = data.get('notes_metadata', {})

# Define the summaries with correct Unicode encoding
final_summaries = {
    "800_Ressources/100_Philosophy/Friedrich Nietzsche - Amor Fati - Weg zum Glu\u0308ck": {
        "ai_summary": "An exploration of Nietzsche's concept of 'amor fati' (love of fate) as a path to happiness, emphasizing the acceptance and embrace of all life experiences including suffering.",
        "ai_hashtags": ["#philosophy", "#spirituality", "#personal", "#psychology"],
        "ai_keywords": ["Nietzsche", "amor fati", "love of fate", "happiness", "acceptance", "suffering", "stoicism", "positive psychology", "growth", "existentialism"]
    },
    "800_Ressources/100_Philosophy/10 Philosophische Wege zum Glu\u0308ck - Walther Ziegler.excalidraw": {
        "ai_summary": "Visual exploration of 10 philosophical paths to happiness by Walther Ziegler, featuring concepts from existentialism (Sartre, de Beauvoir), amor fati (Nietzsche, Kafka), and Confucian dao.",
        "ai_hashtags": ["#philosophy", "#book", "#spirituality", "#personal"],
        "ai_keywords": ["existentialism", "happiness", "Sartre", "de Beauvoir", "freedom", "self-determination", "amor fati", "philosophical paths", "dao", "life philosophy"]
    }
}

# Update the notes
updated = 0
for note_id, summary_data in final_summaries.items():
    if note_id in notes_metadata:
        notes_metadata[note_id].update(summary_data)
        updated += 1
        print(f"✓ Updated: {note_id}")
    else:
        print(f"✗ Not found: {note_id}")

# Save updated data
with open('vault_analysis.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nUpdated {updated} notes with AI summaries")

# Final count
total_800 = sum(1 for n in notes_metadata if '800_Ressources' in n)
with_ai = sum(1 for n, d in notes_metadata.items() if '800_Ressources' in n and isinstance(d, dict) and d.get('ai_summary'))
print(f"\nFinal status:")
print(f"Total 800_Ressources notes: {total_800}")
print(f"With AI summaries: {with_ai}")
print(f"Completion: {with_ai/total_800*100:.1f}%")

# Clear remaining_notes.json
with open('remaining_notes.json', 'w') as f:
    json.dump([], f)