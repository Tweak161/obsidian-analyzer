#!/usr/bin/env python3
"""Test git integration across different folders"""
import json
from git_history import GitHistoryAnalyzer
from collections import defaultdict

# Load current vault analysis
with open('vault_analysis.json', 'r') as f:
    data = json.load(f)

vault_path = "//mnt/c/Users/hess/OneDrive/Dokumente/MyVault"
notes_metadata = data.get('notes_metadata', {})

# Group files by top-level folder
folder_files = defaultdict(list)
for note_id, meta in notes_metadata.items():
    if isinstance(meta, dict):
        path = meta.get('path', '')
        if path and '/' in path:
            top_folder = path.split('/')[0]
            # Skip 005_Media folder as it has issues
            if top_folder != '005_Media':
                folder_files[top_folder].append(path)

print(f"Found {len(folder_files)} top-level folders")

# Initialize git analyzer
git_analyzer = GitHistoryAnalyzer(vault_path)

if git_analyzer.is_git_repo:
    print("✓ Vault is a git repository\n")
    
    # Sample 5 files from each folder
    for folder, files in sorted(folder_files.items()):
        if not files:
            continue
            
        print(f"\n{folder} ({len(files)} files):")
        
        # Sample up to 5 files
        sample_files = files[:5]
        commit_counts = []
        
        for file_path in sample_files:
            details = git_analyzer.get_file_history_details(file_path)
            commit_count = details.get('commit_count', 0)
            commit_counts.append(commit_count)
            print(f"  {file_path}: {commit_count} commits")
        
        if commit_counts:
            avg = sum(commit_counts) / len(commit_counts)
            print(f"  Average: {avg:.1f} commits")
            
    # Look for files with most commits across all folders
    print("\n\nSearching for files with most commits...")
    high_commit_files = []
    
    # Sample 100 random files
    import random
    all_files = [f for files in folder_files.values() for f in files]
    sample_size = min(100, len(all_files))
    sampled_files = random.sample(all_files, sample_size)
    
    for file_path in sampled_files:
        details = git_analyzer.get_file_history_details(file_path)
        commit_count = details.get('commit_count', 0)
        if commit_count > 1:
            high_commit_files.append((file_path, commit_count))
    
    # Sort by commit count
    high_commit_files.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\nFiles with most commits (from {sample_size} sampled files):")
    for file_path, commits in high_commit_files[:10]:
        print(f"  {file_path}: {commits} commits")
        
else:
    print("✗ Vault is not a git repository")