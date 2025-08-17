#!/usr/bin/env python3
"""
Analyze Obsidian vault with fresh git data
This script ensures git commit counts are always up-to-date
"""
import sys
import os
from obsidian_analyzer import ObsidianAnalyzer, main as analyzer_main

def main():
    """Run analyzer with fresh git data"""
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        # Default vault path
        vault_path = "//mnt/c/Users/hess/Lokal/MyVault"
    
    print(f"Analyzing vault at: {vault_path}")
    print("Note: Git commit counts will be refreshed from the repository")
    
    # Clear any existing git cache before running
    cache_file = "git_history_cache.json"
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print("Cleared existing git cache")
    
    # Run the main analyzer
    # The analyzer will now get fresh git data
    os.system(f'python3 obsidian_analyzer.py "{vault_path}"')

if __name__ == "__main__":
    main()