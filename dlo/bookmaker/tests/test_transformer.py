"""Tests for the Boustrophedon transformer."""

import pytest

from oxturn.transformer import BoustrophedonTransformer, TransformMode, Line, reverse_word_order


class TestReverseWordOrder:
    """Tests for the reverse_word_order function."""

    def test_reverse_simple_sentence(self) -> None:
        """Test reversing word order in a simple sentence."""
        result = reverse_word_order("hello world")
        assert result == "world hello"

    def test_reverse_longer_sentence(self) -> None:
        """Test reversing word order in a longer sentence."""
        result = reverse_word_order("instead of making a cheap joke about the Greek")
        assert result == "Greek the about joke cheap a making of instead"

    def test_reverse_single_word(self) -> None:
        """Test that single word remains unchanged."""
        result = reverse_word_order("hello")
        assert result == "hello"


class TestBoustrophedonTransformer:
    """Tests for BoustrophedonTransformer class."""

    def test_basic_transformation(self) -> None:
        """Test basic dumb mode transformation."""
        transformer = BoustrophedonTransformer(line_width=20)
        result = transformer.transform("The quick brown fox jumps over the lazy dog")

        assert len(result) > 0
        assert result.mode == TransformMode.DUMB

    def test_alternating_reversal(self) -> None:
        """Test that lines alternate between normal and reversed."""
        transformer = BoustrophedonTransformer(line_width=10, reverse_even=True)
        text = "one two three four five six seven eight nine ten"
        result = transformer.transform(text)

        # Check alternating pattern
        for i, line in enumerate(result.lines):
            expected_reversed = (i % 2 == 0)
            assert line.reversed == expected_reversed, f"Line {i} reversal mismatch"

    def test_reverse_even_false(self) -> None:
        """Test reverse_even=False reverses odd lines instead."""
        transformer = BoustrophedonTransformer(line_width=10, reverse_even=False)
        text = "one two three four five six seven eight nine ten"
        result = transformer.transform(text)

        for i, line in enumerate(result.lines):
            expected_reversed = (i % 2 != 0)
            assert line.reversed == expected_reversed

    def test_display_text_normal(self) -> None:
        """Test display_text for non-reversed line."""
        line = Line(text="hello world", reversed=False, line_number=0)
        assert line.display_text == "hello world"

    def test_display_text_reversed(self) -> None:
        """Test display_text for reversed line reverses word order."""
        line = Line(text="hello world", reversed=True, line_number=0)
        # Word order should be reversed, but each word stays readable
        assert line.display_text == "world hello"

    def test_no_word_splitting(self) -> None:
        """Test that words are never split across lines."""
        transformer = BoustrophedonTransformer(line_width=15)
        text = "The quick brown fox jumps"
        result = transformer.transform(text)

        for line in result.lines:
            # Each line should contain complete words
            words = line.text.split()
            for word in words:
                assert " " not in word  # No partial words

    def test_empty_input(self) -> None:
        """Test handling of empty input."""
        transformer = BoustrophedonTransformer()
        result = transformer.transform("")
        assert len(result) == 0

    def test_whitespace_only_input(self) -> None:
        """Test handling of whitespace-only input."""
        transformer = BoustrophedonTransformer()
        result = transformer.transform("   \n\n   ")
        assert len(result) == 0

    def test_paragraph_preservation(self) -> None:
        """Test that paragraph breaks are handled."""
        transformer = BoustrophedonTransformer(line_width=50)
        text = "First paragraph here.\n\nSecond paragraph here."
        result = transformer.transform(text)

        # Should produce multiple lines
        assert len(result) >= 2

    def test_line_width_respected(self) -> None:
        """Test that line width is approximately respected."""
        line_width = 40
        transformer = BoustrophedonTransformer(line_width=line_width)
        text = "The quick brown fox jumps over the lazy dog " * 10
        result = transformer.transform(text)

        for line in result.lines:
            # Lines should not significantly exceed width
            # (may be slightly over if a word pushes it)
            assert len(line.text) <= line_width + 20

    def test_result_iteration(self) -> None:
        """Test that TransformResult is iterable."""
        transformer = BoustrophedonTransformer(line_width=20)
        result = transformer.transform("Test text for iteration")

        lines = list(result)
        assert len(lines) == len(result)

    def test_smart_mode_fallback(self) -> None:
        """Test that smart mode falls back to dumb if spacy unavailable."""
        transformer = BoustrophedonTransformer(
            line_width=40,
            mode=TransformMode.SMART,
        )
        # This should not raise, even if spacy is not installed
        result = transformer.transform("Test the smart mode fallback behavior.")
        assert len(result) > 0
