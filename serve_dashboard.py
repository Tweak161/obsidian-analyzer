#!/usr/bin/env python3
"""Serve the dashboard with visible console output"""
import subprocess
import sys

print("Starting dashboard server...")
print("Check console output for debug messages")
print("Dashboard will be available at http://localhost:5006")
print("-" * 50)

# Run the dashboard with output visible
subprocess.run([sys.executable, "dashboard.py"])