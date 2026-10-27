"""Desktop app: fetches fresh data on start and shows the tracker in its own window."""
import json, os, shutil, sys, threading
import webview
import fetch

HERE = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))  # bundled files
HOME = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "Aion2Tracker")  # user data
URL = os.path.join(HOME, "index.html")


class Api:
    def edit_members(self):
        os.startfile(os.path.join(HOME, "members.txt"))

    def members(self):
        return list(fetch.members())

    def search(self, keyword):
        return fetch.search(keyword) if keyword.strip() else []

    def add(self, name, server):
        rows = [r for r in fetch.members() if r[0].lower() != name.lower()]
        fetch.save_members(rows + [(name, server)])
        self.refresh()

    def remove(self, name):
        fetch.save_members([r for r in fetch.members() if r[0] != name])
        try:
            data = json.load(open("data.json", encoding="utf-8"))
            data["members"].pop(name, None)
            json.dump(data, open("data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        except FileNotFoundError:
            pass
        window.load_url(URL)

    def refresh(self):
        threading.Thread(target=update, daemon=True).start()


def update():
    try:
        fetch.main()
    except Exception as e:
        print("update failed:", e)
    window.load_url(URL)


os.makedirs(HOME, exist_ok=True)
for f in ("index.html", "icon.svg"):  # always ship the latest page
    shutil.copy(os.path.join(HERE, f), HOME)
if not os.path.exists(os.path.join(HOME, "members.txt")):
    shutil.copy(os.path.join(HERE, "members.txt"), HOME)
os.chdir(HOME)  # fetch.py reads members.txt and writes data.json in the current folder

window = webview.create_window("Aion2 Group Tracker", URL, js_api=Api(), width=950, height=650)
webview.start(lambda: Api().refresh(), http_server=True)
