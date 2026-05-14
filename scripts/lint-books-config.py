#!/usr/bin/env python3
"""
Configuration and constants for the free-programming-books linter.

This module defines rules, patterns, and settings used by lint-books.py
to validate markdown files in the repository.
"""

import re

# ---------------------------------------------------------------------------
# URL / link patterns
# ---------------------------------------------------------------------------

# Matches any Markdown inline link: [text](url)
MD_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Detects plain http:// URLs that could be upgraded to https://
HTTP_URL_PATTERN = re.compile(r'http://(?!localhost|127\.0\.0\.1|0\.0\.0\.0)')

# Detects URLs with trailing whitespace or punctuation inside the parentheses
TRAILING_CHARS_IN_URL = re.compile(r'\(([^)]+[\s,;.])\)')

# ---------------------------------------------------------------------------
# Markdown structural patterns
# ---------------------------------------------------------------------------

# ATX-style headers (# through ######)
HEADER_PATTERN = re.compile(r'^#{1,6}\s')

# Bullet list items (-, *, +)
LIST_ITEM_PATTERN = re.compile(r'^[\s]*([-*+])\s')

# Detects lines with trailing whitespace
TRAILING_WHITESPACE_PATTERN = re.compile(r'[ \t]+$')

# ---------------------------------------------------------------------------
# Book entry patterns
# ---------------------------------------------------------------------------

# A valid book entry line looks like:
#   * [Title](url) - Author *(note)*
# or simply:
#   * [Title](url)
BOOK_ENTRY_PATTERN = re.compile(
    r'^\s*[-*+]\s+'
    r'\[(?P<title>[^\]]+)\]'
    r'\((?P<url>[^)]+)\)'
    r'(?P<rest>.*)$'
)

# Detects duplicate spaces inside a title or author field
DOUBLE_SPACE_PATTERN = re.compile(r'  +')

# ---------------------------------------------------------------------------
# Allowed file extensions / formats mentioned in entries
# ---------------------------------------------------------------------------

KNOWN_FORMATS = {
    'PDF', 'EPUB', 'MOBI', 'HTML', 'Markdown', 'AsciiDoc',
    'Jupyter Notebook', 'Online', 'GitBook',
}

# ---------------------------------------------------------------------------
# Linting rule severity levels
# ---------------------------------------------------------------------------

SEVERITY_ERROR = 'ERROR'
SEVERITY_WARNING = 'WARNING'
SEVERITY_INFO = 'INFO'

# ---------------------------------------------------------------------------
# Files / directories to skip during linting
# ---------------------------------------------------------------------------

SKIP_PATHS = {
    'README.md',
    'CONTRIBUTING.md',
    'CODE_OF_CONDUCT.md',
    'CHANGELOG.md',
    '.github',
    'scripts',
    'node_modules',
    '.git',
}

# ---------------------------------------------------------------------------
# Maximum allowed consecutive blank lines between sections
# ---------------------------------------------------------------------------

MAX_CONSECUTIVE_BLANK_LINES = 1

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def is_header(line: str) -> bool:
    """Return True if *line* is an ATX-style Markdown header."""
    return bool(HEADER_PATTERN.match(line))


def is_list_item(line: str) -> bool:
    """Return True if *line* looks like a Markdown bullet-list entry."""
    return bool(LIST_ITEM_PATTERN.match(line))


def extract_url(line: str) -> str | None:
    """Return the first URL found in a Markdown link on *line*, or None."""
    match = MD_LINK_PATTERN.search(line)
    return match.group(2).strip() if match else None


def has_trailing_whitespace(line: str) -> bool:
    """Return True if *line* contains trailing whitespace."""
    return bool(TRAILING_WHITESPACE_PATTERN.search(line))


def is_http_url(url: str) -> bool:
    """Return True if *url* uses plain http:// (not localhost)."""
    return bool(HTTP_URL_PATTERN.match(url))
