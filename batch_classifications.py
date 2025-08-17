#!/usr/bin/env python3
"""Add batch classifications"""

from ai_classifier import AIClassifier
import json

vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
classifier = AIClassifier(vault_path)

# Classifications for the 10 files
classifications = [
    {
        "file_path": "001_Inbox/I'm 35, I'm stuck and I can't get my years back.md",
        "hashtags": ["#career", "#personal", "#psychology", "#productivity"],
        "keywords": ["midlife crisis", "career transition", "depression", "motivation", "confidence", "John Sonmez"],
        "summary": "Email from John Sonmez addressing feelings of being stuck at age 35, discussing depression about career progress and introducing a 'kill reward' mental technique from video game design to overcome these feelings."
    },
    {
        "file_path": "002_Input/% Podcast Test Note for checking Airr Recording and Readwise Extracting Workflow.md",
        "hashtags": ["#technology", "#programming", "#science"],
        "keywords": ["cybersecurity", "ransomware", "zero day", "cyberwar", "Nicole Perlroth", "Lex Fridman"],
        "summary": "Podcast notes from Lex Fridman's interview with Nicole Perlroth about cybersecurity, discussing ransomware attacks, zero-day exploits, and the increasing frequency of nation-state cyber attacks."
    },
    {
        "file_path": "002_Input/( Bullet Journal - Creation Tips and Tutorials.md",
        "hashtags": ["#productivity", "#writing", "#personal", "#creativity"],
        "keywords": ["bullet journal", "journaling", "organization", "daily log", "rapid logging", "values", "planning"],
        "summary": "Comprehensive guide to bullet journaling methodology, explaining how to combine diary, calendar, to-do lists, and creative elements with emphasis on linking daily actions to personal values and the 'why' behind tasks."
    },
    {
        "file_path": "002_Input/+ Book Notes in Obsidian MD Beginner Workflow, Guide, Tips for Linked Notes).md",
        "hashtags": ["#productivity", "#education", "#writing", "#personal"],
        "keywords": ["book notes", "Obsidian", "note-taking", "reading workflow", "permanent notes", "spaced repetition", "personal reflection"],
        "summary": "Tutorial on creating effective book notes in Obsidian, featuring a two-note system (book template and personal reflection) and emphasizing linking book content to personal experience for better retention."
    },
    {
        "file_path": "002_Input/+ Breaking - Obsidian Insiders Release 0.11.0 Graph Cluster Styling & Persistent Folds.md",
        "hashtags": ["#technology", "#productivity", "#programming"],
        "keywords": ["Obsidian", "graph view", "CSS styling", "update features", "persistent folders", "Bryan Jenks"],
        "summary": "Overview of Obsidian 0.11.0 release features including graph cluster styling with CSS customization, file renaming through links, and persistent folder states."
    },
    {
        "file_path": "002_Input/+ Build a Kanban Board with Obsidian and Dataview Plugin.md",
        "hashtags": ["#productivity", "#technology", "#programming"],
        "keywords": ["Kanban", "Obsidian", "Dataview plugin", "task management", "project visualization", "workflow"],
        "summary": "Tutorial on creating a Kanban board in Obsidian using the Dataview plugin, demonstrating how to visualize tasks across ToDo, Doing, and Done columns with query examples."
    },
    {
        "file_path": "002_Input/+ Feynman Method - Most effective Learning Method!.md",
        "hashtags": ["#education", "#science", "#productivity", "#personal"],
        "keywords": ["Feynman technique", "learning method", "illusion of competence", "explanation", "understanding", "Richard Feynman"],
        "summary": "Explanation of the Feynman learning technique, which involves explaining concepts in simple terms, identifying knowledge gaps, and linking new concepts to existing knowledge through metaphors and analogies."
    },
    {
        "file_path": "002_Input/+ How I Use Maps Of Content (MOCs) EP 5 Mastering Obsidian.md",
        "hashtags": ["#productivity", "#technology", "#writing", "#creativity"],
        "keywords": ["Maps of Content", "MOCs", "Obsidian", "note organization", "bidirectional linking", "knowledge management"],
        "summary": "Guide to using Maps of Content (MOCs) in Obsidian, emphasizing 'create first, organize later' philosophy and demonstrating both bottom-up and top-down approaches to organizing notes."
    },
    {
        "file_path": "002_Input/+ Kanban Made Easy in Obsidian - Kanban Plugin.md",
        "hashtags": ["#productivity", "#technology", "#business"],
        "keywords": ["Kanban plugin", "Obsidian", "task management", "visual boards", "workflow optimization"],
        "summary": "Brief tutorial on installing and configuring the Kanban plugin for Obsidian, including setup of keyboard shortcuts for creating new cards."
    },
    {
        "file_path": "002_Input/+ Note Taking Tools Comparison - Which Tool is Right for You and Tipps and Tricks.md",
        "hashtags": ["#productivity", "#technology", "#writing", "#education"],
        "keywords": ["note-taking tools", "PKM personality types", "Obsidian", "Roam", "collector", "writer", "connector", "databaser"],
        "summary": "Comprehensive comparison of note-taking tools based on four PKM personality types (Collector, Writer, Connector, Databaser), emphasizing that tools shape users and recommending focus on connecting and writing over collecting."
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