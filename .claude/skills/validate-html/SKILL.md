---
name: validate-html
description: Check a newsletter HTML file for broken links, missing sections, and accessibility issues
---

Validate a newsletter HTML file from "The AI Learning Digest" project.

File to check: $ARGUMENTS
(If blank, list the available .html files in the project root and ask the user to pick one.)

Checks to perform:
1. Internal links — every href ending in .html must resolve to an existing file in
   the project root. List any that are broken.
2. Required structure — confirm the file contains:
   - .masthead with .kicker, h1, and .issue-line
   - At least one h3.section heading
   - A .next nav block
   - A <footer>
3. Images — every <img> must have a non-empty alt attribute.
4. Empty anchors — flag any <a href="#"> unless clearly intentional.
5. Navigation consistency — if there is a "previous issue" link, verify the href
   points to the correct prior file.

Report findings grouped as:
  ✅ Passed
  ⚠️  Warnings (should fix)
  ❌ Errors (must fix)

If everything passes, say so clearly.
