#!/usr/bin/env python3
"""
Deterministic diff -> HTML renderer for the human-review skill.

No AI involved anywhere in this file: it shells out to git, parses unified
diff text, and writes a self-contained HTML page with a placeholder "why"
slot per file. A separate step (an AI, or a human) fills those slots in via
inject_why.py.

Modes:
  current                  uncommitted changes vs HEAD in --repo
  commit <sha>             the diff introduced by a single commit
  range <base>..<head>     diff between two refs (three-dot / merge-base)
  worktree <path>          uncommitted + branch changes in another worktree,
                            diffed against its merge-base with --base

Usage:
  gen_diff.py current [--repo PATH] --out out.html [--json out.json]
  gen_diff.py commit <sha> [--repo PATH] --out out.html [--json out.json]
  gen_diff.py range <base>..<head> [--repo PATH] --out out.html [--json out.json]
  gen_diff.py worktree <path> [--base main] --out out.html [--json out.json]
"""
import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path


def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode not in (0, 1):  # git diff exits 1 when there IS a diff, in some modes
        sys.stderr.write(result.stderr)
        sys.exit(result.returncode)
    return result.stdout


def detect_base(repo):
    for ref in ("main", "master"):
        out = subprocess.run(["git", "rev-parse", "--verify", ref], cwd=repo,
                              capture_output=True, text=True)
        if out.returncode == 0:
            return ref
    return "HEAD"


def untracked_diff(repo):
    """Synthesize added-file diffs for untracked files, without touching the index."""
    status = run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo)
    paths = [line[3:] for line in status.split("\n") if line.startswith("?? ")]
    parts = []
    for path in paths:
        result = subprocess.run(["git", "diff", "--no-index", "--", "/dev/null", path],
                                 cwd=repo, capture_output=True, text=True)
        if result.returncode in (0, 1):
            parts.append(result.stdout)
    return "\n".join(parts)


def commit_log(repo, rev_range):
    out = run(["git", "log", "--format=%H%x1f%s%x1f%b%x1e", rev_range], cwd=repo)
    commits = []
    for rec in out.strip("\x1e\n").split("\x1e"):
        rec = rec.strip("\n")
        if not rec:
            continue
        parts = rec.split("\x1f", 2)
        h, s, b = (parts + ["", "", ""])[:3]
        commits.append({"hash": h[:10], "subject": s, "body": b.strip()})
    return commits


FILE_HEADER_RE = re.compile(r"^diff --git a/(.*) b/(.*)$")


def parse_diff(diff_text):
    """Split unified diff text into per-file records with pre-classified lines."""
    files = []
    current = None

    def flush():
        if current is not None:
            files.append(current)

    for line in diff_text.split("\n"):
        m = FILE_HEADER_RE.match(line)
        if m:
            flush()
            current = {
                "path": m.group(2) if m.group(2) != "/dev/null" else m.group(1),
                "old_path": m.group(1),
                "status": "modified",
                "binary": False,
                "additions": 0,
                "deletions": 0,
                "lines": [],  # (kind, text) kind in hunk/add/del/ctx/meta
            }
            continue
        if current is None:
            continue
        if line.startswith("new file mode"):
            current["status"] = "added"
        elif line.startswith("deleted file mode"):
            current["status"] = "deleted"
        elif line.startswith("rename from"):
            current["status"] = "renamed"
        elif line.startswith("Binary files") and "differ" in line:
            current["binary"] = True
            current["lines"].append(("meta", line))
        elif line.startswith("@@"):
            current["lines"].append(("hunk", line))
        elif line.startswith("+++") or line.startswith("---"):
            continue
        elif line.startswith("+"):
            current["additions"] += 1
            current["lines"].append(("add", line[1:]))
        elif line.startswith("-"):
            current["deletions"] += 1
            current["lines"].append(("del", line[1:]))
        elif line.startswith("\\"):
            current["lines"].append(("meta", line))
        elif line.startswith("index ") or line.startswith("similarity index") \
                or line.startswith("rename to") or line.startswith("old mode") \
                or line.startswith("new mode"):
            continue
        else:
            current["lines"].append(("ctx", line[1:] if line.startswith(" ") else line))
    flush()
    return files


STYLE = """
:root{
  --bg:#ffffff; --fg:#1f2328; --muted:#6e7781; --border:#d0d7de;
  --add-bg:#e6ffec; --add-fg:#116329; --del-bg:#ffebe9; --del-fg:#82071e;
  --hunk-fg:#8250df; --why-bg:#f6f8fa; --code-bg:#ffffff; --link:#0969da;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#0d1117; --fg:#e6edf3; --muted:#8b949e; --border:#30363d;
    --add-bg:#0f3d20; --add-fg:#7ee2a8; --del-bg:#4b1113; --del-fg:#ffb1ae;
    --hunk-fg:#c8a3ff; --why-bg:#161b22; --code-bg:#0d1117; --link:#4493f8;
  }
}
:root[data-theme="dark"]{
  --bg:#0d1117; --fg:#e6edf3; --muted:#8b949e; --border:#30363d;
  --add-bg:#0f3d20; --add-fg:#7ee2a8; --del-bg:#4b1113; --del-fg:#ffb1ae;
  --hunk-fg:#c8a3ff; --why-bg:#161b22; --code-bg:#0d1117; --link:#4493f8;
}
body{background:var(--bg);color:var(--fg);margin:0;font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
.wrap{max-width:1100px;margin:0 auto;padding:24px 16px 64px;}
header h1{font-size:18px;margin:0 0 4px;}
header .meta{color:var(--muted);font-size:13px;margin-bottom:16px;}
.commits{border:1px solid var(--border);border-radius:8px;padding:10px 14px;margin-bottom:20px;font-size:13px;}
.commits h2{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin:0 0 8px;}
.commits ul{margin:0;padding-left:18px;}
.commits code{color:var(--muted);}
.file{border:1px solid var(--border);border-radius:8px;margin-bottom:16px;overflow:hidden;}
.file summary{cursor:pointer;list-style:none;padding:10px 14px;display:flex;gap:10px;align-items:center;font-weight:600;}
.file summary::-webkit-details-marker{display:none;}
.file summary .path{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;}
.file summary .stat{font-weight:400;font-size:12px;color:var(--muted);margin-left:auto;}
.file summary .stat .add{color:var(--add-fg);}
.file summary .stat .del{color:var(--del-fg);}
.badge{font-size:11px;font-weight:600;padding:1px 6px;border-radius:4px;border:1px solid var(--border);color:var(--muted);}
.why{background:var(--why-bg);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:10px 14px;font-size:13px;}
.why .label{font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);margin-right:6px;}
.why-text{white-space:pre-wrap;}
.why-text.pending{color:var(--muted);font-style:italic;}
pre.code{margin:0;background:var(--code-bg);overflow-x:auto;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;}
.line{padding:0 14px;white-space:pre;}
.line.add{background:var(--add-bg);color:var(--add-fg);}
.line.del{background:var(--del-bg);color:var(--del-fg);}
.line.hunk{color:var(--hunk-fg);background:transparent;padding-top:6px;padding-bottom:6px;}
.line.meta{color:var(--muted);font-style:italic;}
.empty{color:var(--muted);font-style:italic;padding:12px 14px;}
"""


def render_file(f):
    status_badge = {"added": "added", "deleted": "deleted", "renamed": "renamed",
                     "modified": "modified"}[f["status"]]
    path = html.escape(f["path"])
    stat = f'<span class="add">+{f["additions"]}</span> <span class="del">-{f["deletions"]}</span>'
    if f["binary"]:
        body = '<div class="empty">Binary file changed.</div>'
    else:
        rows = []
        for kind, text in f["lines"]:
            rows.append(f'<div class="line {kind}">{html.escape(text)}</div>')
        body = f'<pre class="code">{"".join(rows)}</pre>'
    why_id = html.escape(f["path"], quote=True)
    return f"""
<details class="file" open>
  <summary><span class="badge">{status_badge}</span><span class="path">{path}</span><span class="stat">{stat}</span></summary>
  <div class="why"><span class="label">Why</span><span class="why-text pending" data-file="{why_id}">[why-pending]</span></div>
  {body}
</details>"""


def render_html(title, subtitle, commits, files):
    commit_html = ""
    if commits:
        items = "".join(
            f'<li><code>{html.escape(c["hash"])}</code> {html.escape(c["subject"])}</li>'
            for c in commits
        )
        commit_html = f'<div class="commits"><h2>Commits in range</h2><ul>{items}</ul></div>'
    if files:
        files_html = "".join(render_file(f) for f in files)
    else:
        files_html = '<div class="empty">No changes.</div>'
    return f"""<title>{html.escape(title)}</title>
<style>{STYLE}</style>
<div class="wrap">
  <header>
    <h1>{html.escape(title)}</h1>
    <div class="meta">{html.escape(subtitle)}</div>
  </header>
  {commit_html}
  {files_html}
</div>"""


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["current", "commit", "range", "worktree"])
    p.add_argument("target", nargs="?", default=None)
    p.add_argument("--repo", default=".")
    p.add_argument("--base", default=None, help="base ref for worktree mode (default: auto-detect main/master)")
    p.add_argument("--out", required=True, help="path to write the HTML page")
    p.add_argument("--json", dest="json_out", default=None, help="optional path to write structured JSON for the why-writing step")
    args = p.parse_args()

    repo = Path(args.repo).resolve()
    commits = []
    title = ""
    subtitle = ""

    if args.mode == "current":
        diff_text = run(["git", "diff", "HEAD"], cwd=repo) + "\n" + untracked_diff(repo)
        title = "Current changes"
        subtitle = f"Uncommitted diff vs HEAD in {repo} (including untracked files)"
    elif args.mode == "commit":
        if not args.target:
            sys.exit("commit mode requires a commit sha")
        diff_text = run(["git", "show", "--format=", args.target], cwd=repo)
        commits = commit_log(repo, f"{args.target}~1..{args.target}")
        title = f"Commit {args.target}"
        subtitle = commits[0]["subject"] if commits else args.target
    elif args.mode == "range":
        if not args.target or ".." not in args.target:
            sys.exit("range mode requires base..head")
        base, head = re.split(r"\.{2,3}", args.target, maxsplit=1)
        diff_text = run(["git", "diff", f"{base}...{head}"], cwd=repo)
        commits = commit_log(repo, f"{base}..{head}")
        title = f"{base}...{head}"
        subtitle = f"{len(commits)} commit(s) in {repo}"
    elif args.mode == "worktree":
        if not args.target:
            sys.exit("worktree mode requires a path")
        repo = Path(args.target).resolve()
        base = args.base or detect_base(repo)
        diff_text = run(["git", "diff", f"{base}...HEAD"], cwd=repo) + "\n" + untracked_diff(repo)
        commits = commit_log(repo, f"{base}..HEAD")
        title = f"Worktree: {repo.name}"
        subtitle = f"vs {base}, {len(commits)} commit(s), plus any uncommitted/untracked changes"

    files = parse_diff(diff_text)
    page = render_html(title, subtitle, commits, files)

    out_path = Path(args.out)
    out_path.write_text(page)

    if args.json_out:
        payload = {
            "title": title,
            "subtitle": subtitle,
            "commits": commits,
            "files": [
                {
                    "path": f["path"],
                    "status": f["status"],
                    "binary": f["binary"],
                    "additions": f["additions"],
                    "deletions": f["deletions"],
                    "diff": "\n".join(
                        (("+" if k == "add" else "-" if k == "del" else " " if k == "ctx" else "") + t)
                        for k, t in f["lines"]
                    ),
                }
                for f in files
            ],
        }
        Path(args.json_out).write_text(json.dumps(payload, indent=2))

    print(f"Wrote {out_path} ({len(files)} file(s) changed)")


if __name__ == "__main__":
    main()
