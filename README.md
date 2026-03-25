# AI Workflow

Small utility project for automating interactions with Google Drive / Sheets and running analysis.

## Overview

This repository contains scripts to access Google APIs, parse inputs, and run the main workflow from `main.py`.

## Project structure

- `main.py` — primary entry point for the workflow
- `drive.py` — Google Drive helper functions
- `sheets.py` — Google Sheets helper functions
- `parser.py` — input parsing utilities
- `credentials.json`, `credentials_drive.json` — OAuth/service credentials (NOT checked into version control)
- `main.spec` — PyInstaller spec used to build a standalone executable
- `build/` — output from packaging/build steps
- `Original/` — original credential backups

## Setup

1. Create and activate a virtual environment (recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies (create `requirements.txt` if missing):

   ```powershell
   pip install -r requirements.txt
   ```

3. Place your Google API credentials as `credentials.json` and `credentials_drive.json` in the project root.

## Usage

Run the main workflow:

```powershell
python main.py
```

If packaging a binary with PyInstaller (spec included):

```powershell
pyinstaller main.spec
```

