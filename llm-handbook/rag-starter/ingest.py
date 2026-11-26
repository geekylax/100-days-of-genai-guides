"""Step 1: clean + chunk + embed your docs.

    python ingest.py            # indexes ./docs
    python ingest.py my_folder  # or any folder of .md / .txt / .html files
"""
import sys
from pathlib import Path

from rag import build_index

folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "docs"
build_index(folder)
