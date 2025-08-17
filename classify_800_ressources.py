#!/usr/bin/env python3
"""
Script to generate AI summaries for all notes in 800_Ressources folder
"""

import json
import os
from pathlib import Path
from ai_classifier import AIClassifier

# Load vault analysis data
with open("vault_analysis.json", "r") as f:
    vault_data = json.load(f)

# Get vault path from the data
vault_path = vault_data.get("vault_path", "002_Slipbox")

# Initialize classifier
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("Error: ANTHROPIC_API_KEY environment variable not set")
    print("Please set it with: export ANTHROPIC_API_KEY='your-api-key'")
    exit(1)

classifier = AIClassifier(vault_path, api_key)

# Get all notes in 800_Ressources
ressources_notes = []
for note_id, metadata in vault_data["notes_metadata"].items():
    path = metadata.get("path", "")
    if path.startswith("800_Ressources/"):
        # Check if already has AI summary
        if not metadata.get("ai_summary"):
            ressources_notes.append(path)

print(f"Found {len(ressources_notes)} notes in 800_Ressources without AI summaries")

if ressources_notes:
    print("\nStarting AI classification...")
    
    # Process each note
    for i, note_path in enumerate(ressources_notes, 1):
        print(f"\n[{i}/{len(ressources_notes)}] Processing: {note_path}")
        
        try:
            # Read note content
            full_path = Path(vault_path) / note_path
            if full_path.exists():
                classification = classifier.classify_with_api(full_path)
                if classification:
                    print(f"  ✓ Summary: {classification.ai_summary[:80]}...")
                    print(f"  ✓ Hashtags: {', '.join(classification.ai_hashtags[:5])}")
                else:
                    print("  ✗ Classification failed")
            else:
                print(f"  ✗ File not found: {full_path}")
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    # Save classifications
    classifier._save_classifications()
    print("\n✓ Classifications saved to ai_classifications.json")
    
    # Update vault analysis with new classifications
    print("\nUpdating vault analysis with AI summaries...")
    
    # Reload classifications
    with open("ai_classifications.json", "r") as f:
        classifications = json.load(f)
    
    # Update vault data
    updates = 0
    for file_path, classification in classifications.items():
        # Find matching note in vault data
        for note_id, metadata in vault_data["notes_metadata"].items():
            if metadata.get("path") == file_path:
                metadata["ai_summary"] = classification["ai_summary"]
                metadata["ai_hashtags"] = classification["ai_hashtags"]
                metadata["ai_keywords"] = classification["ai_keywords"]
                updates += 1
                break
    
    # Save updated vault analysis
    with open("vault_analysis.json", "w") as f:
        json.dump(vault_data, f, indent=2)
    
    print(f"✓ Updated {updates} notes in vault_analysis.json")
    print("\nDone! Restart the dashboard to see the AI summaries.")
else:
    print("\nAll notes in 800_Ressources already have AI summaries!")