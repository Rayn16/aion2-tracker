# Aion2 Group Tracker

Daily combat power, item level and gear for our legion, ranked by player, with a 7-day gain and trend.

- Profile: your characters and your friends' characters. Inside Premade's Aion 2 page the tracker knows your League account and friends from Premade, so you only pick which Aion 2 characters are yours, once. Those picks are kept by Premade's server (`/aion`) and read by the update every 30 minutes.
- Legion: every player, ranked by their strongest character, with all their characters.
- Classes: a guide page for each of the 8 classes (role, skills in the order to level them, Daevanion picks, the legion’s best gear for it), built from the same build lists as Next upgrade.
- Gear checkup (on each character's Gear tab): empty manastone and Theostone slots, Common manastones and items below max enchant, from each item's own page (read again once a day, or when the item or its enchant changes).
- Latest: what each character gained between updates (enchants, new gear, titles, skills, Daevanion nodes), on Legion and on your Profile.
- News: Aion 2's own patch notes and announcements, with a banner when maintenance is coming.
- To add a character by hand, put it in `members.txt` (`Name, Server, Owner's Riot ID`, EU region).
- `python3 fetch.py` pulls fresh data into `data.json` (no installs needed). `python3 fetch.py --test` runs the self-check.
- Open `index.html` through any web server (e.g. `python3 -m http.server`) to view it.
- Phone: open the web page, then "Add to Home Screen".
- On GitHub: the workflow refreshes data every 30 minutes; GitHub Pages serves the page.

Data comes from PLAYNC's public character pages (unofficial, no API key). Keep refreshes to every 30 minutes or slower.
