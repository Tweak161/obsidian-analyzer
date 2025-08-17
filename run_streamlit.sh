#!/bin/bash
# Run Streamlit dashboard for Obsidian Vault Analyzer

echo "Starting Streamlit Dashboard..."
echo "This will be accessible from Windows at: http://localhost:8501"
echo ""

# Run streamlit with network settings for WSL
streamlit run streamlit_dashboard.py \
    --server.address 0.0.0.0 \
    --server.port 8501 \
    --browser.gatherUsageStats false \
    --server.headless true