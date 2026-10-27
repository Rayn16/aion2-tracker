# Aion2 Group Tracker

Daily combat power, item level and gear for our legion, ranked by player, with a 7-day gain and trend.

- Profile: your characters and your friends' characters. Inside Premade's Aion 2 page the tracker knows your League account and friends from Premade, so you only pick which Aion 2 characters are yours, once. Those picks are kept by Premade's server (`/aion`) and read by the daily update.
- Legion: every player, ranked by their strongest character, with all their characters.
- To add a character by hand, put it in `members.txt` (`Name, Server, Owner's Riot ID`, EU region).
- `python3 fetch.py` pulls fresh data into `data.json` (no installs needed). `python3 fetch.py --test` runs the self-check.
- Open `index.html` through any web server (e.g. `python3 -m http.server`) to view it.
- Phone: open the web page, then "Add to Home Screen".
- On GitHub: the workflow refreshes data once a day at 06:00 UTC; GitHub Pages serves the page.

Data comes from PLAYNC's public character pages (unofficial, no API key). Keep refreshes to once a day.
