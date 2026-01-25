---
author: Jim Calhoun
date: '2026-01-19'
domain: protocol
last_synced: '2026-01-19T22:07:04.335573'
local_file: 260119-s-protocol-a2ui-protocol-evaluation-for-grove-inspector-architecture.md--FINAL.md
notion_id: 2ed780a7-8eef-8145-b606-d27f8eaad206
notion_url: https://www.notion.so/A2UI-Protocol-Evaluation-for-Grove-Inspector-Architecture-2ed780a78eef8145b606d27f8eaad206
status: final
title: A2UI Protocol Evaluation for Grove Inspector Architecture
type: software
---

# A2UI Protocol Evaluation for Grove Inspector Architecture

## Executive Summary

**Bottom Line:** The current implementation is *more compatible* with A2UI than it appears at first glance, but we're not ready to adopt A2UI now. The strategic move is **to build a thin adapter layer** that preserves optionality while we continue development.

| Criterion | Current State | A2UI Alignment |
|---|---|---|
| Data addressing | JSON Pointer (RFC 6901) ✓ | Full compatibility |
| Mutation format | JSON Patch (RFC 6902) ✓ | Full compatibility |
| State management | Imperative (useReducer) | Conflict - needs reactive binding |
| Component rendering | Hardcoded React | Conflict - needs schema-driven |
| Form handling | Callback-based | Partial - needs userAction mapping |
