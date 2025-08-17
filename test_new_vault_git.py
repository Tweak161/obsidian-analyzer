#!/usr/bin/env python3
"""Test git history for new vault location"""
from git_history import GitHistoryAnalyzer

vault_path = "//mnt/c/Users/hess/Lokal/MyVault"
test_file = "003_Zettelkasten/Mitteldistanz Triathlon 2026.excalidraw.md"

# Initialize git analyzer
git_analyzer = GitHistoryAnalyzer(vault_path)

print(f"Vault path: {vault_path}")
print(f"Is git repo: {git_analyzer.is_git_repo}")

if git_analyzer.is_git_repo:
    # Get history for the specific file
    details = git_analyzer.get_file_history_details(test_file)
    print(f"\nFile: {test_file}")
    print(f"Commit count: {details.get('commit_count', 0)}")
    print(f"Git importance score: {git_analyzer.calculate_git_importance_score(details.get('commit_count', 0))}")
    print(f"Full details: {details}")
    
    # Test a few more files
    print("\nTesting other files with potential commits:")
    test_files = [
        ".obsidian/workspace.json",
        "004_Journal/Daily/2025-08-15.md",
        "800_Ressources/100_Philosophy/Friedrich Nietzsche - Overview.excalidraw.md"
    ]
    
    for file in test_files:
        details = git_analyzer.get_file_history_details(file)
        if details.get('commit_count', 0) > 1:
            print(f"  {file}: {details.get('commit_count', 0)} commits")