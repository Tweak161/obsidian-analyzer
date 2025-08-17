# Git History Integration Plan

## Overview
Add git commit history tracking to the Obsidian analyzer to better assess note importance based on how frequently files have been edited.

## Implementation Plan

### 1. Data Collection (Git Integration)
- **Command to use**: `git rev-list --count HEAD -- <file_path>`
- **Batch processing**: Process all files in chunks to avoid performance issues
- **Data to collect**:
  - Commit count per file
  - First commit date (creation date)
  - Last commit date (last modification)
  - Optional: Commit frequency (commits per month)

### 2. Performance Considerations
- The vault has 16,522 files, so we need efficient batch processing
- Use subprocess with proper buffering
- Consider caching results since git history doesn't change for past commits
- Process files in parallel using multiprocessing

### 3. Data Storage
Add to each note's metadata in `vault_analysis.json`:
```json
{
  "note_id": "...",
  "git_stats": {
    "commit_count": 15,
    "first_commit_date": "2023-01-15",
    "last_commit_date": "2025-08-14",
    "commits_per_month": 0.5
  }
}
```

### 4. Importance Score Update
Current formula:
```python
importance_score = (
    0.3 * pagerank_score +
    0.25 * backlinks_count +
    0.25 * outgoing_links_count +
    0.15 * content_richness +
    0.05 * update_frequency
)
```

Proposed update to include git history:
```python
importance_score = (
    0.25 * pagerank_score +
    0.20 * backlinks_count +
    0.20 * outgoing_links_count +
    0.15 * content_richness +
    0.10 * git_commit_score +  # NEW
    0.10 * recency_score       # Based on last commit date
)
```

Where `git_commit_score` is normalized (0-1) based on:
- Notes with 1 commit: 0.0
- Notes with 2-5 commits: 0.3
- Notes with 6-10 commits: 0.6
- Notes with 11-20 commits: 0.8
- Notes with 20+ commits: 1.0

### 5. Dashboard Updates
Add "Commits" column to all relevant tables:
- Important Notes tab
- Orphaned Notes tab
- Hashtags tab (when viewing notes)
- Search results

### 6. Implementation Steps

#### Step 1: Create Git History Collector
- Create `git_analyzer.py` module
- Implement efficient batch processing
- Handle edge cases (deleted files, renames, etc.)

#### Step 2: Update Main Analyzer
- Integrate git stats collection into `obsidian_analyzer.py`
- Update importance score calculation
- Store git stats in metadata

#### Step 3: Update Dashboard
- Add commit count column to tables
- Update sorting/filtering options
- Add visual indicators (e.g., color coding for high-commit files)

### 7. Edge Cases to Handle
- Files not in git (new files)
- Renamed files (use `git log --follow`)
- Binary files (Excalidraw files)
- Files with special characters in names
- Very large repositories (performance)

### 8. Optional Enhancements
- Show commit heatmap in timeline view
- Track authors if multiple contributors
- Show commit messages for recent changes
- Identify "hot" files (many recent commits)

## Benefits
1. **Better importance scoring**: Frequently edited notes are likely more important
2. **Activity insights**: See which notes are actively maintained
3. **Historical context**: Understand note evolution
4. **Maintenance indicators**: Identify stale vs active content