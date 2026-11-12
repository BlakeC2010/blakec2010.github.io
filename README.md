# Blake Cary — Portfolio Website

This is a fully static portfolio website built with HTML, CSS, JavaScript, and a separate Markdown content file. It is ready for GitHub Pages and does **not** require a framework, API key, account, build service, or external images.

## Start here

- **`website-content.md`** — Your editable website writing. Change any of the paragraphs to sound like you. This is the source of truth for the website's copy.
- **`index.html`** — The built website. Open it in Chrome to preview it.
- **`styles.css`** — Colors, typography, spacing, and responsive layouts.
- **`script.js`** — Scroll reveal effects, progress bar, mobile menu, and project filters.
- **`assets/resume.pdf`** — A PDF exported from your Google Docs resume on November 12, 2026.
- **`assets/favicon.svg`** — A simple BC favicon; no personal photo required.
- **`template.html`** — The HTML design template. Edit this if you want to change the website's structure.
- **`build_site.py`** — Rebuilds `index.html` from the editable content file using Python's standard library.

## How to edit the wording without touching code

1. Open `website-content.md` in VS Code, Notepad, or any Markdown editor.
2. Edit the text below each `###` field heading in your own voice. You can write multiple lines or paragraphs.
3. Leave the `##` section names and `###` field names unchanged; the builder uses them to place the text correctly.
4. Save the file.
5. In the site folder, run:

   ```bash
   python build_site.py
   ```

   If `python` does not work on Windows, try `py build_site.py`.
6. Open or refresh `index.html` in Chrome. Your wording changes now appear on the website.

No `npm install`, package manager, or framework is necessary. You can also directly edit `index.html`, but future rebuilds will replace those edits. Put ongoing text revisions in the Markdown file.

## How to preview

Double-click `index.html` to view it locally. The site works without running a server. You can also use VS Code Live Server if you prefer.

Check it on both desktop and phone after major edits. Scroll to test the section transitions, use the project filters, test the email and GitHub links, and open the resume PDF.

## How to publish to your existing GitHub Pages site

**This package does not automatically update your live website.** Before replacing it, create a backup branch or copy of your existing `BlakeC2010/blakec2010.github.io` repository.

Copy the **contents** of this folder into the *root* of the GitHub Pages repository, preserving these paths:

```
index.html
styles.css
script.js
assets/favicon.svg
assets/resume.pdf
```

Only those five files are required for the published website. For future editable updates, also keep `website-content.md`, `template.html`, `build_site.py`, and `README.md` in your repository (or store those source files locally). Preserve any existing `CNAME` or other hosting configuration if your repository uses it.

Commit and push to your GitHub Pages publishing branch. Confirm the live page and links work after publishing. The site's URL should remain `https://blakec2010.github.io/` if your existing Pages configuration is unchanged.

## Important accuracy and privacy notes

- **Published/public work:** Context Titles and AI Chat Notifications link to public GitHub repositories.
- **Private projects:** Zoro and GitHub Sync are explicitly marked as private and in development. They do not link to private repositories or imply a public release.
- **Certifications:** CompTIA Tech+ is shown as completed, while CompTIA A+ Core 1 & Core 2 coursework is clearly in progress.
- **Goals:** MIT, valedictorian, scholarships, and a technology startup are framed as ambitions, not achievements.
- **Leadership:** The collaboration section is intentionally general; the specific class study-materials story is reserved for interviews.
- **Photos:** None are used or required.
- **Contact:** Only your public email and GitHub are published; the website does not expose your phone number, home address, or any private repository credentials.
- **Resume:** To use a revised resume later, export the updated Google Doc as PDF and overwrite `assets/resume.pdf` before republishing.

## Style notes

The design uses a paper-like off-white background, dark forest-green typography accents, editorial type, subtle illustration panels, and scroll-triggered movement. It's intentionally not a futuristic neon design. To adjust the palette, change the variables at the top of `styles.css`.

The site respects reduced-motion settings and remains usable with keyboard navigation.