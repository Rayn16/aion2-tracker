# Aion2 Group Tracker

Daily combat power, item level and gear for our legion, ranked by player, with a 7-day gain and trend.

- Profile: your characters and your friends' characters. Inside Premade's Aion 2 page the tracker knows your League account and friends from Premade, so you only pick which Aion 2 characters are yours, once. Those picks are kept by Premade's server (`/aion`) and read by the update every 30 minutes.
- Legion: every player, ranked by their strongest character, with all their characters.
- Classes: a guide page for each of the 8 classes (role, skills in the order to level them, Daevanion picks, the legion’s best gear for it), built from the same build lists as Next upgrade.
- Gear checkup (on each character's Gear tab): empty manastone and Theostone slots, Common manastones and items below max enchant, from each item's own page (read again once a day, or when the item or its enchant changes). Compare shows both characters' manastones and Theostones slot by slot.
- Latest: what each character gained between updates (enchants, new gear, titles, skills, Daevanion nodes), on Legion and on your Profile.
- News: Aion 2's own patch notes and announcements, with a banner when maintenance is coming.
- Timers: the daily and weekly resets, the hourly Shugo Festival and Dimensional Invasion, and the field bosses of your server's map (Verteron or Altgard) with their respawn times. Mark a kill and the legion sees when the boss is back. Alerts: each of field bosses, Shugo Festival, Dimensional Invasion and the daily reset with its own lead time (off to 15 minutes), plus an optional chime and spoken line (ideas from the Abyss DPS Meter analysis, without its traffic reading). Kills are kept by Premade's server (`/aion/boss`).
- Checklist: each of your characters' dailies and weeklies (Nightmare, Transcendence, Conquest, Ascension Trial, Subjugation, and the ones a server's characters share), ticked in Premade and reset with the game (07:00 UTC, weekly on Wednesday), and what your friends still have to do. Ticks are kept by Premade's server (`/aion/ticks`).
- DPS: while Aion 2 is open, Premade's app reads each fight off the game's own Combat Analysis (Ctrl+X) once its numbers stop (battle time, DPS, total damage, target, top 7 skills) and keeps it in Premade's storage (`lpc-aion-fights`). This page sends each one to Premade's server (`/aion/fights`) with the character whose skills it used, and shows the best on each target with friends side by side, the best DPS each day as a chart, party fights (friends' fights on the same target saved within 3 minutes of each other, with each one's share of the damage), and your fights. Premade reads only Aion 2's window, never the game's files or network traffic, so only your own character's numbers: a friend's come from their own Premade.
- To add a character by hand, put it in `members.txt` (`Name, Server, Owner's Riot ID`, EU region).
- `python3 fetch.py` pulls fresh data into `data.json` (no installs needed). `python3 fetch.py --test` runs the self-check.
- Open `index.html` through any web server (e.g. `python3 -m http.server`) to view it.
- Phone: open the web page, then "Add to Home Screen".
- On GitHub: Premade's server starts the update workflow every 30 minutes (GitHub's own schedule only runs it every few hours); GitHub Pages serves the page.

Data comes from PLAYNC's public character pages (unofficial, no API key). Keep refreshes to every 30 minutes or slower.
