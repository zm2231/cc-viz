#!/usr/bin/env python3
"""
strip-html.py — Strip a cc-viz HTML artifact to readable markdown text.

Use to fact-check generated pages. Renders the prose, headings, lists, tables,
and code blocks of an HTML output as plain markdown so claims can be grepped,
quoted, and verified against source repos.

Usage:
    python3 strip-html.py <input.html>                 # writes <input>.stripped.md next to it
    python3 strip-html.py <input.html> -o <output.md>  # custom output path
    python3 strip-html.py <input.html> --stdout        # print to stdout instead of writing

Exit codes:
    0 — success
    1 — input not found or unreadable
"""

import argparse
import re
import sys
from pathlib import Path


def html_to_text(html: str) -> str:
    """Strip HTML to readable markdown-ish text.

    Lossy: tables flatten, complex layouts collapse, JS-rendered content is
    invisible. Good enough to grep claims against; not for preserving design.
    """
    # Drop script and style blocks entirely
    html = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Convert structural elements to whitespace / markdown
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</(p|div|li|h[1-6]|tr|section|article|aside|blockquote|figure)>',
                  '\n', html, flags=re.IGNORECASE)

    # Headings → markdown
    html = re.sub(r'<h1[^>]*>', '\n# ', html, flags=re.IGNORECASE)
    html = re.sub(r'<h2[^>]*>', '\n## ', html, flags=re.IGNORECASE)
    html = re.sub(r'<h3[^>]*>', '\n### ', html, flags=re.IGNORECASE)
    html = re.sub(r'<h4[^>]*>', '\n#### ', html, flags=re.IGNORECASE)
    html = re.sub(r'<h5[^>]*>', '\n##### ', html, flags=re.IGNORECASE)
    html = re.sub(r'<h6[^>]*>', '\n###### ', html, flags=re.IGNORECASE)

    # Lists
    html = re.sub(r'<li[^>]*>', '- ', html, flags=re.IGNORECASE)

    # Inline emphasis
    for tag, marker in [('strong', '**'), ('b', '**'), ('em', '*'), ('i', '*'), ('code', '`')]:
        html = re.sub(rf'<{tag}[^>]*>', marker, html, flags=re.IGNORECASE)
        html = re.sub(rf'</{tag}>', marker, html, flags=re.IGNORECASE)

    # Pull quotes / blockquotes — render with > prefix
    html = re.sub(r'<blockquote[^>]*>', '\n> ', html, flags=re.IGNORECASE)

    # Cite tags
    html = re.sub(r'<cite[^>]*>', '— ', html, flags=re.IGNORECASE)

    # Table rows: separate cells with | for grep-ability
    html = re.sub(r'</td>', ' | ', html, flags=re.IGNORECASE)
    html = re.sub(r'</th>', ' | ', html, flags=re.IGNORECASE)

    # Strip remaining tags
    html = re.sub(r'<[^>]+>', '', html)

    # Decode common HTML entities
    entities = [
        ('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'),
        ('&mdash;', '—'), ('&ndash;', '–'), ('&hellip;', '…'),
        ('&#39;', "'"), ('&apos;', "'"), ('&quot;', '"'),
        ('&nbsp;', ' '), ('&copy;', '©'), ('&reg;', '®'),
        ('&laquo;', '«'), ('&raquo;', '»'),
        ('&ldquo;', '"'), ('&rdquo;', '"'),
        ('&lsquo;', "'"), ('&rsquo;', "'"),
    ]
    for entity, replacement in entities:
        html = html.replace(entity, replacement)

    # Collapse whitespace
    html = re.sub(r'\n{3,}', '\n\n', html)
    html = re.sub(r'[ \t]+', ' ', html)
    html = re.sub(r' +\n', '\n', html)
    html = re.sub(r'\n +', '\n', html)

    return html.strip()


def parse_args():
    ap = argparse.ArgumentParser(
        description="Strip a cc-viz HTML artifact to readable markdown text for fact-checking.",
        epilog="Output goes next to input (<input>.stripped.md) by default. Use -o to override or --stdout to print."
    )
    ap.add_argument('input', type=Path, help='HTML file to strip')
    ap.add_argument('-o', '--output', type=Path, default=None,
                    help='Output path (default: <input>.stripped.md)')
    ap.add_argument('--stdout', action='store_true',
                    help='Print stripped output to stdout instead of writing a file')
    return ap.parse_args()


def main():
    args = parse_args()

    if not args.input.exists():
        print(f"error: input not found: {args.input}", file=sys.stderr)
        return 1

    try:
        html = args.input.read_text(encoding='utf-8')
    except Exception as e:
        print(f"error reading {args.input}: {e}", file=sys.stderr)
        return 1

    text = html_to_text(html)

    if args.stdout:
        print(text)
    else:
        out_path = args.output or args.input.with_suffix(args.input.suffix + '.stripped.md')
        out_path.write_text(text, encoding='utf-8')
        print(f"stripped: {out_path} ({len(text):,} chars)", file=sys.stderr)

    return 0


if __name__ == '__main__':
    sys.exit(main())
