#!/usr/bin/env python3
"""Test git integration on a subset of files"""
import json
from git_history import GitHistoryAnalyzer

# Load current vault analysis
with open('vault_analysis.json', 'r') as f:
    data = json.load(f)

vault_path = "//mnt/c/Users/hess/OneDrive/Dokumente/MyVault"
notes_metadata = data.get('notes_metadata', {})

# Filter to just 800_Ressources files
ressources_files = []
for note_id, meta in notes_metadata.items():
    if '800_Ressources' in note_id and isinstance(meta, dict):
        path = meta.get('path', '')
        if path:
            ressources_files.append(path)

print(f"Testing git integration on {len(ressources_files)} files from 800_Ressources...")

# Initialize git analyzer
git_analyzer = GitHistoryAnalyzer(vault_path)

if git_analyzer.is_git_repo:
    print("✓ Vault is a git repository")
    
    # Test on first 5 files
    test_files = ressources_files[:5]
    
    for file_path in test_files:
        details = git_analyzer.get_file_history_details(file_path)
        print(f"\n{file_path}:")
        print(f"  Commits: {details.get('commit_count', 0)}")
        print(f"  Importance score: {git_analyzer.calculate_git_importance_score(details.get('commit_count', 0))}")
        
    # Get vault statistics on subset
    print("\nGetting statistics for all 800_Ressources files...")
    stats = git_analyzer.get_vault_statistics(ressources_files)
    
    print(f"\nGit Statistics:")
    print(f"  Total files: {stats['total_files']}")
    print(f"  Files with history: {stats['files_with_history']}")
    print(f"  Average commits: {stats['average_commits']:.2f}")
    print(f"  Max commits: {stats['max_commits']}")
    print(f"\n  Most edited files:")
    for item in stats['most_edited_files'][:5]:
        print(f"    {item['file']}: {item['commits']} commits")
        
else:
    print("✗ Vault is not a git repository")