#!/usr/bin/env python3
"""Show progress of AI summary generation"""
import json

# Load vault data
with open("vault_analysis.json", "r") as f:
    vault_data = json.load(f)

# Count progress
total = 0
completed = 0
by_folder = {}

for note_id, metadata in vault_data["notes_metadata"].items():
    path = metadata.get("path", "")
    if path.startswith("800_Ressources/"):
        total += 1
        folder = path.split("/")[1] if "/" in path else "root"
        
        if folder not in by_folder:
            by_folder[folder] = {"total": 0, "completed": 0}
        
        by_folder[folder]["total"] += 1
        
        if metadata.get("ai_summary"):
            completed += 1
            by_folder[folder]["completed"] += 1

# Display progress
print("AI Summary Generation Progress")
print("=" * 50)
print(f"Overall: {completed}/{total} ({completed/total*100:.1f}% complete)")
print(f"Remaining: {total - completed} notes")
print("\nBy subfolder:")
for folder, stats in sorted(by_folder.items()):
    pct = stats["completed"]/stats["total"]*100 if stats["total"] > 0 else 0
    print(f"  {folder}: {stats['completed']}/{stats['total']} ({pct:.1f}%)")

print(f"\nEstimated batches remaining (10 notes/batch): {(total - completed + 9) // 10}")