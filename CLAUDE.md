# Python Solutions for Analyzing and Visualizing Obsidian Vaults

## Initial Plan

Let's create a Python script that scans my Obsidian Vault and displays the scanned results on an interactive HTML dashboard.
I would like to visualize what I have been working on and make finding notes and revisiting easier.
E.g. I would like to have a visualized timeline showing the documents I worked on (e.g. modified last). Also a timeline showing when I created files.
Then I would to have a list of orphaned notes without links to other notes.
I would like a list of important notes. Notes can be .excalidraw, .md. Notes are important if they contain a lot of links to other notes or are often linked by other notes, if they contain a lot of content (many images, pdfs, text, ...).
Also think about other ways to visualize the content and propose them to be.
Clarify if anything is unclear.
Before starting do a deeper research on different solutions and draw up a plan.

## Comprehensive implementation strategy for multi-GB vault analysis

For analyzing a large Obsidian vault (multiple GB with thousands of notes), the optimal Python solution combines specialized libraries for parsing, NLP analysis, and interactive visualization. Research reveals that **obsidiantools with NetworkX** provides the foundation for vault structure analysis, while **Panel with Pyvis** offers the best balance of performance and flexibility for interactive dashboards.

## Core library recommendations by component

The parsing layer should utilize **obsidiantools** (`pip install obsidiantools`) as the primary framework, which provides NetworkX graph representations and comprehensive metadata extraction. For basic parsing needs, **danymat/Obsidian-Markdown-Parser** handles wikilinks, tags, and YAML frontmatter efficiently. The regex pattern `r'\[\[([^|\\]]+)(?:\|([^\\]]+))?\]\]'` reliably extracts internal links, while Excalidraw files require JSON extraction from their markdown wrapper.

For visualization, **Pyvis** excels at network graphs with its force-directed layouts handling 1000+ nodes efficiently through GPU acceleration. Timeline visualizations perform best with **Plotly's WebGL-enabled charts**, which can render up to 1 million data points smoothly. The dashboard framework choice depends on requirements: **Panel** offers maximum flexibility with Datashader integration for very large vaults, **Dash** provides production-ready scalability, while **Streamlit** enables rapid prototyping in under 20 lines of code.

## Natural language processing architecture

Keyword extraction benchmarks show **RAKE** delivers the best speed-to-accuracy ratio, processing 2000 documents in 2 seconds. For document similarity, **TF-IDF with cosine similarity** surprisingly outperforms newer methods in efficiency, taking only 1.5 minutes for large corpora compared to 50+ hours for BERT approaches. Note importance scoring should combine PageRank network analysis with custom metrics:

```python
importance_score = (
    0.3 * pagerank_score +
    0.25 * backlinks_count +
    0.25 * outgoing_links_count +
    0.15 * content_richness +
    0.05 * update_frequency
)
```

For similarity search at scale, **FAISS** provides GPU-accelerated approximate nearest neighbor search achieving 1,500,000 queries/second, while **Annoy** offers memory-efficient file-based indexes for static datasets.

## Performance optimization strategies

Contrary to common assumptions, **synchronous I/O with multiprocessing outperforms async I/O** for local file operations. Async file reading can be 15-300x slower due to thread pool overhead. The optimal scanning pattern uses ThreadPoolExecutor for file I/O combined with ProcessPoolExecutor for CPU-intensive parsing, achieving 4-8x speedup on multi-core systems.

Memory-mapped files provide up to 100x speedup for files over 15MB:

```python
import mmap
with open(filepath, 'r+b') as f:
    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
        content = mmapped_file[:1000]  # Direct memory access
```

For incremental scanning, track modification times and process only changed files. The **watchdog** library enables real-time monitoring without periodic scanning overhead.

## Database and caching architecture

SQLite with proper optimization handles millions of operations per second. Critical settings include WAL mode for 3-10x write performance improvement:

```python
conn.execute("PRAGMA journal_mode = WAL")
conn.execute("PRAGMA synchronous = NORMAL")
conn.execute("PRAGMA cache_size = 2000")
```

For caching, **DiskCache** outperforms Redis for single-machine deployments, claiming faster performance than Redis/Memcached for local usage. Store pre-computed embeddings as serialized numpy arrays in SQLite BLOBs, with full-text search enabled through FTS5 virtual tables.

## Orphan detection and network analysis

Orphan detection combines graph traversal with set operations. BFS traversal identifies connected components in O(V+E) time, while set difference operations provide O(1) average lookup for unlinked notes. Edge cases require special handling: exclude daily notes patterns, skip template folders, and parse embedded links within Excalidraw files.

The graph structure should utilize NetworkX's DiGraph with node attributes for metadata:

```python
G.add_node('note1', title='Note Title', tags=['tag1'], 
           word_count=500, created_date='2023-01-01')
G.add_edge('note1', 'note2', link_type='wikilink')
```

## Interactive dashboard implementation

For the HTML dashboard with click interactions and file opening capabilities, the architecture depends on deployment context:

**For desktop distribution**: Electron + Python backend solves file:// protocol restrictions and enables native file system access. PyFlaDesk provides a Flask + Electron framework for packaging.

**For web deployment**: FastAPI backend with React frontend offers complete control and scalability. The backend serves files through HTTP endpoints while the frontend handles visualizations:

```python
@app.get("/api/vault/stats")
def get_vault_stats():
    return {
        "note_count": len(vault.md_file_index),
        "backlinks": vault.get_note_metadata(),
        "graph_data": vault.graph.nodes(data=True)
    }
```

**For rapid development**: Panel with HoloViews provides the best balance, supporting all major visualization libraries with efficient crossfiltering for linked visualizations.

## Existing tool approaches to learn from

The Graph Analysis plugin uses co-citations and 2nd-order backlinks analysis with TypeScript-based algorithms. Juggl integrates Cytoscape.js for 3D visualization with advanced styling. InfraNodus combines network science with GPT-4 for gap identification. The obsidiantools Python library demonstrates effective use of NetworkX for vault analysis, providing methods like `get_note_metadata()` for extracting comprehensive statistics.

## Memory management for multi-GB vaults

Stream processing maintains constant memory usage regardless of vault size:

```python
def process_large_vault_streaming(vault_path, chunk_size=1024*1024):
    for file_path in get_markdown_files(vault_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            while chunk := f.read(chunk_size):
                yield process_chunk(chunk)
```

Use tracemalloc for profiling and disable automatic garbage collection during batch processing, triggering manual collection every 100 batches for optimal performance.

## Recommended implementation architecture

For vaults under 1000 notes, use spaCy preprocessing, RAKE keyword extraction, TF-IDF similarity, and simple graph metrics. For 1000-10000 notes, add multiprocessing, switch to YAKE for balanced accuracy, implement PageRank importance scoring, and cache embeddings. For vaults exceeding 10000 notes, deploy Ray for distributed processing, use FAISS for approximate similarity, implement incremental processing, and consider database storage for computed features.

Real-world testing on a 727MB vault with 2,459 books and 161,820 block references shows smooth editing performance on 14MB files, though block reference functionality degrades at scale. Initial loading remains the primary bottleneck for very large vaults.

The complete solution integrates these components into a cohesive system: obsidiantools for parsing, Pyvis for network visualization, Plotly for timelines, RAKE for keywords, TF-IDF for similarity, PageRank for importance, SQLite with WAL for metadata, DiskCache for results, and Panel or Dash for the interactive dashboard. This architecture efficiently handles multi-GB Obsidian vaults while providing responsive, feature-rich analysis capabilities.

## AI-Powered Note Summaries

The analyzer includes AI-powered summary generation using Claude API to automatically create summaries, extract keywords, and assign hashtags to your notes. This feature is particularly useful for large vaults where manual categorization would be time-consuming.

### Setting up AI Summaries

**IMPORTANT**: Use the manual method through Claude Code conversation instead of API keys. This is the preferred method as it doesn't require additional API costs and allows for review of summaries before saving.

1. **Manual Method (Preferred)**
   - Use the `manual_summary_helper.py` script to generate prompts
   - Paste prompts into your Claude Code conversation
   - Save the JSON responses and import them back
   - See MANUAL_SUMMARIES_GUIDE.md for detailed instructions

2. **API Method (Alternative)**
   - Only use if you need to process hundreds of notes automatically
   - Requires Anthropic API key and costs ~$0.003 per note
   - Install with: `pip install anthropic`

### Generating Summaries for Specific Folders

The most common use case is generating summaries for resource folders like `800_Ressources`:

```bash
# Quick method for 800_Ressources folder
./summarize_ressources.sh

# Or use the full script with options
python3 generate_ai_summaries.py --folder "800_Ressources" --limit 10
```

### Advanced AI Summary Options

The `generate_ai_summaries.py` script provides several options:

```bash
# Dry run to preview what will be processed
python3 generate_ai_summaries.py --folder "800_Ressources" --dry-run

# Process all notes in vault (no folder filter)
python3 generate_ai_summaries.py --folder ""

# Change batch save frequency (default: every 10 notes)
python3 generate_ai_summaries.py --folder "MyFolder" --batch-size 5

# Limit processing to first N notes
python3 generate_ai_summaries.py --folder "800_Ressources" --limit 50
```

### AI Summary Features

For each note, the AI generates:
- **Summary**: A 1-2 sentence description of the note's content
- **Hashtags**: Up to 5 relevant tags from predefined categories (#book, #AI, #meditation, #spirituality, #philosophy, #productivity, #programming, #health, #finance, #psychology, #relationship, #career, #education, #travel, #creativity, #science, #technology, #business, #writing, #personal)
- **Keywords**: 5-10 key concepts or terms from the note

### Viewing AI Summaries

After generating summaries, they are automatically integrated into the dashboard:
- Summaries appear in the note details panel when clicking on any note
- The Important Notes tab shows summaries for high-value notes
- AI-generated hashtags are included in the hashtag analysis
- Keywords enhance the search and similarity features

### Performance and Cost Considerations

- **Processing Speed**: Approximately 1-2 seconds per note due to API calls
- **Batch Processing**: Progress is saved every 10 notes by default
- **Resume Capability**: Already processed notes are automatically skipped
- **Rate Limiting**: Built-in delays prevent hitting API limits
- **Cost**: Approximately $0.003 per note using Claude 3 Sonnet

### Implementation Details

The AI classification system (`ai_classifier.py`) uses:
- Content-aware prompts that analyze the first 3000 characters of each note
- JSON-structured responses for reliable parsing
- File hash tracking to detect changes and avoid reprocessing
- Persistent storage in `ai_classifications.json`
- Integration with the main analyzer through `vault_analysis.json`

This AI enhancement transforms the Obsidian analyzer from a structural analysis tool into a comprehensive content understanding system, making it easier to navigate and understand large knowledge bases.

## Git Integration

The analyzer tracks git commit history for each file and uses it as a factor in importance scoring. Files with more commits are considered more important as they've been edited more frequently.

### Automatic Git Updates

**IMPORTANT**: Git commit counts are automatically refreshed every time you run the analyzer. The git cache is cleared before each analysis to ensure you always see the most current commit counts.

### Quick Git Update

To update only the git commit counts without re-analyzing the entire vault:

```bash
python3 update_git_counts.py
```

This script:
1. Clears the git cache
2. Updates commit counts for all files
3. Recalculates importance scores
4. Saves the updated analysis

### Git Importance Scoring

The git importance score is calculated based on commit count:
- 0 commits: 0.0 score
- 1 commit: 0.2 score (base for tracked files)
- 2 commits: 0.5 score
- 3 commits: 0.7 score
- 4-5 commits: 0.85 score
- 6+ commits: 1.0 score (maximum)

This score contributes 10% to the overall importance score of each note.

### Viewing Git Stats

In the dashboard:
- **Commit Count Column**: Shows the number of git commits for each file in all tables
- **Git Statistics Sidebar**: Displays overall git statistics for the vault
- **Importance Score Breakdown**: Shows how git activity contributes to note importance

### Changing Vault Location

If you move your vault to a new location, update the path in:
- `obsidian_analyzer.py` (main function)
- `update_vault_with_git.py` (vault_path variable)
- `run_analysis.py` (default argument)
- `analyze_vault.sh` (VAULT_PATH variable)

The analyzer will automatically detect the new git repository and update commit counts accordingly.

## Dashboard Development

### Important: Always Restart Dashboard After Changes

**CRITICAL**: After making any changes to `dashboard.py`, you MUST restart the dashboard server for the changes to take effect. The dashboard runs as a persistent web server and will not reflect code changes until restarted.

To restart the dashboard:
```bash
# Kill existing process and start new one
pkill -f 'python3 dashboard.py' && sleep 1 && nohup python3 dashboard.py > dashboard.log 2>&1 &

# Or use the convenience script
./restart_dashboard.sh
```

Always verify the dashboard is running after restart:
```bash
lsof -i :5006
```

This applies to ALL changes in dashboard.py including:
- Adding new tabs or features
- Modifying existing visualizations
- Updating data processing logic
- Changing UI elements or layouts
- Fixing bugs or issues
