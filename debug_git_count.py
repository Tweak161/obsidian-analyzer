#!/usr/bin/env python3
"""Debug git commit counting"""
import subprocess

vault_path = "//mnt/c/Users/hess/Lokal/MyVault"
file_path = "003_Zettelkasten/Mitteldistanz Triathlon 2026.excalidraw.md"

# Test the exact command our analyzer uses
cmd = ["git", "-C", vault_path, "rev-list", "--count", "HEAD", "--", file_path]
print(f"Running command: {' '.join(cmd)}")

result = subprocess.run(cmd, capture_output=True, text=True)
print(f"Return code: {result.returncode}")
print(f"Stdout: '{result.stdout}'")
print(f"Stderr: '{result.stderr}'")

if result.stdout.strip():
    print(f"Parsed count: {int(result.stdout.strip())}")

# Also try without HEAD
cmd2 = ["git", "-C", vault_path, "rev-list", "--count", "--all", "--", file_path]
print(f"\nTrying with --all: {' '.join(cmd2)}")
result2 = subprocess.run(cmd2, capture_output=True, text=True)
print(f"Result: {result2.stdout.strip()}")