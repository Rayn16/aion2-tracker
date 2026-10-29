"""Fetch each member's combat power, item level and gear from PLAYNC and append to data.json."""
import datetime, json, re, time, urllib.parse, urllib.request

REGION = "eu"
SEARCH = "https://api-search.plaync.com/aion2global/search/v2/character?keyword={kw}&region={region}&localeInfo=en-US&page=1&size=20"
API = "https://aion2.plaync.com/api/character/{kind}?region={region}&lang=en-US&characterId={cid}&serverId={sid}"
ITEM = "https://aion2.plaync.com/api/character/equipment/item?id={id}&enchantLevel={ench}&slotPos={slot}&characterId={cid}&serverId={sid}&lang=en-US&region={region}"
# characters people picked as theirs on the Profile page, kept by Premade's server: [{"n", "s", "o": owner's Riot ID}]
CLAIMS = "https://league-proxchat.league-proxchat-server.workers.dev/aion"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "aion2-group-tracker (small friends group, every 30 min)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def clean(name):
    return re.sub(r"<[^>]+>", "", name)


def find(search, name, server):
    for c in search["list"]:
        if clean(c["name"]).lower() == name.lower() and c["serverName"].lower() == server.lower():
            return c


def item_level(info):
    return next((s["value"] for s in info["stat"]["statList"] if s["type"] == "ItemLevel"), None)


def gear(equip):
    return [{k: g[k] for k in ("slotPosName", "name", "grade", "enchantLevel", "icon")}
            for g in equip["equipment"]["equipmentList"]]


def details(item):
    """What the gear checkup uses from an item's own page: enchant cap, manastones, Theostone and where it drops."""
    return {"max": item.get("maxEnchantLevel"), "slots": item.get("magicStoneSlotCount") or 0,
            "stones": [[s["name"], s["value"], s["grade"]] for s in item.get("magicStoneStat") or []],
            "godSlots": item.get("godStoneSlotCount") or 0, "god": [s.get("name", "") for s in item.get("godStoneStat") or []],
            "src": item.get("sources") or []}


def add_details(new, raw, old, fresh, ids):
    """Each item keeps its details while it and its enchant stay the same; fresh (once a day) reads every item again,
    for manastones and Theostones changed on the same item."""
    was = {g["slotPosName"]: g for g in old}
    for g, r in zip(new, raw):
        o = was.get(g["slotPosName"])
        if not fresh and o and "max" in o and (o["name"], o["enchantLevel"]) == (g["name"], g["enchantLevel"]):
            g.update({k: o[k] for k in ("max", "slots", "stones", "godSlots", "god", "src")})
            continue
        try:
            g.update(details(get(ITEM.format(id=r["id"], ench=r["enchantLevel"], slot=r["slotPos"], **ids))))
            time.sleep(0.5)  # be polite
        except Exception as e:  # the item still shows, without its details
            print(f"item failed: {g['name']}: {e}")


def changes(old, new):
    """What a character gained since the last update, as short lines for the legion feed."""
    out = []
    if new["level"] > old.get("level", new["level"]):
        out.append(f"reached level {new['level']}")
    was = {g["slotPosName"]: g for g in old.get("gear") or []}
    for g in new["gear"]:
        o = was.get(g["slotPosName"])
        if not o or o["name"] != g["name"]:
            out.append(f"new {g['name']} +{g['enchantLevel']}")
        elif o["enchantLevel"] != g["enchantLevel"]:
            out.append(f"{g['name']} +{o['enchantLevel']} → +{g['enchantLevel']}")
    titles = lambda m: (m.get("title") or {}).get("ownedCount") or 0
    if old.get("title") and titles(new) > titles(old):
        n = titles(new) - titles(old)
        out.append(f"{n} new title{'s' if n > 1 else ''}")
    nodes = lambda m: sum(b["openNodeCount"] for b in (m.get("daevanion") or {}).get("boardList") or [])
    if old.get("daevanion") and nodes(new) > nodes(old):
        out.append(f"opened {nodes(new) - nodes(old)} Daevanion nodes")
    levels = lambda m: {s["name"]: s["skillLevel"] for s in (m.get("skill") or {}).get("skillList") or [] if s["acquired"]}
    a = levels(old)
    up = [f"{n} {v}" for n, v in levels(new).items() if a and v > a.get(n, 0)]
    if up:
        out.append("skills up: " + ", ".join(up[:4]) + (f" and {len(up) - 4} more" if len(up) > 4 else ""))
    return out


def board(detail):
    """A Daevanion board as "row|col|grade|open|name" per node; the start node counts as open."""
    return [f"{n['row']}|{n['col']}|{'Start' if n['type'] == 'Start' else n['grade']}|{int(n['open'] or n['type'] == 'Start')}|{n['name']}"
            for n in detail["nodeList"] if n["grade"] != "None" or n["type"] == "Start"]


def members(path="members.txt"):
    """(name, server, owner's Riot ID or "") from members.txt."""
    for line in open(path, encoding="utf-8"):
        if line.strip() and not line.startswith("#"):
            name, server, owner = ([p.strip() for p in line.split(",")] + [""])[:3]
            yield name, server, owner


def roster(claims):
    """members.txt plus the claimed characters; members.txt wins for a character on both."""
    rows = {n.lower(): (n, s, o) for n, s, o in members()}
    for c in claims:
        rows.setdefault(c["n"].lower(), (c["n"], c["s"], c["o"]))
    return list(rows.values())


def main():
    try:
        data = json.load(open("data.json", encoding="utf-8"))
    except FileNotFoundError:
        data = {"members": {}}
    today = datetime.date.today().isoformat()
    try:
        claims = get(CLAIMS)["chars"]
    except Exception as e:  # server down: keep everyone we have, just add no one new
        print(f"claims not read: {e}")
        claims = None
    rows = roster(claims or [])
    if claims is not None:  # a character nobody lists or claims any more leaves the legion
        keep = {n for n, _, _ in rows}
        data["members"] = {n: m for n, m in data["members"].items() if n in keep}
    for name, server, owner in rows:
        try:
            c = find(get(SEARCH.format(kw=urllib.parse.quote(name), region=REGION)), name, server)
            if not c:
                print(f"not found: {name} on {server}")
                continue
            # characterId comes back already URL-encoded; pass it through as-is
            ids = dict(region=REGION, cid=c["characterId"], sid=c["serverId"])
            info = get(API.format(kind="info", **ids))
            equip = get(API.format(kind="equipment", **ids))
            # every node of each open board, for the "next node" advice
            boards = {b["id"]: board(get(API.format(kind="daevanion/detail", **ids) + f"&boardId={b['id']}"))
                      for b in (info.get("daevanion") or {}).get("boardList", []) if b["open"]}
        except Exception as e:  # one bad member shouldn't stop the rest
            print(f"failed: {name}: {e}")
            continue
        m = data["members"].setdefault(name, {"history": []})
        before = dict(m)
        g = gear(equip)
        # the first update of the day reads every item's details again; later ones only items that changed
        add_details(g, equip["equipment"]["equipmentList"], m.get("gear") or [], not any(h["date"] == today for h in m["history"]), ids)
        m.update(server=server, owner=owner, level=c["level"], cp=info["profile"]["combatPower"],
                 il=item_level(info), gear=g, pic=info["profile"].get("profileImage"),
                 # the rest of the character sheet, kept as the game sends it
                 stats=info["stat"]["statList"], title=info.get("title"), ranking=info.get("ranking"),
                 daevanion=info.get("daevanion"), boards=boards, skill=equip.get("skill"), petwing=equip.get("petwing"),
                 pcId=c.get("pcId"), race=c.get("race"))
        m["history"] = [h for h in m["history"] if h["date"] != today] + [{"date": today, "cp": m["cp"], "il": m["il"]}]
        if before.get("gear"):  # newest first; a character's first update has nothing to compare with
            at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
            data["feed"] = [{"t": at, "n": name, "x": x} for x in changes(before, m)] + data.get("feed", [])
        print(f"{name}: CP {m['cp']}, IL {m['il']}")
        time.sleep(3)  # be polite
    data["feed"] = data.get("feed", [])[:300]
    data["updated"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    json.dump(data, open("data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def demo():
    s = {"list": [{"name": "<strong>YasuoMain</strong>16", "serverName": "Tassin"},
                  {"name": "<strong>YasuoMain</strong>", "serverName": "Tassin"}]}
    assert find(s, "YasuoMain", "tassin")["name"].endswith("</strong>")
    assert find(s, "YasuoMain16", "Tassin")["name"].endswith("16")
    assert find(s, "YasuoMain", "Nathara") is None
    nodes = {"nodeList": [{"row": 8, "col": 8, "grade": "None", "type": "Start", "open": 0, "name": "Nezekan - Start"},
                          {"row": 8, "col": 9, "grade": "Common", "type": "Stat", "open": 1, "name": "Attack"},
                          {"row": 1, "col": 1, "grade": "None", "type": "None", "open": 0, "name": ""}]}
    assert board(nodes) == ["8|8|Start|1|Nezekan - Start", "8|9|Common|1|Attack"]
    import os, tempfile
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "members.txt"), "w").write("# x\nA, Tassin\nB, Tassin, Me#EU\n")
        cwd = os.getcwd(); os.chdir(d)
        try:
            assert roster([{"n": "a", "s": "Tassin", "o": "X#1"}, {"n": "C", "s": "Ariel", "o": "Y#2"}]) == \
                [("A", "Tassin", ""), ("B", "Tassin", "Me#EU"), ("C", "Ariel", "Y#2")]
        finally:
            os.chdir(cwd)
    assert item_level({"stat": {"statList": [{"type": "X", "value": 1}, {"type": "ItemLevel", "value": 1937}]}}) == 1937
    d = details({"maxEnchantLevel": 15, "magicStoneSlotCount": 4, "godStoneSlotCount": 1, "sources": ["Expedition"],
                 "magicStoneStat": [{"name": "Attack", "value": "+3", "grade": "Rare", "slotPos": 1}]})
    assert d == {"max": 15, "slots": 4, "stones": [["Attack", "+3", "Rare"]], "godSlots": 1, "god": [], "src": ["Expedition"]}
    sword = {"slotPosName": "MainHand", "name": "Sword", "enchantLevel": 14}
    old, new = [dict(sword, **d)], [dict(sword)]
    add_details(new, [{}], old, False, {})  # same item, same enchant: no request, details kept
    assert new[0]["stones"] == [["Attack", "+3", "Rare"]]
    before = {"level": 44, "gear": [sword], "title": {"ownedCount": 10}, "daevanion": {"boardList": [{"openNodeCount": 5}]},
              "skill": {"skillList": [{"name": "Keen Strike", "skillLevel": 14, "acquired": 1}]}}
    after = {"level": 45, "gear": [dict(sword, enchantLevel=15), {"slotPosName": "Ring1", "name": "Ring", "enchantLevel": 0}],
             "title": {"ownedCount": 11}, "daevanion": {"boardList": [{"openNodeCount": 7}]},
             "skill": {"skillList": [{"name": "Keen Strike", "skillLevel": 15, "acquired": 1}]}}
    assert changes(before, after) == ["reached level 45", "Sword +14 → +15", "new Ring +0", "1 new title",
                                      "opened 2 Daevanion nodes", "skills up: Keen Strike 15"]
    assert changes(after, after) == []


if __name__ == "__main__":
    import sys
    demo() if "--test" in sys.argv else main()
