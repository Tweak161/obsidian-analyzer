#!/usr/bin/env python3
"""Add batch classifications - Batch 6 (20 files)"""

from ai_classifier import AIClassifier

vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
classifier = AIClassifier(vault_path)

# Classifications for the next 20 files
classifications = [
    {
        "file_path": "002_Input/Alpenüberquerung E5 Juni 2023.md",
        "hashtags": ["#travel", "#personal", "#health"],
        "keywords": ["Alpenüberquerung", "E5", "hiking", "packing list", "Alps crossing", "outdoor gear"],
        "summary": "Detailed packing list and planning notes for Alps crossing via E5 route in June 2023."
    },
    {
        "file_path": "002_Input/Happiness Score.md",
        "hashtags": ["#personal", "#psychology", "#productivity"],
        "keywords": ["happiness", "well-being", "life satisfaction", "metrics", "personal tracking"],
        "summary": "Notes on tracking and measuring personal happiness scores and well-being metrics."
    },
    {
        "file_path": "002_Input/How to efficiently store and query time-series data.md",
        "hashtags": ["#programming", "#technology", "#science"],
        "keywords": ["time-series data", "database optimization", "data storage", "query performance", "technical guide"],
        "summary": "Technical guide on efficient storage and querying methods for time-series data."
    },
    {
        "file_path": "002_Input/Humberman Lab - # Controlling Your Dopamine For Motivation, Focus & Satisfaction.md",
        "hashtags": ["#health", "#science", "#psychology", "#productivity"],
        "keywords": ["Huberman Lab", "dopamine", "motivation", "focus", "neuroscience", "satisfaction"],
        "summary": "Notes from Huberman Lab podcast episode about controlling dopamine for improved motivation, focus, and life satisfaction."
    },
    {
        "file_path": "002_Input/Input List.md",
        "hashtags": ["#productivity", "#personal"],
        "keywords": ["input list", "organization", "task management", "tracking"],
        "summary": "List for tracking various inputs and items to process."
    },
    {
        "file_path": "002_Input/Instant Pot Beans Preparation.md",
        "hashtags": ["#health", "#creativity", "#personal"],
        "keywords": ["Instant Pot", "beans", "cooking", "meal prep", "pressure cooking", "recipes"],
        "summary": "Guide for preparing various types of beans using an Instant Pot pressure cooker."
    },
    {
        "file_path": "002_Input/Kauf Rechereche - Kompressor.md",
        "hashtags": ["#personal", "#business", "#technology"],
        "keywords": ["Kompressor", "purchasing research", "air compressor", "buying guide", "German"],
        "summary": "Research notes for purchasing an air compressor, including comparisons and recommendations."
    },
    {
        "file_path": "002_Input/Learning Programming.md",
        "hashtags": ["#programming", "#education", "#productivity"],
        "keywords": ["programming", "learning strategies", "coding education", "skill development", "best practices"],
        "summary": "Strategies and best practices for effectively learning programming and developing coding skills."
    },
    {
        "file_path": "002_Input/Less Plastic Waste - Soap and Shampoo.md",
        "hashtags": ["#personal", "#health", "#creativity"],
        "keywords": ["plastic waste reduction", "sustainable living", "eco-friendly", "soap bars", "shampoo bars"],
        "summary": "Guide for reducing plastic waste by switching to bar soaps and shampoos."
    },
    {
        "file_path": "002_Input/Linux Commands Usefull in Obsidian.md",
        "hashtags": ["#technology", "#productivity", "#programming"],
        "keywords": ["Linux commands", "Obsidian", "terminal", "command line", "productivity tools"],
        "summary": "Collection of useful Linux commands for enhancing Obsidian workflow and file management."
    },
    {
        "file_path": "002_Input/Major System Zahlen Merken.md",
        "hashtags": ["#education", "#productivity", "#personal"],
        "keywords": ["Major System", "memory techniques", "number memorization", "mnemonic system", "German"],
        "summary": "Guide to the Major System for memorizing numbers using mnemonic techniques."
    },
    {
        "file_path": "002_Input/Meal Prep Building Block.md",
        "hashtags": ["#health", "#productivity", "#creativity"],
        "keywords": ["meal prep", "building blocks", "nutrition", "cooking strategy", "meal planning"],
        "summary": "Building block approach to meal preparation for efficient and varied meal planning."
    },
    {
        "file_path": "002_Input/Meal Prep Plan.md",
        "hashtags": ["#health", "#productivity", "#personal"],
        "keywords": ["meal planning", "weekly prep", "nutrition", "cooking schedule", "food preparation"],
        "summary": "Structured meal preparation plan for efficient weekly food planning and cooking."
    },
    {
        "file_path": "002_Input/Meal Prep.md",
        "hashtags": ["#health", "#productivity", "#personal"],
        "keywords": ["meal prep", "batch cooking", "time-saving", "healthy eating", "food storage"],
        "summary": "General notes and strategies for meal preparation and batch cooking."
    },
    {
        "file_path": "002_Input/MOC - Books.md",
        "hashtags": ["#education", "#productivity", "#writing"],
        "keywords": ["Map of Content", "MOC", "books", "reading", "literature organization"],
        "summary": "Map of Content organizing book-related notes and reading materials."
    },
    {
        "file_path": "002_Input/MOC - C++.md",
        "hashtags": ["#programming", "#education", "#technology"],
        "keywords": ["Map of Content", "MOC", "C++", "programming language", "learning resources"],
        "summary": "Map of Content for C++ programming resources, tutorials, and learning materials."
    },
    {
        "file_path": "002_Input/MOC - CICD.md",
        "hashtags": ["#programming", "#technology", "#productivity"],
        "keywords": ["Map of Content", "MOC", "CI/CD", "continuous integration", "continuous deployment", "DevOps"],
        "summary": "Map of Content for CI/CD (Continuous Integration/Continuous Deployment) resources and practices."
    },
    {
        "file_path": "002_Input/MOC - Cooking.md",
        "hashtags": ["#health", "#creativity", "#personal"],
        "keywords": ["Map of Content", "MOC", "cooking", "recipes", "culinary skills", "food"],
        "summary": "Map of Content organizing cooking-related notes, recipes, and culinary techniques."
    },
    {
        "file_path": "002_Input/MOC - Fire Project - Full Stack CRUD App.md",
        "hashtags": ["#programming", "#finance", "#technology"],
        "keywords": ["Map of Content", "MOC", "FIRE project", "full stack", "CRUD application", "web development"],
        "summary": "Map of Content for FIRE project full stack CRUD application development resources."
    },
    {
        "file_path": "002_Input/MOC - Git.md",
        "hashtags": ["#programming", "#technology", "#productivity"],
        "keywords": ["Map of Content", "MOC", "Git", "version control", "source control", "development tools"],
        "summary": "Map of Content for Git version control resources, commands, and best practices."
    }
]

# Add all classifications, skip if file doesn't exist
success_count = 0
for item in classifications:
    try:
        classifier.add_manual_classification(
            file_path=item["file_path"],
            hashtags=item["hashtags"],
            keywords=item["keywords"],
            summary=item["summary"]
        )
        print(f"✓ {item['file_path']}")
        success_count += 1
    except FileNotFoundError:
        print(f"✗ File not found: {item['file_path']}")
    except Exception as e:
        print(f"✗ Error with {item['file_path']}: {e}")

print(f"\nSuccessfully classified {success_count} files")
print(f"Classifications saved to: {classifier.classifications_file}")