#!/bin/bash
# Script to process the next unprocessed batch

# Find the next unprocessed batch
for i in {001..999}; do
    PROMPT_FILE="batch_${i}_prompt.txt"
    RESPONSE_FILE="batch_${i}_response.json"
    
    if [ -f "$PROMPT_FILE" ] && [ ! -f "$RESPONSE_FILE" ]; then
        echo "Next batch to process: $PROMPT_FILE"
        echo ""
        echo "Steps:"
        echo "1. Copy the content of $PROMPT_FILE"
        echo "2. Paste into Claude conversation"
        echo "3. Save response to $RESPONSE_FILE"
        echo "4. Run: python3 ../manual_summary_helper.py save $RESPONSE_FILE"
        echo ""
        echo "Opening prompt file..."
        cat "$PROMPT_FILE"
        break
    fi
done

if [ ! -f "$PROMPT_FILE" ]; then
    echo "All batches have been processed!"
fi
