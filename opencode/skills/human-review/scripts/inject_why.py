#!/usr/bin/env python3
"""
Splice per-file "why" explanations into an HTML page produced by gen_diff.py.

Deterministic string substitution only — the only place any prose enters is
the why-map JSON supplied by the caller (normally written by the AI after
reading gen_diff.py's --json output).

Usage:
  inject_why.py --html page.html --why why.json [--out page.html]

why.json shape: {"path/to/file.py": "why explanation text", ...}
Paths not present in why.json are left as "[why-pending]".
"""
import argparse
import html
import json
import re
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--html", required=True)
    p.add_argument("--why", required=True)
    p.add_argument("--out", default=None, help="defaults to overwriting --html")
    args = p.parse_args()

    page = Path(args.html).read_text()
    why_map = json.loads(Path(args.why).read_text())

    def replace_one(path, text):
        nonlocal page
        escaped_path = html.escape(path, quote=True)
        pattern = re.compile(
            r'(<span class="why-text)( pending)?(" data-file="' + re.escape(escaped_path) + r'">)'
            r'\[why-pending\](</span>)'
        )
        replacement = r'\1\3' + html.escape(text).replace("\\", r"\\") + r'\4'
        page, n = pattern.subn(replacement, page, count=1)
        return n

    missing = []
    for path, text in why_map.items():
        page_before = page
        n = replace_one(path, text)
        if n == 0:
            missing.append(path)

    out_path = Path(args.out) if args.out else Path(args.html)
    out_path.write_text(page)

    if missing:
        print(f"Warning: no placeholder found for {len(missing)} path(s): {missing}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
