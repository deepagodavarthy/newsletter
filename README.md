# The AI Learning Digest

A two-issue static HTML newsletter that gives curious beginners a calm, no-jargon
roadmap from "complete beginner" to "I can build things with AI."

## Issues

| Issue | Title | File |
|-------|-------|------|
| No. 01 | Your First Steps into AI — the big picture & a 6-phase roadmap | [`index.html`](index.html) |
| No. 02 | Study Plan, Resources & Projects — a 12-week plan, curated resources, project ideas & a glossary | [`issue-02.html`](issue-02.html) |

## Viewing locally

No build step or dependencies — it's plain HTML and CSS. Just open the files in a browser:

```bash
# macOS
open index.html
# Windows
start index.html
# Linux
xdg-open index.html
```

Or serve the folder with any static server, e.g.:

```bash
python -m http.server 8000
# then visit http://localhost:8000
```

## Hosting on GitHub Pages

This repo is ready for [GitHub Pages](https://pages.github.com/). To publish it live:

1. Push to GitHub (the `.nojekyll` file tells Pages to serve the HTML as-is).
2. In the repo, go to **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to *Deploy from a branch*,
   pick the branch and the `/ (root)` folder, then **Save**.
4. After a minute, your newsletter will be live at
   `https://<username>.github.io/newsletter/`.

## License

Released under the [MIT License](LICENSE).
