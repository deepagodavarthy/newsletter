Create a new numbered HTML issue for "The AI Learning Digest" newsletter.

Topic (if provided): $ARGUMENTS

Steps:
1. Scan the project root for existing issue files to find the next number.
   - index.html = Issue 01
   - issue-02.html = Issue 02, issue-03.html = Issue 03, etc.
2. If no topic was given via $ARGUMENTS, ask: "What topic should Issue No. <N> cover?"
3. Create the new HTML file (issue-<NN>.html) by following the structure and CSS
   classes already used in index.html. Reuse the same :root variables and stylesheet.
   Update: <title>, issue number in the masthead, the date to today, subtitle in
   .issue-line, and all body content sections for the new topic.
4. In the previous issue file, update (or add) the .next nav block so its link
   points to the new file.
5. Add a "Go Back" .next nav block in the new file pointing to the previous issue.
6. Report: which file was created, which file was updated, and the issue title.
