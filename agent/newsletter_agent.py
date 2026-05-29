#!/usr/bin/env python3
"""
Newsletter HTML agent for The AI Learning Digest.
Uses the Claude API to generate styled HTML issues in three modes.

Usage:
  python newsletter_agent.py generate "Understanding Neural Networks"
  python newsletter_agent.py convert  path/to/notes.md
  python newsletter_agent.py expand   path/to/outline.txt

Requires: ANTHROPIC_API_KEY environment variable set.
Install deps: pip install -r requirements.txt
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

import anthropic

REPO_ROOT = Path(__file__).resolve().parent.parent
MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """\
You are a writer for "The AI Learning Digest", a calm, encouraging newsletter for
complete beginners learning AI/ML. You write the HTML body content only — no
<html>, <head>, or <style> tags.

Use only these CSS classes (already defined in the stylesheet):
  .lead, .lead h2, .lead .dek, .dropcap
  h3.section, p
  .concepts, .concept, .concept .tag
  .phase, .phase .num, .phase .skills
  .callout, .callout h3, .callout ol
  .quote
  table, thead, tbody, th, td, td.wk
  .res, .res h4, .res .meta, .free, .paid
  .proj, .projcol, .projcol .lvl
  .gloss, .habits

Do NOT use inline styles or introduce new class names.
Return only the body content HTML, starting with <section class="lead"> and
ending before any navigation or footer block.
Keep the tone jargon-free, warm, and practical."""


def _client() -> anthropic.Anthropic:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Error: ANTHROPIC_API_KEY environment variable is not set.")
    return anthropic.Anthropic(api_key=key)


def _next_issue_number() -> int:
    numbers = [1]
    for f in REPO_ROOT.glob("issue-*.html"):
        m = re.search(r"issue-(\d+)\.html", f.name)
        if m:
            numbers.append(int(m.group(1)))
    return max(numbers) + 1


def _issue_path(n: int) -> Path:
    return REPO_ROOT / ("index.html" if n == 1 else f"issue-{n:02d}.html")


def _css_block() -> str:
    src_file = REPO_ROOT / "index.html"
    if not src_file.exists():
        return ""
    m = re.search(r"<style>(.*?)</style>", src_file.read_text(encoding="utf-8"), re.DOTALL)
    return m.group(0) if m else ""


def _today() -> str:
    d = date.today()
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def _call_claude(client: anthropic.Anthropic, user_prompt: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user_prompt}],
    )
    return response.content[0].text


def _short_subtitle(client: anthropic.Anthropic, hint: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=30,
        messages=[
            {
                "role": "user",
                "content": (
                    "Return only a short subtitle (4-7 words, no punctuation at the end) "
                    f"for a beginner AI newsletter issue about: {hint[:200]}"
                ),
            }
        ],
    )
    return response.content[0].text.strip()


def _wrap_html(issue_num: int, subtitle: str, body_html: str, today: str) -> str:
    css = _css_block()
    prev_num = issue_num - 1
    prev_href = "index.html" if prev_num == 1 else f"issue-{prev_num:02d}.html"
    prev_exists = _issue_path(prev_num).exists() if prev_num >= 1 else False

    nav_back = (
        f'  <div class="next">\n'
        f'    <div>\n'
        f'      <div class="label">Go Back &mdash; Issue No. {prev_num:02d}</div>\n'
        f'      <a href="{prev_href}">&larr; Previous Issue</a>\n'
        f'    </div>\n'
        f'  </div>\n'
    ) if prev_exists else ""

    return (
        f'<!DOCTYPE html>\n'
        f'<html lang="en">\n'
        f'<head>\n'
        f'<meta charset="UTF-8">\n'
        f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<title>The AI Learning Digest — Issue No. {issue_num:02d}</title>\n'
        f'{css}\n'
        f'</head>\n'
        f'<body>\n'
        f'<div class="wrap">\n\n'
        f'  <header class="masthead">\n'
        f'    <div class="kicker">A Newsletter for Curious Beginners</div>\n'
        f'    <h1>The AI Learning Digest</h1>\n'
        f'    <div class="issue-line">\n'
        f'      <span>Issue No. {issue_num:02d}</span>\n'
        f'      <span>{subtitle}</span>\n'
        f'      <span>{today}</span>\n'
        f'    </div>\n'
        f'  </header>\n\n'
        f'{body_html}\n\n'
        f'{nav_back}'
        f'  <footer>\n'
        f'    The AI Learning Digest &middot; Issue No. {issue_num:02d} &middot; Curated for your journey<br>\n'
        f'    Progress &gt; perfection.\n'
        f'  </footer>\n\n'
        f'</div>\n'
        f'</body>\n'
        f'</html>\n'
    )


def _update_prev_issue_next_link(issue_num: int) -> None:
    """Add/update the 'Up Next' nav block in the previous issue."""
    prev_path = _issue_path(issue_num - 1)
    if not prev_path.exists():
        return
    new_href = f"issue-{issue_num:02d}.html"
    content = prev_path.read_text(encoding="utf-8")
    next_block = (
        f'  <div class="next">\n'
        f'    <div>\n'
        f'      <div class="label">Up Next &mdash; Issue No. {issue_num:02d}</div>\n'
        f'      <a href="{new_href}">Continue to Issue {issue_num:02d} &rarr;</a>\n'
        f'    </div>\n'
        f'  </div>'
    )
    # Replace existing .next block if present, else insert before footer
    if 'class="next"' in content:
        content = re.sub(r'<div class="next">.*?</div>\s*</div>', next_block, content, count=1, flags=re.DOTALL)
    else:
        content = content.replace("  <footer>", next_block + "\n\n  <footer>")
    prev_path.write_text(content, encoding="utf-8")
    print(f"Updated:  {prev_path.name}")


def cmd_generate(topic: str) -> None:
    client = _client()
    today = _today()
    issue_num = _next_issue_number()
    print(f"Generating Issue No. {issue_num:02d}: {topic!r} ...")

    body = _call_claude(
        client,
        f"Write Issue No. {issue_num:02d} of The AI Learning Digest on the topic: {topic!r}. "
        "Include: a lead section, 2-3 content sections with h3.section headings, "
        "a callout box with 3-4 concrete action items, and an inspiring quote block.",
    )
    subtitle = _short_subtitle(client, topic)
    html = _wrap_html(issue_num, subtitle, body, today)

    out = _issue_path(issue_num)
    out.write_text(html, encoding="utf-8")
    print(f"Created:  {out.name}")
    _update_prev_issue_next_link(issue_num)


def cmd_convert(input_file: str) -> None:
    client = _client()
    today = _today()
    src = Path(input_file).read_text(encoding="utf-8")
    issue_num = _next_issue_number()
    print(f"Converting {Path(input_file).name} → Issue No. {issue_num:02d} ...")

    body = _call_claude(
        client,
        f"Convert this Markdown content into the HTML body for Issue No. {issue_num:02d} "
        "of The AI Learning Digest. Preserve all facts and structure from the source.\n\n"
        + src,
    )
    subtitle = _short_subtitle(client, src[:300])
    html = _wrap_html(issue_num, subtitle, body, today)

    out = _issue_path(issue_num)
    out.write_text(html, encoding="utf-8")
    print(f"Created:  {out.name}")
    _update_prev_issue_next_link(issue_num)


def cmd_expand(input_file: str) -> None:
    client = _client()
    today = _today()
    src = Path(input_file).read_text(encoding="utf-8")
    issue_num = _next_issue_number()
    print(f"Expanding {Path(input_file).name} → Issue No. {issue_num:02d} ...")

    body = _call_claude(
        client,
        f"Expand this outline into a full HTML body for Issue No. {issue_num:02d} "
        "of The AI Learning Digest. Use the bullet points as a guide; write full "
        "paragraphs, examples, and concrete beginner advice around each point.\n\n"
        + src,
    )
    subtitle = _short_subtitle(client, src[:300])
    html = _wrap_html(issue_num, subtitle, body, today)

    out = _issue_path(issue_num)
    out.write_text(html, encoding="utf-8")
    print(f"Created:  {out.name}")
    _update_prev_issue_next_link(issue_num)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Newsletter HTML agent — generate, convert, or expand issues"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    gen = sub.add_parser("generate", help="Generate a full issue from a topic string")
    gen.add_argument("topic", help='e.g. "Understanding Neural Networks"')

    conv = sub.add_parser("convert", help="Convert a Markdown file into a styled HTML issue")
    conv.add_argument("file", help="Path to .md file")

    exp = sub.add_parser("expand", help="Expand a bullet-point outline into a full HTML issue")
    exp.add_argument("file", help="Path to outline .txt or .md file")

    args = parser.parse_args()

    if args.cmd == "generate":
        cmd_generate(args.topic)
    elif args.cmd == "convert":
        cmd_convert(args.file)
    elif args.cmd == "expand":
        cmd_expand(args.file)


if __name__ == "__main__":
    main()
