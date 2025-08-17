#!/usr/bin/env python3
"""
Enhanced script to generate AI summaries for notes in specified folders
Supports batch processing, resume capability, and progress tracking
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import argparse

from ai_classifier import AIClassifier


def load_vault_analysis() -> dict:
    """Load the vault analysis data"""
    analysis_file = Path("vault_analysis.json")
    if not analysis_file.exists():
        print("Error: vault_analysis.json not found. Please run the analyzer first.")
        sys.exit(1)
    
    with open(analysis_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_vault_analysis(vault_data: dict):
    """Save the updated vault analysis data"""
    with open("vault_analysis.json", "w", encoding="utf-8") as f:
        json.dump(vault_data, f, indent=2, ensure_ascii=False)


def get_notes_needing_summaries(vault_data: dict, folder_filter: Optional[str] = None) -> List[str]:
    """Get list of notes that need AI summaries"""
    notes_to_process = []
    
    for note_id, metadata in vault_data["notes_metadata"].items():
        path = metadata.get("path", "")
        
        # Apply folder filter if specified
        if folder_filter and not path.startswith(folder_filter):
            continue
        
        # Check if note needs AI summary
        if not metadata.get("ai_summary"):
            notes_to_process.append(path)
    
    return notes_to_process


def update_vault_with_classifications(vault_data: dict, classifications_file: Path) -> int:
    """Update vault analysis with AI classifications"""
    if not classifications_file.exists():
        return 0
    
    with open(classifications_file, "r", encoding="utf-8") as f:
        classifications = json.load(f)
    
    updates = 0
    for file_path, classification in classifications.items():
        # Find matching note in vault data
        for note_id, metadata in vault_data["notes_metadata"].items():
            if metadata.get("path") == file_path:
                metadata["ai_summary"] = classification.get("ai_summary", "")
                metadata["ai_hashtags"] = classification.get("ai_hashtags", [])
                metadata["ai_keywords"] = classification.get("ai_keywords", [])
                updates += 1
                break
    
    return updates


def main():
    parser = argparse.ArgumentParser(description="Generate AI summaries for Obsidian notes")
    parser.add_argument("--folder", type=str, default="800_Ressources",
                      help="Folder to process (default: 800_Ressources)")
    parser.add_argument("--limit", type=int, default=None,
                      help="Limit number of notes to process")
    parser.add_argument("--batch-size", type=int, default=10,
                      help="Save progress every N notes (default: 10)")
    parser.add_argument("--dry-run", action="store_true",
                      help="Show what would be processed without making API calls")
    
    args = parser.parse_args()
    
    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key and not args.dry_run:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Please set it with: export ANTHROPIC_API_KEY='your-api-key'")
        print("\nYou can get an API key from: https://console.anthropic.com/")
        sys.exit(1)
    
    # Load vault data
    print("Loading vault analysis...")
    vault_data = load_vault_analysis()
    vault_path = vault_data.get("vault_path", "002_Slipbox")
    
    # Get notes to process
    notes_to_process = get_notes_needing_summaries(vault_data, args.folder)
    
    if args.limit:
        notes_to_process = notes_to_process[:args.limit]
    
    print(f"\nFound {len(notes_to_process)} notes in {args.folder} without AI summaries")
    
    if not notes_to_process:
        print(f"\nAll notes in {args.folder} already have AI summaries!")
        return
    
    if args.dry_run:
        print("\nDRY RUN - Notes that would be processed:")
        for i, path in enumerate(notes_to_process[:10], 1):
            print(f"  {i}. {path}")
        if len(notes_to_process) > 10:
            print(f"  ... and {len(notes_to_process) - 10} more")
        return
    
    # Initialize classifier
    print("\nInitializing AI classifier...")
    classifier = AIClassifier(vault_path, api_key)
    
    # Process notes
    print(f"\nStarting AI classification (batch size: {args.batch_size})...")
    start_time = time.time()
    processed = 0
    failed = 0
    
    for i, note_path in enumerate(notes_to_process, 1):
        print(f"\n[{i}/{len(notes_to_process)}] Processing: {note_path}")
        
        try:
            full_path = Path(vault_path) / note_path
            if full_path.exists():
                classification = classifier.classify_with_api(full_path)
                if classification:
                    print(f"  ✓ Summary: {classification.ai_summary[:80]}...")
                    print(f"  ✓ Hashtags: {', '.join(classification.ai_hashtags[:5])}")
                    processed += 1
                else:
                    print("  ✗ Classification failed")
                    failed += 1
            else:
                print(f"  ✗ File not found: {full_path}")
                failed += 1
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            failed += 1
        
        # Save progress periodically
        if i % args.batch_size == 0:
            print(f"\nSaving progress after {i} notes...")
            classifier._save_classifications()
            
            # Update vault analysis
            updates = update_vault_with_classifications(vault_data, classifier.classifications_file)
            save_vault_analysis(vault_data)
            print(f"✓ Saved {updates} summaries to vault_analysis.json")
            
            # Show time estimate
            elapsed = time.time() - start_time
            rate = i / elapsed
            remaining = len(notes_to_process) - i
            eta = remaining / rate if rate > 0 else 0
            print(f"Progress: {i}/{len(notes_to_process)} | Rate: {rate:.1f} notes/min | ETA: {eta/60:.1f} min")
        
        # Rate limiting to avoid API limits
        time.sleep(0.5)  # Adjust based on your API rate limits
    
    # Final save
    print("\nSaving final results...")
    classifier._save_classifications()
    updates = update_vault_with_classifications(vault_data, classifier.classifications_file)
    save_vault_analysis(vault_data)
    
    # Summary
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"✓ Processing complete!")
    print(f"  - Processed: {processed} notes")
    print(f"  - Failed: {failed} notes")
    print(f"  - Time taken: {elapsed/60:.1f} minutes")
    print(f"  - Final updates: {updates} notes in vault_analysis.json")
    print(f"\nRestart the dashboard to see the AI summaries.")


if __name__ == "__main__":
    main()