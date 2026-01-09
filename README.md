```markdown
# Mettur Dam - automatic daily data update

This repo contains a small static page that displays the Mettur dam water level and a GitHub Actions workflow that fetches the latest water level once per day.

Files
- `index.html` — frontend chart (water-level time series + daily delta bars) and summary.
- `scripts/fetch_mettur.py` — scraper that extracts Mettur level from the Tamil Nadu reservoir status page.
- `data/data.json` — sample starting data (script appends/updates this).
- `.github/workflows/update-data.yml` — GitHub Actions workflow to run the fetch script daily and commit updates to the branch.

Setup & usage
1. Edit the fetch script (optional)
   - Open `scripts/fetch_mettur.py` and confirm `SOURCE_URL` (default: `https://www.tnagrisnet.tn.gov.in/home/reservoir/`).
   - If you want a different source, change `SOURCE_URL`. If the provider requires an API key, update the script and store the key as a GitHub secret; modify the workflow to pass it as an environment variable.

2. Add files to branch `metturdam-patch-1`
   - Use the GitHub web editor or clone locally and push to `metturdam-patch-1`.

3. Test locally (recommended)
   - Install dependencies:
     ```
     pip install requests beautifulsoup4
     ```
   - Run the script:
     ```
     python scripts/fetch_mettur.py
     ```
   - Check `data/data.json` updated.

4. Run the workflow on GitHub
   - Go to Actions → "Update Mettur data" → Run workflow → select branch `metturdam-patch-1`.
   - Check logs and the `data/data.json` commit (if a change was detected).

Notes
- The scraper tries to find the table row containing "Mettur" and extract the numeric value. It will convert feet to meters when obvious. If the official page is client-side rendered (JS), the simple scraper may fail — in that case we can switch to a JSON API (if available) or use a headless browser in the workflow.
- The chart (`index.html`) expects `data/data.json` to be an array of objects: `[{ "date": "YYYY-MM-DD", "level": <meters> }, ...]`.
- The workflow commits changes to `metturdam-patch-1`. If that branch is protected, allow Actions to write or adjust branch protection.

If you want me to:
- Create the branch and push these files for you, say "Please push now" and confirm the repo URL and that I should push to `metturdam-patch-1`.
- Or I can walk you through pasting these files into GitHub web UI — tell me which file you'd like to paste first.
```
