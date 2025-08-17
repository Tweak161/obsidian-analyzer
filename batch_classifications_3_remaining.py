#!/usr/bin/env python3
"""Add batch classifications - Batch 3 remaining files"""

from ai_classifier import AIClassifier
import json

vault_path = r'/mnt/c/Users/hess/OneDrive/Dokumente/MyVault'
classifier = AIClassifier(vault_path)

# Classifications for the remaining files from batch 3
classifications = [
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