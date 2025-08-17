# Git Ignore Information

This project excludes the following files from version control to protect privacy:

## Excluded Files

### Vault Analysis Data
- `vault_analysis.json` - Contains full analysis of your personal vault including note content, links, and metadata
- `vault_analysis_with_git.json` - Extended analysis including git history of your notes
- `git_history_cache.json` - Cached git commit data for your vault files
- `ai_classifications.json` - AI-generated summaries and classifications of your personal notes

### Batch Processing Files
- `*_batch.json` - Temporary batch processing files containing note content
- `batch*.json` - AI summary batch files with personal note data
- `current_batch.json`, `next_batch_to_classify.json` - Processing queue files
- `remaining_notes.json` - List of notes pending processing

### Log Files
- `*.log` - All log files that may contain paths and content from your vault

### Other Sensitive Data
- Any files containing "private" or "personal" in the name
- Backup files (*.bak, *.backup)
- API keys and configuration files

## What IS Included

The repository includes only the source code and documentation:
- Python scripts for analysis (`obsidian_analyzer.py`, `dashboard.py`, etc.)
- Helper scripts and utilities
- Documentation files (README.md, guides)
- Requirements file
- This gitignore information file

## Before Running

When you clone this repository, you'll need to:
1. Configure your vault path in the scripts
2. Run the analysis to generate your own data files
3. These generated files will be automatically ignored by git