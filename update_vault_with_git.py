#!/usr/bin/env python3
"""Update existing vault analysis with git commit counts"""
import json
from git_history import GitHistoryAnalyzer
from datetime import datetime

print("Loading existing vault analysis...")
with open('vault_analysis.json', 'r') as f:
    data = json.load(f)

vault_path = "//mnt/c/Users/hess/Lokal/MyVault"
notes_metadata = data.get('notes_metadata', {})

# Initialize git analyzer
git_analyzer = GitHistoryAnalyzer(vault_path)

# Clear cache to ensure fresh git data
print("Clearing git cache to ensure fresh data...")
git_analyzer.clear_cache()

if not git_analyzer.is_git_repo:
    print("Vault is not a git repository!")
    exit(1)

print(f"✓ Vault is a git repository")
print(f"Updating git stats for {len(notes_metadata)} notes...")

# Collect all file paths
file_paths = []
for note_id, meta in notes_metadata.items():
    if isinstance(meta, dict) and meta.get('path'):
        file_paths.append(meta.get('path'))

# Analyze git history in batches
git_results = git_analyzer.analyze_files_batch(file_paths, batch_size=100, max_workers=8)

# Update notes metadata with git stats
updated_count = 0
for note_id, meta in notes_metadata.items():
    if isinstance(meta, dict):
        path = meta.get('path', '')
        if path in git_results:
            git_details = git_results[path]
            meta['git_stats'] = git_details
            meta['commit_count'] = git_details.get('commit_count', 0)
            
            # Recalculate importance score with git component
            in_degree = meta.get('in_degree', 0)
            out_degree = meta.get('out_degree', 0)
            pagerank_score = meta.get('pagerank', 0.0)
            word_count = meta.get('word_count', 0)
            images_count = len(meta.get('images', []))
            tags_count = len(meta.get('tags', []))
            
            # Content richness score
            content_richness = (
                word_count / 1000.0 +  # Normalize word count
                images_count * 0.5 +     # Images add value
                tags_count * 0.2         # Tags indicate organization
            )
            
            # Git activity score
            commit_count = git_details.get('commit_count', 0)
            git_score = git_analyzer.calculate_git_importance_score(commit_count)
            
            # Calculate composite importance score
            importance_score = (
                0.30 * git_score * 10 +            # Git activity (scaled) - MOST IMPORTANT
                0.20 * pagerank_score * 100 +       # PageRank (scaled)
                0.15 * in_degree +                  # Incoming links
                0.15 * out_degree +                 # Outgoing links
                0.10 * min(content_richness, 10) + # Content (capped)
                0.10 * 1.0                         # Base score
            )
            
            meta['importance_score'] = importance_score
            meta['git_score'] = git_score
            updated_count += 1

print(f"Updated {updated_count} notes with git stats")

# Track importance score changes
print("\nNotes with significant importance score changes:")
score_changes = []
for note_id, meta in notes_metadata.items():
    if isinstance(meta, dict):
        path = meta.get('path', '')
        new_score = meta.get('importance_score', 0)
        # Find old score in previous important notes
        old_score = 0
        for old_note in data.get('important_notes', []):
            if old_note.get('path') == path:
                old_score = old_note.get('importance_score', 0)
                break
        if abs(new_score - old_score) > 0.5:  # Significant change
            score_changes.append({
                'path': path,
                'old_score': old_score,
                'new_score': new_score,
                'change': new_score - old_score,
                'commit_count': meta.get('commit_count', 0)
            })

# Sort by change magnitude
score_changes.sort(key=lambda x: abs(x['change']), reverse=True)
for item in score_changes[:10]:  # Show top 10 changes
    direction = "↑" if item['change'] > 0 else "↓"
    print(f"  {direction} {item['path'].split('/')[-1]}: {item['old_score']:.1f} → {item['new_score']:.1f} (commits: {item['commit_count']})")

# Get overall git statistics
print("Calculating vault git statistics...")
git_stats = git_analyzer.get_vault_statistics(file_paths)

# Update stats
data['stats']['is_git_repo'] = True
data['stats']['git_stats'] = git_stats

# Regenerate important notes list based on new scores
print("Regenerating important notes list...")
important_notes = []
for note_id, metadata in notes_metadata.items():
    if isinstance(metadata, dict) and metadata.get('importance_score', 0) > 5:
        important_notes.append(metadata)

# Sort by importance score
important_notes.sort(key=lambda x: x['importance_score'], reverse=True)
data['important_notes'] = important_notes[:100]  # Top 100

# Update orphaned notes with commit counts and importance scores
orphaned_notes = []
for note in data.get('orphaned_notes', []):
    if isinstance(note, dict):
        path = note.get('path', '')
        # Find the metadata for this orphaned note
        for note_id, meta in notes_metadata.items():
            if isinstance(meta, dict) and meta.get('path') == path:
                note['commit_count'] = meta.get('commit_count', 0)
                note['git_stats'] = meta.get('git_stats', {})
                note['importance_score'] = meta.get('importance_score', 0)
                note['git_score'] = meta.get('git_score', 0)
                break
        orphaned_notes.append(note)
data['orphaned_notes'] = orphaned_notes

# Update timeline data with commit counts and importance scores
for timeline_type in ['created', 'modified']:
    timeline_data = data.get('timeline', {}).get(timeline_type, [])
    for item in timeline_data:
        if isinstance(item, dict):
            path = item.get('path', '')
            # Find the metadata for this timeline item
            for note_id, meta in notes_metadata.items():
                if isinstance(meta, dict) and meta.get('path') == path:
                    item['commit_count'] = meta.get('commit_count', 0)
                    item['importance_score'] = meta.get('importance_score', 0)
                    item['git_score'] = meta.get('git_score', 0)
                    break

# Update notes_metadata in the main data (so hashtag browser has updated scores)
data['notes_metadata'] = notes_metadata

# Save updated analysis
print("Saving updated analysis...")
data['stats']['analysis_date'] = datetime.now().isoformat()
with open('vault_analysis_with_git.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✓ Analysis updated successfully!")
print(f"Git Statistics:")
print(f"  Files with history: {git_stats['files_with_history']}")
print(f"  Average commits: {git_stats['average_commits']:.2f}")
print(f"  Max commits: {git_stats['max_commits']}")
if git_stats['most_edited_files']:
    print(f"\nMost edited files:")
    for item in git_stats['most_edited_files'][:5]:
        print(f"  {item['file']}: {item['commits']} commits")