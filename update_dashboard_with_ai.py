#!/usr/bin/env python3
"""Quick update of dashboard data with AI classifications"""

import json
from pathlib import Path

# Load existing vault analysis
with open("vault_analysis.json", "r") as f:
    data = json.load(f)

# Load AI classifications
ai_classifications_file = Path("/mnt/c/Users/hess/OneDrive/Dokumente/ai_classifications.json")
with open(ai_classifications_file, "r") as f:
    ai_classifications = json.load(f)

print(f"Loaded {len(ai_classifications)} AI classifications")

# Update notes metadata with AI data
updated_count = 0
for note_id, metadata in data["notes_metadata"].items():
    note_path = metadata.get("path", "")
    
    if note_path in ai_classifications:
        ai_data = ai_classifications[note_path]
        
        # Get existing hashtags
        existing_hashtags = metadata.get("auto_hashtags", [])
        
        # Add AI hashtags
        ai_hashtags = ai_data.get("ai_hashtags", [])
        combined_hashtags = list(set(existing_hashtags + ai_hashtags))
        
        # Update metadata
        metadata["auto_hashtags"] = combined_hashtags
        metadata["ai_hashtags"] = ai_hashtags
        metadata["ai_keywords"] = ai_data.get("ai_keywords", [])
        metadata["ai_summary"] = ai_data.get("ai_summary", "")
        
        updated_count += 1

print(f"Updated {updated_count} notes with AI classifications")

# Recalculate hashtag counts
hashtag_counts = {}
for note_id, metadata in data["notes_metadata"].items():
    for hashtag in metadata.get("auto_hashtags", []):
        hashtag_counts[hashtag] = hashtag_counts.get(hashtag, 0) + 1

# Update hashtags data
data["hashtags"] = [
    {"hashtag": tag, "count": count}
    for tag, count in sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)
]

# Save updated data
with open("vault_analysis.json", "w") as f:
    json.dump(data, f, default=str, indent=2)

print("Dashboard data updated with AI classifications!")

# Show sample
print("\nSample updated notes:")
sample_count = 0
for note_id, metadata in data["notes_metadata"].items():
    if "ai_summary" in metadata and metadata["ai_summary"]:
        print(f"\n{metadata['path']}:")
        print(f"  AI Hashtags: {', '.join(metadata.get('ai_hashtags', []))}")
        print(f"  Combined Hashtags: {', '.join(metadata.get('auto_hashtags', []))}")
        print(f"  AI Summary: {metadata['ai_summary'][:80]}...")
        sample_count += 1
        if sample_count >= 3:
            break