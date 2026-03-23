"""Chapter boundary detection and text chunking."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class DetectedChapter:
    """A chapter boundary found in raw text."""
    title: str
    chapter_number: int
    start_pos: int
    content: str = field(default="", repr=False)


# ── Regex patterns for chapter boundary detection ──────────────────────

CHAPTER_PATTERNS: list[re.Pattern] = [
    # "Chapter 12: Cardiovascular Pathology"
    re.compile(
        r'^(chapter\s+(\d+)[:\s\u2014\-]+(.+))$',
        re.IGNORECASE | re.MULTILINE,
    ),
    # "CHAPTER 12" (all caps, possibly no subtitle)
    re.compile(
        r'^(CHAPTER\s+(\d+)(?:[:\s\u2014\-]+([A-Z][^\n]+))?)$',
        re.MULTILINE,
    ),
    # "12. Cardiovascular Pathology" (numbered section at line start)
    re.compile(
        r'^((\d{1,2})\.\s+([A-Z][^\n]{5,}))$',
        re.MULTILINE,
    ),
    # "1.0  Introduction" style
    re.compile(
        r'^((\d+)\.0\s+([A-Z][^\n]+))$',
        re.MULTILINE,
    ),
]


def detect_chapters(text: str) -> list[DetectedChapter]:
    """Scan raw text and return detected chapter boundaries.

    Tries patterns in order from most-specific to least-specific.
    Falls back to returning the entire text as a single chapter.
    """
    matches: list[tuple[int, int, str]] = []  # (start, chapter_num, title)

    for pattern in CHAPTER_PATTERNS:
        for m in pattern.finditer(text):
            num_str = m.group(2)
            title_part = (m.group(3) or '').strip()
            full_heading = m.group(1).strip()

            try:
                num = int(num_str)
            except (ValueError, IndexError):
                num = len(matches) + 1

            title = f"Chapter {num}: {title_part}" if title_part else f"Chapter {num}"
            matches.append((m.start(), num, title))

        if matches:
            break  # Stop at first pattern that finds anything

    if not matches:
        # No chapter markers found — treat entire text as one unit
        return [DetectedChapter(
            title="Untitled Chapter",
            chapter_number=1,
            start_pos=0,
            content=text.strip(),
        )]

    # Sort by position, deduplicate overlapping
    matches.sort(key=lambda x: x[0])
    chapters: list[DetectedChapter] = []

    for i, (start, num, title) in enumerate(matches):
        end = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        chapters.append(DetectedChapter(
            title=title,
            chapter_number=num,
            start_pos=start,
            content=content,
        ))

    return chapters


def split_into_sections(text: str, min_section_words: int = 50) -> list[tuple[str, str]]:
    """Split text into (heading, body) tuples based on heading patterns.

    Returns list of (section_heading, section_text) pairs.
    """
    # Look for lines that look like section headings:
    # ALL CAPS lines, or Title Case short lines followed by content
    heading_pattern = re.compile(
        r'^([A-Z][A-Z\s&/,:\-]{3,60})$',
        re.MULTILINE,
    )

    positions: list[tuple[int, str]] = []
    for m in heading_pattern.finditer(text):
        heading = m.group(1).strip()
        # Filter out lines that are just chapter titles we already handled
        if not re.match(r'CHAPTER\s+\d+', heading, re.IGNORECASE):
            positions.append((m.start(), heading))

    if not positions:
        return [("General", text.strip())]

    sections: list[tuple[str, str]] = []
    for i, (start, heading) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        body = text[start:end].strip()
        word_count = len(body.split())
        if word_count >= min_section_words:
            sections.append((heading, body))

    return sections if sections else [("General", text.strip())]


def chunk_text(text: str, max_chars: int = 30_000) -> list[str]:
    """Split text into chunks of at most max_chars, breaking on paragraph boundaries."""
    if len(text) <= max_chars:
        return [text]

    paragraphs = re.split(r'\n\s*\n', text)
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) > max_chars:
            if current:
                chunks.append(current.strip())
            current = para
        else:
            current = (current + "\n\n" + para).strip()

    if current:
        chunks.append(current.strip())

    return chunks
