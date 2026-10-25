"""Fetch each member's combat power, item level and gear from PLAYNC and append to data.json."""
import datetime, json, re, time, urllib.parse, urllib.request

REGION = "eu"
SEARCH = "https://api-search.plaync.com/aion2global/search/v2/character?keyword={kw}&region={region}&localeInfo=en-US&page=1&size=20"
API = "https://aion2.plaync.com/api/character/{kind}?region={region}&lang=en-US&characterId={cid}&serverId={sid}"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "aion2-group-tracker (small friends group, daily)"})
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


def members(path="members.txt"):
    for line in open(path, encoding="utf-8"):
        if line.strip() and not line.startswith("#"):
            name, server = (p.strip() for p in line.split(","))
            yield name, server


def main():
    try:
        data = json.load(open("data.json", encoding="utf-8"))
    except FileNotFoundError:
        data = {"members": {}}
    today = datetime.date.today().isoformat()
    for name, server in members():
        try:
            c = find(get(SEARCH.format(kw=urllib.parse.quote(name), region=REGION)), name, server)
            if not c:
                print(f"not found: {name} on {server}")
                continue
            # characterId comes back already URL-encoded; pass it through as-is
            ids = dict(region=REGION, cid=c["characterId"], sid=c["serverId"])
            info = get(API.format(kind="info", **ids))
            equip = get(API.format(kind="equipment", **ids))
        except Exception as e:  # one bad member shouldn't stop the rest
            print(f"failed: {name}: {e}")
            continue
        m = data["members"].setdefault(name, {"history": []})
        m.update(server=server, level=c["level"], cp=info["profile"]["combatPower"],
                 il=item_level(info), gear=gear(equip))
        m["history"] = [h for h in m["history"] if h["date"] != today] + [{"date": today, "cp": m["cp"], "il": m["il"]}]
        print(f"{name}: CP {m['cp']}, IL {m['il']}")
        time.sleep(3)  # be polite
    data["updated"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    json.dump(data, open("data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def demo():
    s = {"list": [{"name": "<strong>YasuoMain</strong>16", "serverName": "Tassin"},
                  {"name": "<strong>YasuoMain</strong>", "serverName": "Tassin"}]}
    assert find(s, "YasuoMain", "tassin")["name"].endswith("</strong>")
    assert find(s, "YasuoMain16", "Tassin")["name"].endswith("16")
    assert find(s, "YasuoMain", "Nathara") is None
    assert item_level({"stat": {"statList": [{"type": "X", "value": 1}, {"type": "ItemLevel", "value": 1937}]}}) == 1937


if __name__ == "__main__":
    import sys
    demo() if "--test" in sys.argv else main()
