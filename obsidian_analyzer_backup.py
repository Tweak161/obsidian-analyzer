#!/usr/bin/env python3
"""
Obsidian Vault Analyzer
Scans and analyzes Obsidian vaults to create interactive visualizations
"""

import os
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


class ObsidianAnalyzer:
    """Main analyzer class for Obsidian vaults"""
    
    def __init__(self, vault_path: str, cache_dir: str = ".cache"):
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
        self.wikilink_pattern = re.compile(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]')
        self.tag_pattern = re.compile(r'#([\w\-\_\/]+)')
        self.image_pattern = re.compile(r'!\[\[([^\]]+)\]\]|!\[([^\]]*)\]\(([^\)]+)\)')
        
        # Keyword extraction
        self.rake = Rake(max_length=3, min_length=1)
        self.stemmer = PorterStemmer()
        
        # Try to load English words dictionary
        try:
            nltk.download('words', quiet=True)
            self.english_words = set(words.words())
        except:
            print("Warning: Could not load English words dictionary")
            self.english_words = set()
        
        # Enhanced hashtag categories with weighted keywords and stems (English + German)
        self.hashtag_categories = {
            "#book": {
                "keywords": ["book", "reading", "literature", "author", "novel", "chapter", "summary", "review", "read", "write", "story", "fiction", "nonfiction",
                           "buch", "bücher", "lesen", "literatur", "autor", "roman", "kapitel", "zusammenfassung", "rezension", "geschichte", "fiktion"],
                "weight": 1.0
            },
            "#AI": {
                "keywords": ["ai", "artificial", "intelligence", "machine", "learning", "neural", "deep", "model", "algorithm", "gpt", "llm", "transformer", "chatgpt", "claude", "openai", "anthropic", "prompt", "dataset", "training",
                           "ki", "künstlich", "intelligenz", "maschinelles", "lernen", "neuronales", "netz", "modell", "algorithmus", "daten"],
                "weight": 1.2
            },
            "#meditation": {
                "keywords": ["meditation", "meditate", "mindfulness", "mindful", "breathing", "breath", "awareness", "aware", "focus", "concentration", "calm", "zen", "vipassana", "anapana", "samadhi", "sila", "panna", "dhamma", "sitting", "practice", "retreat", "noble", "eightfold", "path",
                           "meditation", "meditieren", "achtsamkeit", "achtsam", "atmen", "atem", "atmung", "bewusstsein", "bewusst", "fokus", "konzentration", "ruhe", "ruhig", "praxis", "übung", "sitzen"],
                "weight": 1.3
            },
            "#spirituality": {
                "keywords": ["spiritual", "spirit", "soul", "consciousness", "enlightenment", "enlighten", "buddha", "buddhist", "buddhism", "dharma", "karma", "transcendent", "transcend", "sacred", "divine", "mystic", "mystical", "awakening", "awaken",
                           "spirituell", "spiritualität", "geist", "seele", "bewusstsein", "erleuchtung", "erleuchtet", "buddha", "buddhismus", "dharma", "karma", "transzendent", "heilig", "göttlich", "mystisch", "mystik", "erwachen", "erwacht"],
                "weight": 1.2
            },
            "#philosophy": {
                "keywords": ["philosophy", "philosophical", "philosopher", "ethics", "ethical", "morality", "moral", "existential", "metaphysics", "epistemology", "logic", "reason", "kant", "nietzsche", "plato", "aristotle", "socrates", "wisdom",
                           "philosophie", "philosophisch", "philosoph", "ethik", "ethisch", "moral", "moralisch", "existentiell", "metaphysik", "epistemologie", "logik", "vernunft", "weisheit", "denken", "gedanke"],
                "weight": 1.1
            },
            "#productivity": {
                "keywords": ["productivity", "productive", "efficiency", "efficient", "workflow", "task", "goal", "habit", "routine", "time", "management", "organize", "organization", "planning", "plan", "gtd", "pomodoro", "schedule",
                           "produktivität", "produktiv", "effizienz", "effizient", "arbeitsablauf", "aufgabe", "ziel", "gewohnheit", "routine", "zeit", "management", "organisieren", "organisation", "planung", "plan", "zeitplan"],
                "weight": 1.0
            },
            "#programming": {
                "keywords": ["code", "coding", "programming", "programmer", "software", "development", "developer", "function", "class", "algorithm", "debug", "api", "python", "javascript", "java", "typescript", "react", "node", "git", "github", "variable", "method", "compile", "syntax",
                           "code", "programmierung", "programmieren", "programmierer", "software", "entwicklung", "entwickler", "funktion", "klasse", "algorithmus", "fehler", "variabel", "methode", "syntax"],
                "weight": 1.1
            },
            "#health": {
                "keywords": ["health", "healthy", "fitness", "fit", "exercise", "nutrition", "wellness", "medical", "medicine", "doctor", "treatment", "disease", "symptom", "therapy", "diet", "sleep", "stress", "mental", "physical",
                           "gesundheit", "gesund", "fitness", "übung", "sport", "ernährung", "wohlbefinden", "medizin", "medizinisch", "arzt", "behandlung", "krankheit", "symptom", "therapie", "diät", "schlaf", "stress", "mental", "körper", "körperlich"],
                "weight": 1.0
            },
            "#finance": {
                "keywords": ["finance", "financial", "money", "investment", "invest", "stock", "budget", "savings", "save", "wealth", "trading", "trade", "crypto", "cryptocurrency", "bitcoin", "market", "portfolio", "dividend", "compound", "interest", "retirement", "fire",
                           "finanzen", "finanziell", "geld", "investition", "investieren", "aktie", "budget", "ersparnisse", "sparen", "vermögen", "handel", "handeln", "krypto", "markt", "portfolio", "dividende", "zinsen", "rente", "ruhestand"],
                "weight": 1.1
            },
            "#psychology": {
                "keywords": ["psychology", "psychological", "mental", "cognitive", "behavior", "behaviour", "emotion", "emotional", "therapy", "therapist", "mindset", "personality", "depression", "anxiety", "trauma", "healing", "freud", "jung",
                           "psychologie", "psychologisch", "mental", "kognitiv", "verhalten", "emotion", "emotional", "therapie", "therapeut", "persönlichkeit", "depression", "angst", "trauma", "heilung"],
                "weight": 1.1
            },
            "#relationship": {
                "keywords": ["relationship", "relate", "love", "partner", "dating", "date", "marriage", "marry", "family", "friend", "friendship", "communication", "communicate", "connection", "connect", "social", "interpersonal",
                           "beziehung", "liebe", "partner", "partnerschaft", "heirat", "heiraten", "ehe", "familie", "freund", "freundschaft", "kommunikation", "kommunizieren", "verbindung", "sozial", "zwischenmenschlich"],
                "weight": 1.0
            },
            "#career": {
                "keywords": ["career", "job", "work", "professional", "profession", "resume", "interview", "skills", "skill", "promotion", "promote", "salary", "employer", "employee", "workplace", "linkedin", "networking",
                           "karriere", "beruf", "arbeit", "arbeiten", "professionell", "lebenslauf", "bewerbung", "interview", "fähigkeiten", "beförderung", "gehalt", "arbeitgeber", "arbeitnehmer", "arbeitsplatz", "netzwerk"],
                "weight": 1.0
            },
            "#education": {
                "keywords": ["education", "educational", "learning", "learn", "study", "course", "university", "college", "knowledge", "research", "academic", "student", "teacher", "professor", "degree", "school", "curriculum",
                           "bildung", "ausbildung", "lernen", "studium", "studieren", "kurs", "universität", "hochschule", "wissen", "forschung", "akademisch", "student", "lehrer", "professor", "abschluss", "schule"],
                "weight": 1.0
            },
            "#travel": {
                "keywords": ["travel", "trip", "vacation", "destination", "journey", "explore", "exploration", "tourist", "tourism", "adventure", "flight", "hotel", "country", "city", "culture", "passport", "luggage",
                           "reise", "reisen", "urlaub", "ferien", "reiseziel", "erkunden", "tourist", "tourismus", "abenteuer", "flug", "hotel", "land", "stadt", "kultur", "reisepass", "gepäck"],
                "weight": 1.0
            },
            "#creativity": {
                "keywords": ["creative", "creativity", "create", "art", "artist", "artistic", "design", "designer", "imagination", "imagine", "innovation", "innovate", "brainstorm", "inspiration", "inspire", "craft", "draw", "paint",
                           "kreativ", "kreativität", "kunst", "künstler", "künstlerisch", "design", "designer", "fantasie", "vorstellung", "innovation", "innovativ", "inspiration", "inspirieren", "handwerk", "zeichnen", "malen"],
                "weight": 1.0
            },
            "#science": {
                "keywords": ["science", "scientific", "scientist", "experiment", "research", "theory", "hypothesis", "physics", "chemistry", "biology", "mathematics", "data", "analysis", "evidence", "peer", "review", "study",
                           "wissenschaft", "wissenschaftlich", "wissenschaftler", "experiment", "forschung", "theorie", "hypothese", "physik", "chemie", "biologie", "mathematik", "daten", "analyse", "beweis", "studie"],
                "weight": 1.1
            },
            "#technology": {
                "keywords": ["technology", "tech", "technical", "digital", "software", "hardware", "internet", "computer", "device", "app", "application", "web", "cloud", "server", "database", "network", "cyber",
                           "technologie", "technik", "technisch", "digital", "software", "hardware", "internet", "computer", "gerät", "app", "anwendung", "web", "cloud", "server", "datenbank", "netzwerk"],
                "weight": 1.0
            },
            "#business": {
                "keywords": ["business", "entrepreneur", "entrepreneurship", "startup", "company", "management", "manager", "strategy", "strategic", "marketing", "market", "sales", "revenue", "profit", "customer", "client", "product",
                           "geschäft", "unternehmer", "unternehmertum", "startup", "firma", "unternehmen", "management", "manager", "strategie", "strategisch", "marketing", "markt", "verkauf", "umsatz", "gewinn", "kunde", "klient", "produkt"],
                "weight": 1.0
            },
            "#writing": {
                "keywords": ["writing", "write", "writer", "author", "blog", "blogging", "article", "journal", "draft", "editing", "edit", "publish", "story", "narrative", "essay", "prose", "poetry", "content",
                           "schreiben", "schrift", "schriftsteller", "autor", "blog", "artikel", "tagebuch", "journal", "entwurf", "bearbeitung", "bearbeiten", "veröffentlichen", "geschichte", "erzählung", "aufsatz", "prosa", "poesie", "inhalt"],
                "weight": 1.0
            },
            "#personal": {
                "keywords": ["personal", "self", "reflection", "reflect", "journal", "diary", "thoughts", "thought", "experience", "life", "growth", "development", "identity", "values", "beliefs", "goals",
                           "persönlich", "selbst", "reflexion", "reflektieren", "tagebuch", "gedanken", "gedanke", "erfahrung", "leben", "wachstum", "entwicklung", "identität", "werte", "glauben", "ziele"],
                "weight": 0.8
            }
        }
        
    def scan_vault(self) -> Dict:
        """Scan the entire vault and collect metadata"""
        print(f"Scanning vault at: {self.vault_path}")
        
        # Find all markdown and excalidraw files
        md_files = list(self.vault_path.rglob("*.md"))
        excalidraw_files = list(self.vault_path.rglob("*.excalidraw"))
        excalidraw_md_files = list(self.vault_path.rglob("*.excalidraw.md"))
        
        # Remove .excalidraw.md files from md_files to avoid double counting
        md_files = [f for f in md_files if not str(f).endswith('.excalidraw.md')]
        
        # Combine all excalidraw files
        all_excalidraw_files = excalidraw_files + excalidraw_md_files
        
        print(f"Found {len(md_files)} markdown files and {len(all_excalidraw_files)} excalidraw files")
        
        # Process each file
        for file_path in md_files + all_excalidraw_files:
            self._process_file(file_path)
        
        # Calculate graph metrics
        self._calculate_importance_scores()
        self._identify_orphans()
        
        # Extract keywords and classify notes
        self._extract_keywords_and_classify()
        
        # Save keyword metadata
        self._save_keyword_metadata()
        
        return {
            "total_notes": len(self.notes_metadata),
            "markdown_count": len(md_files),
            "excalidraw_count": len(all_excalidraw_files),
            "orphaned_count": len(self.orphaned_notes),
            "graph_nodes": self.graph.number_of_nodes(),
            "graph_edges": self.graph.number_of_edges()
        }
    
    def _process_file(self, file_path: Path) -> None:
        """Process a single file and extract metadata"""
        # Skip if it's actually a directory
        if file_path.is_dir():
            print(f"Skipping directory: {file_path}")
            return
            
        relative_path = file_path.relative_to(self.vault_path)
        note_id = str(relative_path.with_suffix(''))
        
        # Get file stats
        try:
            stat = file_path.stat()
        except OSError as e:
            print(f"Error accessing file {file_path}: {e}")
            return
        
        metadata = {
            "path": str(relative_path),
            "absolute_path": str(file_path),
            "type": "excalidraw" if (str(file_path).endswith(".excalidraw.md") or file_path.suffix == ".excalidraw") else file_path.suffix[1:],  # Remove the dot
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.fromtimestamp(stat.st_mtime),
            "links_out": [],
            "links_in": [],
            "tags": [],
            "images": [],
            "word_count": 0,
            "content_hash": self._get_file_hash(file_path)
        }
        
        # Parse content based on file type
        if str(file_path).endswith(".excalidraw.md") or file_path.suffix == ".excalidraw":
            self._parse_excalidraw(file_path, metadata)
        elif file_path.suffix == ".md":
            self._parse_markdown(file_path, metadata)
        
        # Add to graph
        self.graph.add_node(note_id, **metadata)
        
        # Add edges for outgoing links
        for link in metadata["links_out"]:
            # Only add edge if target exists or create placeholder
            if link not in self.graph:
                # Add placeholder node for link target
                self.graph.add_node(link, path=link, type="missing", 
                                  importance_score=0.0, in_degree=0, out_degree=0)
            self.graph.add_edge(note_id, link)
        
        self.notes_metadata[note_id] = metadata
    
    def _parse_markdown(self, file_path: Path, metadata: Dict) -> None:
        """Parse markdown file for links, tags, and content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self._parse_markdown_content(content, metadata)
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
    
    def _parse_excalidraw(self, file_path: Path, metadata: Dict) -> None:
        """Parse excalidraw file for embedded markdown and links"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if this is a .excalidraw.md file (with frontmatter)
            if str(file_path).endswith('.excalidraw.md'):
                # Find the JSON data section (after the frontmatter and markers)
                # Look for the JSON that starts with {"type":"excalidraw"
                json_start = content.find('{"type":"excalidraw"')
                if json_start != -1:
                    # Find the end of the JSON (matching closing brace)
                    # This is a simplified approach - for complex nested JSON, 
                    # we'd need a proper parser
                    brace_count = 0
                    json_end = json_start
                    for i in range(json_start, len(content)):
                        if content[i] == '{':
                            brace_count += 1
                        elif content[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                json_end = i + 1
                                break
                    
                    json_content = content[json_start:json_end]
                    data = json.loads(json_content)
                else:
                    # No JSON found, just parse as markdown
                    self._parse_markdown_content(content, metadata)
                    return
            else:
                # Regular .excalidraw file - pure JSON
                data = json.loads(content)
            
            # Look for text elements that might contain links
            for element in data.get("elements", []):
                if element.get("type") == "text" and element.get("text"):
                    text = element["text"]
                    
                    # Extract wikilinks from text
                    wikilinks = self.wikilink_pattern.findall(text)
                    for link_match in wikilinks:
                        link_target = link_match[0]
                        metadata["links_out"].append(link_target)
            
            # Count elements as "content"
            metadata["word_count"] = len(data.get("elements", []))
            
        except Exception as e:
            print(f"Error parsing excalidraw {file_path}: {e}")
    
    def _parse_markdown_content(self, content: str, metadata: Dict) -> None:
        """Parse markdown content for links, tags, and other metadata"""
        # Extract wikilinks
        wikilinks = self.wikilink_pattern.findall(content)
        for link_match in wikilinks:
            link_target = link_match[0]
            metadata["links_out"].append(link_target)
        
        # Extract tags
        tags = self.tag_pattern.findall(content)
        metadata["tags"] = list(set(tags))
        
        # Extract images
        images = self.image_pattern.findall(content)
        metadata["images"] = [img[0] or img[2] for img in images]
        
        # Calculate word count
        metadata["word_count"] = len(content.split())
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate file hash for change detection"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            print(f"Error hashing {file_path}: {e}")
            return ""
    
    def _calculate_importance_scores(self) -> None:
        """Calculate importance scores for all notes"""
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
            
            # Calculate composite importance score
            importance_score = (
                0.3 * pagerank_score * 100 +       # PageRank (scaled)
                0.25 * in_degree +                  # Incoming links
                0.25 * out_degree +                 # Outgoing links
                0.15 * min(content_richness, 10) +  # Content (capped)
                0.05 * 1.0                          # Base score
            )
            
            metadata["importance_score"] = importance_score
            metadata["in_degree"] = in_degree
            metadata["out_degree"] = out_degree
            metadata["pagerank"] = pagerank_score
    
    def _identify_orphans(self) -> None:
        """Identify notes without any connections"""
        for note_id, metadata in self.notes_metadata.items():
            # Check if this is an actual file (not a missing link target)
            if metadata.get("type") != "missing":
                if (self.graph.in_degree(note_id) == 0 and 
                    self.graph.out_degree(note_id) == 0):
                    self.orphaned_notes.add(note_id)
    
    def _is_valid_word(self, word: str) -> bool:
        """Check if a word is valid (not hex codes, etc.)"""
        # Remove common punctuation
        word_clean = word.strip().lower()
        
        # Skip if too short or too long
        if len(word_clean) < 3 or len(word_clean) > 25:  # Increased for German compound words
            return False
            
        # Skip if contains too many numbers
        if sum(c.isdigit() for c in word_clean) > len(word_clean) * 0.5:
            return False
            
        # Skip if looks like hex code (e.g., ffffff)
        if all(c in '0123456789abcdef' for c in word_clean) and len(word_clean) >= 6:
            return False
            
        # Check if contains at least one letter (handles German umlauts)
        if not any(c.isalpha() for c in word_clean):
            return False
            
        # For longer words, optionally check dictionary (but allow German words)
        # Skip dictionary check for now since we don't have a German dictionary
        
        return True
    
    def _extract_keywords_and_classify(self) -> None:
        """Extract keywords from each note and classify with hashtags"""
        print("Extracting keywords and classifying notes...")
        
        total_notes = len(self.notes_metadata)
        processed = 0
        
        for note_id, metadata in self.notes_metadata.items():
            if metadata.get("type") == "missing":
                continue
                
            # Combine content from various sources
            text_parts = []
            
            # Add filename (without extension)
            filename = Path(metadata["path"]).stem
            text_parts.append(filename.replace("-", " ").replace("_", " "))
            
            # Add existing tags
            text_parts.extend(metadata.get("tags", []))
            
            # Add linked note names
            for link in metadata.get("links_out", []):
                text_parts.append(link.replace("-", " ").replace("_", " "))
            
            # Read file content for keyword extraction (limit to first 3000 chars for better context)
            try:
                with open(metadata["absolute_path"], 'r', encoding='utf-8') as f:
                    content = f.read(3000)
                    # Remove code blocks and special characters
                    content = re.sub(r'```[^`]*```', '', content)  # Remove code blocks
                    content = re.sub(r'`[^`]+`', '', content)      # Remove inline code
                    content = re.sub(r'https?://\S+', '', content)  # Remove URLs
                    text_parts.append(content)
            except Exception:
                pass
            
            # Combine all text
            full_text = " ".join(text_parts)
            
            # Extract keywords using RAKE with filtering
            keywords = []
            if full_text.strip():
                try:
                    # Clean text for RAKE
                    clean_text = re.sub(r'[^\w\s]', ' ', full_text)
                    clean_text = ' '.join(word for word in clean_text.split() if self._is_valid_word(word))
                    
                    self.rake.extract_keywords_from_text(clean_text)
                    keyword_scores = self.rake.get_ranked_phrases_with_scores()
                    
                    # Filter and get top keywords
                    valid_keywords = []
                    for score, phrase in keyword_scores:
                        # Check if phrase contains valid words
                        words = phrase.split()
                        if all(self._is_valid_word(w) for w in words):
                            valid_keywords.append(phrase)
                        if len(valid_keywords) >= 15:  # Limit to 15 keywords
                            break
                    
                    keywords = valid_keywords
                except Exception as e:
                    print(f"Error extracting keywords from {note_id}: {e}")
            
            # Enhanced hashtag classification with weighted scoring
            hashtag_scores = {}
            full_text_lower = full_text.lower()
            words_in_text = set(full_text_lower.split())
            
            for hashtag, category_data in self.hashtag_categories.items():
                score = 0
                matched_keywords = []
                
                # Check each category keyword
                for keyword in category_data["keywords"]:
                    # Direct match
                    if keyword in full_text_lower:
                        score += 2.0
                        matched_keywords.append(keyword)
                    # Word match
                    elif keyword in words_in_text:
                        score += 1.5
                        matched_keywords.append(keyword)
                    # Stem match
                    else:
                        keyword_stem = self.stemmer.stem(keyword)
                        for word in words_in_text:
                            if self.stemmer.stem(word) == keyword_stem:
                                score += 1.0
                                matched_keywords.append(f"{word}→{keyword}")
                                break
                
                # Apply weight and threshold
                if score > 0:
                    weighted_score = score * category_data["weight"]
                    if weighted_score >= 2.0:  # Threshold for classification
                        hashtag_scores[hashtag] = (weighted_score, matched_keywords)
            
            # Select hashtags with highest scores (max 5)
            selected_hashtags = sorted(hashtag_scores.items(), key=lambda x: x[1][0], reverse=True)[:5]
            hashtags = [tag for tag, _ in selected_hashtags]
            
            # Check for AI classifications
            relative_path = metadata["path"]
            ai_data = self.ai_classifications.get(relative_path, {})
            
            # Combine rule-based and AI hashtags
            combined_hashtags = list(set(hashtags + ai_data.get("ai_hashtags", [])))
            combined_keywords = list(set(keywords + ai_data.get("ai_keywords", [])))
            
            # Store keyword metadata
            self.keyword_metadata[note_id] = {
                "keywords": combined_keywords,
                "hashtags": combined_hashtags,
                "path": metadata["path"],
                "ai_summary": ai_data.get("ai_summary", "")
            }
            
            # Also add to main metadata
            metadata["keywords"] = combined_keywords
            metadata["auto_hashtags"] = combined_hashtags
            metadata["ai_summary"] = ai_data.get("ai_summary", "")
            
            # Progress update
            processed += 1
            if processed % 100 == 0:
                print(f"  Processed {processed}/{total_notes} notes...")
    
    def _save_keyword_metadata(self) -> None:
        """Save keyword metadata to persistent file"""
        metadata_file = self.vault_path.parent / "keyword_metadata.pkl"
        try:
            with open(metadata_file, 'wb') as f:
                pickle.dump(self.keyword_metadata, f)
            print(f"Saved keyword metadata to {metadata_file}")
        except Exception as e:
            print(f"Error saving keyword metadata: {e}")
    
    def load_keyword_metadata(self) -> Dict:
        """Load keyword metadata from persistent file"""
        metadata_file = self.vault_path.parent / "keyword_metadata.pkl"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading keyword metadata: {e}")
        return {}
    
    def _load_ai_classifications(self) -> Dict:
        """Load AI classifications if available"""
        ai_file = self.vault_path.parent / "ai_classifications.json"
        if ai_file.exists():
            try:
                with open(ai_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Convert to simpler format for easier access
                    return {
                        path: {
                            "ai_hashtags": item.get("ai_hashtags", []),
                            "ai_keywords": item.get("ai_keywords", []),
                            "ai_summary": item.get("ai_summary", "")
                        }
                        for path, item in data.items()
                    }
            except Exception as e:
                print(f"Error loading AI classifications: {e}")
        return {}
    
    def get_timeline_data(self) -> Dict:
        """Get data for timeline visualizations"""
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame.from_dict(self.notes_metadata, orient='index')
        
        # Sort by dates
        created_timeline = df[['created', 'path', 'type', 'importance_score']].sort_values('created')
        modified_timeline = df[['modified', 'path', 'type', 'importance_score']].sort_values('modified')
        
        return {
            "created": created_timeline.to_dict('records'),
            "modified": modified_timeline.to_dict('records')
        }
    
    def get_important_notes(self, top_n: int = 20) -> List[Dict]:
        """Get the most important notes"""
        sorted_notes = sorted(
            self.notes_metadata.items(),
            key=lambda x: x[1]["importance_score"],
            reverse=True
        )
        
        return [
            {
                "id": note_id,
                **metadata
            }
            for note_id, metadata in sorted_notes[:top_n]
        ]
    
    def get_orphaned_notes(self) -> List[Dict]:
        """Get all orphaned notes"""
        return [
            {
                "id": note_id,
                **self.notes_metadata[note_id]
            }
            for note_id in self.orphaned_notes
        ]
    
    def get_notes_by_hashtag(self, hashtag: str) -> List[Dict]:
        """Get all notes with a specific hashtag"""
        notes = []
        for note_id, metadata in self.notes_metadata.items():
            if metadata.get("type") != "missing" and hashtag in metadata.get("auto_hashtags", []):
                notes.append({
                    "id": note_id,
                    **metadata
                })
        return sorted(notes, key=lambda x: x.get("importance_score", 0), reverse=True)
    
    def get_all_hashtags(self) -> List[Dict]:
        """Get all unique hashtags with counts"""
        hashtag_counts = Counter()
        for metadata in self.notes_metadata.values():
            if metadata.get("type") != "missing":
                for hashtag in metadata.get("auto_hashtags", []):
                    hashtag_counts[hashtag] += 1
        
        return [{"hashtag": tag, "count": count} 
                for tag, count in hashtag_counts.most_common()]
    
    def export_graph_data(self) -> Dict:
        """Export graph data for visualization"""
        nodes = []
        edges = []
        
        for node_id, data in self.graph.nodes(data=True):
            # Skip nodes without proper data (might be link targets without files)
            if "path" not in data:
                continue
                
            importance = data.get("importance_score", 0.0)
            nodes.append({
                "id": node_id,
                "label": Path(data["path"]).stem if "path" in data else node_id,
                "title": f"{data.get('path', node_id)}\nImportance: {importance:.2f}",
                "value": importance,
                "group": data.get("type", "unknown")
            })
        
        for source, target in self.graph.edges():
            edges.append({
                "from": source,
                "to": target
            })
        
        return {"nodes": nodes, "edges": edges}


def main():
    """Main entry point"""
    vault_path = r"\\mnt\\c\\Users\\hess\\OneDrive\\Dokumente\\MyVault"
    
    # Convert Windows path to WSL path if needed
    if vault_path.startswith(r"\\mnt\\"):
        vault_path = vault_path.replace("\\", "/")
    
    analyzer = ObsidianAnalyzer(vault_path)
    
    # Scan the vault
    stats = analyzer.scan_vault()
    print(f"\nVault Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Get important notes
    important_notes = analyzer.get_important_notes(10)
    print(f"\nTop 10 Important Notes:")
    for note in important_notes:
        print(f"  - {note['path']} (score: {note['importance_score']:.2f})")
    
    # Get orphaned notes
    orphaned = analyzer.get_orphaned_notes()
    print(f"\nOrphaned Notes ({len(orphaned)} total):")
    for note in orphaned[:10]:  # Show first 10
        print(f"  - {note['path']}")
    
    # Export data for dashboard
    timeline_data = analyzer.get_timeline_data()
    graph_data = analyzer.export_graph_data()
    hashtags = analyzer.get_all_hashtags()
    
    # Save data for dashboard
    output_data = {
        "stats": stats,
        "important_notes": important_notes,
        "orphaned_notes": orphaned,
        "timeline": timeline_data,
        "graph": graph_data,
        "hashtags": hashtags,
        "notes_metadata": analyzer.notes_metadata
    }
    
    with open("vault_analysis.json", "w") as f:
        json.dump(output_data, f, default=str, indent=2)
    
    print("\nAnalysis complete! Data saved to vault_analysis.json")


if __name__ == "__main__":
    main()