"""TODO: load .md/.txt/.pdf files, split into chunks and preserve metadata."""
from pathlib import Path

DOCS_DIR = Path("data/documents")

def main():
    paths = sorted(p for p in DOCS_DIR.glob("*") if p.is_file())
    print(f"Found {len(paths)} document(s) in {DOCS_DIR}")
    for path in paths:
        print(f"- {path.name}")

if __name__ == "__main__":
    main()
