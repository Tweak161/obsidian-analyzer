#!/usr/bin/env python3
"""Add batch classifications - Batch 7 (final batch to reach 100)"""

from ai_classifier import AIClassifier

vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
classifier = AIClassifier(vault_path)

# Classifications for the final batch
classifications = [
    {
        "file_path": "002_Input/Alpenüberquerung E5 Juni 2023.md",
        "hashtags": ["#travel", "#personal", "#health"],
        "keywords": ["Alpenüberquerung", "E5", "hiking", "packing list", "Alps crossing", "outdoor gear"],
        "summary": "Detailed packing list and planning notes for Alps crossing via E5 route in June 2023."
    },
    {
        "file_path": "002_Input/MOC - Habits.md",
        "hashtags": ["#productivity", "#personal", "#psychology"],
        "keywords": ["Map of Content", "MOC", "habits", "behavior change", "personal development"],
        "summary": "Map of Content for habit-related notes and resources."
    },
    {
        "file_path": "002_Input/MOC - Health.md",
        "hashtags": ["#health", "#productivity", "#personal"],
        "keywords": ["Map of Content", "MOC", "health", "supplements", "blood glucose", "wellness"],
        "summary": "Map of Content organizing health-related notes including supplements, blood glucose monitoring, and medical tests."
    },
    {
        "file_path": "002_Input/MOC - Lifedesign.md",
        "hashtags": ["#personal", "#productivity", "#philosophy"],
        "keywords": ["Map of Content", "MOC", "life design", "values", "goals", "happiness", "remote work"],
        "summary": "Map of Content for life design philosophy following the Values → Goals → Strategies → Actions framework."
    },
    {
        "file_path": "002_Input/MOC - Produktrecherche.md",
        "hashtags": ["#personal", "#business", "#productivity"],
        "keywords": ["Map of Content", "MOC", "product research", "purchasing decisions", "German"],
        "summary": "Map of Content for product research and purchasing decisions."
    },
    {
        "file_path": "002_Input/MOC - Programming.md",
        "hashtags": ["#programming", "#technology", "#education"],
        "keywords": ["Map of Content", "MOC", "programming", "learning", "C++", "Git", "CICD", "full stack"],
        "summary": "Map of Content organizing programming resources including learning strategies, languages, and development tools."
    },
    {
        "file_path": "002_Input/MOC - Projects.md",
        "hashtags": ["#productivity", "#creativity", "#personal"],
        "keywords": ["Map of Content", "MOC", "projects", "FIRE app", "digital nomad", "resin lamp"],
        "summary": "Map of Content tracking various personal and professional projects."
    },
    {
        "file_path": "002_Input/MOC - Trading and Finance.md",
        "hashtags": ["#finance", "#education", "#business"],
        "keywords": ["Map of Content", "MOC", "trading", "investing", "MMT", "Warren Buffett", "ETF"],
        "summary": "Map of Content for trading and finance resources including courses, investment strategies, and financial theory."
    },
    {
        "file_path": "002_Input/MOC Solar.md",
        "hashtags": ["#technology", "#personal", "#business"],
        "keywords": ["Map of Content", "MOC", "solar energy", "solar installation", "renewable energy"],
        "summary": "Map of Content for solar energy installation planning and costs."
    },
    {
        "file_path": "002_Input/Moosbild.md",
        "hashtags": ["#creativity", "#personal", "#business"],
        "keywords": ["moss art", "Moosbild", "wall decoration", "plant art", "dimensions", "German"],
        "summary": "Notes about moss wall art (Moosbild) including product links and dimensions."
    },
    {
        "file_path": "002_Input/My 2021 Comprehensive Obsidian Zettelkasten Workflow.md",
        "hashtags": ["#productivity", "#technology", "#writing", "#education"],
        "keywords": ["Obsidian", "Zettelkasten", "workflow", "Bryan Jenks", "note-taking", "knowledge management"],
        "summary": "Bryan Jenks' comprehensive 2021 Obsidian Zettelkasten workflow video tutorial."
    },
    {
        "file_path": "002_Input/Nordic Hamstring Curl.md",
        "hashtags": ["#health", "#personal"],
        "keywords": ["Nordic hamstring curl", "exercise", "hamstring", "warmup", "muscle activation", "fitness"],
        "summary": "Exercise guide for Nordic Hamstring Curl including proper form, warmup, and muscle activation techniques."
    },
    {
        "file_path": "002_Input/Nut Butter.md",
        "hashtags": ["#health", "#creativity", "#personal"],
        "keywords": ["nut butter", "super seed", "recipes", "healthy food"],
        "summary": "Notes about nut butter varieties including super seed nut butter."
    },
    {
        "file_path": "002_Input/Obsidian - How To Create Visual Boards Easily - Kanban Boards Plugin.md",
        "hashtags": ["#productivity", "#technology", "#writing"],
        "keywords": ["Obsidian", "Kanban boards", "visual organization", "plugin", "Santi Younger", "project management"],
        "summary": "Tutorial by Santi Younger on creating visual Kanban boards in Obsidian using the Kanban plugin."
    },
    {
        "file_path": "002_Input/Obsidian - Templates.md",
        "hashtags": ["#productivity", "#technology", "#writing"],
        "keywords": ["Obsidian", "templates", "note-taking", "automation"],
        "summary": "Brief note about Obsidian templates functionality."
    },
    {
        "file_path": "002_Input/Obsidian - The Power of Backlinks and the Knowledge Graph - Effective Remote Work.md",
        "hashtags": ["#productivity", "#technology", "#writing"],
        "keywords": ["Obsidian", "backlinks", "knowledge graph", "note connections", "remote work", "knowledge management"],
        "summary": "Video tutorial on leveraging backlinks and the knowledge graph in Obsidian for effective knowledge management."
    },
    {
        "file_path": "002_Input/Obsidian Hotkeys List.md",
        "hashtags": ["#productivity", "#technology"],
        "keywords": ["Obsidian", "hotkeys", "keyboard shortcuts", "productivity", "navigation"],
        "summary": "Reference list of Obsidian keyboard shortcuts for efficient navigation and editing."
    },
    {
        "file_path": "002_Input/Obsidian Regex.md",
        "hashtags": ["#technology", "#programming", "#productivity"],
        "keywords": ["Obsidian", "regex", "regular expressions", "search patterns", "text manipulation"],
        "summary": "Notes on using regular expressions (regex) in Obsidian for advanced search and text manipulation."
    },
    {
        "file_path": "002_Input/Openmediavault NAS.md",
        "hashtags": ["#technology", "#personal", "#productivity"],
        "keywords": ["OpenMediaVault", "NAS", "network storage", "hard drives", "server", "data storage"],
        "summary": "Documentation of OpenMediaVault NAS setup including physical and logical drive configurations."
    },
    {
        "file_path": "002_Input/Pantry Stables.md",
        "hashtags": ["#health", "#personal", "#productivity"],
        "keywords": ["pantry", "food storage", "staples", "meal planning", "groceries"],
        "summary": "List of pantry staple items for meal planning and food storage."
    },
    # Adding a few more from other folders to reach exactly 100
    {
        "file_path": "excalibrain.md",
        "hashtags": ["#technology", "#productivity", "#creativity"],
        "keywords": ["Excalibrain", "Excalidraw", "mind mapping", "visualization", "Obsidian plugin"],
        "summary": "Configuration file for Excalibrain plugin that provides visual mind-mapping capabilities in Obsidian."
    },
    {
        "file_path": "002_Input/Pareto Principle 80 20 Rule.md",
        "hashtags": ["#productivity", "#business", "#education"],
        "keywords": ["Pareto Principle", "80/20 rule", "efficiency", "optimization", "productivity"],
        "summary": "Notes on the Pareto Principle (80/20 rule) and its applications for productivity and efficiency."
    },
    {
        "file_path": "002_Input/Passives Einkommen Ideen.md",
        "hashtags": ["#finance", "#business", "#personal"],
        "keywords": ["passive income", "passives Einkommen", "income streams", "financial independence", "German"],
        "summary": "Ideas and strategies for generating passive income streams."
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

# Final count
total = len(classifier.classifications)
print(f"\nTOTAL CLASSIFICATIONS: {total}")