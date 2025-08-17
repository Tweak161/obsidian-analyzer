#!/usr/bin/env python3
"""Analyze git commit distribution for the vault"""
import subprocess
import json
from collections import Counter
from pathlib import Path

vault_path = "//mnt/c/Users/hess/OneDrive/Dokumente/MyVault"

# Load current vault analysis to get all tracked files
with open('vault_analysis.json', 'r') as f:
    data = json.load(f)

notes_metadata = data.get('notes_metadata', {})

# Sample analysis on 800_Ressources files
ressources_files = [meta.get('path', '') for note_id, meta in notes_metadata.items() 
                   if '800_Ressources' in note_id and isinstance(meta, dict)]

print(f"Analyzing {len(ressources_files)} files from 800_Ressources...")

commit_counts = []
errors = 0

for i, file_path in enumerate(ressources_files):
    if i % 20 == 0:
        print(f"Progress: {i}/{len(ressources_files)}")
    
    try:
        result = subprocess.run(
            ["git", "-C", vault_path, "rev-list", "--count", "HEAD", "--", file_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            count = int(result.stdout.strip())
            commit_counts.append(count)
        else:
            errors += 1
            
    except Exception as e:
        errors += 1

# Analyze distribution
if commit_counts:
    count_freq = Counter(commit_counts)
    
    print(f"\nCommit Count Distribution:")
    print(f"Total files analyzed: {len(commit_counts)}")
    print(f"Errors: {errors}")
    print(f"Min commits: {min(commit_counts)}")
    print(f"Max commits: {max(commit_counts)}")
    print(f"Average commits: {sum(commit_counts) / len(commit_counts):.2f}")
    
    print("\nFrequency distribution:")
    for commits, freq in sorted(count_freq.items()):
        print(f"  {commits} commits: {freq} files ({freq/len(commit_counts)*100:.1f}%)")
    
    # Suggested scoring buckets
    print("\nSuggested scoring buckets based on distribution:")
    percentiles = [0, 25, 50, 75, 90, 100]
    for p in percentiles:
        if commit_counts:
            idx = int(len(sorted(commit_counts)) * p / 100)
            if idx >= len(commit_counts):
                idx = len(commit_counts) - 1
            value = sorted(commit_counts)[idx]
            print(f"  {p}th percentile: {value} commits")