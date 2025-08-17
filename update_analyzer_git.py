#!/usr/bin/env python3
"""Script to update the analyzer with git history functionality"""

# First, let's backup the original
import shutil
shutil.copy('obsidian_analyzer.py', 'obsidian_analyzer_backup.py')

# Now read the original file and update it
with open('obsidian_analyzer.py', 'r') as f:
    content = f.read()

# Add import for git_history
import_section = """import os
import re
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional
import hashlib

import networkx as nx
from obsidiantools.api import Vault
import pandas as pd
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from diskcache import Cache
from collections import Counter
import pickle
import string
from nltk.stem import PorterStemmer
from nltk.corpus import words
import nltk

from git_history import GitHistoryAnalyzer"""

content = content.replace("""import os
import re
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional
import hashlib

import networkx as nx
from obsidiantools.api import Vault
import pandas as pd
from rake_nltk import Rake
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from diskcache import Cache
from collections import Counter
import pickle
import string
from nltk.stem import PorterStemmer
from nltk.corpus import words
import nltk""", import_section)

# Update the __init__ method to include git analyzer
init_update = """    def __init__(self, vault_path: str, cache_dir: str = ".cache"):
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")
        
        self.cache = Cache(cache_dir)
        self.graph = nx.DiGraph()
        self.notes_metadata = {}
        self.orphaned_notes = set()
        self.important_notes = []
        self.keyword_metadata = {}
        self.ai_classifications = self._load_ai_classifications()
        
        # Initialize git analyzer
        self.git_analyzer = GitHistoryAnalyzer(str(self.vault_path))
        
        # Regex patterns
        self.wikilink_pattern = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')"""

content = content.replace("""    def __init__(self, vault_path: str, cache_dir: str = ".cache"):
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")
        
        self.cache = Cache(cache_dir)
        self.graph = nx.DiGraph()
        self.notes_metadata = {}
        self.orphaned_notes = set()
        self.important_notes = []
        self.keyword_metadata = {}
        self.ai_classifications = self._load_ai_classifications()
        
        # Regex patterns
        self.wikilink_pattern = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')""", init_update)

# Update the _process_file method to add git stats
# Find the line where metadata is assigned
process_update = """                                  ai_summary=ai_classification.get("ai_summary", ""),
                                  ai_hashtags=ai_classification.get("ai_hashtags", []),
                                  ai_keywords=ai_classification.get("ai_keywords", []))
        
        # Add git history stats
        if self.git_analyzer.is_git_repo:
            git_details = self.git_analyzer.get_file_history_details(str(relative_path))
            metadata["git_stats"] = git_details
            metadata["commit_count"] = git_details.get("commit_count", 0)
        else:
            metadata["git_stats"] = {"commit_count": 0}
            metadata["commit_count"] = 0"""

content = content.replace("""                                  ai_summary=ai_classification.get("ai_summary", ""),
                                  ai_hashtags=ai_classification.get("ai_hashtags", []),
                                  ai_keywords=ai_classification.get("ai_keywords", []))""", process_update)

# Update importance score calculation
importance_update = """    def _calculate_importance_scores(self) -> None:
        \"\"\"Calculate importance scores for all notes\"\"\"
        # Calculate PageRank
        try:
            pagerank = nx.pagerank(self.graph)
        except:
            pagerank = {node: 0.0 for node in self.graph.nodes()}
        
        # Calculate importance for each note
        for note_id, metadata in self.notes_metadata.items():
            # Get graph metrics
            in_degree = self.graph.in_degree(note_id)
            out_degree = self.graph.out_degree(note_id)
            pagerank_score = pagerank.get(note_id, 0.0)
            
            # Content richness score
            content_richness = (
                metadata["word_count"] / 1000.0 +  # Normalize word count
                len(metadata["images"]) * 0.5 +     # Images add value
                len(metadata["tags"]) * 0.2         # Tags indicate organization
            )
            
            # Git activity score
            commit_count = metadata.get("commit_count", 0)
            git_score = self.git_analyzer.calculate_git_importance_score(commit_count)
            
            # Calculate composite importance score
            importance_score = (
                0.25 * pagerank_score * 100 +       # PageRank (scaled)
                0.20 * in_degree +                  # Incoming links
                0.20 * out_degree +                 # Outgoing links
                0.15 * min(content_richness, 10) + # Content (capped)
                0.10 * git_score * 10 +            # Git activity (scaled)
                0.10 * 1.0                         # Base score
            )
            
            metadata["importance_score"] = importance_score
            metadata["in_degree"] = in_degree
            metadata["out_degree"] = out_degree
            metadata["pagerank"] = pagerank_score
            metadata["git_score"] = git_score"""

# Find and replace the _calculate_importance_scores method
import re
pattern = r'def _calculate_importance_scores\(self\) -> None:.*?metadata\["pagerank"\] = pagerank_score'
match = re.search(pattern, content, re.DOTALL)
if match:
    content = content.replace(match.group(0), importance_update.strip())

# Add git stats to the main function output
stats_update = """    stats = {
        "total_notes": len(analyzer.notes_metadata),
        "markdown_count": len(md_files),
        "excalidraw_count": len(excalidraw_files),
        "orphaned_count": len(analyzer.orphaned_notes),
        "graph_edges": analyzer.graph.number_of_edges(),
        "vault_path": str(vault_path),
        "analysis_date": datetime.now().isoformat(),
        "is_git_repo": analyzer.git_analyzer.is_git_repo
    }
    
    # Add git statistics if available
    if analyzer.git_analyzer.is_git_repo:
        file_paths = [meta.get("path", "") for meta in analyzer.notes_metadata.values()]
        git_stats = analyzer.git_analyzer.get_vault_statistics(file_paths)
        stats["git_stats"] = git_stats"""

# Replace the stats creation
content = re.sub(
    r'stats = \{[^}]+\}',
    stats_update.strip(),
    content,
    flags=re.DOTALL
)

# Write the updated file
with open('obsidian_analyzer.py', 'w') as f:
    f.write(content)

print("✓ Updated obsidian_analyzer.py with git history integration")