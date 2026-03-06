"""Tests for core/intelligence/rag/chunker.py"""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "core" / "intelligence" / "rag"))

from chunker import Chunk, _split_by_sections, _recursive_split


class TestChunkModel:
    """Tests for the Chunk data model."""

    def test_chunk_creation(self):
        chunk = Chunk(text="Hello world", source_file="test.md")
        assert chunk.text == "Hello world"
        assert chunk.source_file == "test.md"
        assert chunk.chunk_id.startswith("ch_")
        assert len(chunk.chunk_id) == 11  # "ch_" + 8 hex chars

    def test_chunk_deterministic_id(self):
        chunk1 = Chunk(text="Same content", source_file="test.md", start_char=0)
        chunk2 = Chunk(text="Same content", source_file="test.md", start_char=0)
        assert chunk1.chunk_id == chunk2.chunk_id

    def test_chunk_different_content_different_id(self):
        chunk1 = Chunk(text="Content A", source_file="test.md")
        chunk2 = Chunk(text="Content B", source_file="test.md")
        assert chunk1.chunk_id != chunk2.chunk_id

    def test_chunk_metadata(self):
        chunk = Chunk(
            text="test",
            source_file="test.md",
            person="hormozi",
            domain="sales",
            layer="L1-PHILOSOPHIES",
        )
        assert chunk.person == "hormozi"
        assert chunk.domain == "sales"
        assert chunk.layer == "L1-PHILOSOPHIES"

    def test_chunk_to_dict(self):
        chunk = Chunk(text="test", source_file="test.md", person="cole")
        d = chunk.to_dict()
        assert isinstance(d, dict)
        assert d["text"] == "test"
        assert d["source_file"] == "test.md"
        assert d["person"] == "cole"
        assert "chunk_id" in d


class TestSplitBySections:
    """Tests for markdown section splitting."""

    def test_single_section(self):
        text = "# Title\n\nSome content here."
        sections = _split_by_sections(text)
        assert len(sections) >= 1

    def test_multiple_sections(self):
        text = "# Title\n\nContent 1\n\n## Section 2\n\nContent 2\n\n## Section 3\n\nContent 3"
        sections = _split_by_sections(text)
        assert len(sections) >= 2

    def test_empty_text(self):
        sections = _split_by_sections("")
        assert isinstance(sections, list)

    def test_no_headers(self):
        text = "Just plain text without any markdown headers."
        sections = _split_by_sections(text)
        assert len(sections) >= 1


class TestRecursiveSplit:
    """Tests for recursive character splitting."""

    def test_short_text_below_min_skipped(self):
        """Text below MIN_CHUNK_SIZE (100 chars) is skipped by recursive split."""
        text = "Short text"
        chunks = _recursive_split(text, max_size=2048)
        assert len(chunks) == 0  # Below MIN_CHUNK_SIZE threshold

    def test_text_above_min_no_split(self):
        """Text above MIN_CHUNK_SIZE but below max_size returns single chunk."""
        text = "A" * 150  # Above MIN_CHUNK_SIZE (100), below max_size (2048)
        chunks = _recursive_split(text, max_size=2048)
        assert len(chunks) == 1

    def test_long_text_splits(self):
        text = "A" * 5000
        chunks = _recursive_split(text, max_size=2048)
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk) <= 2048

    def test_split_preserves_content(self):
        text = "Hello world. " * 200  # ~2600 chars
        chunks = _recursive_split(text, max_size=2048)
        joined = "".join(chunks)
        # Content should be preserved (may have overlap)
        assert "Hello world" in joined
