"""Dependency checks for DocuMind (milestone P1.5).

These checks prove that the libraries DocuMind depends on really work on this
machine, not just that they import. Run it from the backend folder with:
    python scripts/check_dependencies.py

To check another library later, add one function and one line to CHECKS.
"""

import importlib.metadata
import subprocess
import sys
import tempfile
from pathlib import Path


def check_pymupdf() -> str:
    """Build a 2-page PDF with an outline, save it, reopen it and read it back."""
    import pymupdf

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        pdf_path = str(Path(folder) / "sample.pdf")

        doc = pymupdf.open()
        for number in (1, 2):
            page = doc.new_page()
            page.insert_text((72, 72), f"DocuMind test page {number}")
        doc.set_toc([[1, "Introduction", 1], [1, "Citations", 2]])
        doc.save(pdf_path)
        doc.close()

        reopened = pymupdf.open(pdf_path)
        try:
            assert reopened.page_count == 2, f"expected 2 pages, got {reopened.page_count}"
            for number in (1, 2):
                text = reopened[number - 1].get_text()
                assert f"DocuMind test page {number}" in text, f"page {number} text was {text!r}"
            titles = [entry[1] for entry in reopened.get_toc()]
            assert titles == ["Introduction", "Citations"], f"outline was {titles}"
        finally:
            reopened.close()

    version = importlib.metadata.version("pymupdf")
    return f"PyMuPDF {version} created, saved and reopened a PDF; read 2 pages and the outline"


# Three tiny "chunks" for the ChromaDB check. Each has a made-up 3-number
# embedding. Real embeddings (Phase 5) have hundreds of numbers; the idea is
# identical: the store finds the stored vector closest to the query vector.
CHROMA_CHUNKS = [
    {"id": "a-p1", "document_id": "doc-a", "page": 1, "text": "alpha page one", "vector": [1.0, 0.0, 0.0]},
    {"id": "a-p2", "document_id": "doc-a", "page": 2, "text": "alpha page two", "vector": [0.0, 1.0, 0.0]},
    {"id": "b-p1", "document_id": "doc-b", "page": 1, "text": "beta page one", "vector": [0.0, 0.0, 1.0]},
]


def open_chroma(folder: str):
    """Open (or create) a ChromaDB store in a folder, with telemetry switched off."""
    import chromadb

    return chromadb.PersistentClient(
        path=folder,
        settings=chromadb.Settings(anonymized_telemetry=False),
    )


def seed_chroma(folder: str) -> None:
    """Write the sample chunks to a ChromaDB store. Run in a separate process by check_chromadb."""
    collection = open_chroma(folder).get_or_create_collection("spike")
    collection.add(
        ids=[chunk["id"] for chunk in CHROMA_CHUNKS],
        embeddings=[chunk["vector"] for chunk in CHROMA_CHUNKS],
        documents=[chunk["text"] for chunk in CHROMA_CHUNKS],
        metadatas=[{"document_id": chunk["document_id"], "page": chunk["page"]} for chunk in CHROMA_CHUNKS],
    )


def check_chromadb() -> str:
    """Store vectors in one process, then reopen, search and delete in another."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
        # Step 1: a separate Python process writes the vectors and exits. That
        # simulates the server being stopped and started again.
        subprocess.run([sys.executable, __file__, "--seed", folder], check=True)

        # Step 2: this process opens the same folder. The vectors must still be there.
        collection = open_chroma(folder).get_collection("spike")
        assert collection.count() == 3, f"expected 3 stored vectors, got {collection.count()}"

        # Step 3: nearest-neighbour search. [0.9, 0.1, 0.0] is closest to doc-a page 1.
        result = collection.query(query_embeddings=[[0.9, 0.1, 0.0]], n_results=1)
        assert result["ids"][0] == ["a-p1"], f"nearest id was {result['ids'][0]}"
        assert result["metadatas"][0][0]["page"] == 1, f"metadata was {result['metadatas'][0][0]}"
        assert result["documents"][0] == ["alpha page one"], f"text was {result['documents'][0]}"

        # Step 4: delete every vector that belongs to one document (safe deletion, TD-006).
        collection.delete(where={"document_id": "doc-a"})
        assert collection.count() == 1, f"expected 1 vector left, got {collection.count()}"
        remaining = collection.get()["ids"]
        assert remaining == ["b-p1"], f"remaining ids were {remaining}"

    version = importlib.metadata.version("chromadb")
    return f"ChromaDB {version} stored 3 vectors, kept them across a restart, found the nearest, and deleted one document's vectors"


CHECKS = [
    ("PyMuPDF", check_pymupdf),
    ("ChromaDB", check_chromadb),
]


def main() -> int:
    # Hidden mode used by check_chromadb: write the sample data, then stop.
    if len(sys.argv) == 3 and sys.argv[1] == "--seed":
        seed_chroma(sys.argv[2])
        return 0

    failures = 0
    for name, check in CHECKS:
        try:
            message = check()
        except Exception as error:
            failures += 1
            print(f"FAIL {name}: {type(error).__name__}: {error}")
        else:
            print(f"PASS {name}: {message}")

    print("All checks passed" if failures == 0 else f"{failures} check(s) failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())