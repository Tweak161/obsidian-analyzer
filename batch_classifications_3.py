#!/usr/bin/env python3
"""Add batch classifications - Batch 3"""

from ai_classifier import AIClassifier
import json

vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
classifier = AIClassifier(vault_path)

# Classifications for the next 10 files
classifications = [
    {
        "file_path": "002_Input/3D Printer Laser Engraving.md",
        "hashtags": ["#technology", "#creativity", "#business"],
        "keywords": ["3D printer", "laser engraving", "Inkscape", "laser plugin", "maker", "DIY"],
        "summary": "Brief note about using Inkscape laser plugin for 3D printer laser engraving, including a link to JTech Photonics resources."
    },
    {
        "file_path": "002_Input/3D Printing Getting Started with Ender 3 S1.md",
        "hashtags": ["#technology", "#creativity", "#education"],
        "keywords": ["Ender 3 S1", "Cura slicer", "PLA", "ABS", "PETG", "calibration", "Octoprint", "3D printing settings"],
        "summary": "Comprehensive guide for getting started with Ender 3 S1 3D printer, including detailed Cura slicer settings for different materials, calibration tips, and Octoprint setup."
    },
    {
        "file_path": "002_Input/= Aware Media Consumption - Plan the Media you consume, Never consume based on Impulses.md",
        "hashtags": ["#productivity", "#personal", "#psychology"],
        "keywords": ["media consumption", "mindful browsing", "digital wellness", "intentional learning", "impulse control"],
        "summary": "Guidelines for conscious media consumption, emphasizing planned content consumption over impulse-driven browsing and avoiding recommendation algorithms."
    },
    {
        "file_path": "002_Input/= Markdown Notebook Data Extraction and Plotting with Python and Markdown Parser.md",
        "hashtags": ["#programming", "#productivity", "#technology"],
        "keywords": ["markdown", "data extraction", "Python", "data mining", "structured data", "plain text", "KISS principle"],
        "summary": "Idea for extracting and mining data from markdown notes using Python, with example code for parsing markdown tables and emphasis on consistent data formatting."
    },
    {
        "file_path": "002_Input/= Steal From Notion - Media Template.md",
        "hashtags": ["#productivity", "#technology", "#creativity"],
        "keywords": ["Notion templates", "media template", "Obsidian", "YAML header", "Dataview", "template design"],
        "summary": "Concept for adapting Notion's media template structure for use in Obsidian, utilizing YAML headers for metadata that can be queried with Dataview."
    },
    {
        "file_path": "002_Input/Alfred App Settings and Tips.md",
        "hashtags": ["#technology", "#productivity"],
        "keywords": ["Alfred app", "macOS", "productivity tools", "workflows", "ChatGPT", "DALL-E"],
        "summary": "Notes on Alfred app configuration and useful workflows, including ChatGPT and DALL-E integration."
    },
    {
        "file_path": "002_Input/Alpenüberquerung E5 Juni 2023.md",
        "hashtags": ["#travel", "#personal", "#health"],
        "keywords": ["Alpenüberquerung", "E5", "hiking", "packing list", "Alps crossing", "outdoor gear", "June 2023"],
        "summary": "Detailed packing list and planning notes for Alps crossing via E5 route in June 2023, including clothing, hygiene items, outdoor gear, and first aid supplies."
    },
    {
        "file_path": "002_Input/Anbau Weimerstal Schuppen Fahrrad.md",
        "hashtags": ["#creativity", "#personal", "#business"],
        "keywords": ["shed construction", "bicycle storage", "wood construction", "DIY project", "building plans", "cost calculation"],
        "summary": "Detailed construction plans for a bicycle storage shed in Weimerstal, including dimensions, material costs, design options, and foundation planning."
    },
    {
        "file_path": "002_Input/Backup and Upgrade Nextcloud.md",
        "hashtags": ["#technology", "#programming", "#productivity"],
        "keywords": ["Nextcloud", "backup", "upgrade", "Docker", "SSH", "container", "homelab"],
        "summary": "Technical guide for backing up and upgrading Nextcloud installation using command line and Docker containers."
    },
    {
        "file_path": "002_Input/Backup, Upgrade and Configure Nextcloud.md",
        "hashtags": ["#technology", "#programming", "#productivity"],
        "keywords": ["Nextcloud", "backup strategies", "restore procedures", "rsync", "incremental backup", "Proxmox", "external storage"],
        "summary": "Comprehensive guide for Nextcloud backup strategies including both the Nextcloud Backup App and manual backup methods using rsync, with detailed restore procedures."
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