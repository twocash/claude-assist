#!/usr/bin/env python3
"""
Grove Docs Refinery

A two-layer system for batch content refactoring:
- Grove Editorial Engine — The stable methodology
- Grove Docs Refinery — The orchestration process

Usage:
    from grove_docs_refinery import RefineryOrchestrator

    orchestrator = RefineryOrchestrator()
    orchestrator.initialize()
    manifest = orchestrator.run_batch()
"""

from .refinery import RefineryOrchestrator, RunManifest
from .checkpoint import EditorialCheckpoint, load_checkpoint
from .editor import EditorAgent, Analysis, Draft
from .reviewer import ReviewerAgent, Review, Assessment
from .config import get_config, RefineryConfig

__version__ = "1.0"

__all__ = [
    # Orchestrator
    "RefineryOrchestrator",
    "RunManifest",
    # Checkpoint
    "EditorialCheckpoint",
    "load_checkpoint",
    # Editor
    "EditorAgent",
    "Analysis",
    "Draft",
    # Reviewer
    "ReviewerAgent",
    "Review",
    "Assessment",
    # Config
    "get_config",
    "RefineryConfig",
]
