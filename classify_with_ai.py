#!/usr/bin/env python3
"""
Helper script for AI classification of Obsidian notes
Supports both manual and API-based classification
"""

import os
import sys
from ai_classifier import AIClassifier
import json


def manual_classification_workflow(vault_path: str):
    """Interactive workflow for manual classification"""
    classifier = AIClassifier(vault_path)
    
    while True:
        # Get batch of unclassified files
        batch = classifier.prepare_batch_for_manual_classification(1)
        
        if not batch:
            print("\nNo more files to classify!")
            break
        
        item = batch[0]
        print("\n" + "="*80)
        print(f"File: {item['file_name']}")
        print(f"Path: {item['file_path']}")
        print("\n--- CONTENT PREVIEW ---")
        print(item['content_preview'][:500] + "...")
        print("\n--- PROMPT FOR CLAUDE ---")
        print(item['prompt'])
        print("="*80)
        
        # Get user input
        print("\nPaste the Claude response (JSON format) or 'skip' to skip this file:")
        response = input().strip()
        
        if response.lower() == 'skip':
            continue
        elif response.lower() == 'quit':
            break
        
        try:
            # Parse JSON response
            data = json.loads(response)
            
            # Add classification
            classifier.add_manual_classification(
                file_path=item['file_path'],
                hashtags=data.get('hashtags', []),
                keywords=data.get('keywords', []),
                summary=data.get('summary', '')
            )
            
            print(f"✓ Successfully classified: {item['file_name']}")
            
        except json.JSONDecodeError:
            print("❌ Invalid JSON format. Please try again.")
        except Exception as e:
            print(f"❌ Error: {e}")


def api_classification_workflow(vault_path: str, api_key: str, limit: int = 10):
    """Automated classification using Claude API"""
    classifier = AIClassifier(vault_path, api_key)
    
    print(f"Starting AI classification (limit: {limit} files)...")
    classifier.classify_vault(limit=limit)
    
    # Show summary
    print("\nClassification complete!")
    print(f"Total classifications: {len(classifier.classifications)}")


def show_example_prompts(vault_path: str, num_examples: int = 3):
    """Show example prompts for manual classification"""
    classifier = AIClassifier(vault_path)
    batch = classifier.prepare_batch_for_manual_classification(num_examples)
    
    print(f"\nExample prompts for {len(batch)} files:")
    print("Copy these to Claude and paste the responses back\n")
    
    for i, item in enumerate(batch):
        print(f"\n{'='*80}")
        print(f"FILE {i+1}: {item['file_name']}")
        print(f"{'='*80}")
        print(item['prompt'])
        print(f"{'='*80}\n")


def main():
    vault_path = r"/mnt/c/Users/hess/OneDrive/Dokumente/MyVault"
    
    print("Obsidian AI Classifier")
    print("=====================")
    print("\nOptions:")
    print("1. Manual classification (interactive)")
    print("2. Show example prompts")
    print("3. API classification (requires API key)")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        manual_classification_workflow(vault_path)
    elif choice == "2":
        num = input("How many examples? (default 3): ").strip()
        num = int(num) if num else 3
        show_example_prompts(vault_path, num)
    elif choice == "3":
        api_key = input("Enter your Anthropic API key: ").strip()
        if api_key:
            limit = input("How many files to classify? (default 10): ").strip()
            limit = int(limit) if limit else 10
            api_classification_workflow(vault_path, api_key, limit)
        else:
            print("API key required for automated classification")
    else:
        print("Exiting...")


if __name__ == "__main__":
    main()