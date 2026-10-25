# Aion2 Group Tracker

Daily combat power, item level and gear for our group, ranked, with a 7-day gain and trend.

- Add friends to `members.txt` (`Name, Server`, EU region).
- `python3 fetch.py` pulls fresh data into `data.json` (no installs needed). `python3 fetch.py --test` runs the self-check.
- Open `index.html` through any web server (e.g. `python3 -m http.server`) to view it.
- Windows app: download `Aion2Tracker.exe` from the [latest release](../../releases/latest) and double-click it. It refreshes on start; use "Edit members" to add friends.
- Phone app: open the web page, then "Add to Home Screen".
- On GitHub: the workflow refreshes data once a day; turn on GitHub Pages (Settings → Pages → deploy from branch `main`) to share the page.

Data comes from PLAYNC's public character pages (unofficial, no API key). Keep refreshes to once a day.
