"""Tests for chapter boundary detection and text chunking."""

import pytest
from backend.chapter_parser import detect_chapters, split_into_sections, chunk_text


SAMPLE_TEXT = """
Chapter 1: Introduction to Pathology

Pathology is the study of disease. It encompasses the examination
of cells, tissues, and organs to understand the mechanisms of disease.

Cells respond to injury in several ways including:
- Adaptation
- Cell injury
- Cell death

Chapter 2: Cell Injury and Death

Cells can be injured by hypoxia, toxins, infections, and immune reactions.
The most important cause of cell death in clinical medicine is ischemia.

Necrosis is the sum of morphological changes that follow cell death.
Apoptosis is programmed cell death.
"""


def test_detect_chapters_finds_boundaries():
    chapters = detect_chapters(SAMPLE_TEXT)
    assert len(chapters) == 2
    assert chapters[0].chapter_number == 1
    assert "Introduction" in chapters[0].title
    assert chapters[1].chapter_number == 2
    assert "Cell Injury" in chapters[1].title


def test_detect_chapters_populates_content():
    chapters = detect_chapters(SAMPLE_TEXT)
    assert "Pathology" in chapters[0].content
    assert "ischemia" in chapters[1].content


def test_detect_chapters_fallback():
    """Text with no chapter markers returns a single chapter."""
    plain = "This is just some plain text without any chapter markers."
    chapters = detect_chapters(plain)
    assert len(chapters) == 1
    assert chapters[0].chapter_number == 1
    assert chapters[0].content == plain


def test_split_into_sections_fallback():
    """Text with no detectable headings returns a single General section."""
    text = "Some content without section headings."
    sections = split_into_sections(text)
    assert len(sections) == 1
    assert sections[0][0] == "General"


def test_chunk_text_no_split_needed():
    short = "Short text"
    chunks = chunk_text(short, max_chars=1000)
    assert chunks == [short]


def test_chunk_text_splits_on_paragraphs():
    para = "Word " * 100  # ~500 chars
    text = (para + "\n\n") * 10  # ~5000 chars
    chunks = chunk_text(text, max_chars=1000)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 1500  # Some slack for paragraph boundaries
