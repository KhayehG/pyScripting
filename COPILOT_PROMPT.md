# GitHub Copilot Prompt — Finalize & Upload supply-chain-data-toolkit

Paste this entire prompt into GitHub Copilot Chat (VS Code) after opening the project folder.

---

## PROMPT (copy everything below this line)

---

I have a Python project called `supply-chain-data-toolkit` that I need you to help me finalize and upload to a new GitHub repository. Here is exactly what I need you to do, step by step.

---

### STEP 1 — Verify the project files exist

Check that the following files are present in the current workspace folder:

```
pipeline.py
scripts/__init__.py
scripts/generate_sample_data.py
scripts/cleaner.py
scripts/analyser.py
scripts/reporter.py
requirements.txt
README.md
```

If any file is missing, tell me which one and stop. Do not proceed until all files are confirmed present.

---

### STEP 2 — Create a `.gitignore` file

Create a `.gitignore` file in the project root with this exact content:

```
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.eggs/

# Generated outputs (reproducible, no need to track)
data/sample_orders.csv
outputs/cleaned_orders.csv
outputs/orders.db
outputs/summary_report.txt

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
```

---

### STEP 3 — Create the `data/` and `outputs/` directories with `.gitkeep` files

Run the following in the terminal so Git tracks the empty folders:

```bash
mkdir -p data outputs
touch data/.gitkeep outputs/.gitkeep
```

---

### STEP 4 — Run the pipeline once to confirm everything works

Run this command in the terminal and confirm the output ends with "✅ Pipeline complete!":

```bash
python pipeline.py
```

If there are any errors, fix them before proceeding to the next step.

---

### STEP 5 — Initialise a local Git repository

Run the following commands in the terminal exactly as written:

```bash
git init
git add .
git commit -m "Initial commit: supply chain data automation pipeline

- 4-step pipeline: generate, clean, analyse, report
- SQL-based analysis with SQLite (7 metrics)
- Data validation with 8 quality rules
- CLI interface with argparse
- No external dependencies (stdlib only)"
```

---

### STEP 6 — Create a new GitHub repository via the GitHub CLI

Run the following command to create a **public** repo on GitHub and push to it:

```bash
gh repo create supply-chain-data-toolkit \
  --public \
  --description "Python automation pipeline for supply chain order data: cleaning, SQL analysis, and reporting" \
  --push \
  --source=.
```

If `gh` (GitHub CLI) is not installed, tell me and provide the manual alternative instructions instead (using `git remote add origin` with the HTTPS URL).

---

### STEP 7 — Confirm the upload succeeded

Run this command and confirm it shows the remote URL on GitHub:

```bash
git remote -v
```

Then open the repo URL in the browser:

```bash
gh repo view --web
```

---

### STEP 8 — Add repository topics (tags) for discoverability

Run this to tag the repo so it shows up in GitHub searches:

```bash
gh repo edit --add-topic python
gh repo edit --add-topic data-pipeline
gh repo edit --add-topic sql
gh repo edit --add-topic sqlite
gh repo edit --add-topic data-cleaning
gh repo edit --add-topic supply-chain
gh repo edit --add-topic automation
gh repo edit --add-topic analytics
```

---

### STEP 9 — Final checklist

Confirm all of the following are true before telling me you are done:

- [ ] All source files are committed and pushed
- [ ] `.gitignore` is in place and `outputs/` generated files are excluded
- [ ] `data/` and `outputs/` folders exist in the repo (via `.gitkeep`)
- [ ] The repo is public and visible at `https://github.com/KhayehG/supply-chain-data-toolkit`
- [ ] The repo has a description and topics set
- [ ] `python pipeline.py` runs without errors locally

Once all boxes are checked, give me the final GitHub URL I can paste into my portfolio and CV.

---

## Notes for Copilot

- My GitHub username is `KhayehG`
- Do not rename any files or change any existing code
- If the GitHub CLI (`gh`) is not authenticated, guide me through `gh auth login` first
- Python version required: 3.10 or higher (`python --version` to check)
- If I am on Windows, replace `touch` with `New-Item` or `type nul >` equivalents
