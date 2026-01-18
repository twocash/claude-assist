# Chicago Citation Guide

## Footnote Format

Grove research documents use Chicago-style footnotes. Place a marker in the text where the citation applies, then provide the full citation at the document end.

### In-Text Marker
```
The Grove architecture enables distributed inference.[^1]
```

### Footnote Definition
```
[^1]: Author Name, "Article Title," Publication Name, Date, URL.
```

---

## Citation Templates

### Grove Documentation
```
[^n]: Author, "Document Title," Grove Documentation, Month Year.
```

**Example:**
```
[^1]: Jim Calhoun, "The Ratchet Thesis," Grove Documentation, January 2026.
```

### Academic Paper
```
[^n]: Author Last, First, "Paper Title," Journal Name Volume, no. Issue (Year): Pages.
```

**Example:**
```
[^2]: Smith, John, "Distributed AI Systems," AI Journal 15, no. 3 (2025): 45-62.
```

### Web Article
```
[^n]: Author, "Article Title," Publication, Date, URL.
```

**Example:**
```
[^3]: Jane Doe, "The Future of Edge Computing," Tech Review, March 15, 2025, https://example.com/article.
```

### Book
```
[^n]: Author Last, First, Book Title (City: Publisher, Year), page.
```

**Example:**
```
[^4]: Anderson, Chris, The Long Tail (New York: Hyperion, 2006), 52.
```

### Interview or Personal Communication
```
[^n]: Name, interview by Author, Date.
```

**Example:**
```
[^5]: Jim Calhoun, interview by author, January 10, 2026.
```

---

## Bibliography Format

The bibliography appears at the document end, after all footnotes. Entries are alphabetized by author's last name.

### Format
```
## Bibliography

Last, First. "Title." Publication, Date. URL.
```

### Example Bibliography
```
## Bibliography

Calhoun, Jim. "The Ratchet Thesis." Grove Documentation, January 2026.

Doe, Jane. "The Future of Edge Computing." Tech Review, March 15, 2025. https://example.com/article.

Smith, John. "Distributed AI Systems." AI Journal 15, no. 3 (2025): 45-62.
```

---

## When to Cite

### Always Cite
- Direct quotes (even short phrases)
- Specific statistics or data points
- Technical specifications
- Claims requiring attribution
- Ideas originating from specific sources

### Usually Cite
- Paraphrased arguments from other works
- Industry benchmarks
- Historical facts not commonly known
- Comparative claims

### Don't Need to Cite
- Common knowledge in the field
- Your own original analysis
- General observations
- Logical conclusions from cited premises

---

## Multiple Citations

When multiple sources support a claim, combine them:

```
Several studies have demonstrated this effect.[^1][^2][^3]
```

Or use a note with multiple sources:

```
[^1]: See Smith, "Study A" (2024); Jones, "Study B" (2025); and Wilson, "Study C" (2025).
```

---

## Quoting

### Short Quote (under 4 lines)
Use quotation marks inline:

```
As Calhoun notes, "The ratchet moves in one direction only."[^1]
```

### Long Quote (4+ lines)
Use a block quote:

```
> The fundamental insight is that distributed systems
> need not sacrifice consistency for availability.
> Instead, we can design for eventual convergence
> while maintaining strong operational guarantees.[^1]
```

---

## Common Mistakes

### Wrong: Citation after period
```
This is a fact.[^1]  ← Wrong placement
```

### Right: Citation before period
```
This is a fact[^1].  ← Also acceptable
```

### Preferred: Citation integrated
```
Research shows this effect[^1], which has implications...
```

---

## Tracking Sources

The CitationManager tracks:
- Citation number
- Source text/snippet
- Title
- Author
- URL
- Date

This enables automatic bibliography generation in proper Chicago format.

---

*Reference: The Chicago Manual of Style, 17th Edition*
