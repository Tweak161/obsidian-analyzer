#!/usr/bin/env python3
"""Create all AI summaries for remaining batches"""
import json
import os

# Process each batch
batches = {
    "batch_3": {
        "summaries": [
            {
                "note_id": "800_Ressources/103_PKM/BoaP How to Take Smart Notes.excalidraw",
                "ai_summary": "Visual summary of 'How to Take Smart Notes' focusing on the Zettelkasten method for effective note-taking and knowledge management.",
                "ai_hashtags": ["#book", "#productivity", "#education", "#writing"],
                "ai_keywords": ["Zettelkasten", "smart notes", "Luhmann", "note-taking", "knowledge management", "writing", "research", "permanent notes", "literature notes", "fleeting notes"]
            },
            {
                "note_id": "800_Ressources/103_PKM/CODE Framework High Level Concept- Handle Divergence and Convergence during Note Taking",
                "ai_summary": "Explains the CODE framework's approach to managing the divergence and convergence phases in note-taking and creative work.",
                "ai_hashtags": ["#productivity", "#education", "#creativity"],
                "ai_keywords": ["CODE framework", "divergence", "convergence", "note-taking", "creative process", "information management", "capture", "organize", "distill", "express"]
            },
            {
                "note_id": "800_Ressources/103_PKM/MOC - Notetaking and Second Brain.excalidraw",
                "ai_summary": "Map of Content organizing notes related to note-taking methodologies, second brain concepts, and personal knowledge management systems.",
                "ai_hashtags": ["#moc", "#productivity", "#education"],
                "ai_keywords": ["map of content", "note-taking", "second brain", "PKM", "knowledge management", "organization", "methodology", "systems", "productivity", "learning"]
            },
            {
                "note_id": "800_Ressources/103_PKM/MOC - Obsidian.excalidraw",
                "ai_summary": "Map of Content for Obsidian-related notes, organizing information about features, plugins, workflows, and best practices.",
                "ai_hashtags": ["#moc", "#productivity", "#technology"],
                "ai_keywords": ["Obsidian", "map of content", "note-taking app", "plugins", "workflows", "markdown", "knowledge graph", "backlinks", "productivity tools", "PKM software"]
            },
            {
                "note_id": "800_Ressources/103_PKM/Motivation for PKM, Second Brain, Notetaking",
                "ai_summary": "Explores the motivations and benefits of maintaining a personal knowledge management system and building a second brain for enhanced learning and productivity.",
                "ai_hashtags": ["#productivity", "#education", "#personal"],
                "ai_keywords": ["PKM motivation", "second brain", "benefits", "knowledge management", "learning", "memory", "productivity", "information overload", "cognitive enhancement", "lifelong learning"]
            },
            {
                "note_id": "800_Ressources/103_PKM/My PKM System Explained",
                "ai_summary": "Personal explanation of the author's knowledge management system, including tools, workflows, and organizational principles.",
                "ai_hashtags": ["#productivity", "#personal", "#education"],
                "ai_keywords": ["PKM system", "personal workflow", "knowledge management", "tools", "organization", "note-taking", "productivity", "custom system", "best practices", "implementation"]
            },
            {
                "note_id": "800_Ressources/103_PKM/Obsidian - Graph View",
                "ai_summary": "Information about Obsidian's graph view feature for visualizing connections between notes and understanding knowledge networks.",
                "ai_hashtags": ["#technology", "#productivity", "#education"],
                "ai_keywords": ["Obsidian", "graph view", "visualization", "connections", "knowledge graph", "backlinks", "network", "relationships", "note connections", "visual thinking"]
            },
            {
                "note_id": "800_Ressources/103_PKM/PARA System for easy Organization of Notes",
                "ai_summary": "Detailed explanation of the PARA method (Projects, Areas, Resources, Archives) for organizing digital information and notes effectively.",
                "ai_hashtags": ["#productivity", "#education", "#personal"],
                "ai_keywords": ["PARA method", "organization", "Projects", "Areas", "Resources", "Archives", "Tiago Forte", "note organization", "productivity system", "actionability"]
            },
            {
                "note_id": "800_Ressources/103_PKM/Rethinking MY PKM - How I Organize Everything In Obsidian (Zsolt).excalidraw",
                "ai_summary": "Visual notes on Zsolt's approach to organizing everything in Obsidian, rethinking traditional PKM methods.",
                "ai_hashtags": ["#productivity", "#technology", "#personal"],
                "ai_keywords": ["Zsolt", "Obsidian organization", "PKM rethinking", "workflow", "digital organization", "note structure", "productivity", "system design", "best practices", "personal system"]
            },
            {
                "note_id": "800_Ressources/103_PKM/Second Brain - Critical Questions",
                "ai_summary": "Important questions to consider when building and maintaining a second brain system for knowledge management.",
                "ai_hashtags": ["#productivity", "#education", "#personal"],
                "ai_keywords": ["second brain", "critical questions", "system design", "knowledge management", "reflection", "effectiveness", "evaluation", "best practices", "implementation", "maintenance"]
            }
        ]
    }
}

# Save all batch files
for batch_name, batch_data in batches.items():
    with open(f'{batch_name}_summaries.json', 'w') as f:
        json.dump(batch_data, f, indent=2)
    print(f"Created {batch_name}_summaries.json")

# Run the processor
os.system("python3 process_all_ai_summaries.py")