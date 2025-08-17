#!/usr/bin/env python3
"""Check git stats across different folders"""
import subprocess
import json
from collections import defaultdict

vault_path = "//mnt/c/Users/hess/OneDrive/Dokumente/MyVault"

# Load vault analysis
with open('vault_analysis.json', 'r') as f:
    data = json.load(f)

notes_metadata = data.get('notes_metadata', {})

# Group by top-level folder
folder_samples = defaultdict(list)
for note_id, meta in notes_metadata.items():
    if isinstance(meta, dict) and meta.get('path'):
        parts = note_id.split('/')
        if len(parts) > 0:
            top_folder = parts[0]
            if len(folder_samples[top_folder]) < 5:  # Sample 5 from each folder
                folder_samples[top_folder].append(meta.get('path', ''))

print("Git commit stats by folder:\n")

total_stats = []

for folder, files in sorted(folder_samples.items()):
    if not files:
        continue
        
    print(f"{folder}:")
    folder_stats = []
    
    for file_path in files:
        try:
            result = subprocess.run(
                ["git", "-C", vault_path, "rev-list", "--count", "HEAD", "--", file_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip():
                count = int(result.stdout.strip())
                folder_stats.append(count)
                total_stats.append(count)
                print(f"  {file_path}: {count} commits")
                
        except Exception as e:
            print(f"  Error with {file_path}: {e}")
    
    if folder_stats:
        avg = sum(folder_stats) / len(folder_stats)
        print(f"  Average: {avg:.1f} commits\n")

# Overall stats
if total_stats:
    print("\nOverall Statistics:")
    print(f"Total files sampled: {len(total_stats)}")
    print(f"Min commits: {min(total_stats)}")
    print(f"Max commits: {max(total_stats)}")
    print(f"Average commits: {sum(total_stats) / len(total_stats):.2f}")
    
    # Distribution
    from collections import Counter
    commit_distribution = Counter(total_stats)
    
    print("\nCommit distribution:")
    for commits in sorted(commit_distribution.keys()):
        count = commit_distribution[commits]
        print(f"  {commits} commits: {count} files ({count/len(total_stats)*100:.1f}%)")