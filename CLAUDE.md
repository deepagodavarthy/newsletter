# The AI Learning Digest — Claude Instructions

## Project overview
A static HTML newsletter for complete beginners learning AI/ML.
Each issue is a single self-contained HTML file styled with inline CSS.

## File naming convention
| File | Issue |
|------|-------|
| `index.html` | Issue No. 01 |
| `issue-02.html` | Issue No. 02 |
| `issue-03.html` | Issue No. 03 |
| … | … |

## Design rules
- All CSS lives in a `<style>` block inside each file — no external stylesheets.
- Use only the CSS variables defined in `:root` (`--ink`, `--accent`, `--paper`, etc.).
- Never introduce new class names or inline styles.
- Every issue must have: `.masthead`, at least one `h3.section`, a `.next` nav block, and a `<footer>`.
- Navigation: each issue links forward to the next and back to the previous.

## Custom slash commands
| Command | What it does |
|---------|-------------|
| `/new-issue [topic]` | Scaffolds the next numbered HTML issue and updates nav links |
| `/validate-html [file]` | Checks links, structure, images, and nav consistency |
| `/preview-issue [file]` | Opens an issue in the default browser |

## Agent script
`agent/newsletter_agent.py` uses the Claude API to generate HTML issues.

```bash
# One-time setup
pip install -r agent/requirements.txt
# Set your key (Windows PowerShell)
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# Modes
python agent/newsletter_agent.py generate "Topic name"
python agent/newsletter_agent.py convert  path/to/notes.md
python agent/newsletter_agent.py expand   path/to/outline.txt
```

## Branch workflow
- `main` is the stable branch — merge into it via pull request.
- Feature branches follow the pattern `feature/<short-description>`.
