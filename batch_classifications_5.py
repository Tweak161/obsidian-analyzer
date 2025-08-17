#!/usr/bin/env python3
"""Add batch classifications - Batch 5 (20 files)"""

from ai_classifier import AIClassifier

vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
classifier = AIClassifier(vault_path)

# Classifications for the next 20 files
classifications = [
    {
        "file_path": "002_Input/Alpenüberquerung E5 Juni 2023.md",
        "hashtags": ["#travel", "#personal", "#health"],
        "keywords": ["Alpenüberquerung", "E5", "hiking", "packing list", "Alps crossing", "outdoor gear", "June 2023"],
        "summary": "Detailed packing list and planning notes for Alps crossing via E5 route in June 2023, including clothing, hygiene items, outdoor gear, and first aid supplies."
    },
    {
        "file_path": "002_Input/Capsule Wardrobe.md",
        "hashtags": ["#personal", "#productivity", "#creativity"],
        "keywords": ["capsule wardrobe", "minimalism", "clothing", "fashion", "organization"],
        "summary": "Notes on creating and maintaining a capsule wardrobe for simplified clothing choices and minimalist lifestyle."
    },
    {
        "file_path": "002_Input/Caras Homelab.md",
        "hashtags": ["#technology", "#programming", "#personal"],
        "keywords": ["homelab", "server setup", "networking", "self-hosting", "infrastructure"],
        "summary": "Documentation about Cara's homelab setup and configuration."
    },
    {
        "file_path": "002_Input/Carb Side Dishes.md",
        "hashtags": ["#health", "#creativity", "#personal"],
        "keywords": ["carbohydrates", "side dishes", "recipes", "cooking", "meal planning"],
        "summary": "Collection of carbohydrate-based side dish ideas for meal planning."
    },
    {
        "file_path": "002_Input/CRUD App Hello World.md",
        "hashtags": ["#programming", "#technology", "#education"],
        "keywords": ["CRUD", "web development", "hello world", "application development", "backend"],
        "summary": "Basic CRUD (Create, Read, Update, Delete) application hello world example for learning web development."
    },
    {
        "file_path": "002_Input/Debug Python Django Application in Docker Container with Visual Studio Code.md",
        "hashtags": ["#programming", "#technology", "#productivity"],
        "keywords": ["Python", "Django", "Docker", "debugging", "Visual Studio Code", "containerization", "development"],
        "summary": "Technical guide for debugging Python Django applications running in Docker containers using Visual Studio Code."
    },
    {
        "file_path": "002_Input/Digital Nomad, Freelancing, Remote Work.md",
        "hashtags": ["#career", "#personal", "#productivity", "#travel"],
        "keywords": ["digital nomad", "freelancing", "remote work", "location independence", "work from anywhere"],
        "summary": "Notes on digital nomad lifestyle, freelancing opportunities, and remote work strategies."
    },
    {
        "file_path": "002_Input/Django REST Backend - Hello World Application.md",
        "hashtags": ["#programming", "#technology", "#education"],
        "keywords": ["Django", "REST API", "backend development", "Python", "web services", "hello world"],
        "summary": "Tutorial or notes on creating a basic Django REST backend hello world application."
    },
    {
        "file_path": "002_Input/Drink.md",
        "hashtags": ["#personal", "#health"],
        "keywords": ["beverages", "drinks", "hydration", "recipes"],
        "summary": "Notes about drinks and beverages."
    },
    {
        "file_path": "002_Input/Drohnen Registrierung.md",
        "hashtags": ["#technology", "#personal", "#business"],
        "keywords": ["drone registration", "Drohne", "regulations", "German drone laws", "UAV"],
        "summary": "Information about drone registration requirements and procedures in Germany."
    },
    {
        "file_path": "002_Input/Elektroautos.md",
        "hashtags": ["#technology", "#personal", "#business"],
        "keywords": ["electric cars", "Elektroautos", "EV", "sustainable transport", "German automotive"],
        "summary": "Notes about electric vehicles and related information."
    },
    {
        "file_path": "002_Input/Excalidraw.md",
        "hashtags": ["#technology", "#productivity", "#creativity"],
        "keywords": ["Excalidraw", "diagramming", "visual thinking", "sketching", "drawing tool"],
        "summary": "Notes about using Excalidraw for diagramming and visual note-taking."
    },
    {
        "file_path": "002_Input/Fire Finance data Databse storage.md",
        "hashtags": ["#finance", "#programming", "#technology"],
        "keywords": ["FIRE movement", "financial data", "database design", "data storage", "personal finance"],
        "summary": "Database storage design for FIRE (Financial Independence Retire Early) finance data tracking."
    },
    {
        "file_path": "002_Input/Fire Project - Architecture.md",
        "hashtags": ["#finance", "#programming", "#technology"],
        "keywords": ["FIRE project", "software architecture", "system design", "financial tracking", "application structure"],
        "summary": "Architecture design documentation for FIRE financial tracking project."
    },
    {
        "file_path": "002_Input/Fire Project - Dashboard.md",
        "hashtags": ["#finance", "#programming", "#technology"],
        "keywords": ["FIRE dashboard", "data visualization", "financial metrics", "UI design", "project interface"],
        "summary": "Dashboard design and implementation notes for FIRE financial tracking project."
    },
    {
        "file_path": "002_Input/Fire Project Actual Database Creation.md",
        "hashtags": ["#finance", "#programming", "#technology"],
        "keywords": ["database creation", "FIRE project", "SQL", "schema design", "implementation"],
        "summary": "Implementation details for creating the actual database for FIRE financial tracking project."
    },
    {
        "file_path": "002_Input/Freundin Finden.md",
        "hashtags": ["#personal", "#relationship", "#psychology"],
        "keywords": ["dating", "relationships", "Freundin finden", "personal development", "social skills"],
        "summary": "Personal notes about finding a girlfriend and relationship strategies."
    },
    {
        "file_path": "002_Input/Frisur, Haarschnitt.md",
        "hashtags": ["#personal", "#creativity"],
        "keywords": ["Frisur", "Haarschnitt", "hairstyle", "haircut", "grooming", "personal appearance"],
        "summary": "Notes about hairstyles and haircut options."
    },
    {
        "file_path": "002_Input/Frozen Meals.md",
        "hashtags": ["#health", "#productivity", "#personal"],
        "keywords": ["frozen meals", "meal prep", "convenience food", "time-saving", "nutrition"],
        "summary": "Ideas and notes about frozen meal options for convenient meal planning."
    },
    {
        "file_path": "002_Input/Hair Transplant Research.md",
        "hashtags": ["#health", "#personal", "#science"],
        "keywords": ["hair transplant", "medical procedure", "hair loss", "research", "cosmetic surgery"],
        "summary": "Research notes on hair transplant procedures, options, and considerations."
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