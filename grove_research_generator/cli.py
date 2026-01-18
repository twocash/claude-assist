#!/usr/bin/env python3
"""
Grove Research Generator CLI

Manual invocation for testing and development.

Usage:
    python -m grove_research_generator test
    python -m grove_research_generator generate --draft draft.md --direction "turn into blog about X"
    python -m grove_research_generator generate --topic "Distributed Inference" --format blog
"""

import argparse
import sys
from pathlib import Path

from .config import get_config
from .orchestrator import ResearchOrchestrator, ResearchRequest


def cmd_test(args):
    """Test the research generator setup."""
    print("Testing Grove Research Generator...")
    print("=" * 50)

    config = get_config()
    print(f"Config loaded: {config}")
    print(f"Prompts dir: {config.prompts_dir}")
    print(f"LEANN index: {config.leann_index_path}")

    # Check prompts exist
    print("\nChecking prompts...")
    for prompt_file in ["research_engine.md", "research_checkpoint.md", "citation_guide.md"]:
        path = config.prompts_dir / prompt_file
        status = "OK" if path.exists() else "MISSING"
        print(f"  {prompt_file}: {status}")

    # Test orchestrator creation
    print("\nTesting orchestrator...")
    try:
        orchestrator = ResearchOrchestrator(config)
        print("  Orchestrator created: OK")
    except Exception as e:
        print(f"  ERROR: {e}")
        return

    # Test request parsing
    print("\nTesting request parsing...")
    request = orchestrator.parse_research_request(
        page_id="test-123",
        draft_content="# Test Draft\n\nThis is about Trellis Architecture.",
        comment_text="@atlas turn this into a blog post about distributed inference",
    )
    print(f"  Topic: {request.topic}")
    print(f"  Format: {request.format}")
    print(f"  Direction: {request.user_direction[:50]}...")

    print("\n" + "=" * 50)
    print("Test complete!")


def cmd_generate(args):
    """Generate a research document."""
    config = get_config()
    orchestrator = ResearchOrchestrator(config)

    # Get draft content
    if args.draft:
        draft_path = Path(args.draft)
        if not draft_path.exists():
            print(f"ERROR: Draft file not found: {draft_path}")
            sys.exit(1)
        draft_content = draft_path.read_text(encoding="utf-8")
    else:
        draft_content = f"# {args.topic}\n\nDraft content about {args.topic}."

    # Build direction
    direction = args.direction or f"@atlas create a {args.format} about {args.topic}"

    print(f"Generating {args.format} document...")
    print(f"Topic: {args.topic or '(from draft)'}")
    print(f"Direction: {direction[:50]}...")
    print()

    # Run pipeline
    result = orchestrator.run_pipeline(
        page_id="cli-manual",
        draft_content=draft_content,
        comment_text=direction,
        dry_run=args.dry_run,
    )

    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(result["markdown"], encoding="utf-8")
        print(f"Saved to: {output_path}")
    else:
        print("=" * 50)
        print(result["markdown"])
        print("=" * 50)

    # Show validation if not dry run
    if not args.dry_run and "validation" in result:
        validation = result["validation"]
        print(f"\nValidation: {validation.status}")
        if validation.issues:
            print("Issues:")
            for issue in validation.issues:
                print(f"  - {issue}")


def cmd_validate(args):
    """Validate an existing document."""
    config = get_config()
    orchestrator = ResearchOrchestrator(config)

    doc_path = Path(args.document)
    if not doc_path.exists():
        print(f"ERROR: Document not found: {doc_path}")
        sys.exit(1)

    content = doc_path.read_text(encoding="utf-8")

    print(f"Validating: {doc_path.name}")
    print()

    result = orchestrator.handle_completion(
        page_id="cli-validate",
        final_content=content,
    )

    validation = result["validation"]
    print(f"Status: {validation.status}")
    print(f"Destination: {validation.destination}")
    print()
    print(validation.feedback)


def cmd_build_index(args):
    """Build LEANN index for Grove docs."""
    from .build_index import build_grove_index
    from pathlib import Path

    project_root = Path(__file__).parent.parent

    if args.docs_dir:
        docs_dirs = [Path(d) for d in args.docs_dir]
    else:
        docs_dirs = [
            project_root / "grove_docs_refinery" / "refined",
            project_root / "grove_docs_refinery" / "drafts",
        ]

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(__file__).parent / "grove-knowledge.leann"

    build_grove_index(
        docs_dirs=docs_dirs,
        output_path=output_path,
        embedding_model=args.embedding_model,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Grove Research Generator CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # test command
    test_parser = subparsers.add_parser("test", help="Test setup")
    test_parser.set_defaults(func=cmd_test)

    # generate command
    gen_parser = subparsers.add_parser("generate", help="Generate research document")
    gen_parser.add_argument("--draft", help="Path to draft markdown file")
    gen_parser.add_argument("--topic", help="Topic for the document")
    gen_parser.add_argument("--direction", help="User direction for generation")
    gen_parser.add_argument(
        "--format",
        choices=["blog", "whitepaper", "deep_dive"],
        default="blog",
        help="Document format",
    )
    gen_parser.add_argument("--output", "-o", help="Output file path")
    gen_parser.add_argument("--dry-run", action="store_true", help="Skip validation")
    gen_parser.set_defaults(func=cmd_generate)

    # validate command
    val_parser = subparsers.add_parser("validate", help="Validate existing document")
    val_parser.add_argument("document", help="Path to document to validate")
    val_parser.set_defaults(func=cmd_validate)

    # build-index command
    idx_parser = subparsers.add_parser("build-index", help="Build LEANN index for Grove docs")
    idx_parser.add_argument("--docs-dir", nargs="+", help="Directories containing documents")
    idx_parser.add_argument("--output", "-o", help="Output path for index")
    idx_parser.add_argument(
        "--embedding-model",
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Embedding model to use",
    )
    idx_parser.add_argument("--chunk-size", type=int, default=512, help="Chunk size")
    idx_parser.add_argument("--chunk-overlap", type=int, default=128, help="Chunk overlap")
    idx_parser.set_defaults(func=cmd_build_index)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
