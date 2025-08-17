#!/bin/bash
# Convenience script to generate AI summaries for 800_Ressources folder

echo "AI Summary Generator for 800_Ressources"
echo "======================================="

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: ANTHROPIC_API_KEY environment variable not set"
    echo ""
    echo "Please set your API key first:"
    echo "  export ANTHROPIC_API_KEY='your-api-key-here'"
    echo ""
    echo "You can get an API key from: https://console.anthropic.com/"
    exit 1
fi

# Run the generator
python3 generate_ai_summaries.py --folder "800_Ressources" "$@"