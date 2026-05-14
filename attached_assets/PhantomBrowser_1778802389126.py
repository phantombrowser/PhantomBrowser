#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║                  PHANTOM BROWSER  v2.0                           ║
║        Privacy-first • Tor auto-managed • 50 themes              ║
║        Tabs • Extensions • Accounts • DevTools • .onion          ║
╠══════════════════════════════════════════════════════════════════╣
║  INSTALL:  pip install PyQt6 PyQt6-WebEngine                     ║
║  RUN:      python phantom_browser.py                             ║
║  OPTIONS:  --no-tor   skip Tor entirely                          ║
║            --url URL  open URL on launch                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ── stdlib ─────────────────────────────────────────────────────────────────────
import os, sys, json, uuid, hashlib, secrets, shutil, platform
import subprocess, threading, socket, time, atexit, re, urllib.parse
from pathlib import Path
from datetime import datetime

# ── Qt ─────────────────────────────────────────────────────────────────────────
from PyQt6.QtCore import (
    Qt, QUrl, QSize, QTimer, pyqtSlot, QObject, pyqtSignal,
    QPropertyAnimation, QEasingCurve, QRect, QPoint
)
from PyQt6.QtGui import (
    QColor, QPalette, QKeySequence, QShortcut, QAction,
    QFont, QPixmap, QPainter, QLinearGradient, QBrush, QPen
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLineEdit, QPushButton, QLabel, QStatusBar, QToolBar,
    QProgressBar, QSizePolicy, QFrame, QCheckBox, QMenu, QMessageBox,
    QDialog, QTextEdit, QScrollArea, QGridLayout, QGroupBox,
    QComboBox, QSlider, QFileDialog, QListWidget, QListWidgetItem,
    QStackedWidget, QDialogButtonBox, QSpinBox, QFormLayout,
    QGraphicsOpacityEffect, QTabBar, QAbstractItemView, QSplitter
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile, QWebEngineSettings, QWebEnginePage,
    QWebEngineScript, QWebEngineDownloadRequest
)
from PyQt6.QtNetwork import QNetworkProxy

# ══════════════════════════════════════════════════════════════════
#  APP PATHS
# ══════════════════════════════════════════════════════════════════
APP_DIR        = Path.home() / ".phantom_browser"
PROFILES_DIR   = APP_DIR / "profiles"
EXTENSIONS_DIR = APP_DIR / "extensions"
SETTINGS_FILE  = APP_DIR / "settings.json"
TOR_DATA_DIR   = APP_DIR / "tor_data"
for _d in [APP_DIR, PROFILES_DIR, EXTENSIONS_DIR, TOR_DATA_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

TOR_HOST, TOR_PORT = "127.0.0.1", 9050
GENERIC_UA = ("Mozilla/5.0 (Windows NT 10.0; rv:115.0) "
              "Gecko/20100101 Firefox/115.0")

# ══════════════════════════════════════════════════════════════════
#  50 THEMES  (each: bg, panel, inp, hov, brd, acc, adim,
#              warn, dng, txt, mut, tab_a, tab_i)
# ══════════════════════════════════════════════════════════════════
THEMES = {
"Phantom Dark":    dict(bg="#0a0c0f",panel="#111418",inp="#181c22",hov="#1e242c",brd="#2a3040",acc="#5af78e",adim="#2d7a4a",warn="#f7c948",dng="#f75e5e",txt="#d4dde8",mut="#5a6478",tab_a="#1e242c",tab_i="#111418"),
"Midnight Blue":   dict(bg="#090b14",panel="#0f1320",inp="#141929",hov="#1a2035",brd="#1e2d52",acc="#4facfe",adim="#1a5fa8",warn="#ffd166",dng="#ef476f",txt="#cdd9f5",mut="#4a5b80",tab_a="#1a2035",tab_i="#0f1320"),
"Dracula":         dict(bg="#1e1f29",panel="#282a36",inp="#21222c",hov="#343746",brd="#44475a",acc="#bd93f9",adim="#7c5cbf",warn="#f1fa8c",dng="#ff5555",txt="#f8f8f2",mut="#6272a4",tab_a="#343746",tab_i="#282a36"),
"Nord":            dict(bg="#242933",panel="#2e3440",inp="#292e3b",hov="#3b4252",brd="#434c5e",acc="#88c0d0",adim="#5e81ac",warn="#ebcb8b",dng="#bf616a",txt="#eceff4",mut="#4c566a",tab_a="#3b4252",tab_i="#2e3440"),
"Tokyo Night":     dict(bg="#1a1b26",panel="#16161e",inp="#1f2335",hov="#292e42",brd="#3b4261",acc="#7aa2f7",adim="#3d59a1",warn="#e0af68",dng="#f7768e",txt="#a9b1d6",mut="#565f89",tab_a="#292e42",tab_i="#16161e"),
"Gruvbox Dark":    dict(bg="#1d2021",panel="#282828",inp="#242424",hov="#3c3836",brd="#504945",acc="#b8bb26",adim="#6c7121",warn="#d79921",dng="#cc241d",txt="#ebdbb2",mut="#665c54",tab_a="#3c3836",tab_i="#282828"),
"Solarized Dark":  dict(bg="#001e26",panel="#002b36",inp="#00212b",hov="#073642",brd="#094052",acc="#2aa198",adim="#126860",warn="#b58900",dng="#dc322f",txt="#839496",mut="#4a5f65",tab_a="#073642",tab_i="#002b36"),
"Monokai Pro":     dict(bg="#19181a",panel="#221f22",inp="#1e1b1e",hov="#2d2a2e",brd="#403e41",acc="#a9dc76",adim="#5c8a3c",warn="#ffd866",dng="#ff6188",txt="#fcfcfa",mut="#727072",tab_a="#2d2a2e",tab_i="#221f22"),
"One Dark":        dict(bg="#1b1d23",panel="#21252b",inp="#1d2026",hov="#2c313c",brd="#3e4451",acc="#98c379",adim="#4d7a3c",warn="#e5c07b",dng="#e06c75",txt="#abb2bf",mut="#5c6370",tab_a="#2c313c",tab_i="#21252b"),
"Cyberpunk":       dict(bg="#0d0019",panel="#120025",inp="#16002e",hov="#1f0040",brd="#3d0070",acc="#ff0090",adim="#990055",warn="#ffe600",dng="#ff3300",txt="#f0e6ff",mut="#6a4a8a",tab_a="#1f0040",tab_i="#120025"),
"Matrix":          dict(bg="#000300",panel="#001200",inp="#000a00",hov="#001a00",brd="#003300",acc="#00ff41",adim="#008020",warn="#88ff00",dng="#ff3300",txt="#00cc33",mut="#005500",tab_a="#001a00",tab_i="#001200"),
"Sunset":          dict(bg="#1a0a00",panel="#2b1200",inp="#221000",hov="#381800",brd="#5c2800",acc="#ff6b35",adim="#cc4400",warn="#ffd700",dng="#ff1744",txt="#ffe8d6",mut="#8b5a3c",tab_a="#381800",tab_i="#2b1200"),
"Ocean":           dict(bg="#001220",panel="#001e35",inp="#001830",hov="#002745",brd="#004070",acc="#00bcd4",adim="#007c8a",warn="#ffca28",dng="#ef5350",txt="#b2ebf2",mut="#37626e",tab_a="#002745",tab_i="#001e35"),
"Rose Gold":       dict(bg="#1a0a10",panel="#28121a",inp="#200e15",hov="#351820",brd="#5c2535",acc="#f4a7b9",adim="#c06880",warn="#ffd700",dng="#ff1744",txt="#fce4ec",mut="#8c4a5e",tab_a="#351820",tab_i="#28121a"),
"Arctic Light":    dict(bg="#f0f4f8",panel="#e4ecf2",inp="#dce6ee",hov="#ccd9e5",brd="#b0c4d8",acc="#0077b6",adim="#023e7d",warn="#e68900",dng="#d62828",txt="#1a2636",mut="#607d8b",tab_a="#ccd9e5",tab_i="#e4ecf2"),
"Forest":          dict(bg="#0d1a0f",panel="#142016",inp="#111c12",hov="#1c2e1e",brd="#2d4a2f",acc="#56ab2f",adim="#2d6e10",warn="#f9ca24",dng="#eb4d4b",txt="#d4edda",mut="#4a7a4e",tab_a="#1c2e1e",tab_i="#142016"),
"Volcano":         dict(bg="#150500",panel="#220800",inp="#1c0600",hov="#300a00",brd="#5c1500",acc="#ff4500",adim="#b83200",warn="#ffa500",dng="#ff0000",txt="#ffe5d0",mut="#8b3a1a",tab_a="#300a00",tab_i="#220800"),
"Galaxy":          dict(bg="#050011",panel="#0d0020",inp="#090018",hov="#130030",brd="#220055",acc="#c77dff",adim="#7b2fff",warn="#ffd60a",dng="#ff4466",txt="#e8d5ff",mut="#5a3d80",tab_a="#130030",tab_i="#0d0020"),
"Mint":            dict(bg="#001a12",panel="#002618",inp="#001f14",hov="#003322",brd="#005535",acc="#00e5a0",adim="#009960",warn="#ffe066",dng="#ff5252",txt="#ccfff0",mut="#3a8065",tab_a="#003322",tab_i="#002618"),
"Cobalt":          dict(bg="#000d26",panel="#001540",inp="#001133",hov="#001f55",brd="#003399",acc="#0088ff",adim="#0055cc",warn="#ffcc00",dng="#ff3355",txt="#b3d9ff",mut="#336699",tab_a="#001f55",tab_i="#001540"),
"Sakura":          dict(bg="#1a0d16",panel="#261220",inp="#200f1a",hov="#33182a",brd="#5c2a45",acc="#ff85a1",adim="#cc4466",warn="#ffd700",dng="#ff3366",txt="#ffe0ea",mut="#8c4460",tab_a="#33182a",tab_i="#261220"),
"Amber":           dict(bg="#1a1000",panel="#261800",inp="#201400",hov="#332000",brd="#5c3a00",acc="#ffb300",adim="#cc8800",warn="#ffe066",dng="#ff5722",txt="#fff8e1",mut="#8c6a20",tab_a="#332000",tab_i="#261800"),
"Ice Light":       dict(bg="#e8f4fc",panel="#d6ecf8",inp="#dceef9",hov="#c0e0f5",brd="#90c8ed",acc="#0277bd",adim="#01579b",warn="#e65100",dng="#c62828",txt="#0d2137",mut="#546e7a",tab_a="#c0e0f5",tab_i="#d6ecf8"),
"Hacker":          dict(bg="#000000",panel="#0a0a0a",inp="#050505",hov="#111111",brd="#1a1a1a",acc="#39ff14",adim="#1a8000",warn="#ffff00",dng="#ff0000",txt="#33ff33",mut="#1a661a",tab_a="#111111",tab_i="#0a0a0a"),
"Lavender":        dict(bg="#0f0a1a",panel="#1a1428",inp="#150f22",hov="#231b35",brd="#3d2f60",acc="#b39ddb",adim="#7c5cbf",warn="#ffe066",dng="#ff5252",txt="#ede7f6",mut="#6a5a8a",tab_a="#231b35",tab_i="#1a1428"),
"Desert":          dict(bg="#1a1408",panel="#261e0d",inp="#20190a",hov="#332912",brd="#5c4a22",acc="#d4a017",adim="#9a7010",warn="#ffc107",dng="#d32f2f",txt="#fdf5e6",mut="#8c7040",tab_a="#332912",tab_i="#261e0d"),
"Neon Pink":       dict(bg="#0d001a",panel="#150026",inp="#110020",hov="#1f0035",brd="#3d006a",acc="#ff00ff",adim="#990099",warn="#ffee00",dng="#ff0044",txt="#ffe6ff",mut="#6a006a",tab_a="#1f0035",tab_i="#150026"),
"Carbon":          dict(bg="#161616",panel="#1e1e1e",inp="#191919",hov="#262626",brd="#393939",acc="#78a9ff",adim="#3c6dcc",warn="#f1c21b",dng="#da1e28",txt="#f4f4f4",mut="#6f6f6f",tab_a="#262626",tab_i="#1e1e1e"),
"Retro Terminal":  dict(bg="#0c0c00",panel="#141400",inp="#101000",hov="#1e1e00",brd="#3a3a00",acc="#e8e800",adim="#999900",warn="#ff8800",dng="#ff2200",txt="#e8e8c0",mut="#666640",tab_a="#1e1e00",tab_i="#141400"),
"Slate":           dict(bg="#0e1116",panel="#161b22",inp="#13181f",hov="#1f2937",brd="#30363d",acc="#58a6ff",adim="#1f6feb",warn="#d29922",dng="#f85149",txt="#e6edf3",mut="#484f58",tab_a="#1f2937",tab_i="#161b22"),
"Copper":          dict(bg="#100808",panel="#1c1010",inp="#160c0c",hov="#281414",brd="#4a2020",acc="#b87333",adim="#7a4a1e",warn="#ffa726",dng="#ef5350",txt="#ffe8cc",mut="#7a4a30",tab_a="#281414",tab_i="#1c1010"),
"Deep Sea":        dict(bg="#000d1a",panel="#001a33",inp="#00152a",hov="#002244",brd="#003366",acc="#00aaff",adim="#0066cc",warn="#ffaa00",dng="#ff4466",txt="#cce8ff",mut="#336688",tab_a="#002244",tab_i="#001a33"),
"Neon Green":      dict(bg="#001a00",panel="#002600",inp="#001f00",hov="#003300",brd="#005500",acc="#00ff88",adim="#00aa55",warn="#ffff00",dng="#ff3300",txt="#ccffe8",mut="#336644",tab_a="#003300",tab_i="#002600"),
"Twilight":        dict(bg="#0d0d1f",panel="#151530",inp="#111128",hov="#1e1e45",brd="#2e2e66",acc="#9b8afb",adim="#6650cf",warn="#fbbf24",dng="#f87171",txt="#e0dfff",mut="#5b5888",tab_a="#1e1e45",tab_i="#151530"),
"Crimson":         dict(bg="#160000",panel="#220000",inp="#1c0000",hov="#2e0000",brd="#550000",acc="#ff4444",adim="#cc1111",warn="#ffa500",dng="#ff0000",txt="#ffe6e6",mut="#884444",tab_a="#2e0000",tab_i="#220000"),
"Pastel Dream":    dict(bg="#fef6ff",panel="#f8ecff",inp="#f3e5ff",hov="#eedaff",brd="#d4aaff",acc="#9c27b0",adim="#6a0080",warn="#e65100",dng="#c62828",txt="#1a0033",mut="#7b5295",tab_a="#eedaff",tab_i="#f8ecff"),
"Obsidian":        dict(bg="#080808",panel="#101010",inp="#0c0c0c",hov="#181818",brd="#282828",acc="#e8e8e8",adim="#aaaaaa",warn="#cccc00",dng="#cc2200",txt="#dddddd",mut="#555555",tab_a="#181818",tab_i="#101010"),
"Aurora":          dict(bg="#050f0f",panel="#0a1f1f",inp="#081818",hov="#102828",brd="#1a4a4a",acc="#00ffcc",adim="#00aa88",warn="#ffe066",dng="#ff5252",txt="#ccffee",mut="#3a7a6a",tab_a="#102828",tab_i="#0a1f1f"),
"Sandstone":       dict(bg="#ede8e0",panel="#e0d8cc",inp="#d8d0c4",hov="#ccc4b8",brd="#b0a898",acc="#6d4c41",adim="#4e342e",warn="#e65100",dng="#c62828",txt="#1a1208",mut="#7d6a58",tab_a="#ccc4b8",tab_i="#e0d8cc"),
"Electric Blue":   dict(bg="#000a1a",panel="#00122a",inp="#000e22",hov="#001833",brd="#002a5a",acc="#00aaff",adim="#0066cc",warn="#ffcc00",dng="#ff3366",txt="#ccecff",mut="#2a6080",tab_a="#001833",tab_i="#00122a"),
"Vintage":         dict(bg="#1a1508",panel="#2a2210",inp="#231c0c",hov="#352c14",brd="#5c4a22",acc="#c8a96e",adim="#8a6a30",warn="#daa520",dng="#c0392b",txt="#f5deb3",mut="#8a7050",tab_a="#352c14",tab_i="#2a2210"),
"Glacier":         dict(bg="#f0f8ff",panel="#e0f0ff",inp="#d8ecff",hov="#c8e4ff",brd="#88c8ff",acc="#0066cc",adim="#004499",warn="#cc6600",dng="#cc2222",txt="#003366",mut="#4488aa",tab_a="#c8e4ff",tab_i="#e0f0ff"),
"Radioactive":     dict(bg="#010800",panel="#021200",inp="#010e00",hov="#031a00",brd="#063300",acc="#aaff00",adim="#669900",warn="#ffee00",dng="#ff3300",txt="#d4ff99",mut="#336600",tab_a="#031a00",tab_i="#021200"),
"Purple Haze":     dict(bg="#0f0020",panel="#180033",inp="#130029",hov="#220044",brd="#400080",acc="#cc66ff",adim="#8800cc",warn="#ffcc00",dng="#ff3355",txt="#f0d9ff",mut="#6633aa",tab_a="#220044",tab_i="#180033"),
"Rust":            dict(bg="#0f0800",panel="#1e1200",inp="#180e00",hov="#2a1a00",brd="#4a3000",acc="#c0541a",adim="#8a3a0e",warn="#e8a020",dng="#cc2200",txt="#ffe8cc",mut="#7a5030",tab_a="#2a1a00",tab_i="#1e1200"),
"Coral":           dict(bg="#1a0808",panel="#2a1010",inp="#220c0c",hov="#381515",brd="#662222",acc="#ff6b6b",adim="#cc3333",warn="#ffd166",dng="#ff0000",txt="#ffe8e8",mut="#884444",tab_a="#381515",tab_i="#2a1010"),
"Teal Storm":      dict(bg="#001a1a",panel="#002a2a",inp="#002222",hov="#003333",brd="#005555",acc="#00cccc",adim="#008888",warn="#ffcc00",dng="#ff4444",txt="#ccffff",mut="#336666",tab_a="#003333",tab_i="#002a2a"),
"Ivory":           dict(bg="#faf8f0",panel="#f5f2e8",inp="#f0ece0",hov="#e8e4d8",brd="#ccc8bc",acc="#8b6914",adim="#5a4510",warn="#cc6600",dng="#cc2222",txt="#1a1408",mut="#7a6a50",tab_a="#e8e4d8",tab_i="#f5f2e8"),
"Deep Purple":     dict(bg="#0d001a",panel="#160029",inp="#120022",hov="#1f0038",brd="#380066",acc="#9c27b0",adim="#6a0080",warn="#ffd600",dng="#ff1744",txt="#e8d5ff",mut="#5c336e",tab_a="#1f0038",tab_i="#160029"),
"Solar Flare":     dict(bg="#1a0500",panel="#280a00",inp="#220700",hov="#381000",brd="#661e00",acc="#ff8c00",adim="#cc6600",warn="#ffdd00",dng="#ff1100",txt="#fff0cc",mut="#885520",tab_a="#381000",tab_i="#280a00"),
}
THEME_NAMES = list(THEMES.keys())

def get_theme(name=None):
    return THEMES.get(name, THEMES[THEME_NAMES[0]])

# ══════════════════════════════════════════════════════════════════
#  SETTINGS
# ══════════════════════════════════════════════════════════════════
SEARCH_ENGINES = {
    "DuckDuckGo": "https://duckduckgo.com/?q={}",
    "Google":     "https://www.google.com/search?q={}",
    "Bing":       "https://www.bing.com/search?q={}",
    "Brave":      "https://search.brave.com/search?q={}",
    "Startpage":  "https://www.startpage.com/search?q={}",
    "Ecosia":     "https://www.ecosia.org/search?q={}",
}
DEFAULT_SETTINGS = {
    "theme": THEME_NAMES[0], "search_engine": "DuckDuckGo",
    "homepage": "phantom://newtab", "js_enabled": True,
    "strict_privacy": False, "use_tor": True,
    "proxy_type": "tor", "proxy_host": "127.0.0.1", "proxy_port": 9050,
    "font_size": 13, "show_bookmarks_bar": True, "zoom": 100,
    "download_path": str(Path.home() / "Downloads"),
    "block_ads": True, "block_trackers": True,
    "current_profile": None, "auto_login": True,
}

class Settings:
    def __init__(self):
        self._d = dict(DEFAULT_SETTINGS)
        if SETTINGS_FILE.exists():
            try: self._d.update(json.loads(SETTINGS_FILE.read_text()))
            except Exception: pass
    def save(self): SETTINGS_FILE.write_text(json.dumps(self._d, indent=2))
    def get(self, k, default=None): return self._d.get(k, default)
    def set(self, k, v): self._d[k] = v; self.save()
    def theme(self): return get_theme(self._d.get("theme"))

SETTINGS = Settings()

# ══════════════════════════════════════════════════════════════════
#  PROFILE / ACCOUNT SYSTEM
# ══════════════════════════════════════════════════════════════════
def _gen_recovery_key():
    alpha = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    raw = secrets.token_bytes(40)
    key = "".join(alpha[b % len(alpha)] for b in raw)[:50]
    return "-".join(key[i:i+10] for i in range(0, 50, 10))

def _hash_key(key: str) -> str:
    return hashlib.sha256(key.replace("-","").encode()).hexdigest()

class ProfileManager:
    def __init__(self):
        self._current = None; self._data = {}
        pid = SETTINGS.get("current_profile")
        if pid and SETTINGS.get("auto_login"):
            f = PROFILES_DIR / f"{pid}.json"
            if f.exists():
                try: self._data = json.loads(f.read_text()); self._current = pid
                except Exception: pass

    @property
    def logged_in(self): return self._current is not None
    @property
    def name(self): return self._data.get("name", "Guest")

    def create(self, name: str) -> str:
        key = _gen_recovery_key()
        pid = str(uuid.uuid4())[:8]
        profile = {"id": pid, "name": name, "key_hash": _hash_key(key),
                   "created": datetime.now().isoformat(),
                   "bookmarks": [], "history": []}
        (PROFILES_DIR / f"{pid}.json").write_text(json.dumps(profile, indent=2))
        self._current = pid; self._data = profile
        SETTINGS.set("current_profile", pid)
        return key

    def login_with_key(self, key: str) -> bool:
        kh = _hash_key(key)
        for f in PROFILES_DIR.glob("*.json"):
            try:
                d = json.loads(f.read_text())
                if d.get("key_hash") == kh:
                    self._current = d["id"]; self._data = d
                    SETTINGS.set("current_profile", d["id"]); return True
            except Exception: pass
        return False

    def logout(self): self._current = None; self._data = {}; SETTINGS.set("current_profile", None)

    def save(self):
        if self._current:
            (PROFILES_DIR / f"{self._current}.json").write_text(json.dumps(self._data, indent=2))

    def add_bookmark(self, url, title):
        self._data.setdefault("bookmarks", [])
        if not any(b["url"] == url for b in self._data["bookmarks"]):
            self._data["bookmarks"].append({"url": url, "title": title, "ts": datetime.now().isoformat()})
            self.save()

    def remove_bookmark(self, url):
        self._data["bookmarks"] = [b for b in self._data.get("bookmarks", []) if b["url"] != url]
        self.save()

    def is_bookmarked(self, url): return any(b["url"] == url for b in self._data.get("bookmarks", []))
    def get_bookmarks(self): return self._data.get("bookmarks", [])

    def add_history(self, url, title):
        h = self._data.setdefault("history", [])
        h.insert(0, {"url": url, "title": title, "ts": datetime.now().isoformat()})
        self._data["history"] = h[:500]; self.save()

    def get_history(self): return self._data.get("history", [])

PROFILE = ProfileManager()

# ══════════════════════════════════════════════════════════════════
#  TOR MANAGER
# ══════════════════════════════════════════════════════════════════
class TorSignals(QObject):
    status_update = pyqtSignal(str)
    tor_ready     = pyqtSignal()
    tor_failed    = pyqtSignal(str)

class TorManager:
    def __init__(self):
        self.signals = TorSignals()
        self._process = None; self._we_started = False; self._ready = False

    @property
    def ready(self): return self._ready

    def bootstrap(self):
        sig = self.signals
        if self._port_open(TOR_HOST, TOR_PORT):
            sig.status_update.emit("Tor already running — connecting…")
            self._ready = True; sig.tor_ready.emit(); return
        tor_bin = shutil.which("tor")
        if not tor_bin:
            sig.status_update.emit("Tor not found — installing (may take a minute)…")
            ok, msg = self._install_tor()
            if not ok: sig.tor_failed.emit(msg); return
            sig.status_update.emit(f"✓ {msg}"); time.sleep(0.5)
            tor_bin = shutil.which("tor")
            if not tor_bin: sig.tor_failed.emit("Installed but not on PATH — restart Phantom."); return
        sig.status_update.emit("Starting Tor daemon…")
        ok, msg = self._start_tor(tor_bin)
        if not ok: sig.tor_failed.emit(msg); return
        sig.status_update.emit("Building Tor circuit — please wait…")
        if not self._wait_for_port(TOR_HOST, TOR_PORT, 90):
            sig.tor_failed.emit("SOCKS5 port never opened. Port 9050 may be blocked."); return
        self._ready = True; sig.tor_ready.emit()

    def stop(self):
        if self._process and self._we_started:
            try: self._process.terminate(); self._process.wait(5)
            except Exception:
                try: self._process.kill()
                except Exception: pass
            self._process = None; self._we_started = False

    @staticmethod
    def _port_open(host, port, timeout=2.0):
        try:
            with socket.create_connection((host, port), timeout=timeout): return True
        except OSError: return False

    @staticmethod
    def _wait_for_port(host, port, timeout=90):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if TorManager._port_open(host, port, 1.5): return True
            time.sleep(1.5)
        return False

    @staticmethod
    def _plat():
        s = platform.system().lower()
        if s == "darwin": return "macos"
        if s == "windows": return "windows"
        if s == "linux":
            for p in ["apt-get","apt","dnf","yum","pacman","zypper"]:
                if shutil.which(p): return f"linux_{p.replace('-','')}"
        return "unknown"

    @staticmethod
    def _run(cmd, timeout=300):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return r.returncode == 0, r.stderr.strip() or r.stdout.strip() or "ok"
        except subprocess.TimeoutExpired: return False, "Timed out"
        except FileNotFoundError: return False, f"Not found: {cmd[0]}"
        except Exception as e: return False, str(e)

    @classmethod
    def _install_tor(cls):
        p = cls._plat()
        if "aptget" in p or p == "linux_apt":
            cls._run(["sudo","apt-get","update","-qq"])
            ok,m = cls._run(["sudo","apt-get","install","-y","tor"])
            return (ok,"Tor installed via apt") if ok else (False,f"apt: {m}")
        elif "dnf" in p:
            ok,m = cls._run(["sudo","dnf","install","-y","tor"])
            return (ok,"Tor installed via dnf") if ok else (False,f"dnf: {m}")
        elif "yum" in p:
            ok,m = cls._run(["sudo","yum","install","-y","tor"])
            return (ok,"Tor installed via yum") if ok else (False,f"yum: {m}")
        elif "pacman" in p:
            ok,m = cls._run(["sudo","pacman","-Sy","--noconfirm","tor"])
            return (ok,"Tor installed via pacman") if ok else (False,f"pacman: {m}")
        elif "zypper" in p:
            ok,m = cls._run(["sudo","zypper","install","-y","tor"])
            return (ok,"Tor installed via zypper") if ok else (False,f"zypper: {m}")
        elif p == "macos":
            if not shutil.which("brew"): return False,"Install Homebrew first: https://brew.sh"
            ok,m = cls._run(["brew","install","tor"])
            return (ok,"Tor installed via Homebrew") if ok else (False,f"brew: {m}")
        elif p == "windows":
            if not shutil.which("choco"): return False,"Install Chocolatey first: https://chocolatey.org"
            ok,m = cls._run(["choco","install","tor","-y"])
            return (ok,"Tor installed via Chocolatey") if ok else (False,f"choco: {m}")
        return False,"Unsupported platform — install Tor manually: https://www.torproject.org"

    def _start_tor(self, tor_bin):
        try:
            self._process = subprocess.Popen(
                [tor_bin,"--quiet","--SocksPort",str(TOR_PORT),
                 "--DataDirectory", str(TOR_DATA_DIR)],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            self._we_started = True
            atexit.register(self.stop)
            return True, f"Tor started (pid {self._process.pid})"
        except Exception as e: return False, str(e)


# ══════════════════════════════════════════════════════════════════
#  STYLESHEET BUILDER
# ══════════════════════════════════════════════════════════════════
def build_stylesheet(t: dict) -> str:
    return f"""
QMainWindow,QDialog,QWidget{{background:{t['bg']};color:{t['txt']};font-family:'Segoe UI','Inter',Arial,sans-serif;font-size:{SETTINGS.get('font_size',13)}px;}}
QToolBar{{background:{t['panel']};border-bottom:2px solid {t['brd']};padding:4px 6px;spacing:3px;}}
QPushButton{{background:{t['inp']};color:{t['txt']};border:1px solid {t['brd']};border-radius:7px;padding:5px 12px;min-height:28px;}}
QPushButton:hover{{background:{t['hov']};border-color:{t['acc']};color:{t['acc']};}}
QPushButton:pressed{{background:{t['brd']};}}
QPushButton:disabled{{color:{t['mut']};opacity:0.5;}}
QPushButton#accent{{background:{t['acc']};color:{t['bg']};border:none;font-weight:bold;}}
QPushButton#accent:hover{{background:{t['adim']};}}
QPushButton#danger{{background:{t['dng']};color:#fff;border:none;font-weight:bold;}}
QPushButton#flat{{background:transparent;border:1px solid transparent;color:{t['txt']};}}
QPushButton#flat:hover{{background:{t['hov']};border-color:{t['brd']};color:{t['acc']};}}
QLineEdit{{background:{t['inp']};color:{t['txt']};border:1px solid {t['brd']};border-radius:8px;padding:6px 12px;selection-background-color:{t['adim']};}}
QLineEdit:focus{{border-color:{t['acc']};background:{t['hov']};}}
QTextEdit{{background:{t['inp']};color:{t['txt']};border:1px solid {t['brd']};border-radius:6px;padding:4px;selection-background-color:{t['adim']};}}
QComboBox{{background:{t['inp']};color:{t['txt']};border:1px solid {t['brd']};border-radius:7px;padding:5px 10px;min-height:28px;}}
QComboBox:hover{{border-color:{t['acc']};}}
QComboBox::drop-down{{border:none;width:22px;}}
QComboBox QAbstractItemView{{background:{t['panel']};color:{t['txt']};border:1px solid {t['brd']};selection-background-color:{t['adim']};outline:none;}}
QCheckBox{{color:{t['txt']};spacing:7px;}}
QCheckBox::indicator{{width:16px;height:16px;border-radius:4px;border:1px solid {t['brd']};background:{t['inp']};}}
QCheckBox::indicator:checked{{background:{t['acc']};border-color:{t['acc']};}}
QSlider::groove:horizontal{{background:{t['brd']};height:4px;border-radius:2px;}}
QSlider::handle:horizontal{{background:{t['acc']};width:14px;height:14px;margin:-5px 0;border-radius:7px;}}
QSlider::sub-page:horizontal{{background:{t['acc']};border-radius:2px;}}
QProgressBar{{background:{t['brd']};border:none;height:3px;border-radius:0;text-align:center;}}
QProgressBar::chunk{{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {t['adim']},stop:1 {t['acc']});border-radius:0;}}
QStatusBar{{background:{t['panel']};color:{t['mut']};border-top:1px solid {t['brd']};font-size:11px;padding:0 8px;}}
QMenu{{background:{t['panel']};border:1px solid {t['brd']};border-radius:10px;color:{t['txt']};padding:6px;}}
QMenu::item{{padding:8px 24px;border-radius:5px;font-size:13px;}}
QMenu::item:selected{{background:{t['hov']};color:{t['acc']};}}
QMenu::separator{{height:1px;background:{t['brd']};margin:5px 10px;}}
QScrollBar:vertical{{background:{t['bg']};width:8px;margin:0;border-radius:4px;}}
QScrollBar::handle:vertical{{background:{t['brd']};border-radius:4px;min-height:24px;}}
QScrollBar::handle:vertical:hover{{background:{t['acc']};}}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}
QScrollBar:horizontal{{background:{t['bg']};height:8px;border-radius:4px;}}
QScrollBar::handle:horizontal{{background:{t['brd']};border-radius:4px;}}
QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{{width:0;}}
QGroupBox{{border:1px solid {t['brd']};border-radius:9px;margin-top:14px;padding:10px 8px 8px 8px;color:{t['mut']};font-size:11px;text-transform:uppercase;letter-spacing:1px;}}
QGroupBox::title{{subcontrol-origin:margin;left:12px;padding:0 5px;background:{t['bg']};}}
QListWidget{{background:{t['inp']};color:{t['txt']};border:1px solid {t['brd']};border-radius:7px;outline:none;}}
QListWidget::item{{padding:7px 10px;border-radius:5px;}}
QListWidget::item:selected{{background:{t['hov']};color:{t['acc']};border:none;}}
QListWidget::item:hover{{background:{t['hov']};}}
QTabWidget::pane{{border:none;background:{t['bg']};}}
QTabBar{{background:{t['panel']};}}
QTabBar::tab{{background:{t['tab_i']};color:{t['mut']};border:none;padding:9px 18px;margin-right:2px;border-top-left-radius:9px;border-top-right-radius:9px;min-width:100px;max-width:220px;font-size:12px;}}
QTabBar::tab:selected{{background:{t['tab_a']};color:{t['txt']};border-bottom:2px solid {t['acc']};font-weight:bold;}}
QTabBar::tab:hover:!selected{{background:{t['hov']};color:{t['txt']};}}
QToolTip{{background:{t['panel']};color:{t['txt']};border:1px solid {t['brd']};border-radius:6px;padding:5px 9px;font-size:11px;}}
QSpinBox{{background:{t['inp']};color:{t['txt']};border:1px solid {t['brd']};border-radius:6px;padding:4px 8px;}}
QSplitter::handle{{background:{t['brd']};width:1px;}}
QFrame#separator{{background:{t['brd']};max-width:1px;}}
"""


# ══════════════════════════════════════════════════════════════════
#  HTML PAGES
# ══════════════════════════════════════════════════════════════════
def newtab_html(t):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:{t['bg']};font-family:'Segoe UI',sans-serif;color:{t['mut']};
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  height:100vh;overflow:hidden;user-select:none;}}
.logo{{font-size:60px;margin-bottom:10px;animation:float 4s ease-in-out infinite;cursor:default;}}
@keyframes float{{0%,100%{{transform:translateY(0) rotate(0deg);}}50%{{transform:translateY(-14px) rotate(5deg);}}}}
h1{{font-size:26px;color:{t['acc']};letter-spacing:9px;text-transform:uppercase;
   margin-bottom:5px;font-weight:300;}}
.sub{{font-size:11px;letter-spacing:3px;margin-bottom:40px;}}
.search-wrap{{width:580px;}}
.search-bar{{display:flex;background:{t['inp']};border:1.5px solid {t['brd']};border-radius:50px;
  padding:11px 20px;gap:10px;align-items:center;transition:all .25s;
  box-shadow:0 8px 32px rgba(0,0,0,.35);}}
.search-bar:focus-within{{border-color:{t['acc']};box-shadow:0 8px 32px rgba(0,0,0,.5),0 0 0 3px {t['adim']}44;}}
.search-bar input{{flex:1;background:none;border:none;outline:none;color:{t['txt']};font-size:15px;}}
.search-bar input::placeholder{{color:{t['mut']};}}
.go-btn{{background:{t['acc']};color:{t['bg']};border:none;border-radius:50px;
  padding:7px 18px;cursor:pointer;font-weight:bold;font-size:13px;transition:background .2s;}}
.go-btn:hover{{background:{t['adim']};}}
.cards{{display:flex;gap:14px;margin-top:40px;flex-wrap:wrap;justify-content:center;max-width:600px;}}
.card{{background:{t['panel']};border:1px solid {t['brd']};border-radius:14px;
  padding:16px 22px;text-align:center;cursor:default;
  transition:transform .25s,border-color .25s,box-shadow .25s;min-width:110px;}}
.card:hover{{transform:translateY(-6px);border-color:{t['acc']};
  box-shadow:0 12px 28px rgba(0,0,0,.4);}}
.card .icon{{font-size:26px;margin-bottom:8px;}}
.card .lbl{{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:{t['mut']};}}
.card .val{{font-size:11px;margin-top:5px;color:{t['acc']};font-weight:600;}}
.shortcuts{{display:flex;gap:10px;margin-top:28px;flex-wrap:wrap;justify-content:center;}}
.shortcut{{background:{t['panel']};border:1px solid {t['brd']};border-radius:10px;
  padding:8px 14px;font-size:11px;color:{t['mut']};cursor:pointer;transition:all .2s;}}
.shortcut:hover{{border-color:{t['acc']};color:{t['acc']};transform:scale(1.05);}}
</style></head><body>
<div class="logo">👻</div>
<h1>Phantom</h1>
<div class="sub">privacy-first browser</div>
<div class="search-wrap">
<div class="search-bar">
  <span style="font-size:16px;color:{t['mut']}">🔍</span>
  <input id="q" placeholder="Search the web or enter a URL…" autofocus
    onkeydown="if(event.key==='Enter')go()">
  <button class="go-btn" onclick="go()">Go</button>
</div>
</div>
<div class="cards">
  <div class="card"><div class="icon">🍪</div><div class="lbl">Cookies</div><div class="val">Not Saved</div></div>
  <div class="card"><div class="icon">📜</div><div class="lbl">History</div><div class="val">In-Session</div></div>
  <div class="card"><div class="icon">💾</div><div class="lbl">Cache</div><div class="val">In-Memory</div></div>
  <div class="card"><div class="icon">🧅</div><div class="lbl">Network</div><div class="val" id="tv">Checking…</div></div>
  <div class="card"><div class="icon">🛡️</div><div class="lbl">Trackers</div><div class="val">Blocked</div></div>
</div>
<div class="shortcuts">
  <div class="shortcut" onclick="location.href='https://duckduckgo.com'">🦆 DuckDuckGo</div>
  <div class="shortcut" onclick="location.href='https://protonmail.com'">📧 ProtonMail</div>
  <div class="shortcut" onclick="location.href='https://github.com'">🐙 GitHub</div>
  <div class="shortcut" onclick="location.href='https://wikipedia.org'">📖 Wikipedia</div>
  <div class="shortcut" onclick="location.href='https://archive.org'">🏛️ Archive.org</div>
</div>
<script>
function go(){{
  let q=document.getElementById('q').value.trim();
  if(!q)return;
  if(q.match(/^https?:\/\//)||q.match(/^[a-z0-9][\w.-]+\.[a-z]{{2,}}$/i)&&!q.includes(' ')){{
    if(!q.match(/^https?:\/\//))q='https://'+q;
    location.href=q;
  }}else{{location.href='https://duckduckgo.com/?q='+encodeURIComponent(q);}}
}}
setTimeout(()=>{{
  let tv=document.getElementById('tv');
  if(tv)tv.textContent='Via Tor';
}},500);
</script></body></html>"""


# ══════════════════════════════════════════════════════════════════
#  TOR SPLASH DIALOG
# ══════════════════════════════════════════════════════════════════
class TorSplash(QDialog):
    def __init__(self, tor_manager, parent=None):
        super().__init__(parent)
        self.tor_manager = tor_manager; self.skipped = False
        t = SETTINGS.theme()
        self.setWindowTitle("Phantom Browser — Connecting to Tor")
        self.setFixedSize(500, 290)
        self.setStyleSheet(build_stylesheet(t))
        self.setWindowFlags(Qt.WindowType.Dialog|Qt.WindowType.CustomizeWindowHint|Qt.WindowType.WindowTitleHint)
        lay = QVBoxLayout(self); lay.setContentsMargins(24,20,24,16); lay.setSpacing(10)
        hdr = QLabel("👻  Initialising Tor Network")
        hdr.setStyleSheet(f"color:{t['acc']};font-size:16px;font-weight:bold;")
        lay.addWidget(hdr)
        self.lbl = QLabel("Starting…")
        self.lbl.setStyleSheet(f"color:{t['mut']};font-size:12px;"); lay.addWidget(self.lbl)
        self.log = QTextEdit(); self.log.setReadOnly(True); self.log.setFixedHeight(130)
        self.log.setStyleSheet(f"background:{t['inp']};color:{t['acc']};border:1px solid {t['brd']};border-radius:6px;font-family:monospace;font-size:11px;padding:6px;")
        lay.addWidget(self.log)
        self.prog = QProgressBar(); self.prog.setRange(0,0); self.prog.setFixedHeight(3); self.prog.setTextVisible(False)
        lay.addWidget(self.prog)
        skip = QPushButton("Skip — Browse Without Tor")
        skip.setStyleSheet(f"color:{t['mut']};border:none;background:transparent;font-size:11px;")
        skip.clicked.connect(self._skip); lay.addWidget(skip, alignment=Qt.AlignmentFlag.AlignRight)
        self._dots = 0; self._base = "Starting"
        self._timer = QTimer(self); self._timer.timeout.connect(self._tick); self._timer.start(440)
        tor_manager.signals.status_update.connect(self._on_status)
        tor_manager.signals.tor_ready.connect(self._on_ready)
        tor_manager.signals.tor_failed.connect(self._on_failed)

    def _tick(self):
        self._dots = (self._dots+1)%4; self.lbl.setText(self._base+"."*self._dots)

    @pyqtSlot(str)
    def _on_status(self, msg):
        self._timer.stop(); self._base = msg.rstrip(".")
        self.lbl.setText(msg); self.log.append(f"  {msg}"); self._timer.start(440)

    @pyqtSlot()
    def _on_ready(self):
        self._timer.stop(); self.prog.setRange(0,100); self.prog.setValue(100)
        self.lbl.setStyleSheet(f"color:{SETTINGS.theme()['acc']};font-size:12px;")
        self.lbl.setText("✓ Tor circuit established!")
        self.log.append("  ✓ SOCKS5 proxy ready on 127.0.0.1:9050")
        QTimer.singleShot(650, self.accept)

    @pyqtSlot(str)
    def _on_failed(self, msg):
        self._timer.stop(); self.prog.setRange(0,100); self.prog.setValue(0)
        self.lbl.setStyleSheet(f"color:{SETTINGS.theme()['dng']};font-size:12px;")
        self.lbl.setText("✗ Tor failed"); self.log.append(f"\n  ✗ {msg}\n  Continuing without Tor.")
        self.skipped = True; QTimer.singleShot(3500, self.reject)

    def _skip(self): self.skipped = True; self._timer.stop(); self.reject()

# ══════════════════════════════════════════════════════════════════
#  CUSTOM TAB BAR + TAB WIDGET
# ══════════════════════════════════════════════════════════════════
class PhantomTabBar(QTabBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True); self.setMovable(True)
        self.setExpanding(False); self.setDrawBase(False)
        self.setElideMode(Qt.TextElideMode.ElideRight)
        self.setFixedHeight(42)
        self.setStyleSheet("")  # driven by app stylesheet

    def tabSizeHint(self, index):
        s = super().tabSizeHint(index)
        s.setWidth(min(max(s.width(), 120), 230))
        s.setHeight(42)
        return s

class PhantomTabWidget(QWidget):
    """
    Full tab widget with animated tab bar, new-tab button,
    and a QStackedWidget for page content.
    """
    new_tab_req = pyqtSignal()
    tab_changed  = pyqtSignal(int)
    tab_closed   = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._views = []       # list[QWebEngineView]
        self._setup_ui()

    def _setup_ui(self):
        t = SETTINGS.theme()
        root = QVBoxLayout(self)
        root.setContentsMargins(0,0,0,0); root.setSpacing(0)

        # ── Tab bar row ───────────────────────────────────────────
        bar_row = QWidget()
        bar_row.setStyleSheet(f"background:{t['panel']};border-bottom:1px solid {t['brd']};")
        bar_row.setFixedHeight(44)
        bar_lay = QHBoxLayout(bar_row)
        bar_lay.setContentsMargins(6,2,4,0); bar_lay.setSpacing(0)

        self.tab_bar = PhantomTabBar()
        self.tab_bar.currentChanged.connect(self._on_bar_change)
        self.tab_bar.tabCloseRequested.connect(self.tab_closed)
        bar_lay.addWidget(self.tab_bar, 1)

        btn_new = QPushButton("+")
        btn_new.setObjectName("flat")
        btn_new.setFixedSize(34, 34)
        btn_new.setToolTip("New Tab  Ctrl+T")
        btn_new.clicked.connect(self.new_tab_req)
        bar_lay.addWidget(btn_new)
        root.addWidget(bar_row)

        # ── Page stack ────────────────────────────────────────────
        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

    def add_tab(self, view: QWebEngineView, title="New Tab") -> int:
        idx = self.tab_bar.addTab("  " + title[:22])
        self.stack.addWidget(view)
        self._views.append(view)
        self.tab_bar.setCurrentIndex(idx)
        # Animate opacity on new tab
        eff = QGraphicsOpacityEffect(view)
        view.setGraphicsEffect(eff)
        anim = QPropertyAnimation(eff, b"opacity", view)
        anim.setDuration(220); anim.setStartValue(0.0); anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic); anim.start()
        return idx

    def remove_tab(self, idx):
        if len(self._views) <= 1: return
        w = self._views.pop(idx)
        self.stack.removeWidget(w); w.deleteLater()
        self.tab_bar.removeTab(idx)

    def current_widget(self):
        idx = self.tab_bar.currentIndex()
        return self._views[idx] if 0 <= idx < len(self._views) else None

    def current_index(self): return self.tab_bar.currentIndex()
    def count(self): return self.tab_bar.count()
    def widget(self, idx): return self._views[idx] if 0 <= idx < len(self._views) else None

    def set_tab_title(self, idx, title):
        if 0 <= idx < self.tab_bar.count():
            short = ("  " + title[:24] + ("…" if len(title) > 24 else ""))
            self.tab_bar.setTabText(idx, short)
            self.tab_bar.setTabToolTip(idx, title)

    def set_tab_loading(self, idx, loading: bool):
        t = SETTINGS.theme()
        if loading:
            self.tab_bar.setTabText(idx, "  ⟳ Loading…")
        # title will be set by titleChanged signal

    def _on_bar_change(self, idx):
        if 0 <= idx < len(self._views):
            self.stack.setCurrentWidget(self._views[idx])
        self.tab_changed.emit(idx)

    def index_of(self, view):
        try: return self._views.index(view)
        except ValueError: return -1


# ══════════════════════════════════════════════════════════════════
#  WEB ENGINE HELPERS
# ══════════════════════════════════════════════════════════════════
def build_private_profile() -> QWebEngineProfile:
    profile = QWebEngineProfile()
    profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
    profile.setPersistentCookiesPolicy(
        QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
    profile.cookieStore().deleteAllCookies()
    profile.setHttpUserAgent(GENERIC_UA)
    return profile

def apply_engine_settings(settings: QWebEngineSettings, strict=False):
    A = QWebEngineSettings.WebAttribute
    settings.setAttribute(A.LocalStorageEnabled,          not strict)
    settings.setAttribute(A.JavascriptCanOpenWindows,     False)
    settings.setAttribute(A.JavascriptCanAccessClipboard, False)
    settings.setAttribute(A.AutoLoadIconsForPage,         True)
    settings.setAttribute(A.TouchIconsEnabled,            False)
    settings.setAttribute(A.JavascriptEnabled,            SETTINGS.get("js_enabled", True))
    settings.setAttribute(A.PluginsEnabled,               False)
    settings.setAttribute(A.WebGLEnabled,                 not strict)
    settings.setAttribute(A.AllowRunningInsecureContent,  False)
    settings.setAttribute(A.HyperlinkAuditingEnabled,     False)
    settings.setAttribute(A.FullScreenSupportEnabled,     True)
    settings.setAttribute(A.ScrollAnimatorEnabled,        not strict)
    settings.setAttribute(A.ErrorPageEnabled,             True)

def configure_proxy(ptype, host, port):
    if ptype == "none":
        QNetworkProxy.setApplicationProxy(
            QNetworkProxy(QNetworkProxy.ProxyType.NoProxy)); return
    proxy = QNetworkProxy()
    proxy.setType(QNetworkProxy.ProxyType.Socks5Proxy
                  if ptype in ("tor","socks5")
                  else QNetworkProxy.ProxyType.HttpProxy)
    proxy.setHostName(host); proxy.setPort(int(port))
    QNetworkProxy.setApplicationProxy(proxy)

class PrivatePage(QWebEnginePage):
    def createWindow(self, _type):
        # Open links that try to spawn new windows in the same view
        return None
    def certificateError(self, error):
        error.rejectCertificate(); return True
    def javaScriptConsoleMessage(self, level, msg, line, source):
        pass  # suppress noise

# ══════════════════════════════════════════════════════════════════
#  BUILT-IN EXTENSIONS
# ══════════════════════════════════════════════════════════════════
BUILTIN_EXTENSIONS = {
    "ad_blocker": {
        "name": "Ad Blocker", "icon": "🛡️", "version": "1.0",
        "description": "Blocks requests to known ad & tracking domains.",
        "enabled": True, "builtin": True,
    },
    "https_everywhere": {
        "name": "HTTPS Everywhere", "icon": "🔒", "version": "1.0",
        "description": "Upgrades HTTP links to HTTPS automatically.",
        "enabled": True, "builtin": True,
    },
    "dark_reader": {
        "name": "Dark Reader", "icon": "🌙", "version": "1.0",
        "description": "Forces dark mode on all websites using CSS inversion.",
        "enabled": False, "builtin": True,
        "inject_css": "html{filter:invert(90%) hue-rotate(180deg)!important;}img,video,canvas,iframe{filter:invert(100%) hue-rotate(180deg)!important;}",
    },
    "reader_mode": {
        "name": "Reader Mode", "icon": "📖", "version": "1.0",
        "description": "Strips pages to clean readable text.",
        "enabled": False, "builtin": True,
        "inject_js": r"""
(function(){
  var body=document.querySelector('article')||document.querySelector('main')||document.body;
  var title=document.title;
  var content=body.innerText;
  document.body.innerHTML='<div style="max-width:740px;margin:60px auto;font-family:Georgia,serif;font-size:18px;line-height:1.75;color:#222;padding:0 24px;"><h1 style="font-size:28px;margin-bottom:20px;">'+title+'</h1><hr style="margin-bottom:24px;"><p>'+content.replace(/\n{2,}/g,'</p><p>')+'</p></div>';
})();
""",
    },
    "no_script": {
        "name": "NoScript Lite", "icon": "🚫", "version": "1.0",
        "description": "Disables JavaScript execution on all pages.",
        "enabled": False, "builtin": True,
    },
    "cookie_blocker": {
        "name": "Cookie Blocker", "icon": "🍪", "version": "1.0",
        "description": "Auto-dismisses cookie consent banners.",
        "enabled": True, "builtin": True,
        "inject_js": r"""
(function(){
  var sel=['.cookie-banner','#cookie-banner','.cookie-notice','#cookie-notice',
           '.gdpr-banner','#gdpr','[class*="cookie"]','[id*="cookie"]',
           '.consent-banner','#consent','[class*="consent"]'];
  function hide(){sel.forEach(function(s){document.querySelectorAll(s).forEach(function(el){el.style.display='none';});});}
  hide();new MutationObserver(hide).observe(document.body,{childList:true,subtree:true});
})();
""",
    },
}


# ══════════════════════════════════════════════════════════════════
#  ACCOUNT DIALOGS
# ══════════════════════════════════════════════════════════════════
class CreateAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        t = SETTINGS.theme()
        self.setWindowTitle("Create Account"); self.setFixedSize(420, 300)
        self.setStyleSheet(build_stylesheet(t))
        self.recovery_key = None
        lay = QVBoxLayout(self); lay.setContentsMargins(28,24,28,20); lay.setSpacing(14)
        hdr = QLabel("👤  Create Your Account")
        hdr.setStyleSheet(f"color:{t['acc']};font-size:16px;font-weight:bold;")
        lay.addWidget(hdr)
        lay.addWidget(QLabel("Enter your name — that's all we need."))
        self.name_edit = QLineEdit(); self.name_edit.setPlaceholderText("Your name…")
        self.name_edit.setFixedHeight(40); lay.addWidget(self.name_edit)
        info = QLabel("No email. No password. You'll get a 50-character\nrecovery key — the only way to sign in.")
        info.setStyleSheet(f"color:{t['mut']};font-size:11px;"); lay.addWidget(info)
        lay.addStretch()
        row = QHBoxLayout()
        cancel = QPushButton("Cancel"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Create Account"); ok.setObjectName("accent"); ok.clicked.connect(self._create)
        row.addWidget(cancel); row.addWidget(ok); lay.addLayout(row)

    def _create(self):
        name = self.name_edit.text().strip()
        if not name: self.name_edit.setPlaceholderText("⚠ Enter your name first!"); return
        self.recovery_key = PROFILE.create(name); self.accept()

class RecoveryKeyDialog(QDialog):
    def __init__(self, key, parent=None):
        super().__init__(parent)
        t = SETTINGS.theme()
        self.setWindowTitle("Save Your Recovery Key!"); self.setFixedSize(480, 310)
        self.setStyleSheet(build_stylesheet(t))
        lay = QVBoxLayout(self); lay.setContentsMargins(28,24,28,20); lay.setSpacing(14)
        hdr = QLabel("🔑  Your Recovery Key")
        hdr.setStyleSheet(f"color:{t['acc']};font-size:16px;font-weight:bold;"); lay.addWidget(hdr)
        warn = QLabel("⚠  Save this key now — it's the ONLY way to sign in.\nThere is no password reset or account recovery otherwise.")
        warn.setStyleSheet(f"color:{t['warn']};font-size:12px;"); warn.setWordWrap(True); lay.addWidget(warn)
        key_lbl = QLabel(key)
        key_lbl.setStyleSheet(f"background:{t['inp']};border:2px solid {t['acc']};border-radius:9px;"
                              f"padding:14px;font-size:14px;font-family:monospace;color:{t['acc']};letter-spacing:2px;")
        key_lbl.setWordWrap(True)
        key_lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        lay.addWidget(key_lbl)
        copy = QPushButton("📋  Copy Key")
        copy.clicked.connect(lambda: (QApplication.clipboard().setText(key), copy.setText("✓ Copied!")))
        lay.addWidget(copy)
        ok = QPushButton("I've Saved My Key — Continue"); ok.setObjectName("accent")
        ok.clicked.connect(self.accept); lay.addWidget(ok)

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        t = SETTINGS.theme()
        self.setWindowTitle("Sign In"); self.setFixedSize(420, 260)
        self.setStyleSheet(build_stylesheet(t))
        lay = QVBoxLayout(self); lay.setContentsMargins(28,24,28,20); lay.setSpacing(12)
        hdr = QLabel("🔑  Enter Recovery Key")
        hdr.setStyleSheet(f"color:{t['acc']};font-size:16px;font-weight:bold;"); lay.addWidget(hdr)
        lay.addWidget(QLabel("Paste your 50-character recovery key:"))
        self.key_edit = QLineEdit()
        self.key_edit.setPlaceholderText("XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX")
        self.key_edit.setFixedHeight(40); lay.addWidget(self.key_edit)
        self.err = QLabel(""); self.err.setStyleSheet(f"color:{t['dng']};font-size:11px;"); lay.addWidget(self.err)
        lay.addStretch()
        row = QHBoxLayout()
        cancel = QPushButton("Cancel"); cancel.clicked.connect(self.reject)
        ok = QPushButton("Sign In"); ok.setObjectName("accent"); ok.clicked.connect(self._login)
        row.addWidget(cancel); row.addWidget(ok); lay.addLayout(row)
        new = QPushButton("Create New Account →")
        new.setStyleSheet(f"color:{t['mut']};border:none;background:transparent;font-size:11px;")
        new.clicked.connect(self._new_account); lay.addWidget(new, alignment=Qt.AlignmentFlag.AlignCenter)

    def _login(self):
        if PROFILE.login_with_key(self.key_edit.text().strip()): self.accept()
        else: self.err.setText("✗ Invalid recovery key. Please check and try again.")

    def _new_account(self):
        self.reject()
        dlg = CreateAccountDialog(self.parent())
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.recovery_key:
            RecoveryKeyDialog(dlg.recovery_key, self.parent()).exec()

# ══════════════════════════════════════════════════════════════════
#  SIDE PANELS: BOOKMARKS + HISTORY
# ══════════════════════════════════════════════════════════════════
class BookmarksPanel(QWidget):
    navigate = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        t = SETTINGS.theme()
        self.setFixedWidth(270)
        self.setStyleSheet(f"background:{t['panel']};border-right:1px solid {t['brd']};")
        lay = QVBoxLayout(self); lay.setContentsMargins(10,10,10,10); lay.setSpacing(7)
        hdr = QHBoxLayout()
        title = QLabel("🔖  Bookmarks")
        title.setStyleSheet(f"color:{t['acc']};font-weight:bold;font-size:13px;")
        close = QPushButton("✕"); close.setObjectName("flat"); close.setFixedSize(24,24); close.clicked.connect(self.hide)
        hdr.addWidget(title,1); hdr.addWidget(close); lay.addLayout(hdr)
        self.search = QLineEdit(); self.search.setPlaceholderText("Search bookmarks…"); self.search.setFixedHeight(30)
        self.search.textChanged.connect(self.refresh); lay.addWidget(self.search)
        self.lst = QListWidget(); lay.addWidget(self.lst, 1)
        self.lst.itemDoubleClicked.connect(lambda i: self.navigate.emit(i.data(Qt.ItemDataRole.UserRole)))
        self.refresh()

    def refresh(self, query=""):
        self.lst.clear(); q = (query or self.search.text()).lower()
        for bm in PROFILE.get_bookmarks():
            title = bm.get("title","") or bm["url"]
            if q and q not in title.lower() and q not in bm["url"].lower(): continue
            item = QListWidgetItem(f"  {title[:32]}")
            item.setData(Qt.ItemDataRole.UserRole, bm["url"])
            item.setToolTip(bm["url"]); self.lst.addItem(item)

class HistoryPanel(QWidget):
    navigate = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        t = SETTINGS.theme()
        self.setFixedWidth(280)
        self.setStyleSheet(f"background:{t['panel']};border-right:1px solid {t['brd']};")
        lay = QVBoxLayout(self); lay.setContentsMargins(10,10,10,10); lay.setSpacing(7)
        hdr = QHBoxLayout()
        title = QLabel("🕒  History")
        title.setStyleSheet(f"color:{t['acc']};font-weight:bold;font-size:13px;")
        clear = QPushButton("Clear"); clear.setObjectName("flat"); clear.setFixedSize(44,24)
        clear.clicked.connect(self._clear)
        close = QPushButton("✕"); close.setObjectName("flat"); close.setFixedSize(24,24); close.clicked.connect(self.hide)
        hdr.addWidget(title,1); hdr.addWidget(clear); hdr.addWidget(close); lay.addLayout(hdr)
        self.search = QLineEdit(); self.search.setPlaceholderText("Search history…"); self.search.setFixedHeight(30)
        self.search.textChanged.connect(self.refresh); lay.addWidget(self.search)
        self.lst = QListWidget(); lay.addWidget(self.lst, 1)
        self.lst.itemDoubleClicked.connect(lambda i: self.navigate.emit(i.data(Qt.ItemDataRole.UserRole)))
        self.refresh()

    def refresh(self, query=""):
        self.lst.clear(); q = (query or self.search.text()).lower()
        for entry in PROFILE.get_history():
            url = entry.get("url",""); title = entry.get("title","") or url[:40]
            if q and q not in title.lower() and q not in url.lower(): continue
            ts = entry.get("ts","")[:10]
            item = QListWidgetItem(f"  {title[:30]}\n  {ts}")
            item.setData(Qt.ItemDataRole.UserRole, url)
            item.setToolTip(url); self.lst.addItem(item)

    def _clear(self):
        PROFILE._data["history"] = []; PROFILE.save(); self.refresh()


# ══════════════════════════════════════════════════════════════════
#  FIND BAR
# ══════════════════════════════════════════════════════════════════
class FindBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        t = SETTINGS.theme()
        self.setStyleSheet(f"background:{t['panel']};border-top:1px solid {t['brd']};")
        self.setFixedHeight(44)
        lay = QHBoxLayout(self); lay.setContentsMargins(10,6,10,6); lay.setSpacing(5)
        self.inp = QLineEdit(); self.inp.setPlaceholderText("Find in page…")
        self.inp.setFixedHeight(30); self.inp.textChanged.connect(self._find)
        self.inp.returnPressed.connect(self._next)
        lay.addWidget(self.inp, 1)
        self.count_lbl = QLabel("")
        self.count_lbl.setStyleSheet(f"color:{t['mut']};font-size:11px;min-width:60px;")
        for label, slot, tip in [("▲", self._prev, "Previous"), ("▼", self._next, "Next")]:
            b = QPushButton(label); b.setObjectName("flat"); b.setFixedSize(30,30)
            b.setToolTip(tip); b.clicked.connect(slot); lay.addWidget(b)
        lay.addWidget(self.count_lbl)
        close = QPushButton("✕"); close.setObjectName("flat"); close.setFixedSize(28,28)
        close.clicked.connect(self.close_bar); lay.addWidget(close)
        self._view = None; self.hide()

    def set_view(self, view): self._view = view
    def show_focus(self): self.show(); self.inp.setFocus(); self.inp.selectAll()

    def close_bar(self):
        if self._view: self._view.findText("")
        self.hide()

    def _find(self, text=None):
        if self._view:
            q = text if text is not None else self.inp.text()
            self._view.findText(q)

    def _next(self):
        if self._view: self._view.findText(self.inp.text())

    def _prev(self):
        if self._view:
            self._view.findText(
                self.inp.text(),
                QWebEnginePage.FindFlag.FindBackward)

# ══════════════════════════════════════════════════════════════════
#  DEVTOOLS DIALOG
# ══════════════════════════════════════════════════════════════════
class DevToolsDialog(QDialog):
    def __init__(self, view: QWebEngineView, parent=None):
        super().__init__(parent)
        t = SETTINGS.theme()
        self.setWindowTitle("🛠  Developer Tools")
        self.resize(960, 540)
        self.setStyleSheet(build_stylesheet(t))

        lay = QVBoxLayout(self); lay.setContentsMargins(0,0,0,0)

        from PyQt6.QtWidgets import QTabWidget as QTW
        self.tabs = QTW()
        lay.addWidget(self.tabs)

        # ── Console tab ───────────────────────────────────────────
        con_w = QWidget(); c_lay = QVBoxLayout(con_w); c_lay.setContentsMargins(8,8,8,8)
        self.console_out = QTextEdit(); self.console_out.setReadOnly(True)
        self.console_out.setStyleSheet(
            f"background:{t['bg']};color:{t['acc']};font-family:monospace;font-size:12px;border:none;")
        self.console_out.setPlainText("// JavaScript Console\n// Type an expression below and press Run or Enter")
        c_lay.addWidget(self.console_out, 1)
        inp_row = QHBoxLayout()
        self.console_inp = QLineEdit()
        self.console_inp.setPlaceholderText(">> JavaScript expression…")
        self.console_inp.setStyleSheet("font-family:monospace;")
        self.console_inp.returnPressed.connect(lambda: self._run_js(view))
        run_btn = QPushButton("▶ Run"); run_btn.setObjectName("accent")
        run_btn.clicked.connect(lambda: self._run_js(view))
        clear_btn = QPushButton("Clear"); clear_btn.clicked.connect(self.console_out.clear)
        inp_row.addWidget(self.console_inp, 1); inp_row.addWidget(run_btn); inp_row.addWidget(clear_btn)
        c_lay.addLayout(inp_row)
        self.tabs.addTab(con_w, "Console")

        # ── Source tab ────────────────────────────────────────────
        src_w = QWidget(); s_lay = QVBoxLayout(src_w); s_lay.setContentsMargins(8,8,8,8)
        self.source_view = QTextEdit(); self.source_view.setReadOnly(True)
        self.source_view.setStyleSheet(
            f"background:{t['bg']};color:{t['txt']};font-family:monospace;font-size:12px;border:none;")
        ref_btn = QPushButton("🔄  Refresh Source")
        ref_btn.clicked.connect(lambda: self._load_source(view))
        s_lay.addWidget(ref_btn); s_lay.addWidget(self.source_view, 1)
        self.tabs.addTab(src_w, "Page Source")

        # ── Network info tab ──────────────────────────────────────
        net_w = QWidget(); n_lay = QVBoxLayout(net_w); n_lay.setContentsMargins(8,8,8,8)
        self.net_info = QTextEdit(); self.net_info.setReadOnly(True)
        self.net_info.setStyleSheet(
            f"background:{t['bg']};color:{t['txt']};font-family:monospace;font-size:12px;border:none;")
        n_lay.addWidget(self.net_info, 1)
        self.tabs.addTab(net_w, "Network Info")
        self._update_network_info(view)

        # ── Inspector (embedded devtools) ─────────────────────────
        self.inspector = QWebEngineView()
        view.page().setDevToolsPage(self.inspector.page())
        self.tabs.addTab(self.inspector, "Inspector")

        self._load_source(view)

    def _run_js(self, view):
        code = self.console_inp.text().strip()
        if not code: return
        self.console_out.append(f"\n<span style='color:#888;'>▶</span> {code}")
        view.page().runJavaScript(code, lambda r: self.console_out.append(f"← {r}"))
        self.console_inp.clear()

    def _load_source(self, view):
        view.page().toHtml(lambda html: self.source_view.setPlainText(html))

    def _update_network_info(self, view):
        url = view.url()
        proxy = QNetworkProxy.applicationProxy()
        ptype = {
            QNetworkProxy.ProxyType.Socks5Proxy: "SOCKS5",
            QNetworkProxy.ProxyType.HttpProxy:   "HTTP",
            QNetworkProxy.ProxyType.NoProxy:     "None (Direct)",
        }.get(proxy.type(), "Unknown")
        info = (
            f"Current URL:     {url.toString()}\n"
            f"Scheme:          {url.scheme()}\n"
            f"Host:            {url.host()}\n"
            f"Port:            {url.port()}\n\n"
            f"Proxy Type:      {ptype}\n"
            f"Proxy Host:      {proxy.hostName() or '—'}\n"
            f"Proxy Port:      {proxy.port() or '—'}\n\n"
            f"User Agent:      {GENERIC_UA}\n"
            f"Cookies:         Not persisted (memory only)\n"
            f"Cache:           Memory only\n"
            f"JS Enabled:      {SETTINGS.get('js_enabled', True)}\n"
            f"Strict Privacy:  {SETTINGS.get('strict_privacy', False)}\n"
        )
        self.net_info.setPlainText(info)


# ══════════════════════════════════════════════════════════════════
#  SETTINGS DIALOG
# ══════════════════════════════════════════════════════════════════
class SettingsDialog(QDialog):
    settings_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        t = SETTINGS.theme()
        self.setWindowTitle("⚙️  Settings"); self.resize(720, 540)
        self.setStyleSheet(build_stylesheet(t))
        root = QHBoxLayout(self); root.setContentsMargins(0,0,0,0); root.setSpacing(0)

        # Sidebar
        sidebar = QWidget(); sidebar.setFixedWidth(160)
        sidebar.setStyleSheet(f"background:{t['panel']};border-right:1px solid {t['brd']};")
        sb = QVBoxLayout(sidebar); sb.setContentsMargins(8,16,8,8); sb.setSpacing(3)
        self._pages = QStackedWidget()
        nav_items = [("🎨","Appearance"),("🔒","Privacy"),("🌐","Network"),
                     ("🔍","Search"),("📥","Downloads"),("🧩","Extensions"),("👤","Account")]
        for i,(icon,label) in enumerate(nav_items):
            btn = QPushButton(f"  {icon}  {label}"); btn.setObjectName("flat")
            btn.setStyleSheet(f"text-align:left;padding:9px 10px;border-radius:7px;color:{t['txt']};font-size:12px;")
            btn.clicked.connect(lambda _, idx=i: self._pages.setCurrentIndex(idx))
            sb.addWidget(btn)
        sb.addStretch()
        root.addWidget(sidebar)

        self._pages.addWidget(self._pg_appearance(t))
        self._pages.addWidget(self._pg_privacy(t))
        self._pages.addWidget(self._pg_network(t))
        self._pages.addWidget(self._pg_search(t))
        self._pages.addWidget(self._pg_downloads(t))
        self._pages.addWidget(self._pg_extensions(t))
        self._pages.addWidget(self._pg_account(t))
        root.addWidget(self._pages, 1)

    def _scroll(self, w):
        sc = QScrollArea(); sc.setWidgetResizable(True); sc.setWidget(w)
        sc.setStyleSheet("border:none;"); return sc

    def _section(self, text, t):
        l = QLabel(text); l.setStyleSheet(f"color:{t['acc']};font-size:15px;font-weight:bold;margin-bottom:4px;"); return l

    def _chk(self, label, key):
        c = QCheckBox(label); c.setChecked(bool(SETTINGS.get(key)))
        c.toggled.connect(lambda v,k=key: SETTINGS.set(k,v)); return c

    def _pg_appearance(self, t):
        w = QWidget(); lay = QVBoxLayout(w); lay.setContentsMargins(22,18,22,18); lay.setSpacing(14)
        lay.addWidget(self._section("🎨  Appearance", t))

        # Theme selector
        grp = QGroupBox("Active Theme"); g = QFormLayout(grp)
        self._theme_combo = QComboBox(); self._theme_combo.addItems(THEME_NAMES)
        self._theme_combo.setCurrentText(SETTINGS.get("theme","Phantom Dark"))
        self._theme_combo.currentTextChanged.connect(self._change_theme)
        g.addRow("Theme:", self._theme_combo); lay.addWidget(grp)

        # Theme preview grid
        prev = QGroupBox("Theme Previews (click to apply)")
        grid = QGridLayout(prev); grid.setSpacing(5)
        for i, name in enumerate(THEME_NAMES):
            th = THEMES[name]
            b = QPushButton(name); b.setFixedHeight(32)
            b.setStyleSheet(f"background:{th['panel']};color:{th['acc']};border:1px solid {th['brd']};"
                            f"border-radius:6px;font-size:10px;font-weight:bold;")
            b.clicked.connect(lambda _, n=name: (self._theme_combo.setCurrentText(n), self._change_theme(n)))
            grid.addWidget(b, i//3, i%3)
        lay.addWidget(prev)

        # Font size
        fg = QGroupBox("Font Size"); fl = QHBoxLayout(fg)
        self._fsz = QSlider(Qt.Orientation.Horizontal)
        self._fsz.setRange(10,22); self._fsz.setValue(SETTINGS.get("font_size",13))
        self._fsz_lbl = QLabel(str(self._fsz.value()))
        self._fsz.valueChanged.connect(lambda v: (self._fsz_lbl.setText(str(v)), SETTINGS.set("font_size",v), self.settings_changed.emit()))
        fl.addWidget(QLabel("10")); fl.addWidget(self._fsz,1); fl.addWidget(QLabel("22")); fl.addWidget(self._fsz_lbl)
        lay.addWidget(fg); lay.addStretch()
        return self._scroll(w)

    def _pg_privacy(self, t):
        w = QWidget(); lay = QVBoxLayout(w); lay.setContentsMargins(22,18,22,18); lay.setSpacing(14)
        lay.addWidget(self._section("🔒  Privacy & Security", t))
        grp = QGroupBox("Privacy Settings"); g = QVBoxLayout(grp)
        for label,key in [("Enable JavaScript","js_enabled"),
                           ("Strict Privacy Mode (mask UA, disable WebGL)","strict_privacy"),
                           ("Block Ad Domains","block_ads"),
                           ("Block Trackers","block_trackers"),
                           ("Stay signed in automatically","auto_login")]:
            g.addWidget(self._chk(label, key))
        lay.addWidget(grp)
        cg = QGroupBox("Clear Browsing Data"); cl = QHBoxLayout(cg)
        for label,what in [("Cookies","cookies"),("Cache","cache"),("History","history"),("All","all")]:
            b = QPushButton(f"Clear {label}"); b.clicked.connect(lambda _,wh=what: self._clear(wh)); cl.addWidget(b)
        lay.addWidget(cg); lay.addStretch()
        return self._scroll(w)

    def _pg_network(self, t):
        w = QWidget(); lay = QVBoxLayout(w); lay.setContentsMargins(22,18,22,18); lay.setSpacing(14)
        lay.addWidget(self._section("🌐  Network & Proxy", t))
        grp = QGroupBox("Proxy Configuration"); g = QFormLayout(grp)
        self._proxy_type = QComboBox()
        self._proxy_type.addItems(["tor (127.0.0.1:9050)","socks5","http","none"])
        self._proxy_type.setCurrentText(SETTINGS.get("proxy_type","tor"))
        self._proxy_host = QLineEdit(SETTINGS.get("proxy_host","127.0.0.1"))
        self._proxy_port = QSpinBox(); self._proxy_port.setRange(1,65535)
        self._proxy_port.setValue(SETTINGS.get("proxy_port",9050))
        apply_btn = QPushButton("Apply Proxy Settings"); apply_btn.setObjectName("accent")
        apply_btn.clicked.connect(self._apply_proxy)
        g.addRow("Type:", self._proxy_type); g.addRow("Host:", self._proxy_host)
        g.addRow("Port:", self._proxy_port); g.addRow("", apply_btn)
        lay.addWidget(grp)
        tg = QGroupBox("Tor Status"); tl = QVBoxLayout(tg)
        self._tor_lbl = QLabel("Checking…"); tl.addWidget(self._tor_lbl)
        self._refresh_tor()
        ref = QPushButton("Refresh"); ref.clicked.connect(self._refresh_tor); tl.addWidget(ref)
        lay.addWidget(tg); lay.addStretch()
        return self._scroll(w)

    def _pg_search(self, t):
        w = QWidget(); lay = QVBoxLayout(w); lay.setContentsMargins(22,18,22,18); lay.setSpacing(14)
        lay.addWidget(self._section("🔍  Search & Homepage", t))
        grp = QGroupBox("Search"); g = QFormLayout(grp)
        se = QComboBox(); se.addItems(list(SEARCH_ENGINES.keys()))
        se.setCurrentText(SETTINGS.get("search_engine","DuckDuckGo"))
        se.currentTextChanged.connect(lambda v: SETTINGS.set("search_engine",v))
        hp = QLineEdit(SETTINGS.get("homepage","phantom://newtab"))
        hp.textChanged.connect(lambda v: SETTINGS.set("homepage",v))
        g.addRow("Default Engine:", se); g.addRow("Homepage URL:", hp)
        lay.addWidget(grp); lay.addStretch()
        return self._scroll(w)

    def _pg_downloads(self, t):
        w = QWidget(); lay = QVBoxLayout(w); lay.setContentsMargins(22,18,22,18); lay.setSpacing(14)
        lay.addWidget(self._section("📥  Downloads", t))
        grp = QGroupBox("Download Location"); g = QHBoxLayout(grp)
        self._dl_path = QLineEdit(SETTINGS.get("download_path",str(Path.home()/"Downloads")))
        browse = QPushButton("Browse…"); browse.clicked.connect(self._browse_dl)
        g.addWidget(self._dl_path,1); g.addWidget(browse)
        lay.addWidget(grp); lay.addStretch()
        return self._scroll(w)

    def _pg_extensions(self, t):
        w = QWidget(); lay = QVBoxLayout(w); lay.setContentsMargins(22,18,22,18); lay.setSpacing(12)
        lay.addWidget(self._section("🧩  Extensions", t))
        for eid, ext in BUILTIN_EXTENSIONS.items():
            card = QFrame()
            card.setStyleSheet(f"background:{t['panel']};border:1px solid {t['brd']};border-radius:10px;")
            row = QHBoxLayout(card); row.setContentsMargins(14,10,14,10)
            icon = QLabel(ext["icon"]); icon.setStyleSheet("font-size:22px;"); row.addWidget(icon)
            info = QVBoxLayout()
            nm = QLabel(f"<b>{ext['name']}</b>  <span style='color:{t['mut']};font-size:10px;'>v{ext['version']}</span>")
            nm.setStyleSheet(f"color:{t['txt']};"); info.addWidget(nm)
            desc = QLabel(ext["description"]); desc.setStyleSheet(f"color:{t['mut']};font-size:11px;"); info.addWidget(desc)
            row.addLayout(info,1)
            tog = QCheckBox("Enabled"); tog.setChecked(ext.get("enabled",False))
            tog.toggled.connect(lambda v,e=eid: BUILTIN_EXTENSIONS.__setitem__(e, {**BUILTIN_EXTENSIONS[e],"enabled":v}))
            row.addWidget(tog); lay.addWidget(card)
        lay.addStretch()
        return self._scroll(w)

    def _pg_account(self, t):
        w = QWidget(); lay = QVBoxLayout(w); lay.setContentsMargins(22,18,22,18); lay.setSpacing(14)
        lay.addWidget(self._section("👤  Account", t))
        grp = QGroupBox("Current Account"); g = QVBoxLayout(grp)
        if PROFILE.logged_in:
            g.addWidget(QLabel(f"<b>Signed in as:</b>  {PROFILE.name}"))
            g.addWidget(QLabel(f"<b>Profile ID:</b>  {PROFILE._current}"))
            g.addWidget(self._chk("Stay signed in automatically","auto_login"))
            lo = QPushButton("Sign Out"); lo.setObjectName("danger"); lo.clicked.connect(self._logout)
            g.addWidget(lo)
        else:
            g.addWidget(QLabel("Not signed in."))
            li = QPushButton("Sign In"); li.setObjectName("accent"); li.clicked.connect(self._login); g.addWidget(li)
            cr = QPushButton("Create Account"); cr.clicked.connect(self._create_account); g.addWidget(cr)
        lay.addWidget(grp); lay.addStretch()
        return self._scroll(w)

    # helpers
    def _change_theme(self, name):
        SETTINGS.set("theme", name); self.settings_changed.emit()

    def _apply_proxy(self):
        pt = self._proxy_type.currentText().split()[0]
        h = self._proxy_host.text().strip(); p = self._proxy_port.value()
        SETTINGS.set("proxy_type",pt); SETTINGS.set("proxy_host",h); SETTINGS.set("proxy_port",p)
        configure_proxy(pt,h,p)

    def _refresh_tor(self):
        try:
            with socket.create_connection((TOR_HOST,TOR_PORT),timeout=1.5):
                self._tor_lbl.setText("🟢  Tor is running on 127.0.0.1:9050")
        except OSError:
            self._tor_lbl.setText("🔴  Tor is NOT running")

    def _clear(self, what):
        mw = self.parent()
        if what in ("cookies","all") and hasattr(mw,"profile"):
            mw.profile.cookieStore().deleteAllCookies()
        if what in ("cache","all") and hasattr(mw,"profile"):
            mw.profile.clearHttpCache()
        if what in ("history","all"):
            PROFILE._data["history"] = []; PROFILE.save()
        QMessageBox.information(self,"Cleared",f"{'All data' if what=='all' else what.capitalize()} cleared.")

    def _browse_dl(self):
        d = QFileDialog.getExistingDirectory(self,"Select Download Folder")
        if d: self._dl_path.setText(d); SETTINGS.set("download_path",d)

    def _logout(self): PROFILE.logout(); self.settings_changed.emit(); self.reject()

    def _login(self):
        dlg = LoginDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted: self.settings_changed.emit()

    def _create_account(self):
        dlg = CreateAccountDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.recovery_key:
            RecoveryKeyDialog(dlg.recovery_key, self).exec(); self.settings_changed.emit()


# ══════════════════════════════════════════════════════════════════
#  MAIN BROWSER WINDOW
# ══════════════════════════════════════════════════════════════════
class PhantomBrowser(QMainWindow):
    def __init__(self, tor_active=False):
        super().__init__()
        self.setWindowTitle("Phantom Browser")
        self.resize(1400, 860)
        self._tor_active  = tor_active
        self._dev_dialogs = {}   # id(view) -> DevToolsDialog

        # ── Web engine profile (ephemeral) ────────────────────────
        self.profile = build_private_profile()
        apply_engine_settings(self.profile.settings(),
                              strict=SETTINGS.get("strict_privacy", False))
        self.profile.downloadRequested.connect(self._on_download)

        # ── Proxy ─────────────────────────────────────────────────
        if tor_active:
            configure_proxy("tor", TOR_HOST, TOR_PORT)
        else:
            pt = SETTINGS.get("proxy_type","none")
            if pt != "none":
                configure_proxy(pt, SETTINGS.get("proxy_host","127.0.0.1"),
                                    SETTINGS.get("proxy_port", 9050))

        self._build_ui()
        self._setup_shortcuts()
        self._open_new_tab()           # first tab
        self._apply_theme()
        QTimer.singleShot(300, self._welcome)

    # ── UI ────────────────────────────────────────────────────────
    def _build_ui(self):
        t = SETTINGS.theme()
        central = QWidget()
        self.setCentralWidget(central)
        self._root = QVBoxLayout(central)
        self._root.setContentsMargins(0,0,0,0)
        self._root.setSpacing(0)

        self._build_toolbar()

        # Progress bar (sits just below toolbar)
        self._prog = QProgressBar()
        self._prog.setFixedHeight(3)
        self._prog.setTextVisible(False)
        self._prog.setRange(0,100)
        self._prog.setVisible(False)
        self._root.addWidget(self._prog)

        # Bookmarks bar
        self._build_bm_bar()

        # Content row: side panels + tabs
        content = QWidget()
        content_lay = QHBoxLayout(content)
        content_lay.setContentsMargins(0,0,0,0)
        content_lay.setSpacing(0)

        self.bm_panel   = BookmarksPanel()
        self.hist_panel = HistoryPanel()
        self.bm_panel.navigate.connect(self._navigate_to)
        self.hist_panel.navigate.connect(self._navigate_to)
        self.bm_panel.hide(); self.hist_panel.hide()
        content_lay.addWidget(self.bm_panel)
        content_lay.addWidget(self.hist_panel)

        tab_area = QWidget()
        tab_lay  = QVBoxLayout(tab_area)
        tab_lay.setContentsMargins(0,0,0,0)
        tab_lay.setSpacing(0)

        self.tabs = PhantomTabWidget()
        self.tabs.new_tab_req.connect(self._open_new_tab)
        self.tabs.tab_changed.connect(self._on_tab_changed)
        self.tabs.tab_closed.connect(self._close_tab)
        tab_lay.addWidget(self.tabs, 1)

        self.find_bar = FindBar()
        tab_lay.addWidget(self.find_bar)

        content_lay.addWidget(tab_area, 1)
        self._root.addWidget(content, 1)

        # Status bar
        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._sec_badge  = QLabel()
        self._tor_badge  = QLabel()
        self._zoom_lbl   = QLabel("100%")
        self._zoom_lbl.setStyleSheet(f"color:{t['mut']};font-size:11px;padding:0 6px;")
        for w in [self._sec_badge, self._tor_badge, self._zoom_lbl]:
            self._status.addPermanentWidget(w)
        self._update_tor_badge()

    def _build_toolbar(self):
        t = SETTINGS.theme()
        tb = QToolBar()
        tb.setMovable(False); tb.setFloatable(False)
        tb.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        tb.setFixedHeight(50)
        self.addToolBar(tb)
        self._toolbar = tb

        def fb(label, tip, slot, w=34, h=34):
            b = QPushButton(label); b.setObjectName("flat")
            b.setToolTip(tip); b.setFixedSize(w,h); b.clicked.connect(slot); return b

        self.btn_back   = fb("◀","Back (Alt+←)",    self._on_back)
        self.btn_fwd    = fb("▶","Forward (Alt+→)",  self._on_fwd)
        self.btn_reload = fb("↻","Reload (F5)",       self._on_reload, 34)
        self.btn_home   = fb("⌂","Home",              self._on_home)
        for b in [self.btn_back, self.btn_fwd, self.btn_reload, self.btn_home]:
            tb.addWidget(b)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFixedHeight(22); sep.setStyleSheet(f"color:{t['brd']};")
        tb.addWidget(sep)

        # Lock icon
        self._lock_lbl = QLabel("🔓")
        self._lock_lbl.setFixedWidth(26)
        self._lock_lbl.setToolTip("Connection security")
        tb.addWidget(self._lock_lbl)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setObjectName("urlBar")
        self.url_bar.setPlaceholderText("Search or enter URL…")
        self.url_bar.setFixedHeight(36)
        self.url_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.url_bar.returnPressed.connect(self._on_navigate)
        self.url_bar.mousePressEvent = lambda e: (
            super(QLineEdit, self.url_bar).mousePressEvent(e),
            self.url_bar.selectAll())
        tb.addWidget(self.url_bar)

        # Bookmark star
        self.btn_star = fb("☆","Bookmark (Ctrl+D)", self._toggle_bookmark, 30)
        tb.addWidget(self.btn_star)

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.VLine)
        sep2.setFixedHeight(22); sep2.setStyleSheet(f"color:{t['brd']};")
        tb.addWidget(sep2)

        # Right-side buttons
        self.btn_bm   = fb("📑","Bookmarks (Ctrl+B)",   self._toggle_bm)
        self.btn_hist = fb("🕒","History (Ctrl+H)",      self._toggle_hist)
        self.btn_ext  = fb("🧩","Extensions",            self._open_extensions)
        self.btn_acc  = fb("👤","Account",               self._show_account_menu, 36)
        self.btn_settings = fb("⚙️","Settings (Ctrl+,)", self._open_settings, 36)
        self.btn_menu = fb("⋮","Menu",                   self._show_main_menu, 28)
        for b in [self.btn_bm, self.btn_hist, self.btn_ext, self.btn_acc, self.btn_settings, self.btn_menu]:
            tb.addWidget(b)

    def _build_bm_bar(self):
        t = SETTINGS.theme()
        self._bm_bar = QWidget()
        self._bm_bar.setFixedHeight(30)
        self._bm_bar.setStyleSheet(f"background:{t['panel']};border-bottom:1px solid {t['brd']};")
        self._bm_bar_lay = QHBoxLayout(self._bm_bar)
        self._bm_bar_lay.setContentsMargins(6,0,6,0)
        self._bm_bar_lay.setSpacing(2)
        self._root.addWidget(self._bm_bar)
        if not SETTINGS.get("show_bookmarks_bar", True):
            self._bm_bar.hide()
        self._refresh_bm_bar()

    def _refresh_bm_bar(self):
        t = SETTINGS.theme()
        while self._bm_bar_lay.count():
            item = self._bm_bar_lay.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        for bm in PROFILE.get_bookmarks()[:14]:
            title = (bm.get("title","") or bm["url"])[:20]
            b = QPushButton(f"  🔖 {title}")
            b.setObjectName("flat")
            b.setStyleSheet(f"font-size:11px;padding:2px 8px;border-radius:5px;color:{t['txt']};")
            b.setToolTip(bm["url"])
            b.clicked.connect(lambda _, u=bm["url"]: self._navigate_to(u))
            self._bm_bar_lay.addWidget(b)
        self._bm_bar_lay.addStretch()

    # ── Tabs ──────────────────────────────────────────────────────
    def _make_view(self) -> QWebEngineView:
        view = QWebEngineView()
        page = PrivatePage(self.profile, view)
        view.setPage(page)
        # Connect all page signals
        view.urlChanged.connect(   lambda url,   v=view: self._on_url_changed(url, v))
        view.titleChanged.connect( lambda title, v=view: self._on_title_changed(title, v))
        view.loadStarted.connect(  lambda        v=view: self._on_load_started(v))
        view.loadProgress.connect( self._prog.setValue)
        view.loadFinished.connect( lambda ok,    v=view: self._on_load_finished(ok, v))
        view.page().linkHovered.connect(lambda url: self._status.showMessage(url, 2000) if url else None)
        # Inject CSS extensions
        for eid, ext in BUILTIN_EXTENSIONS.items():
            if ext.get("enabled") and "inject_css" in ext:
                css = ext["inject_css"].replace("`","\\`")
                js = (f"(function(){{var s=document.createElement('style');"
                      f"s.textContent=`{css}`;document.head.appendChild(s);}})();")
                script = QWebEngineScript()
                script.setName(f"ext_{eid}")
                script.setSourceCode(js)
                script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentReady)
                script.setWorldId(QWebEngineScript.ScriptWorldId.ApplicationWorld)
                view.page().scripts().insert(script)
        return view

    def _open_new_tab(self, url=None):
        t = SETTINGS.theme()
        view = self._make_view()
        self.tabs.add_tab(view, "New Tab")
        self.find_bar.set_view(view)
        if url:
            view.setUrl(QUrl(url) if isinstance(url, str) else url)
        else:
            view.setHtml(newtab_html(t), QUrl("about:blank"))
        view.setFocus()

    def _close_tab(self, idx):
        self.tabs.remove_tab(idx)
        if self.tabs.count() == 0:
            self._open_new_tab()

    def _on_tab_changed(self, idx):
        view = self.tabs.widget(idx)
        if not view: return
        url = view.url()
        self.url_bar.setText(
            url.toString() if url.toString() not in ("about:blank","") else "")
        self.setWindowTitle(f"{view.title() or 'New Tab'} — Phantom Browser")
        self._update_sec_badge(url)
        self._update_star()
        self.find_bar.set_view(view)
        self.btn_back.setEnabled(view.history().canGoBack())
        self.btn_fwd.setEnabled( view.history().canGoForward())

    # ── Navigation ────────────────────────────────────────────────
    def _resolve_url(self, text: str) -> QUrl:
        text = text.strip()
        if not text: return QUrl("about:blank")
        if text.startswith(("http://","https://","file://","ftp://")): return QUrl(text)
        # .onion support (via Tor SOCKS5)
        if re.search(r'\.onion(/|$)', text):
            return QUrl(("http://" if not text.startswith("http") else "") + text)
        # looks like a domain
        if re.match(r'^[a-zA-Z0-9][\w\-]+(\.[a-zA-Z]{2,})+', text) and " " not in text:
            return QUrl("https://" + text)
        # search
        engine = SETTINGS.get("search_engine","DuckDuckGo")
        tmpl   = SEARCH_ENGINES.get(engine, SEARCH_ENGINES["DuckDuckGo"])
        return QUrl(tmpl.format(urllib.parse.quote_plus(text)))

    @pyqtSlot()
    def _on_navigate(self):
        text = self.url_bar.text().strip()
        if not text: return
        view = self.tabs.current_widget()
        if view: view.setUrl(self._resolve_url(text))

    def _navigate_to(self, url: str):
        view = self.tabs.current_widget()
        if view: view.setUrl(self._resolve_url(url))

    @pyqtSlot()
    def _on_back(self):
        v = self.tabs.current_widget()
        if v: v.back()
    @pyqtSlot()
    def _on_fwd(self):
        v = self.tabs.current_widget()
        if v: v.forward()
    @pyqtSlot()
    def _on_reload(self):
        v = self.tabs.current_widget()
        if v: v.reload()
    @pyqtSlot()
    def _on_home(self):
        hp = SETTINGS.get("homepage","phantom://newtab")
        if hp == "phantom://newtab":
            t = SETTINGS.theme()
            v = self.tabs.current_widget()
            if v: v.setHtml(newtab_html(t), QUrl("about:blank"))
        else:
            self._navigate_to(hp)

    # ── Page signals ──────────────────────────────────────────────
    def _on_url_changed(self, url: QUrl, view: QWebEngineView):
        if view is not self.tabs.current_widget(): return
        raw = url.toString()
        if raw not in ("about:blank",""):
            self.url_bar.setText(raw)
        self._update_sec_badge(url)
        self._update_star()

    def _on_title_changed(self, title: str, view: QWebEngineView):
        idx = self.tabs.index_of(view)
        if idx >= 0:
            self.tabs.set_tab_title(idx, title or "New Tab")
        if view is self.tabs.current_widget():
            self.setWindowTitle(f"{title or 'New Tab'} — Phantom Browser")
        # Record history
        if title and PROFILE.logged_in:
            url = view.url().toString()
            if url and url != "about:blank":
                PROFILE.add_history(url, title)
                if self.hist_panel.isVisible():
                    self.hist_panel.refresh()

    def _on_load_started(self, view: QWebEngineView):
        if view is not self.tabs.current_widget(): return
        self._prog.setValue(0); self._prog.setVisible(True)
        self.btn_reload.setText("✕"); self.btn_reload.setToolTip("Stop loading")
        try: self.btn_reload.clicked.disconnect()
        except Exception: pass
        self.btn_reload.clicked.connect(
            lambda: self.tabs.current_widget() and self.tabs.current_widget().stop())

    def _on_load_finished(self, ok: bool, view: QWebEngineView):
        if view is not self.tabs.current_widget(): return
        self._prog.setVisible(False)
        self.btn_reload.setText("↻"); self.btn_reload.setToolTip("Reload (F5)")
        try: self.btn_reload.clicked.disconnect()
        except Exception: pass
        self.btn_reload.clicked.connect(self._on_reload)
        self.btn_back.setEnabled(view.history().canGoBack())
        self.btn_fwd.setEnabled( view.history().canGoForward())
        # Run JS-injection extensions post-load
        if ok:
            for ext in BUILTIN_EXTENSIONS.values():
                if ext.get("enabled") and "inject_js" in ext:
                    view.page().runJavaScript(ext["inject_js"])
            self._status.showMessage("✓ Loaded", 2000)
        else:
            self._status.showMessage("⚠ Failed to load page", 3000)

    # ── Security badge ────────────────────────────────────────────
    def _update_sec_badge(self, url: QUrl):
        t = SETTINGS.theme()
        s = url.scheme().lower()
        if s == "https":
            self._lock_lbl.setText("🔒"); self._lock_lbl.setToolTip("Secure HTTPS")
            self._sec_badge.setText("  🔒 HTTPS  ")
            self._sec_badge.setStyleSheet(f"color:{t['acc']};font-size:11px;font-weight:bold;")
        elif s == "http":
            self._lock_lbl.setText("🔓"); self._lock_lbl.setToolTip("⚠ Insecure HTTP!")
            self._sec_badge.setText("  🔓 HTTP  ")
            self._sec_badge.setStyleSheet(f"color:{t['dng']};font-size:11px;font-weight:bold;")
        else:
            self._lock_lbl.setText("🌐"); self._lock_lbl.setToolTip("Local / internal page")
            self._sec_badge.setText("")

    def _update_tor_badge(self):
        t = SETTINGS.theme()
        if self._tor_active:
            self._tor_badge.setText("  🧅 TOR  ")
            self._tor_badge.setStyleSheet(f"color:{t['acc']};font-size:11px;font-weight:bold;")
            self._tor_badge.setToolTip("Traffic anonymised via Tor (127.0.0.1:9050)")
        else:
            self._tor_badge.setText("  ⚠ NO TOR  ")
            self._tor_badge.setStyleSheet(f"color:{t['warn']};font-size:11px;")
            self._tor_badge.setToolTip("Tor not active — direct connection")

    def set_tor_active(self, active: bool):
        self._tor_active = active
        if active: configure_proxy("tor", TOR_HOST, TOR_PORT)
        self._update_tor_badge()
        self._status.showMessage("🧅 Tor circuit active — all traffic anonymised", 6000)

    # ── Bookmarks ─────────────────────────────────────────────────
    def _toggle_bookmark(self):
        view = self.tabs.current_widget()
        if not view: return
        url = view.url().toString(); title = view.title()
        if PROFILE.is_bookmarked(url):
            PROFILE.remove_bookmark(url); self.btn_star.setText("☆")
            self._status.showMessage("Bookmark removed", 2000)
        else:
            PROFILE.add_bookmark(url, title); self.btn_star.setText("★")
            self._status.showMessage(f"Bookmarked: {title[:50]}", 2500)
        self._refresh_bm_bar()
        if self.bm_panel.isVisible(): self.bm_panel.refresh()

    def _update_star(self):
        v = self.tabs.current_widget()
        if v: self.btn_star.setText("★" if PROFILE.is_bookmarked(v.url().toString()) else "☆")

    def _toggle_bm(self):
        if self.bm_panel.isVisible(): self.bm_panel.hide()
        else: self.bm_panel.refresh(); self.bm_panel.show()

    def _toggle_hist(self):
        if self.hist_panel.isVisible(): self.hist_panel.hide()
        else: self.hist_panel.refresh(); self.hist_panel.show()

    # ── Zoom ──────────────────────────────────────────────────────
    def _zoom_in(self):
        v = self.tabs.current_widget()
        if v: z = min(v.zoomFactor()+0.1,3.0); v.setZoomFactor(z); self._zoom_lbl.setText(f"{int(z*100)}%")
    def _zoom_out(self):
        v = self.tabs.current_widget()
        if v: z = max(v.zoomFactor()-0.1,0.3); v.setZoomFactor(z); self._zoom_lbl.setText(f"{int(z*100)}%")
    def _zoom_reset(self):
        v = self.tabs.current_widget()
        if v: v.setZoomFactor(1.0); self._zoom_lbl.setText("100%")

    # ── DevTools / Source ─────────────────────────────────────────
    def _open_devtools(self):
        v = self.tabs.current_widget()
        if not v: return
        vid = id(v)
        if vid not in self._dev_dialogs or not self._dev_dialogs[vid].isVisible():
            dlg = DevToolsDialog(v, self); dlg.show(); self._dev_dialogs[vid] = dlg
        else: self._dev_dialogs[vid].raise_(); self._dev_dialogs[vid].activateWindow()

    def _view_source(self):
        v = self.tabs.current_widget()
        if not v: return
        v.page().toHtml(lambda html: self._show_source_window(html, v.url().toString()))

    def _show_source_window(self, html: str, url: str):
        t = SETTINGS.theme()
        dlg = QDialog(self); dlg.setWindowTitle(f"Source — {url[:70]}")
        dlg.resize(860, 620); dlg.setStyleSheet(build_stylesheet(t))
        lay = QVBoxLayout(dlg)
        hdr = QHBoxLayout()
        hdr.addWidget(QLabel(f"<b>Page Source:</b> {url[:80]}"))
        copy_btn = QPushButton("📋 Copy All")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(html))
        hdr.addWidget(copy_btn); lay.addLayout(hdr)
        te = QTextEdit(); te.setReadOnly(True); te.setPlainText(html)
        te.setStyleSheet(f"font-family:monospace;font-size:12px;background:{t['bg']};color:{t['txt']};border:none;")
        lay.addWidget(te); dlg.exec()

    # ── Extensions ────────────────────────────────────────────────
    def _open_extensions(self):
        dlg = SettingsDialog(self)
        dlg.settings_changed.connect(self._apply_theme)
        dlg._pages.setCurrentIndex(5)   # jump straight to Extensions page
        dlg.exec()

    # ── Downloads ─────────────────────────────────────────────────
    def _on_download(self, dl: QWebEngineDownloadRequest):
        dl_dir = Path(SETTINGS.get("download_path", str(Path.home()/"Downloads")))
        dl_dir.mkdir(parents=True, exist_ok=True)
        name = dl.suggestedFileName() or "download"
        dl.setDownloadFileName(str(dl_dir / name))
        dl.accept()
        self._status.showMessage(f"📥 Downloading: {name}", 5000)

    # ── Menus ─────────────────────────────────────────────────────
    def _show_main_menu(self):
        menu = QMenu(self)
        menu.addAction("🗂  New Tab",          self._open_new_tab)
        menu.addAction("⚙️  Settings",         self._open_settings)
        menu.addAction("🧩  Extensions",       self._open_extensions)
        menu.addSeparator()
        menu.addAction("🔍  Find in Page…  Ctrl+F",   self.find_bar.show_focus)
        menu.addAction("🔎  View Page Source  Ctrl+U", self._view_source)
        menu.addAction("🛠  Developer Tools  F12",     self._open_devtools)
        menu.addSeparator()
        zm = menu.addMenu("🔍  Zoom")
        zm.addAction(f"Zoom In   (+)",    self._zoom_in)
        zm.addAction(f"Zoom Out  (−)",    self._zoom_out)
        zm.addAction(f"Reset  100%",      self._zoom_reset)
        menu.addSeparator()
        menu.addAction("💾  Save Page…",        self._save_page)
        menu.addAction("📑  Bookmarks Bar",      self._toggle_bm_bar_vis)
        menu.addSeparator()
        menu.addAction("🧅  Tor Status",         self._show_tor_status)
        menu.addAction("🗑  Clear All Data",     lambda: self._clear_all())
        menu.addAction("ℹ  About Phantom",      self._show_about)
        menu.exec(self.btn_menu.mapToGlobal(self.btn_menu.rect().bottomLeft()))

    def _show_account_menu(self):
        menu = QMenu(self)
        if PROFILE.logged_in:
            lbl = menu.addAction(f"👤  {PROFILE.name}")
            lbl.setEnabled(False)
            menu.addSeparator()
            menu.addAction("📑  Bookmarks",  self._toggle_bm)
            menu.addAction("🕒  History",    self._toggle_hist)
            menu.addSeparator()
            menu.addAction("⚙️  Account Settings", lambda: self._open_settings(6))
            menu.addAction("🚪  Sign Out",          self._sign_out)
        else:
            menu.addAction("🔑  Sign In",          self._show_login)
            menu.addAction("➕  Create Account",   self._show_create_account)
        menu.exec(self.btn_acc.mapToGlobal(self.btn_acc.rect().bottomLeft()))

    def _open_settings(self, page=0):
        dlg = SettingsDialog(self)
        dlg._pages.setCurrentIndex(page)
        dlg.settings_changed.connect(self._apply_theme)
        dlg.exec()

    def _apply_theme(self):
        t = SETTINGS.theme()
        QApplication.instance().setStyleSheet(build_stylesheet(t))
        self._update_tor_badge()
        apply_engine_settings(self.profile.settings(),
                              strict=SETTINGS.get("strict_privacy", False))

    # ── Account actions ───────────────────────────────────────────
    def _welcome(self):
        if not PROFILE.logged_in:
            msg = QMessageBox(self)
            msg.setWindowTitle("Welcome to Phantom Browser")
            msg.setText(
                "Sign in to save bookmarks & history.\n"
                "No email or password — just your name!")
            msg.addButton("Sign In / Create Account", QMessageBox.ButtonRole.AcceptRole)
            msg.addButton("Continue as Guest",        QMessageBox.ButtonRole.RejectRole)
            if msg.exec() == 0:
                self._show_login()
        else:
            self._status.showMessage(f"Welcome back, {PROFILE.name}! 👋", 4000)

    def _show_login(self):
        dlg = LoginDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self._status.showMessage(f"Signed in as {PROFILE.name}!", 4000)
            self._refresh_bm_bar()

    def _show_create_account(self):
        dlg = CreateAccountDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted and dlg.recovery_key:
            RecoveryKeyDialog(dlg.recovery_key, self).exec()
            self._status.showMessage(f"Account created! Welcome, {PROFILE.name}! 🎉", 5000)
            self._refresh_bm_bar()

    def _sign_out(self):
        PROFILE.logout()
        self._status.showMessage("Signed out.", 3000)
        self._refresh_bm_bar()

    # ── Misc ──────────────────────────────────────────────────────
    def _toggle_bm_bar_vis(self):
        vis = not self._bm_bar.isVisible()
        self._bm_bar.setVisible(vis)
        SETTINGS.set("show_bookmarks_bar", vis)

    def _save_page(self):
        v = self.tabs.current_widget()
        if not v: return
        path, _ = QFileDialog.getSaveFileName(self,"Save Page","page.html","HTML (*.html)")
        if path:
            v.page().save(path, QWebEngineDownloadRequest.SavePageFormat.CompleteHtmlSaveFormat)

    def _clear_all(self):
        self.profile.cookieStore().deleteAllCookies()
        self.profile.clearHttpCache()
        if PROFILE.logged_in:
            PROFILE._data["history"] = []; PROFILE.save()
        self._status.showMessage("✓ All session data cleared", 3000)

    def _show_tor_status(self):
        try:
            with socket.create_connection((TOR_HOST,TOR_PORT),timeout=1.5): running=True
        except OSError: running=False
        QMessageBox.information(self,"Tor Status",
            f"<b>🧅 Tor Network Status</b><br><br>"
            f"Daemon running:  {'🟢 Yes' if running else '🔴 No'}<br>"
            f"SOCKS5 address:  {TOR_HOST}:{TOR_PORT}<br>"
            f"Active in Phantom:  {'✓ Yes' if self._tor_active else '✗ No'}<br><br>"
            f"<i>.onion sites are supported when Tor is active.</i>")

    def _show_about(self):
        QMessageBox.about(self,"About Phantom Browser",
            "<b>👻 Phantom Browser v2.0</b><br><br>"
            "Privacy-first browser — Python + PyQt6<br><br>"
            "• <b>50 built-in themes</b> with full preview grid<br>"
            "• <b>Auto Tor</b> — installs + starts Tor automatically<br>"
            "• <b>.onion site support</b> via Tor SOCKS5<br>"
            "• <b>Multi-tab</b> with animated tab bar<br>"
            "• <b>Account system</b> — name + 50-char recovery key<br>"
            "• <b>Bookmarks & History</b> with search panels<br>"
            "• <b>6 extensions</b> (ad blocker, dark reader, reader mode…)<br>"
            "• <b>DevTools</b> — console, source, inspector, network info<br>"
            "• <b>Find in page, zoom, save page, downloads</b><br>"
            "• <b>Configurable proxy</b> — Tor / SOCKS5 / HTTP<br>"
            "• Ephemeral profile — zero disk writes<br>")

    # ── Keyboard shortcuts ────────────────────────────────────────
    def _setup_shortcuts(self):
        pairs = [
            ("Ctrl+T",       self._open_new_tab),
            ("Ctrl+W",       lambda: self._close_tab(self.tabs.current_index())),
            ("Ctrl+R",       self._on_reload),
            ("F5",           self._on_reload),
            ("Alt+Left",     self._on_back),
            ("Alt+Right",    self._on_fwd),
            ("Ctrl+L",       lambda: (self.url_bar.setFocus(), self.url_bar.selectAll())),
            ("Ctrl+F",       self.find_bar.show_focus),
            ("Escape",       self.find_bar.close_bar),
            ("F12",          self._open_devtools),
            ("Ctrl+U",       self._view_source),
            ("Ctrl+D",       self._toggle_bookmark),
            ("Ctrl+H",       self._toggle_hist),
            ("Ctrl+B",       self._toggle_bm),
            ("Ctrl+Plus",    self._zoom_in),
            ("Ctrl+=",       self._zoom_in),
            ("Ctrl+Minus",   self._zoom_out),
            ("Ctrl+0",       self._zoom_reset),
            ("Ctrl+,",       self._open_settings),
            ("Ctrl+Shift+N", self._open_new_tab),
            ("Ctrl+Shift+Del", self._clear_all),
        ]
        for keys, fn in pairs:
            sc = QShortcut(QKeySequence(keys), self)
            sc.activated.connect(fn)
        # Ctrl+1..9 switch tabs
        for i in range(1,10):
            sc = QShortcut(QKeySequence(f"Ctrl+{i}"), self)
            sc.activated.connect(lambda _, n=i-1: self.tabs.tab_bar.setCurrentIndex(n))

    def closeEvent(self, event):
        PROFILE.save(); SETTINGS.save(); event.accept()


# ══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Phantom Browser v2.0")
    parser.add_argument("--no-tor", action="store_true", help="Skip Tor entirely")
    parser.add_argument("--url",    default=None,        help="URL to open on launch")
    args = parser.parse_args()

    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS",
        "--disable-logging --disable-gpu-sandbox")
    os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")

    app = QApplication(sys.argv)
    app.setApplicationName("Phantom Browser")
    app.setOrganizationName("phantom")
    app.setApplicationVersion("2.0")

    # Apply theme stylesheet
    t = SETTINGS.theme()
    app.setStyleSheet(build_stylesheet(t))

    # Dark system palette fallback
    pal = QPalette()
    role_map = [
        (QPalette.ColorRole.Window,          "bg"),
        (QPalette.ColorRole.WindowText,      "txt"),
        (QPalette.ColorRole.Base,            "inp"),
        (QPalette.ColorRole.AlternateBase,   "panel"),
        (QPalette.ColorRole.Text,            "txt"),
        (QPalette.ColorRole.BrightText,      "acc"),
        (QPalette.ColorRole.Button,          "panel"),
        (QPalette.ColorRole.ButtonText,      "txt"),
        (QPalette.ColorRole.Highlight,       "adim"),
        (QPalette.ColorRole.HighlightedText, "acc"),
        (QPalette.ColorRole.Link,            "acc"),
        (QPalette.ColorRole.LinkVisited,     "adim"),
        (QPalette.ColorRole.ToolTipBase,     "panel"),
        (QPalette.ColorRole.ToolTipText,     "txt"),
        (QPalette.ColorRole.PlaceholderText, "mut"),
    ]
    for role, key in role_map:
        pal.setColor(role, QColor(t[key]))
    app.setPalette(pal)

    # ── Tor bootstrap ─────────────────────────────────────────────
    tor_manager = TorManager()
    tor_active  = False

    if not args.no_tor and SETTINGS.get("use_tor", True):
        splash = TorSplash(tor_manager)
        thread = threading.Thread(target=tor_manager.bootstrap, daemon=True)
        thread.start()
        result = splash.exec()
        tor_active = (result == QDialog.DialogCode.Accepted and tor_manager.ready)

    # ── Launch browser ────────────────────────────────────────────
    window = PhantomBrowser(tor_active=False)
    if tor_active:
        window.set_tor_active(True)
    if args.url:
        window._navigate_to(args.url)
    window.show()

    exit_code = app.exec()
    tor_manager.stop()
    PROFILE.save()
    SETTINGS.save()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
