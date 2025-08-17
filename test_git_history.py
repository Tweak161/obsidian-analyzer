#!/usr/bin/env python3
"""Test git history collection for the vault"""
import subprocess
import os
import json

vault_path = "//mnt/c/Users/hess/OneDrive/Dokumente/MyVault"

# Test if vault is a git repository
try:
    result = subprocess.run(
        ["git", "-C", vault_path, "rev-parse", "--git-dir"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Vault is a git repository")
        
        # Test getting commit count for a specific file
        test_file = "800_Ressources/100_Philosophy/Friedrich Nietzsche - Overview.excalidraw.md"
        
        # Method 1: Count commits that changed this file
        result = subprocess.run(
            ["git", "-C", vault_path, "log", "--oneline", "--", test_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            commit_count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            print(f"\nTest file: {test_file}")
            print(f"Commit count: {commit_count}")
            
            # Show first few commits
            print("\nFirst 5 commits:")
            commits = result.stdout.strip().split('\n')[:5]
            for commit in commits:
                if commit:
                    print(f"  {commit}")
        
        # Method 2: Get more detailed stats
        print("\nGit shortlog stats:")
        result = subprocess.run(
            ["git", "-C", vault_path, "log", "--pretty=format:%h %ad %s", "--date=short", "--", test_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout:
            commits = result.stdout.strip().split('\n')[:3]
            for commit in commits:
                print(f"  {commit}")
                
        # Test getting all files with their commit counts (sample)
        print("\n\nTesting batch processing...")
        result = subprocess.run(
            ["git", "-C", vault_path, "ls-tree", "-r", "HEAD", "--name-only"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            all_files = result.stdout.strip().split('\n')
            print(f"Total files in git: {len(all_files)}")
            
            # Sample a few files
            sample_files = [f for f in all_files if '800_Ressources' in f][:5]
            print(f"\nSample commit counts for 800_Ressources files:")
            
            for file_path in sample_files:
                result = subprocess.run(
                    ["git", "-C", vault_path, "rev-list", "--count", "HEAD", "--", file_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    count = int(result.stdout.strip()) if result.stdout.strip() else 0
                    print(f"  {file_path}: {count} commits")
                    
    else:
        print("✗ Vault is not a git repository")
        print(f"Error: {result.stderr}")
        
except Exception as e:
    print(f"Error testing git: {e}")