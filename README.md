# Aion2 Group Tracker

Daily combat power, item level and gear for our legion, ranked by player, with a 7-day gain and trend.

- Profile: your characters and your friends' characters. Inside Premade's Aion 2 page the tracker knows your League account and friends from Premade, so you only pick which Aion 2 characters are yours, once. Those picks are kept by Premade's server (`/aion`) and read by the update every 30 minutes.
- Legion: every player, ranked by their strongest character, with all their characters.
- Classes: a guide page for each of the 8 classes (role, skills in the order to level them, Daevanion picks, the legion’s best gear for it), built from the same build lists as Next upgrade.
- Gear checkup (on each character's Gear tab): empty manastone and Theostone slots, Common manastones and items below max enchant, from each item's own page (read again once a day, or when the item or its enchant changes). Compare shows both characters' manastones and Theostones slot by slot.
- Latest: what each character gained between updates (enchants, new gear, titles, skills, Daevanion nodes), on Legion and on your Profile.
- News: Aion 2's own patch notes and announcements, with a banner when maintenance is coming.
- Timers: the daily and weekly resets, the hourly Shugo Festival and Dimensional Invasion, and the field bosses of your server's map (Verteron or Altgard) with their respawn times. Mark a kill and the legion sees when the boss is back; Premade warns 5 minutes before. Kills are kept by Premade's server (`/aion/boss`).
- Checklist: each of your characters' dailies and weeklies (Nightmare, Transcendence, Conquest, Ascension Trial, Subjugation, and the ones a server's characters share), ticked in Premade and reset with the game (07:00 UTC, weekly on Wednesday), and what your friends still have to do. Ticks are kept by Premade's server (`/aion/ticks`).
- DPS: while Aion 2 is open, Premade's app reads each fight off the game's own Combat Analysis (Ctrl+X) once its numbers stop (battle time, DPS, total damage, target, top 7 skills) and keeps it in Premade's storage (`lpc-aion-fights`). This page sends each one to Premade's server (`/aion/fights`) with the character whose skills it used, and shows the best on each target with friends side by side, the best DPS each day as a chart, and your fights. Premade reads only Aion 2's window, never the game's files or network traffic, so only your own character's numbers: a friend's come from their own Premade.
- What to do next (each character's Overview): Gear next (the top 3 gear steps in the guides' order: a weaker grade replaced, safe enchants to +10, then the Unique +11 to +15 tries with their chance and expected tries, and the expected tries to +15 per item), Next unlock (the next item-level gate and the date at last week's pace) and Checkup (levelled skills off the bar, Common manastones in Unique gear, empty slots, titles, Arcana). The Gear tab has an Arcana panel: the five cards, the 4-piece set and the weakest card.
- Today also has the Spacetime Rift and the Abyss bosses (Watcher Kaira, Nahma, Argo/Kaira/Tamasa), and Tonight's plan: what's about to cap from the live ticket counts, what starts in the next 3 hours, and the week's pace with the Season 1 countdown. Numbers from community guides are marked "unconfirmed" until they're checked in the game. Premade's Aion 2 overlay shows the same tools as panels over the game (written every 30 s as `lpc-aion-prog`, for your strongest character).
- `node check.js` (with `python3 -m http.server 8765` running and Playwright installed) checks those tools.
- Add a legion member (end of Legion, inside Premade): search a member who doesn't use Premade by name and add them; the update reads them every 30 minutes like everyone else. Premade's server keeps them as `+` and the Riot ID of who added them; when the player picks the character on Profile it becomes theirs.
- To add a character by hand, put it in `members.txt` (`Name, Server, Owner's Riot ID`, EU region).
- `python3 fetch.py` pulls fresh data into `data.json` (no installs needed). `python3 fetch.py --test` runs the self-check.
- Open `index.html` through any web server (e.g. `python3 -m http.server`) to view it.
- Phone: open the web page, then "Add to Home Screen".
- On GitHub: Premade's server starts the update workflow every 30 minutes (GitHub's own schedule only runs it every few hours); GitHub Pages serves the page.

Data comes from PLAYNC's public character pages (unofficial, no API key). Keep refreshes to every 30 minutes or slower.
