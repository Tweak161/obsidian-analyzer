#!/usr/bin/env python3
"""Test AI classification integration"""

from obsidian_analyzer import ObsidianAnalyzer
import json

# Initialize analyzer
vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
analyzer = ObsidianAnalyzer(vault_path)

# Check if AI classifications are loaded
print("AI classifications loaded:", len(analyzer.ai_classifications) > 0)
print("Number of AI classifications:", len(analyzer.ai_classifications))

# Test a few files
test_files = [
    "excalibrain.md",
    "002_Input/Book List.md",
    "002_Input/MOC - Programming.md"
]

print("\nSample AI classifications:")
for file_path in test_files:
    if file_path in analyzer.ai_classifications:
        ai_data = analyzer.ai_classifications[file_path]
        print(f"\n{file_path}:")
        print(f"  Hashtags: {', '.join(ai_data.get('ai_hashtags', []))}")
        print(f"  Keywords: {', '.join(ai_data.get('ai_keywords', [])[:3])}...")
        print(f"  Summary: {ai_data.get('ai_summary', '')[:80]}...")

print("\nAI classification integration test complete!")