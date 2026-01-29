"""Core Boustrophedon text transformation logic."""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterator
from typing import Optional


def reverse_word_order(text: str) -> str:
    """Reverse the order of words in text for right-to-left reading.

    Words are reversed in order. Punctuation attached to words is flipped:
    trailing punctuation moves to the start (left), and leading punctuation
    moves to the end (right). This ensures that when reading right-to-left,
    scanning hits the punctuation at the correct semantic boundary.

    Example: 'Hello "world".' -> '.world" Hello'

    Args:
        text: The text to reverse.

    Returns:
        The text with words in reversed order and flipped punctuation.
    """
    words = text.split()
    reversed_words = reversed(words)
    processed_words = []

    # Regex to capture leading non-word chars (1), body (2), trailing non-word chars (3)
    # \W matches any character that is not a word character (alphanumeric plus underscore)
    punct_pattern = re.compile(r"^(\W*)(.*?)(\W*)$")

    for word in reversed_words:
        match = punct_pattern.match(word)
        if match:
            prefix, body, suffix = match.groups()
            # Flip prefix and suffix
            # e.g. "word." -> prefix="", suffix="." -> ".word"
            # e.g. "\"word" -> prefix="\"", suffix="" -> "word\""
            processed_words.append(f"{suffix}{body}{prefix}")
        else:
            processed_words.append(word)

    return " ".join(processed_words)


class TransformMode(Enum):
    """Text transformation mode."""

    DUMB = "dumb"  # Character-count based line reversal
    SMART = "smart"  # NLP-based natural pause detection


@dataclass
class Line:
    """A single line of transformed text."""

    text: str
    reversed: bool
    line_number: int
    is_new_paragraph: bool = False

    @property
    def display_text(self) -> str:
        """Return the text as it should be displayed.

        For reversed lines, word order is reversed so the line reads
        right-to-left but each word remains readable.
        """
        if self.reversed:
            return reverse_word_order(self.text)
        return self.text


@dataclass
class TransformResult:
    """Result of a Boustrophedon transformation."""

    lines: list[Line]
    mode: TransformMode
    line_width: int
    source_length: int

    def __iter__(self) -> Iterator[Line]:
        return iter(self.lines)

    def __len__(self) -> int:
        return len(self.lines)


class BoustrophedonTransformer:
    """Transform text into Boustrophedon format (alternating line directions)."""

    def __init__(
        self,
        line_width: int = 80,
        mode: TransformMode = TransformMode.DUMB,
        reverse_even: bool = False,
    ) -> None:
        """Initialize transformer.

        Args:
            line_width: Maximum characters per line.
            mode: Transformation mode (dumb or smart).
            reverse_even: If True, reverse even-numbered lines (0-indexed).
                         If False, reverse odd-numbered lines.
        """
        self.line_width = line_width
        self.mode = mode
        self.reverse_even = reverse_even

    def transform(self, text: str) -> TransformResult:
        """Transform text into Boustrophedon format.

        If the text contains a separator '---', the part before it is treated
        as a header (kept LTR) and the part after is transformed.

        Args:
            text: Input text to transform.

        Returns:
            TransformResult containing the transformed lines.
        """
        header_lines: list[Line] = []
        body_text = text

        # Check for header separator
        # Match newline(s), 3+ dashes, newline
        match = re.search(r'\r?\n-{3,}\r?\n', text)
        if match:
            sep_start, sep_end = match.span()
            header_text = text[:sep_start]
            body_text = text[sep_end:]

            # Convert header to simple separate LTR lines
            h_sublines = header_text.splitlines()
            # We use negative line numbers for header to avoid affecting body alternation
            for i, h_line in enumerate(h_sublines):
                # Header lines are always new paragraphs contextually
                header_lines.append(
                    Line(
                        text=h_line,
                        reversed=False,
                        line_number=-(len(h_sublines) - i),
                        is_new_paragraph=True,
                    )
                )

        if self.mode == TransformMode.DUMB:
            lines = self._transform_dumb(body_text)
        else:
            lines = self._transform_smart(body_text)

        return TransformResult(
            lines=header_lines + lines,
            mode=self.mode,
            line_width=self.line_width,
            source_length=len(text),
        )

    def _transform_dumb(self, text: str) -> list[Line]:
        """Simple character-count based transformation."""
        # Split into words, preserving paragraph breaks
        paragraphs = text.split("\n\n")
        all_lines: list[Line] = []
        line_num = 0

        for para in paragraphs:
            if not para.strip():
                continue

            words = para.split()
            current_line: list[str] = []
            current_length = 0
            is_start_of_para = True

            for word in words:
                word_len = len(word)
                # +1 for space if not first word
                needed = word_len + (1 if current_line else 0)

                if current_length + needed <= self.line_width:
                    current_line.append(word)
                    current_length += needed
                else:
                    # Emit current line
                    if current_line:
                        line_text = " ".join(current_line)
                        should_reverse = (line_num % 2 == 0) == self.reverse_even
                        all_lines.append(
                            Line(
                                text=line_text,
                                reversed=should_reverse,
                                line_number=line_num,
                                is_new_paragraph=is_start_of_para,
                            )
                        )
                        line_num += 1
                        is_start_of_para = False

                    # Start new line with current word
                    current_line = [word]
                    current_length = word_len

            # Emit final line of paragraph
            if current_line:
                line_text = " ".join(current_line)
                should_reverse = (line_num % 2 == 0) == self.reverse_even
                all_lines.append(
                    Line(
                        text=line_text,
                        reversed=should_reverse,
                        line_number=line_num,
                        is_new_paragraph=is_start_of_para,
                    )
                )
                line_num += 1

        return all_lines

    def _transform_smart(self, text: str) -> list[Line]:
        """NLP-based transformation with natural pause detection.

        Requires spacy to be installed (oxturn[nlp]).
        Falls back to dumb mode if spacy is not available.
        """
        try:
            import spacy

            try:
                nlp = spacy.load("en_core_web_sm")
            except OSError:
                # Model not installed, fall back to dumb mode
                import warnings

                warnings.warn(
                    "spaCy model 'en_core_web_sm' not found. "
                    "Install with: python -m spacy download en_core_web_sm. "
                    "Falling back to dumb mode.",
                    stacklevel=2,
                )
                return self._transform_dumb(text)

        except ImportError:
            import warnings

            warnings.warn(
                "spaCy not installed. Install with: pip install oxturn[nlp]. "
                "Falling back to dumb mode.",
                stacklevel=2,
            )
            return self._transform_dumb(text)

        doc = nlp(text)
        all_lines: list[Line] = []
        line_num = 0

        # Simple loop for smart mode just to fix compile error for now if I was editing it,
        # but the user didn't ask to fix smart mode explicitly, however I should ensure Line(...) calls are correct.
        # Wait, I changed the dataclass default is_new_paragraph=False, so existing calls without it will work.
        # But I should probably update smart mode too if possible.
        # Let's just patch the Line definition in _transform_smart if it is called.
        # Looking at _transform_smart in my previous read_file... I only read up to line 200.
        # Let's read the rest of transformer.py to be safe.


        for sent in doc.sents:
            # Try to break sentences at natural pauses (commas, semicolons)
            chunks = self._split_at_pauses(sent.text)

            for chunk in chunks:
                # Further split if chunk exceeds line width
                sub_lines = self._wrap_text(chunk, self.line_width)

                for line_text in sub_lines:
                    should_reverse = (line_num % 2 == 0) == self.reverse_even
                    all_lines.append(
                        Line(
                            text=line_text,
                            reversed=should_reverse,
                            line_number=line_num,
                        )
                    )
                    line_num += 1

        return all_lines

    def _split_at_pauses(self, text: str) -> list[str]:
        """Split text at natural pauses (commas, semicolons, colons)."""
        import re

        # Split at punctuation followed by space, keeping the punctuation
        parts = re.split(r"([,;:])\s+", text)

        # Recombine punctuation with preceding text
        chunks: list[str] = []
        current = ""

        for i, part in enumerate(parts):
            if part in ",;:":
                current += part
            elif current:
                chunks.append(current.strip())
                current = part
            else:
                current = part

        if current.strip():
            chunks.append(current.strip())

        return [c for c in chunks if c]

    def _wrap_text(self, text: str, width: int) -> list[str]:
        """Wrap text to specified width without breaking words."""
        words = text.split()
        lines: list[str] = []
        current_line: list[str] = []
        current_length = 0

        for word in words:
            word_len = len(word)
            needed = word_len + (1 if current_line else 0)

            if current_length + needed <= width:
                current_line.append(word)
                current_length += needed
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_len

        if current_line:
            lines.append(" ".join(current_line))

        return lines
