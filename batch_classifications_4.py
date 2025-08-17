#!/usr/bin/env python3
"""Add batch classifications - Batch 4"""

from ai_classifier import AIClassifier
import json

vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
classifier = AIClassifier(vault_path)

# Classifications for the next 10 files
classifications = [
    {
        "file_path": "002_Input/Alpenüberquerung E5 Juni 2023.md",
        "hashtags": ["#travel", "#personal", "#health"],
        "keywords": ["Alpenüberquerung", "E5", "hiking", "packing list", "Alps crossing", "outdoor gear", "June 2023"],
        "summary": "Detailed packing list and planning notes for Alps crossing via E5 route in June 2023, including clothing, hygiene items, outdoor gear, and first aid supplies."
    },
    {
        "file_path": "002_Input/Best Practices Postgres Finance Database.md",
        "hashtags": ["#programming", "#technology", "#finance"],
        "keywords": ["PostgreSQL", "time series", "finance database", "BRIN index", "stock exchange", "database optimization", "OLTP", "OLAP"],
        "summary": "Technical guide on PostgreSQL best practices for financial time-series databases, covering BRIN indexes, table partitioning, and performance optimization for stock exchange systems."
    },
    {
        "file_path": "002_Input/Blut Glukose Messung.md",
        "hashtags": ["#health", "#personal", "#science"],
        "keywords": ["blood glucose", "Freestyle Libre 3", "diabetes monitoring", "health tracking", "nutrition", "intermittent fasting", "Blutzucker"],
        "summary": "Personal plan for blood glucose monitoring using Freestyle Libre 3 sensor to optimize health, energy levels, and understand impacts of different foods, exercise, and sleep patterns."
    },
    {
        "file_path": "002_Input/Bluttest Thoma Hess 2022.md",
        "hashtags": ["#health", "#personal"],
        "keywords": ["blood test", "medical records", "2022", "health data"],
        "summary": "Reference to blood test results document from 2022."
    },
    {
        "file_path": "002_Input/Book List.md",
        "hashtags": ["#education", "#personal", "#productivity"],
        "keywords": ["reading list", "book recommendations", "Bret Easton Ellis", "No More Mr Nice Guy", "dataview queries", "reading tracker"],
        "summary": "Personal book list with recommendations and Dataview queries to track reading status (consuming, synthesizing, todo, completed)."
    },
    {
        "file_path": "002_Input/Brandy Tasting.md",
        "hashtags": ["#personal", "#creativity"],
        "keywords": ["brandy tasting", "Dega Velha", "Gran Duque D Alba", "spirits", "tasting notes", "alcohol review"],
        "summary": "Brandy tasting notes comparing Dega Velha Reserva 6 and Gran Duque D Alba Gran Reserva, with detailed ratings on taste, finish, and overall impressions."
    },
    {
        "file_path": "002_Input/Building Block Meals.md",
        "hashtags": ["#health", "#creativity", "#personal"],
        "keywords": ["meal planning", "recipes", "building blocks", "salads", "sandwiches", "quick meals", "healthy eating"],
        "summary": "Simple meal planning framework using building block approach for creating various meals including hot/cold salads, sandwiches, pan dishes, and soups."
    },
    {
        "file_path": "002_Input/Bulgarian Split Squat.md",
        "hashtags": ["#health", "#personal"],
        "keywords": ["Bulgarian split squat", "exercise", "fitness", "leg workout", "weighted variations"],
        "summary": "Brief exercise guide showing weighted and unweighted variations of the Bulgarian split squat exercise."
    },
    {
        "file_path": "002_Input/C++ Learning Ressources and Planning.md",
        "hashtags": ["#programming", "#education", "#productivity"],
        "keywords": ["C++", "programming learning", "Udemy courses", "C++ Primer", "spaced repetition", "learning strategy", "coding resources"],
        "summary": "Comprehensive C++ learning plan listing various resources including books, Udemy courses, CS50, and LeetCode, with learning strategies emphasizing spaced repetition and project-based learning."
    },
    {
        "file_path": "002_Input/C++ Primer Query.md",
        "hashtags": ["#programming", "#education"],
        "keywords": ["C++ Primer", "query", "excalidraw diagram"],
        "summary": "Reference to an Excalidraw diagram related to C++ Primer query concepts."
    }
]

# Add all classifications, skip if file doesn't exist
for item in classifications:
    try:
        classifier.add_manual_classification(
            file_path=item["file_path"],
            hashtags=item["hashtags"],
            keywords=item["keywords"],
            summary=item["summary"]
        )
        print(f"Successfully classified: {item['file_path']}")
    except FileNotFoundError:
        print(f"File not found, skipping: {item['file_path']}")
    except Exception as e:
        print(f"Error classifying {item['file_path']}: {e}")

print(f"\nClassifications saved to: {classifier.classifications_file}")