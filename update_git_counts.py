#!/usr/bin/env python3
"""
Quick script to update git commit counts without re-analyzing the entire vault
"""
import os
import sys

# Clear git cache
if os.path.exists("git_history_cache.json"):
    os.remove("git_history_cache.json")
    print("✓ Cleared git cache")

# Run the update script
print("Updating git commit counts...")
os.system("python3 update_vault_with_git.py")

print("\nTo see the updated counts, restart the dashboard:")
print("  pkill -f 'python3 dashboard.py' && python3 dashboard.py")