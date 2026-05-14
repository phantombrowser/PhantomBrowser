import { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Navbar } from "../components/Navbar";

const THEMES: Record<string, Record<string, string>> = {
  "Phantom Dark":   { bg:"#0a0c0f", panel:"#111418", inp:"#181c22", hov:"#1e242c", brd:"#2a3040", acc:"#5af78e", adim:"#2d7a4a", warn:"#f7c948", dng:"#f75e5e", txt:"#d4dde8", mut:"#5a6478", tab_a:"#1e242c", tab_i:"#111418" },
  "Midnight Blue":  { bg:"#090b14", panel:"#0f1320", inp:"#141929", hov:"#1a2035", brd:"#1e2d52", acc:"#4facfe", adim:"#1a5fa8", warn:"#ffd166", dng:"#ef476f", txt:"#cdd9f5", mut:"#4a5b80", tab_a:"#1a2035", tab_i:"#0f1320" },
  "Dracula":        { bg:"#1e1f29", panel:"#282a36", inp:"#21222c", hov:"#343746", brd:"#44475a", acc:"#bd93f9", adim:"#7c5cbf", warn:"#f1fa8c", dng:"#ff5555", txt:"#f8f8f2", mut:"#6272a4", tab_a:"#343746", tab_i:"#282a36" },
  "Nord":           { bg:"#242933", panel:"#2e3440", inp:"#292e3b", hov:"#3b4252", brd:"#434c5e", acc:"#88c0d0", adim:"#5e81ac", warn:"#ebcb8b", dng:"#bf616a", txt:"#eceff4", mut:"#4c566a", tab_a:"#3b4252", tab_i:"#2e3440" },
  "Tokyo Night":    { bg:"#1a1b26", panel:"#16161e", inp:"#1f2335", hov:"#292e42", brd:"#3b4261", acc:"#7aa2f7", adim:"#3d59a1", warn:"#e0af68", dng:"#f7768e", txt:"#a9b1d6", mut:"#565f89", tab_a:"#292e42", tab_i:"#16161e" },
  "Gruvbox Dark":   { bg:"#1d2021", panel:"#282828", inp:"#242424", hov:"#3c3836", brd:"#504945", acc:"#b8bb26", adim:"#6c7121", warn:"#d79921", dng:"#cc241d", txt:"#ebdbb2", mut:"#665c54", tab_a:"#3c3836", tab_i:"#282828" },
  "Cyberpunk":      { bg:"#0d0019", panel:"#120025", inp:"#16002e", hov:"#1f0040", brd:"#3d0070", acc:"#ff0090", adim:"#990055", warn:"#ffe600", dng:"#ff3300", txt:"#f0e6ff", mut:"#6a4a8a", tab_a:"#1f0040", tab_i:"#120025" },
  "Matrix":         { bg:"#000300", panel:"#001200", inp:"#000a00", hov:"#001a00", brd:"#003300", acc:"#00ff41", adim:"#008020", warn:"#88ff00", dng:"#ff3300", txt:"#00cc33", mut:"#005500", tab_a:"#001a00", tab_i:"#001200" },
  "Ocean":          { bg:"#001220", panel:"#001e35", inp:"#001830", hov:"#002745", brd:"#004070", acc:"#00bcd4", adim:"#007c8a", warn:"#ffca28", dng:"#ef5350", txt:"#b2ebf2", mut:"#37626e", tab_a:"#002745", tab_i:"#001e35" },
  "Monokai Pro":    { bg:"#19181a", panel:"#221f22", inp:"#1e1b1e", hov:"#2d2a2e", brd:"#403e41", acc:"#a9dc76", adim:"#5c8a3c", warn:"#ffd866", dng:"#ff6188", txt:"#fcfcfa", mut:"#727072", tab_a:"#2d2a2e", tab_i:"#221f22" },
  "Galaxy":         { bg:"#050011", panel:"#0d0020", inp:"#090018", hov:"#130030", brd:"#220055", acc:"#c77dff", adim:"#7b2fff", warn:"#ffd60a", dng:"#ff4466", txt:"#e8d5ff", mut:"#5a3d80", tab_a:"#130030", tab_i:"#0d0020" },
  "Hacker":         { bg:"#000000", panel:"#0a0a0a", inp:"#050505", hov:"#111111", brd:"#1a1a1a", acc:"#39ff14", adim:"#1a8000", warn:"#ffff00", dng:"#ff0000", txt:"#33ff33", mut:"#1a661a", tab_a:"#111111", tab_i:"#0a0a0a" },
  "Aurora":         { bg:"#050f0f", panel:"#0a1f1f", inp:"#081818", hov:"#102828", brd:"#1a4a4a", acc:"#00ffcc", adim:"#00aa88", warn:"#ffe066", dng:"#ff5252", txt:"#ccffee", mut:"#3a7a6a", tab_a:"#102828", tab_i:"#0a1f1f" },
  "Neon Pink":      { bg:"#0d001a", panel:"#150026", inp:"#110020", hov:"#1f0035", brd:"#3d006a", acc:"#ff00ff", adim:"#990099", warn:"#ffee00", dng:"#ff0044", txt:"#ffe6ff", mut:"#6a006a", tab_a:"#1f0035", tab_i:"#150026" },
  "Slate":          { bg:"#0e1116", panel:"#161b22", inp:"#13181f", hov:"#1f2937", brd:"#30363d", acc:"#58a6ff", adim:"#1f6feb", warn:"#d29922", dng:"#f85149", txt:"#e6edf3", mut:"#484f58", tab_a:"#1f2937", tab_i:"#161b22" },
  "Volcano":        { bg:"#150500", panel:"#220800", inp:"#1c0600", hov:"#300a00", brd:"#5c1500", acc:"#ff4500", adim:"#b83200", warn:"#ffa500", dng:"#ff0000", txt:"#ffe5d0", mut:"#8b3a1a", tab_a:"#300a00", tab_i:"#220800" },
  "Twilight":       { bg:"#0d0d1f", panel:"#151530", inp:"#111128", hov:"#1e1e45", brd:"#2e2e66", acc:"#9b8afb", adim:"#6650cf", warn:"#fbbf24", dng:"#f87171", txt:"#e0dfff", mut:"#5b5888", tab_a:"#1e1e45", tab_i:"#151530" },
  "Deep Sea":       { bg:"#000d1a", panel:"#001a33", inp:"#00152a", hov:"#002244", brd:"#003366", acc:"#00aaff", adim:"#0066cc", warn:"#ffaa00", dng:"#ff4466", txt:"#cce8ff", mut:"#336688", tab_a:"#002244", tab_i:"#001a33" },
  "Retro Terminal": { bg:"#0c0c00", panel:"#141400", inp:"#101000", hov:"#1e1e00", brd:"#3a3a00", acc:"#e8e800", adim:"#999900", warn:"#ff8800", dng:"#ff2200", txt:"#e8e8c0", mut:"#666640", tab_a:"#1e1e00", tab_i:"#141400" },
  "Forest":         { bg:"#0d1a0f", panel:"#142016", inp:"#111c12", hov:"#1c2e1e", brd:"#2d4a2f", acc:"#56ab2f", adim:"#2d6e10", warn:"#f9ca24", dng:"#eb4d4b", txt:"#d4edda", mut:"#4a7a4e", tab_a:"#1c2e1e", tab_i:"#142016" },
};

const THEME_NAMES = Object.keys(THEMES);

interface Tab {
  id: number;
  title: string;
  url: string;
  page: "newtab" | "ddg" | "proton" | "github" | "wiki";
}

let tabIdCounter = 3;

const privacyCards = [
  { icon: "🍪", label: "Cookies", value: "Not Saved" },
  { icon: "📜", label: "History", value: "In-Session" },
  { icon: "💾", label: "Cache", value: "In-Memory" },
  { icon: "🧅", label: "Network", value: "Via Tor" },
  { icon: "🛡️", label: "Trackers", value: "Blocked" },
];

const shortcuts = [
  { label: "🦆 DuckDuckGo", page: "ddg" as const },
  { label: "📧 ProtonMail", page: "proton" as const },
  { label: "🐙 GitHub", page: "github" as const },
  { label: "📖 Wikipedia", page: "wiki" as const },
];

function NewTabPage({ t, onNavigate }: { t: Record<string, string>; onNavigate: (page: Tab["page"], label: string) => void }) {
  const [query, setQuery] = useState("");
  const [torReady, setTorReady] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setTorReady(true), 700);
    return () => clearTimeout(timer);
  }, []);

  function go() {
    const q = query.trim();
    if (!q) return;
    onNavigate("ddg", `DuckDuckGo: ${q}`);
  }

  return (
    <div
      className="flex flex-col items-center justify-center h-full select-none overflow-hidden"
      style={{ background: t.bg, color: t.mut, fontFamily: "'Segoe UI', sans-serif" }}
    >
      <motion.div
        animate={{ y: [0, -12, 0], rotate: [0, 4, 0] }}
        transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
        style={{ fontSize: 56, marginBottom: 8, cursor: "default" }}
      >👻</motion.div>

      <h1 style={{ fontSize: 22, color: t.acc, letterSpacing: 9, textTransform: "uppercase", marginBottom: 4, fontWeight: 300 }}>
        Phantom
      </h1>
      <p style={{ fontSize: 10, letterSpacing: 3, marginBottom: 32 }}>privacy-first browser</p>

      {/* Search bar */}
      <div style={{ width: 520 }}>
        <div
          style={{
            display: "flex", background: t.inp, border: `1.5px solid ${t.brd}`,
            borderRadius: 50, padding: "10px 18px", gap: 10, alignItems: "center",
            boxShadow: "0 8px 32px rgba(0,0,0,.35)",
          }}
        >
          <span style={{ fontSize: 15, color: t.mut }}>🔍</span>
          <input
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === "Enter" && go()}
            placeholder="Search the web or enter a URL…"
            style={{
              flex: 1, background: "none", border: "none", outline: "none",
              color: t.txt, fontSize: 14,
            }}
          />
          <button
            onClick={go}
            style={{
              background: t.acc, color: t.bg, border: "none", borderRadius: 50,
              padding: "6px 16px", cursor: "pointer", fontWeight: "bold", fontSize: 12,
            }}
          >Go</button>
        </div>
      </div>

      {/* Privacy cards */}
      <div style={{ display: "flex", gap: 12, marginTop: 32, flexWrap: "wrap", justifyContent: "center", maxWidth: 580 }}>
        {privacyCards.map(c => (
          <motion.div
            key={c.label}
            whileHover={{ y: -6, borderColor: t.acc }}
            style={{
              background: t.panel, border: `1px solid ${t.brd}`, borderRadius: 12,
              padding: "14px 20px", textAlign: "center", cursor: "default",
              minWidth: 100, transition: "box-shadow .25s",
            }}
          >
            <div style={{ fontSize: 24, marginBottom: 6 }}>{c.icon}</div>
            <div style={{ fontSize: 8, letterSpacing: 2, textTransform: "uppercase", color: t.mut }}>{c.label}</div>
            <div style={{ fontSize: 10, marginTop: 4, color: c.label === "Network" ? (torReady ? t.acc : t.warn) : t.acc, fontWeight: 600 }}>
              {c.label === "Network" ? (torReady ? "Via Tor" : "Connecting…") : c.value}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Shortcuts */}
      <div style={{ display: "flex", gap: 8, marginTop: 22, flexWrap: "wrap", justifyContent: "center" }}>
        {shortcuts.map(s => (
          <motion.button
            key={s.label}
            whileHover={{ scale: 1.05, borderColor: t.acc, color: t.acc }}
            onClick={() => onNavigate(s.page, s.label)}
            style={{
              background: t.panel, border: `1px solid ${t.brd}`, borderRadius: 8,
              padding: "7px 13px", fontSize: 11, color: t.mut, cursor: "pointer",
            }}
          >
            {s.label}
          </motion.button>
        ))}
      </div>
    </div>
  );
}

function SitePage({ page, t }: { page: Tab["page"]; t: Record<string, string> }) {
  const sites: Record<string, { label: string; desc: string; icon: string; color: string }> = {
    ddg:    { label: "DuckDuckGo", desc: "Your search is private. No tracking, no profiling.", icon: "🦆", color: "#de5833" },
    proton: { label: "ProtonMail", desc: "Encrypted email — no one reads your messages but you.", icon: "📧", color: "#6d4aff" },
    github: { label: "GitHub", desc: "Where the world builds software.", icon: "🐙", color: "#ffffff" },
    wiki:   { label: "Wikipedia", desc: "The free encyclopedia anyone can edit.", icon: "📖", color: "#dddddd" },
  };
  const s = sites[page] || sites.ddg;
  return (
    <div
      className="flex flex-col items-center justify-center h-full"
      style={{ background: t.bg, fontFamily: "'Segoe UI', sans-serif" }}
    >
      <div style={{ fontSize: 56, marginBottom: 16 }}>{s.icon}</div>
      <h2 style={{ fontSize: 28, color: s.color, fontWeight: 700, marginBottom: 8 }}>{s.label}</h2>
      <p style={{ color: t.mut, fontSize: 13, maxWidth: 360, textAlign: "center" }}>{s.desc}</p>
      <div style={{ marginTop: 28, padding: "8px 20px", borderRadius: 8, background: t.panel, border: `1px solid ${t.brd}`, fontSize: 11, color: t.acc }}>
        🔒 Routing via Tor — {s.label.toLowerCase()}.com
      </div>
      <p style={{ marginTop: 12, fontSize: 10, color: t.mut, letterSpacing: 1 }}>
        (simulation only — no actual connection made)
      </p>
    </div>
  );
}

export function PreviewPage() {
  const [themeName, setThemeName] = useState("Phantom Dark");
  const [themeOpen, setThemeOpen] = useState(false);
  const [tabs, setTabs] = useState<Tab[]>([
    { id: 1, title: "New Tab", url: "phantom://newtab", page: "newtab" },
    { id: 2, title: "DuckDuckGo", url: "duckduckgo.com", page: "ddg" },
  ]);
  const [activeTab, setActiveTab] = useState(1);
  const [urlInput, setUrlInput] = useState("phantom://newtab");
  const [urlFocused, setUrlFocused] = useState(false);
  const [torStatus] = useState<"connected" | "connecting">("connected");
  const themeRef = useRef<HTMLDivElement>(null);

  const t = THEMES[themeName] ?? THEMES["Phantom Dark"];
  const currentTab = tabs.find(tab => tab.id === activeTab);

  useEffect(() => {
    if (currentTab) setUrlInput(currentTab.url);
  }, [activeTab, currentTab?.url]);

  useEffect(() => {
    function handler(e: MouseEvent) {
      if (themeRef.current && !themeRef.current.contains(e.target as Node)) {
        setThemeOpen(false);
      }
    }
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  function addTab() {
    const id = ++tabIdCounter;
    setTabs(prev => [...prev, { id, title: "New Tab", url: "phantom://newtab", page: "newtab" }]);
    setActiveTab(id);
  }

  function closeTab(id: number, e: React.MouseEvent) {
    e.stopPropagation();
    const idx = tabs.findIndex(t => t.id === id);
    const newTabs = tabs.filter(t => t.id !== id);
    if (newTabs.length === 0) {
      addTab();
      return;
    }
    setTabs(newTabs);
    if (activeTab === id) {
      const newIdx = Math.min(idx, newTabs.length - 1);
      setActiveTab(newTabs[newIdx].id);
    }
  }

  function navigate(page: Tab["page"], label: string) {
    const urlMap: Record<string, string> = {
      ddg: "duckduckgo.com",
      proton: "protonmail.com",
      github: "github.com",
      wiki: "wikipedia.org",
      newtab: "phantom://newtab",
    };
    setTabs(prev => prev.map(tab =>
      tab.id === activeTab ? { ...tab, page, title: label, url: urlMap[page] } : tab
    ));
    setUrlInput(urlMap[page]);
  }

  function handleUrlGo() {
    const q = urlInput.trim();
    if (!q) return;
    if (q === "phantom://newtab") { navigate("newtab", "New Tab"); return; }
    if (q.includes("duckduckgo")) { navigate("ddg", "DuckDuckGo"); return; }
    if (q.includes("protonmail")) { navigate("proton", "ProtonMail"); return; }
    if (q.includes("github")) { navigate("github", "GitHub"); return; }
    if (q.includes("wikipedia")) { navigate("wiki", "Wikipedia"); return; }
    navigate("ddg", `DuckDuckGo: ${q}`);
  }

  return (
    <div className="min-h-screen bg-[#04040a] text-white overflow-x-hidden">
      <Navbar />

      <div className="pt-24 pb-16 px-6">
        {/* Page header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          className="text-center mb-10 max-w-2xl mx-auto"
        >
          <p className="text-cyan-400 text-xs uppercase tracking-[0.4em] mb-3" style={{ fontFamily: "var(--font-display)" }}>
            Interactive Demo
          </p>
          <h1 className="text-4xl md:text-5xl font-black tracking-tight mb-4" style={{ fontFamily: "var(--font-display)" }}>
            Try Phantom Browser
          </h1>
          <p className="text-white/50 text-base">
            A live simulation of the actual browser UI. Switch themes, open tabs, and explore the interface.
          </p>
        </motion.div>

        {/* Browser Window */}
        <motion.div
          initial={{ opacity: 0, y: 40, scale: 0.97 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.9, ease: [0.16, 1, 0.3, 1] }}
          className="max-w-5xl mx-auto rounded-xl overflow-hidden shadow-[0_0_100px_rgba(0,245,255,0.07)]"
          style={{ border: `1px solid ${t.brd}` }}
        >
          {/* Title bar */}
          <div
            className="flex items-center gap-3 px-4 py-2.5 select-none"
            style={{ background: t.panel, borderBottom: `1px solid ${t.brd}` }}
          >
            {/* Traffic lights */}
            <div className="flex items-center gap-1.5">
              <div className="w-3 h-3 rounded-full bg-[#ff5f57] cursor-pointer hover:opacity-80" title="Close" />
              <div className="w-3 h-3 rounded-full bg-[#ffbd2e] cursor-pointer hover:opacity-80" title="Minimize" />
              <div className="w-3 h-3 rounded-full bg-[#28ca41] cursor-pointer hover:opacity-80" title="Maximize" />
            </div>
            <span className="text-xs mx-auto" style={{ color: t.mut, fontFamily: "var(--font-display)", letterSpacing: 2 }}>
              👻 PHANTOM BROWSER v2.0
            </span>

            {/* Theme picker */}
            <div ref={themeRef} className="relative">
              <button
                onClick={() => setThemeOpen(o => !o)}
                className="flex items-center gap-1.5 px-2.5 py-1 rounded text-xs transition-all"
                style={{ background: t.inp, border: `1px solid ${t.brd}`, color: t.mut, fontFamily: "var(--font-display)" }}
              >
                <span style={{ width: 8, height: 8, borderRadius: "50%", background: t.acc, display: "inline-block" }} />
                {themeName}
                <span style={{ opacity: 0.5 }}>▾</span>
              </button>
              <AnimatePresence>
                {themeOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -6, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: -6, scale: 0.95 }}
                    transition={{ duration: 0.15 }}
                    className="absolute right-0 top-full mt-1 z-50 rounded-lg overflow-y-auto"
                    style={{
                      background: t.panel, border: `1px solid ${t.brd}`,
                      maxHeight: 240, width: 180,
                      boxShadow: "0 16px 40px rgba(0,0,0,0.6)",
                    }}
                  >
                    {THEME_NAMES.map(name => (
                      <button
                        key={name}
                        onClick={() => { setThemeName(name); setThemeOpen(false); }}
                        className="w-full flex items-center gap-2 px-3 py-2 text-left text-xs hover:opacity-80 transition-opacity"
                        style={{
                          background: name === themeName ? t.hov : "transparent",
                          color: name === themeName ? t.acc : t.mut,
                          fontFamily: "var(--font-display)",
                        }}
                      >
                        <span style={{ width: 8, height: 8, borderRadius: "50%", background: THEMES[name]?.acc, flexShrink: 0, display: "inline-block" }} />
                        {name}
                      </button>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Tab bar */}
          <div
            className="flex items-end overflow-x-auto gap-px px-2 pt-2"
            style={{ background: t.bg, borderBottom: `1px solid ${t.brd}` }}
          >
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className="flex items-center gap-2 px-4 py-2 rounded-t text-xs transition-all max-w-[160px] group flex-shrink-0"
                style={{
                  background: tab.id === activeTab ? t.tab_a : t.tab_i,
                  color: tab.id === activeTab ? t.txt : t.mut,
                  borderTop: tab.id === activeTab ? `2px solid ${t.acc}` : "2px solid transparent",
                  fontFamily: "var(--font-display)",
                }}
              >
                <span className="truncate flex-1 text-left">{tab.title}</span>
                <span
                  onClick={e => closeTab(tab.id, e)}
                  className="opacity-0 group-hover:opacity-60 hover:!opacity-100 transition-opacity leading-none text-sm"
                >×</span>
              </button>
            ))}
            <button
              onClick={addTab}
              className="mb-0 px-3 py-2 text-sm rounded-t transition-all hover:opacity-80 flex-shrink-0"
              style={{ color: t.mut, background: "transparent" }}
              title="New Tab"
            >+</button>
          </div>

          {/* Toolbar */}
          <div
            className="flex items-center gap-2 px-3 py-2"
            style={{ background: t.panel, borderBottom: `1px solid ${t.brd}` }}
          >
            {/* Nav buttons */}
            {["←", "→", "↻", "⌂"].map((btn, i) => (
              <button
                key={i}
                onClick={() => i === 3 && navigate("newtab", "New Tab")}
                className="w-7 h-7 flex items-center justify-center rounded text-sm transition-all hover:opacity-80"
                style={{ background: t.hov, color: t.mut }}
                title={["Back", "Forward", "Reload", "Home"][i]}
              >{btn}</button>
            ))}

            {/* URL bar */}
            <div
              className="flex-1 flex items-center gap-2 px-3 py-1.5 rounded-lg"
              style={{
                background: t.inp,
                border: `1px solid ${urlFocused ? t.acc : t.brd}`,
                boxShadow: urlFocused ? `0 0 0 2px ${t.adim}44` : "none",
                transition: "all 0.2s",
              }}
            >
              <span style={{ color: t.acc, fontSize: 12 }}>🔒</span>
              <input
                value={urlInput}
                onChange={e => setUrlInput(e.target.value)}
                onFocus={() => setUrlFocused(true)}
                onBlur={() => setUrlFocused(false)}
                onKeyDown={e => e.key === "Enter" && handleUrlGo()}
                className="flex-1 bg-transparent outline-none text-xs"
                style={{ color: t.txt, fontFamily: "var(--font-display)" }}
              />
            </div>

            {/* Tor badge */}
            <div
              className="flex items-center gap-1.5 px-2 py-1 rounded text-xs"
              style={{ background: t.inp, border: `1px solid ${torStatus === "connected" ? t.acc : t.warn}`, color: torStatus === "connected" ? t.acc : t.warn, fontFamily: "var(--font-display)" }}
            >
              <span>🧅</span>
              <span>{torStatus === "connected" ? "Tor" : "..."}</span>
            </div>

            {/* Menu button */}
            <button
              className="w-7 h-7 flex items-center justify-center rounded text-sm hover:opacity-80"
              style={{ background: t.hov, color: t.mut }}
            >☰</button>
          </div>

          {/* Content area */}
          <div style={{ height: 420, background: t.bg, overflow: "hidden" }}>
            <AnimatePresence mode="wait">
              <motion.div
                key={`${activeTab}-${currentTab?.page}`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.18 }}
                style={{ height: "100%" }}
              >
                {currentTab?.page === "newtab" ? (
                  <NewTabPage t={t} onNavigate={navigate} />
                ) : (
                  <SitePage page={currentTab?.page ?? "ddg"} t={t} />
                )}
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Status bar */}
          <div
            className="flex items-center justify-between px-3 py-1.5"
            style={{ background: t.panel, borderTop: `1px solid ${t.brd}` }}
          >
            <div className="flex items-center gap-3">
              <span className="text-xs" style={{ color: t.acc, fontFamily: "var(--font-display)" }}>
                🧅 Tor Connected
              </span>
              <span className="text-xs" style={{ color: t.mut, fontFamily: "var(--font-display)" }}>
                🍪 0 cookies
              </span>
              <span className="text-xs" style={{ color: t.mut, fontFamily: "var(--font-display)" }}>
                🛡️ 12 trackers blocked
              </span>
            </div>
            <span className="text-xs" style={{ color: t.mut, fontFamily: "var(--font-display)" }}>
              Phantom Browser v2.0 — beta
            </span>
          </div>
        </motion.div>

        {/* CTA below */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.7 }}
          className="text-center mt-12"
        >
          <p className="text-white/40 text-sm mb-4">Ready to browse for real?</p>
          <Link
            to="/install"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg font-bold text-sm uppercase tracking-widest bg-cyan-400 text-black hover:bg-cyan-300 transition-all duration-200 shadow-[0_0_30px_rgba(0,245,255,0.25)]"
            style={{ fontFamily: "var(--font-display)" }}
          >
            👻 Download Phantom Browser
          </Link>
        </motion.div>
      </div>
    </div>
  );
}
