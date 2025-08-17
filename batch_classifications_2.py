#!/usr/bin/env python3
"""Add batch classifications - Batch 2"""

from ai_classifier import AIClassifier
import json

vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
classifier = AIClassifier(vault_path)

# Classifications for the next 10 files
classifications = [
    {
        "file_path": "002_Input/+ Obsidian - How to Organize Your Notes - Effective Remote Work.md",
        "hashtags": ["#productivity", "#technology", "#writing"],
        "keywords": ["Obsidian", "note organization", "remote work", "knowledge management", "file structure"],
        "summary": "Tutorial on organizing notes in Obsidian for effective remote work, covering folder structures and organizational strategies."
    },
    {
        "file_path": "002_Input/+ Obsidian Tutorial - Taking Notes From Books.md",
        "hashtags": ["#education", "#productivity", "#writing", "#personal"],
        "keywords": ["Obsidian", "book notes", "reading", "note-taking", "Ethen Schwandt", "literature notes"],
        "summary": "Tutorial demonstrating methods for taking and organizing notes from books using Obsidian's features."
    },
    {
        "file_path": "002_Input/+ Obsidian VS Roam Research - Why Chose Obsidian.md",
        "hashtags": ["#technology", "#productivity", "#writing"],
        "keywords": ["Obsidian", "Roam Research", "comparison", "note-taking apps", "Bryan Jenks", "local storage", "block references"],
        "summary": "Comprehensive comparison between Obsidian and Roam Research, highlighting Obsidian's advantages in portability, offline usage, and local file storage, with Roam's strength in block-level referencing."
    },
    {
        "file_path": "002_Input/+ Organizing Obsidian with Maps of Content (MOCs).md",
        "hashtags": ["#productivity", "#technology", "#writing", "#creativity"],
        "keywords": ["Maps of Content", "MOCs", "Nick Milo", "Obsidian organization", "workspace", "launchpad", "structure notes"],
        "summary": "Guide to using Maps of Content (MOCs) developed by Nick Milo as workspaces or launchpads to organize and explore topics in Obsidian."
    },
    {
        "file_path": "002_Input/+ Structuring book notes with the Zettelkasten method.md",
        "hashtags": ["#education", "#productivity", "#writing", "#philosophy"],
        "keywords": ["Zettelkasten", "book notes", "atomic notes", "Martin Adams", "knowledge management", "interconnected ideas"],
        "summary": "Explains how to structure book notes using the Zettelkasten method, emphasizing atomic notes and recreating connections between ideas through linking."
    },
    {
        "file_path": "002_Input/+ YAML Metadata and Aliases (Bryan Jenks).md",
        "hashtags": ["#technology", "#productivity", "#programming"],
        "keywords": ["YAML", "metadata", "aliases", "Obsidian", "Bryan Jenks", "tags", "frontmatter"],
        "summary": "Technical guide on using YAML metadata and aliases in Obsidian, including syntax examples for tags, aliases, and custom metadata fields."
    },
    {
        "file_path": "002_Input/+ Zettelkasten deutsch - Smarte Notizen schreiben - Wissensmanagement 2.0.md",
        "hashtags": ["#education", "#productivity", "#writing", "#philosophy"],
        "keywords": ["Zettelkasten", "Wissensmanagement", "Joshua Meyer", "Literaturnotizen", "permanente Notizen", "Gedankenpalast", "Sönke Ahrens"],
        "summary": "German-language tutorial on the Zettelkasten method for smart note-taking, covering the four steps from literature notes to building a 'Gedankenpalast' (palace of thoughts)."
    },
    {
        "file_path": "002_Input/+.md",
        "hashtags": ["#technology", "#productivity"],
        "keywords": ["file notation", "YouTube videos", "content organization", "query"],
        "summary": "Simple index file for YouTube video notes, using '+' as a file notation prefix with a query to list all such files."
    },
    {
        "file_path": "002_Input/2022-03-111.md",
        "hashtags": ["#personal", "#productivity"],
        "keywords": ["daily note", "journal", "goals", "March 2022", "today"],
        "summary": "Daily note template for March 11, 2022, with sections for 'On This Day', notes created, and personal goals."
    },
    {
        "file_path": "002_Input/3 D Drucker Buying Guide.md",
        "hashtags": ["#technology", "#business", "#creativity"],
        "keywords": ["3D printer", "Ender 3", "Artillery Genius", "Elegoo Neptune", "buying guide", "FDM vs resin", "printer comparison"],
        "summary": "Comprehensive 3D printer buying guide comparing various models like Ender 3, Artillery Genius, and alternatives, with community recommendations and comparisons between FDM and resin printing."
    }
]

# Add all classifications
for item in classifications:
    classifier.add_manual_classification(
        file_path=item["file_path"],
        hashtags=item["hashtags"],
        keywords=item["keywords"],
        summary=item["summary"]
    )

print(f"Successfully added {len(classifications)} classifications")
print("Classifications saved to:", classifier.classifications_file)