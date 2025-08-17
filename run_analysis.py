#!/usr/bin/env python3
"""
Main script to run Obsidian vault analysis and launch dashboard
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path


def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def main():
    parser = argparse.ArgumentParser(description="Analyze Obsidian vault and create interactive dashboard")
    parser.add_argument("vault_path", nargs="?", 
                      default=r"/mnt/c/Users/hess/Lokal/MyVault",
                      help="Path to Obsidian vault")
    parser.add_argument("--install", action="store_true", help="Install requirements first")
    parser.add_argument("--analyze-only", action="store_true", help="Only run analysis, don't launch dashboard")
    parser.add_argument("--dashboard-only", action="store_true", help="Only launch dashboard with existing data")
    parser.add_argument("--port", type=int, default=5006, help="Port for dashboard (default: 5006)")
    
    args = parser.parse_args()
    
    if args.install:
        install_requirements()
        print("\nDependencies installed successfully!")
        print("Please run the script again without --install to analyze your vault.")
        sys.exit(0)
    
    # Import modules after installation check
    try:
        from obsidian_analyzer import ObsidianAnalyzer
        from dashboard import ObsidianDashboard
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("\nPlease install dependencies first by running:")
        print("  python run_analysis.py --install")
        sys.exit(1)
    
    if not args.dashboard_only:
        # Run analysis
        print(f"Analyzing vault: {args.vault_path}")
        
        # Convert Windows path if needed
        vault_path = args.vault_path
        if vault_path.startswith(r"\\mnt\\"):
            vault_path = vault_path.replace("\\", "/")
        elif vault_path.startswith(r"C:\\") or vault_path.startswith(r"c:\\"):
            # Convert Windows path to WSL path
            drive = vault_path[0].lower()
            path_part = vault_path[2:].replace("\\", "/")
            vault_path = f"/mnt/{drive}/{path_part}"
        
        # Check if vault exists
        if not Path(vault_path).exists():
            print(f"Error: Vault path does not exist: {vault_path}")
            sys.exit(1)
        
        # Clear git cache to ensure fresh commit counts
        git_cache_file = "git_history_cache.json"
        if os.path.exists(git_cache_file):
            os.remove(git_cache_file)
            print("Cleared git cache for fresh commit data")
        
        analyzer = ObsidianAnalyzer(vault_path)
        stats = analyzer.scan_vault()
        
        print(f"\nVault Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Get and save all data
        output_data = {
            "stats": stats,
            "important_notes": analyzer.get_important_notes(50),  # Get more for analysis
            "orphaned_notes": analyzer.get_orphaned_notes(),
            "timeline": analyzer.get_timeline_data(),
            "graph": analyzer.export_graph_data()
        }
        
        import json
        with open("vault_analysis.json", "w") as f:
            json.dump(output_data, f, default=str, indent=2)
        
        print("\nAnalysis complete! Data saved to vault_analysis.json")
    
    if not args.analyze_only:
        # Launch dashboard
        print(f"\nLaunching dashboard on http://localhost:{args.port}")
        print("Press Ctrl+C to stop the server")
        
        dashboard = ObsidianDashboard()
        dashboard.serve().show(port=args.port, address="0.0.0.0", open=False)
        print(f"\nDashboard is running!")
        print(f"Open in your browser: http://localhost:{args.port}")
        print("Press Ctrl+C to stop")


if __name__ == "__main__":
    main()