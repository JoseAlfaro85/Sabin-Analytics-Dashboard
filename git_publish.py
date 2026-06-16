#!/usr/bin/env python3
"""
Git publication script for the Sabin Dashboard.
Initializes a git repository and creates commits per HANDOFF.md instructions.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Try to use git CLI, fall back to manual git operations
GIT_CLI_AVAILABLE = False
try:
    subprocess.run(["git", "--version"], capture_output=True, check=True)
    GIT_CLI_AVAILABLE = True
except (FileNotFoundError, subprocess.CalledProcessError):
    pass

def get_paths():
    """Return key project paths."""
    dashboard_root = Path(r"C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Sabin Communications - Performance Dashboard")
    scripts_root = Path(r"C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Desktop\Python Scripts")
    sharepoint_root = Path(r"C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Desktop\SharePoint - Sabin Communications\Digital Comms Team\Social & Digital Analytics\Performance Dashboards")
    
    return {
        "dashboard_root": dashboard_root,
        "scripts_root": scripts_root,
        "sharepoint_root": sharepoint_root,
    }

def init_or_get_repo(repo_path):
    """Initialize a git repo or get existing one."""
    try:
        repo = Repo(repo_path)
        print(f"✓ Found existing repository at {repo_path}")
        return repo
    except InvalidGitRepositoryError:
        print(f"Initializing new repository at {repo_path}")
        repo = Repo.init(repo_path)
        
        # Configure basic git identity
        with repo.config_writer() as git_config:
            git_config.set_value("user", "name", "Sabin Dashboard Automation")
            git_config.set_value("user", "email", "dashboard@sabin.org")
        
        print(f"✓ Repository initialized")
        return repo

def stage_commit_1(repo, paths):
    """Commit 1: reporting logic + dashboard refresh"""
    print("\n" + "="*70)
    print("COMMIT 1: Align May dashboard metrics and restore GA4 fallback")
    print("="*70)
    
    files_to_stage = [
        # Reporting logic files
        paths["scripts_root"] / "reporting_framework.py",
        paths["scripts_root"] / "dashboard_preview_builder.py",
        paths["scripts_root"] / "hootsuite_to_dashboard.py",
        # Dashboard files in Performance Dashboard folder
        paths["dashboard_root"] / "index.html",
        paths["dashboard_root"] / "dashboard_server.py",
        paths["dashboard_root"] / "data",
    ]
    
    staged_count = 0
    for file_path in files_to_stage:
        try:
            if file_path.exists():
                # For directories, add all files recursively
                if file_path.is_dir():
                    for subfile in file_path.rglob("*"):
                        if subfile.is_file() and not str(subfile).startswith("."):
                            rel_path = subfile.relative_to(repo.working_dir)
                            repo.index.add([str(rel_path)])
                            staged_count += 1
                else:
                    rel_path = file_path.relative_to(repo.working_dir)
                    repo.index.add([str(rel_path)])
                    staged_count += 1
                print(f"  ✓ Staged: {file_path.name}")
        except Exception as e:
            print(f"  ⚠ Could not stage {file_path.name}: {e}")
    
    if staged_count > 0:
        print(f"\nStaged {staged_count} files")
        repo.index.commit("Align May dashboard metrics and restore GA4 fallback")
        print("✓ Commit 1 created")
        return True
    else:
        print("⚠ No files to stage for Commit 1")
        return False

def stage_commit_2(repo, paths):
    """Commit 2: optional hosting scaffold"""
    print("\n" + "="*70)
    print("COMMIT 2: Prepare dashboard wrapper for hosted deployment")
    print("="*70)
    
    files_to_stage = [
        # Hosting scaffold files
        paths["dashboard_root"] / ".openai",
        paths["dashboard_root"] / "app",
        paths["dashboard_root"] / "build",
        paths["dashboard_root"] / "worker",
        paths["dashboard_root"] / "public",
        paths["dashboard_root"] / "package.json",
        paths["dashboard_root"] / "vite.config.ts",
        paths["dashboard_root"] / "next.config.ts",
        paths["dashboard_root"] / "tsconfig.json",
        paths["dashboard_root"] / "postcss.config.mjs",
        paths["dashboard_root"] / "scripts",
    ]
    
    staged_count = 0
    for file_path in files_to_stage:
        try:
            if file_path.exists():
                if file_path.is_dir():
                    for subfile in file_path.rglob("*"):
                        if subfile.is_file() and not str(subfile).startswith("."):
                            rel_path = subfile.relative_to(repo.working_dir)
                            repo.index.add([str(rel_path)])
                            staged_count += 1
                else:
                    rel_path = file_path.relative_to(repo.working_dir)
                    repo.index.add([str(rel_path)])
                    staged_count += 1
                print(f"  ✓ Staged: {file_path.name}")
        except Exception as e:
            print(f"  ⚠ Could not stage {file_path.name}: {e}")
    
    if staged_count > 0:
        print(f"\nStaged {staged_count} files")
        repo.index.commit("Prepare dashboard wrapper for hosted deployment")
        print("✓ Commit 2 created")
        return True
    else:
        print("⚠ No files to stage for Commit 2")
        return False

def show_status(repo):
    """Show repository status."""
    print("\n" + "="*70)
    print("REPOSITORY STATUS")
    print("="*70)
    print(f"Repository: {repo.working_dir}")
    print(f"Commits: {len(list(repo.iter_commits()))}")
    
    # Show recent commits
    commits = list(repo.iter_commits())[:5]
    if commits:
        print("\nRecent commits:")
        for commit in commits:
            print(f"  • {commit.hexsha[:7]} - {commit.message.strip()}")
    
    # Show remotes
    remotes = repo.remotes
    if remotes:
        print(f"\nRemote origins:")
        for remote in remotes:
            print(f"  • {remote.name}: {remote.url}")
    else:
        print("\n⚠ No remote configured yet")

def add_github_remote(repo):
    """Prompt and add GitHub remote."""
    print("\n" + "="*70)
    print("GITHUB CONFIGURATION")
    print("="*70)
    
    # Check if remote already exists
    if "origin" in [r.name for r in repo.remotes]:
        print("✓ GitHub remote already configured")
        return
    
    print("\nTo push to GitHub, add a remote:")
    print("\nOption 1: Configure now")
    github_url = input("Enter GitHub repository URL (e.g., https://github.com/your-org/dashboard): ").strip()
    
    if github_url:
        try:
            repo.create_remote("origin", github_url)
            print(f"✓ Added remote: {github_url}")
            print("\nNext steps:")
            print(f"  1. Create repository on GitHub if not exists")
            print(f"  2. Push with: python -m git push -u origin main")
        except Exception as e:
            print(f"⚠ Could not add remote: {e}")
    else:
        print("\nYou can add the remote later with:")
        print(f"  git remote add origin <url>")

def main():
    """Main execution."""
    paths = get_paths()
    dashboard_root = paths["dashboard_root"]
    
    print("Sabin Dashboard Git Publication")
    print("================================\n")
    
    # Initialize or get repository
    repo = init_or_get_repo(dashboard_root)
    
    # Show current status
    show_status(repo)
    
    # Ask user what to do
    print("\n" + "="*70)
    print("AVAILABLE ACTIONS")
    print("="*70)
    print("1. Create Commit 1 (reporting logic + dashboard refresh)")
    print("2. Create Commit 2 (hosting scaffold)")
    print("3. Create both commits")
    print("4. Configure GitHub remote")
    print("5. Show status and exit")
    
    choice = input("\nSelect action (1-5): ").strip()
    
    if choice == "1":
        stage_commit_1(repo, paths)
    elif choice == "2":
        stage_commit_2(repo, paths)
    elif choice == "3":
        stage_commit_1(repo, paths)
        stage_commit_2(repo, paths)
    elif choice == "4":
        add_github_remote(repo)
    elif choice == "5":
        pass
    
    # Show final status
    show_status(repo)
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
