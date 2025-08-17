# AI Summaries for Obsidian Notes

This feature allows you to generate AI-powered summaries for your Obsidian notes using Claude API.

## Setup

1. **Get an API Key**
   - Visit https://console.anthropic.com/
   - Create an account and generate an API key
   - Set the environment variable:
     ```bash
     export ANTHROPIC_API_KEY='your-api-key-here'
     ```

2. **Install Requirements**
   ```bash
   pip install anthropic
   ```

## Usage

### Generate Summaries for 800_Ressources

The easiest way is to use the convenience script:

```bash
./summarize_ressources.sh
```

### Advanced Usage

Use the `generate_ai_summaries.py` script for more control:

```bash
# Process a specific folder
python3 generate_ai_summaries.py --folder "800_Ressources"

# Process with a limit
python3 generate_ai_summaries.py --folder "800_Ressources" --limit 10

# Dry run to see what would be processed
python3 generate_ai_summaries.py --folder "800_Ressources" --dry-run

# Change batch save frequency (default is every 10 notes)
python3 generate_ai_summaries.py --folder "800_Ressources" --batch-size 5
```

### Process All Notes

To process all notes without a folder filter:

```bash
python3 generate_ai_summaries.py --folder ""
```

## Features

- **Batch Processing**: Saves progress every N notes (configurable)
- **Resume Capability**: Skips already processed notes
- **Progress Tracking**: Shows ETA and processing rate
- **Error Handling**: Continues processing even if some notes fail
- **Rate Limiting**: Respects API rate limits

## What Gets Generated

For each note, the AI generates:
- A 1-2 sentence summary
- Up to 5 relevant hashtags
- 5-10 key concepts/keywords

## Viewing Results

After processing, restart the dashboard to see the AI summaries:

```bash
python3 run_analysis.py --dashboard-only
```

The summaries will appear in:
- The note details view when clicking on a note
- The Important Notes tab
- Any other place where note metadata is displayed

## Tips

- Start with a small batch (`--limit 10`) to test
- The script automatically saves progress, so you can interrupt and resume
- Processing takes about 1-2 seconds per note due to API calls
- Costs approximately $0.003 per note (based on Claude 3 Sonnet pricing)

## Troubleshooting

- **API Key Not Found**: Make sure to export the ANTHROPIC_API_KEY variable
- **Rate Limits**: The script includes built-in delays, but you can adjust if needed
- **Failed Classifications**: Check the console output for specific error messages