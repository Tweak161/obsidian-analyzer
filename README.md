# Obsidian Vault Analyzer

Ein interaktives Python-Tool zur Analyse und Visualisierung von Obsidian Vaults. Erstellt übersichtliche Dashboards mit Notiz-Beziehungen, Zeitlinien und wichtigen Inhalten.

## Features

- **Timeline Visualizations**: See when notes were created and modified
- **Network Graph**: Interactive visualization of note connections
- **Important Notes**: Identifies key notes based on links, content, and network position
- **Orphan Detection**: Finds notes without any connections
- **Activity Analysis**: Heatmaps and histograms of your writing patterns
- **Real-time Dashboard**: Interactive web interface with filtering and sorting

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start

Run analysis and launch dashboard:
```bash
python run_analysis.py "/path/to/your/vault"
```

For your specific vault:
```bash
python run_analysis.py "/mnt/c/Users/hess/OneDrive/Dokumente/MyVault"
```

### Options

- `--install`: Install requirements before running
- `--analyze-only`: Only analyze vault, don't launch dashboard
- `--dashboard-only`: Launch dashboard with existing analysis data
- `--port PORT`: Specify dashboard port (default: 5006)

### Examples

First time setup:
```bash
python run_analysis.py --install "/mnt/c/Users/hess/OneDrive/Dokumente/MyVault"
```

Re-analyze vault:
```bash
python run_analysis.py --analyze-only
```

Launch dashboard only:
```bash
python run_analysis.py --dashboard-only
```

## How It Works

1. **Scanning**: The analyzer scans all `.md` and `.excalidraw` files in your vault
2. **Parsing**: Extracts links, tags, images, and metadata from each note
3. **Graph Building**: Creates a network graph of all note connections
4. **Scoring**: Calculates importance scores based on:
   - PageRank algorithm (network centrality)
   - Number of incoming/outgoing links
   - Content richness (word count, images, tags)
5. **Visualization**: Creates interactive charts and graphs

## Dashboard Views

### Overview Tab
- Key metrics and statistics
- File type distribution
- Recently modified notes

### Timeline Tab
- Creation timeline scatter plot
- Modification activity histogram
- Activity heatmap by day/hour

### Important Notes Tab
- Ranked list of most important notes
- Importance score breakdown
- Direct links to open in Obsidian

### Orphaned Notes Tab
- List of unconnected notes
- Statistics about orphaned content

### Network Graph Tab
- Interactive force-directed graph
- Zoom, pan, and hover for details
- Color-coded by file type

### Analysis Tab
- Link distribution histograms
- Word count analysis
- Tag frequency charts

## Performance Tips

- First scan may take a few minutes for large vaults (1000+ notes)
- Analysis data is saved to `vault_analysis.json` for quick reloading
- The network graph may take a moment to stabilize for large vaults

## Troubleshooting

### WSL Path Issues
If running from WSL with a Windows vault, the tool automatically converts paths. You can use either:
- `/mnt/c/Users/...` (WSL format)
- `C:\\Users\\...` (Windows format)

### Large Vaults
For vaults with 10,000+ notes:
- Initial analysis may take 5-10 minutes
- Consider using `--analyze-only` first
- Network graph may be slow to render

### Missing Dependencies
Run with `--install` flag or manually install:
```bash
pip install -r requirements.txt
```

## Data Privacy

All analysis is performed locally. No data is sent to external servers. Analysis results are saved to `vault_analysis.json` in the script directory.

## Future Enhancements

Potential additions based on the implementation plan:
- Content similarity analysis using NLP
- Incremental updates for large vaults
- Export to various formats
- Advanced search capabilities
- Theme customization