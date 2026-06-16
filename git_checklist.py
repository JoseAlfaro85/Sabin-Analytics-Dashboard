#!/usr/bin/env python3
"""
Git Publication Checklist Generator for Sabin Dashboard
Generates a step-by-step git command checklist per HANDOFF.md
"""

from pathlib import Path
from datetime import datetime
import json

def generate_git_checklist():
    """Generate git publication checklist."""
    
    dashboard_root = Path(r"C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Sabin Communications - Performance Dashboard")
    scripts_root = Path(r"C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Desktop\Python Scripts")
    
    checklist = f"""
================================================================================
SABIN DASHBOARD - GIT PUBLICATION CHECKLIST
================================================================================

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Repository Root: {dashboard_root}

================================================================================
STEP 1: INITIALIZE REPOSITORY (if not already initialized)
================================================================================

[ ] Open PowerShell and navigate to the dashboard root:
    cd "{dashboard_root}"

[ ] Initialize git repository:
    git init

[ ] Configure git user:
    git config user.name "Sabin Dashboard Automation"
    git config user.email "dashboard@sabin.org"

[ ] Verify initialization:
    git status

================================================================================
STEP 2: COMMIT 1 - Reporting Logic + Dashboard Refresh
================================================================================

Message: "Align May dashboard metrics and restore GA4 fallback"

Files to stage:
  * {scripts_root / "reporting_framework.py"}
  * {scripts_root / "dashboard_preview_builder.py"}
  * {scripts_root / "hootsuite_to_dashboard.py"}
  * {dashboard_root / "index.html"}
  * {dashboard_root / "dashboard_server.py"}
  * {dashboard_root / "data"}

[ ] Stage files:
    git add \\
      "{scripts_root / "reporting_framework.py"}" \\
      "{scripts_root / "dashboard_preview_builder.py"}" \\
      "{scripts_root / "hootsuite_to_dashboard.py"}" \\
      "{dashboard_root / "index.html"}" \\
      "{dashboard_root / "dashboard_server.py"}" \\
      "{dashboard_root / "data"}"

[ ] Check staged files:
    git status

[ ] Create commit:
    git commit -m "Align May dashboard metrics and restore GA4 fallback"

================================================================================
STEP 3: COMMIT 2 - Optional Hosting Scaffold
================================================================================

Message: "Prepare dashboard wrapper for hosted deployment"

Files to stage:
  * {dashboard_root / ".openai"}
  * {dashboard_root / "app"}
  * {dashboard_root / "build"}
  * {dashboard_root / "worker"}
  * {dashboard_root / "public"}
  * {dashboard_root / "package.json"}
  * {dashboard_root / "vite.config.ts"}
  * {dashboard_root / "next.config.ts"}
  * {dashboard_root / "tsconfig.json"}
  * {dashboard_root / "postcss.config.mjs"}
  * {dashboard_root / "scripts"}

[ ] Stage files:
    git add \\
      "{dashboard_root / ".openai"}" \\
      "{dashboard_root / "app"}" \\
      "{dashboard_root / "build"}" \\
      "{dashboard_root / "worker"}" \\
      "{dashboard_root / "public"}" \\
      "{dashboard_root / "package.json"}" \\
      "{dashboard_root / "vite.config.ts"}" \\
      "{dashboard_root / "next.config.ts"}" \\
      "{dashboard_root / "tsconfig.json"}" \\
      "{dashboard_root / "postcss.config.mjs"}" \\
      "{dashboard_root / "scripts"}"

[ ] Check staged files:
    git status

[ ] Create commit:
    git commit -m "Prepare dashboard wrapper for hosted deployment"

================================================================================
STEP 4: VERIFY LOCAL REPOSITORY
================================================================================

[ ] View commit history:
    git log --oneline

[ ] View current status:
    git status

================================================================================
STEP 5: SETUP GITHUB REMOTE (for publication)
================================================================================

[ ] Create a new repository on GitHub (if not already created)
    - Go to https://github.com/new
    - Name: sabin-analytics-dashboard
    - Description: Sabin Vaccine Institute social analytics dashboard
    - Make it private (internal use only)
    - Do NOT initialize with README

[ ] Add GitHub remote to local repository:
    git remote add origin https://github.com/josealfaro85/sabin-analytics-dashboard.git

[ ] Verify remote:
    git remote -v

[ ] Push to GitHub:
    git branch -M main
    git push -u origin main

================================================================================
STEP 6: OPTIONAL - ADD .gitignore
================================================================================

Create a .gitignore file to exclude sensitive data:

[ ] Create .gitignore with:
    
    # Python
    __pycache__/
    *.py[cod]
    *$py.class
    *.egg-info/
    .venv/
    venv/
    
    # Environment
    .env
    .env.local
    *.key
    *.secret
    client_secret_*.json
    
    # Data files
    *.csv
    *.xlsx
    *.xls
    
    # Logs
    logs/
    *.log
    
    # Node
    node_modules/
    package-lock.json
    
    # OS
    .DS_Store
    Thumbs.db
    
    # IDE
    .vscode/
    .idea/
    *.swp

[ ] Stage and commit .gitignore:
    git add .gitignore
    git commit -m "Add .gitignore for sensitive data"
    git push

================================================================================
USEFUL GIT COMMANDS
================================================================================

View changes:
    git diff                          # Show unstaged changes
    git diff --staged                 # Show staged changes
    git log                           # Show full commit history
    git log --oneline -10             # Show last 10 commits (compact)

Undo changes:
    git restore <file>                # Discard changes to a file
    git reset HEAD <file>             # Unstage a file
    git revert <commit>               # Undo a commit (creates new commit)

Branching:
    git branch                        # List local branches
    git branch -a                     # List all branches (local + remote)
    git checkout -b <branch-name>     # Create and switch to new branch
    git switch <branch-name>          # Switch to existing branch

Pushing updates:
    git push                          # Push current branch
    git push origin <branch-name>     # Push specific branch
    git push --all                    # Push all branches

================================================================================
NOTES
================================================================================

* This checklist assumes git is installed and available in PowerShell
* Replace YOUR-ORG with your actual GitHub organization
* Keep sensitive files (.json, .key) out of git using .gitignore
* Commit messages use imperative tense (e.g., "Add feature" not "Added feature")
* The two commits match the HANDOFF.md recommendations

================================================================================
"""
    
    return checklist

def save_checklist(content):
    """Save checklist to file."""
    output_path = Path(r"C:\Users\JAlfaro\OneDrive - Albert B. Sabin Vaccine Institute\Sabin Communications - Performance Dashboard\GIT_PUBLICATION_CHECKLIST.txt")
    output_path.write_text(content)
    print(f"✓ Checklist saved to: {output_path}")

if __name__ == "__main__":
    checklist = generate_git_checklist()
    print(checklist)
    save_checklist(checklist)
    print("\n" + "="*79)
    print("NEXT STEP: Follow the checklist above to publish to GitHub")
    print("="*79)
