#!/usr/bin/env python3
"""Test git history for a single file"""
from git_history import GitHistoryAnalyzer
import subprocess

vault_path = "//mnt/c/Users/hess/OneDrive/Dokumente/MyVault"
file_path = "003_Zettelkasten/Mitteldistanz Triathlon 2026.excalidraw.md"

# Test with our analyzer
analyzer = GitHistoryAnalyzer(vault_path)
details = analyzer.get_file_history_details(file_path)
print(f"Our analyzer results for: {file_path}")
print(f"  Commit count: {details.get('commit_count', 0)}")
print(f"  Details: {details}")

# Test directly with git command
print(f"\nDirect git command test:")
result = subprocess.run(
    ["git", "-C", vault_path, "rev-list", "--count", "HEAD", "--", file_path],
    capture_output=True,
    text=True
)
print(f"  Git rev-list output: {result.stdout.strip()}")
print(f"  Return code: {result.returncode}")

# Test with log
print(f"\nGit log test:")
log_result = subprocess.run(
    ["git", "-C", vault_path, "log", "--oneline", "--", file_path],
    capture_output=True,
    text=True
)
print(f"  Git log output:\n{log_result.stdout}")

# Check if file exists
import os
full_path = os.path.join(vault_path, file_path)
print(f"\nFile exists: {os.path.exists(full_path)}")
print(f"File size: {os.path.getsize(full_path) if os.path.exists(full_path) else 'N/A'} bytes")