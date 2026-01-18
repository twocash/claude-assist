#!/usr/bin/env python3
"""
Build LEANN index for Grove knowledge base.

Usage:
    python -m grove_research_generator.build_index
    python -m grove_research_generator.build_index --docs-dir ./custom-docs
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add leann-repo to path
LEANN_PATH = Path(__file__).parent.parent / "leann-repo" / "packages" / "leann-core" / "src"
sys.path.insert(0, str(LEANN_PATH))

try:
    from leann import LeannBuilder
    LEANN_AVAILABLE = True
except ImportError:
    LEANN_AVAILABLE = False
    print("Warning: LEANN not available. Install with: pip install leann")


def load_markdown_files(docs_dir: Path) -> List[Dict[str, Any]]:
    """Load markdown files and extract metadata."""
    chunks = []

    for md_file in docs_dir.glob("**/*.md"):
        if md_file.name.startswith("."):
            continue

        content = md_file.read_text(encoding="utf-8")

        # Extract title from first heading
        title = md_file.stem
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break

        # Create chunk with metadata
        chunks.append({
            "text": content,
            "metadata": {
                "title": title,
                "source": str(md_file.relative_to(docs_dir)),
                "path": str(md_file),
                "type": "grove_documentation",
            }
        })

    return chunks


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 128) -> List[str]:
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks


def build_grove_index(
    docs_dirs: List[Path],
    output_path: Path,
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    chunk_size: int = 512,
    chunk_overlap: int = 128,
) -> None:
    """Build LEANN index from Grove documentation."""

    if not LEANN_AVAILABLE:
        print("ERROR: LEANN is not installed.")
        print("Install with: pip install leann")
        sys.exit(1)

    print(f"Building Grove knowledge index...")
    print(f"Output: {output_path}")
    print(f"Embedding model: {embedding_model}")
    print()

    # Collect all documents
    all_docs = []
    for docs_dir in docs_dirs:
        if docs_dir.exists():
            docs = load_markdown_files(docs_dir)
            print(f"Loaded {len(docs)} documents from {docs_dir}")
            all_docs.extend(docs)
        else:
            print(f"Warning: Directory not found: {docs_dir}")

    if not all_docs:
        print("ERROR: No documents found to index.")
        sys.exit(1)

    print(f"\nTotal documents: {len(all_docs)}")

    # Build index
    print("\nBuilding index...")
    builder = LeannBuilder(
        embedding_model=embedding_model,
        backend_name="hnsw",
    )

    total_chunks = 0
    for doc in all_docs:
        # Chunk the document
        chunks = chunk_text(doc["text"], chunk_size, chunk_overlap)

        for chunk in chunks:
            # Add chunk with metadata
            builder.add_text(
                chunk,
                metadata={
                    **doc["metadata"],
                    "chunk_index": total_chunks,
                }
            )
            total_chunks += 1

    print(f"Total chunks: {total_chunks}")

    # Build and save
    builder.build_index(str(output_path))
    print(f"\nIndex saved to: {output_path}")
    print("Done!")


def main():
    parser = argparse.ArgumentParser(
        description="Build LEANN index for Grove knowledge base"
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        nargs="+",
        default=None,
        help="Directories containing documents to index",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path for the index (default: grove-knowledge.leann)",
    )
    parser.add_argument(
        "--embedding-model",
        type=str,
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Embedding model to use",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=512,
        help="Chunk size in words",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=128,
        help="Chunk overlap in words",
    )

    args = parser.parse_args()

    # Default directories
    project_root = Path(__file__).parent.parent

    if args.docs_dir:
        docs_dirs = args.docs_dir
    else:
        docs_dirs = [
            project_root / "grove_docs_refinery" / "refined",
            project_root / "grove_docs_refinery" / "drafts",
        ]

    if args.output:
        output_path = args.output
    else:
        output_path = project_root / "grove_research_generator" / "grove-knowledge.leann"

    build_grove_index(
        docs_dirs=docs_dirs,
        output_path=output_path,
        embedding_model=args.embedding_model,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )


if __name__ == "__main__":
    main()
