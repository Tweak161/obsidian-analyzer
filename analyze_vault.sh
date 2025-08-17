#!/bin/bash
# Script to analyze Obsidian vault and launch dashboard

# Default vault path
VAULT_PATH="/mnt/c/Users/hess/Lokal/MyVault"

# Check if custom path provided
if [ "$1" ]; then
    VAULT_PATH="$1"
fi

echo "Obsidian Vault Analyzer"
echo "======================"
echo "Vault path: $VAULT_PATH"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Clear git cache to ensure fresh commit counts
if [ -f "git_history_cache.json" ]; then
    rm -f git_history_cache.json
    echo "Cleared git cache for fresh commit data"
fi

# Run the analysis
python3 run_analysis.py "$VAULT_PATH"