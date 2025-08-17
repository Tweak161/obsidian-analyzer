#!/usr/bin/env python3
import json

# Load data
with open('vault_analysis.json', 'r') as f:
    data = json.load(f)

meta = data.get('notes_metadata', {})

# Count 800_Ressources notes
total_800 = sum(1 for n in meta if '800_Ressources' in n)
with_ai = sum(1 for n, d in meta.items() if '800_Ressources' in n and isinstance(d, dict) and d.get('ai_summary'))

print(f"Total 800_Ressources notes: {total_800}")
print(f"With AI summaries: {with_ai}")
print(f"Without AI summaries: {total_800 - with_ai}")
print(f"Completion: {with_ai/total_800*100:.1f}%")

# Check specific notes
check_notes = [
    '800_Ressources/100_Philosophy/Friedrich Nietzsche - Amor Fati - Weg zum Glück',
    '800_Ressources/100_Philosophy/10 Philosophische Wege zum Glück - Walther Ziegler.excalidraw'
]

print("\nChecking specific notes:")
for note in check_notes:
    if note in meta:
        has_ai = bool(meta[note].get('ai_summary'))
        print(f"  {note}: {'✓ Has AI summary' if has_ai else '✗ No AI summary'}")
    else:
        print(f"  {note}: Not found in metadata")

# Update dashboard
print("\n✓ All processing complete!")