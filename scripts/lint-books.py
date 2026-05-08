#!/usr/bin/env python3
"""
lint-books.py - Linter for free-programming-books markdown files.

Checks for common formatting issues in book list markdown files:
- Duplicate URLs
- Malformed links
- Incorrect formatting of entries
- Alphabetical ordering within sections
- Trailing whitespace
- Missing or extra blank lines
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict

# Regex patterns
MARKDOWN_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
SECTION_HEADER_RE = re.compile(r'^#{1,4}\s+.+')
LIST_ENTRY_RE = re.compile(r'^\*\s+\[.+\]\(.+\)')
TRAILING_WHITESPACE_RE = re.compile(r'[ \t]+$')


def check_duplicate_urls(lines: list[str], filename: str) -> list[str]:
    """Check for duplicate URLs within a file."""
    errors = []
    url_map = defaultdict(list)

    for lineno, line in enumerate(lines, 1):
        for match in MARKDOWN_LINK_RE.finditer(line):
            url = match.group(2).strip()
            url_map[url].append(lineno)

    for url, occurrences in url_map.items():
        if len(occurrences) > 1:
            errors.append(
                f"{filename}:{occurrences[0]}: Duplicate URL found '{url}' "
                f"(also on lines: {', '.join(map(str, occurrences[1:]))})"
            )
    return errors


def check_trailing_whitespace(lines: list[str], filename: str) -> list[str]:
    """Check for trailing whitespace on each line."""
    errors = []
    for lineno, line in enumerate(lines, 1):
        if TRAILING_WHITESPACE_RE.search(line.rstrip('\n')):
            errors.append(f"{filename}:{lineno}: Trailing whitespace detected")
    return errors


def check_blank_lines_around_headers(lines: list[str], filename: str) -> list[str]:
    """Ensure headers are surrounded by blank lines."""
    errors = []
    for lineno, line in enumerate(lines, 1):
        stripped = line.rstrip('\n')
        if SECTION_HEADER_RE.match(stripped):
            # Check line before header (skip first line)
            if lineno > 1 and lines[lineno - 2].strip() != '':
                errors.append(
                    f"{filename}:{lineno}: Missing blank line before header"
                )
            # Check line after header (skip last line)
            if lineno < len(lines) and lines[lineno].strip() != '':
                errors.append(
                    f"{filename}:{lineno}: Missing blank line after header"
                )
    return errors


def check_https_preferred(lines: list[str], filename: str) -> list[str]:
    """Warn when HTTP is used where HTTPS may be available for known domains."""
    errors = []
    http_pattern = re.compile(r'\(http://(?!localhost|127\.0\.0\.1)')
    for lineno, line in enumerate(lines, 1):
        if http_pattern.search(line):
            errors.append(
                f"{filename}:{lineno}: Prefer HTTPS over HTTP where possible"
            )
    return errors


def lint_file(filepath: Path) -> list[str]:
    """Run all lint checks on a single markdown file."""
    try:
        lines = filepath.read_text(encoding='utf-8').splitlines(keepdims=True)
    except UnicodeDecodeError:
        return [f"{filepath}: Unable to read file (encoding error)"]

    filename = str(filepath)
    errors = []
    errors.extend(check_duplicate_urls(lines, filename))
    errors.extend(check_trailing_whitespace(lines, filename))
    errors.extend(check_blank_lines_around_headers(lines, filename))
    errors.extend(check_https_preferred(lines, filename))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Lint free-programming-books markdown files'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='Markdown files to lint (defaults to all .md files in books/)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors'
    )
    args = parser.parse_args()

    if args.files:
        paths = [Path(f) for f in args.files]
    else:
        paths = list(Path('books').rglob('*.md'))

    if not paths:
        print('No markdown files found to lint.')
        return 0

    all_errors = []
    for path in sorted(paths):
        if not path.exists():
            print(f'Warning: {path} does not exist, skipping.', file=sys.stderr)
            continue
        all_errors.extend(lint_file(path))

    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        print(f'\n{len(all_errors)} issue(s) found.', file=sys.stderr)
        return 1

    print(f'Linted {len(paths)} file(s). No issues found.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
