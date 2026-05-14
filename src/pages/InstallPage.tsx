import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Navbar } from "../components/Navbar";

export function InstallPage() {
  return (
    <div className="min-h-screen bg-[#04040a] text-white overflow-x-hidden">
      <Navbar />

      {/* Ambient background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-[500px] h-[500px] rounded-full blur-[180px] opacity-6"
          style={{ background: "radial-gradient(circle, #00f5ff, transparent)" }} />
        <div className="absolute bottom-0 right-1/4 w-[400px] h-[400px] rounded-full blur-[160px] opacity-4"
          style={{ background: "radial-gradient(circle, #7c3aed, transparent)" }} />
      </div>

      <div className="relative pt-32 pb-24 px-6 max-w-3xl mx-auto">

        {/* Beta Warning */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-6 p-4 rounded-xl border border-yellow-500/40 flex items-start gap-4"
          style={{ background: "rgba(234,179,8,0.07)" }}
        >
          <span className="text-2xl flex-shrink-0 mt-0.5">⚠️</span>
          <div>
            <p className="font-bold text-yellow-400 text-sm uppercase tracking-widest mb-1" style={{ fontFamily: "var(--font-display)" }}>
              Beta Software — Expect Bugs
            </p>
            <p className="text-yellow-200/70 text-sm leading-relaxed">
              Phantom Browser is currently in <strong className="text-yellow-300">public beta</strong>. You may encounter crashes, incomplete features, or unexpected behavior. We recommend not using it as your primary browser yet.
            </p>
          </div>
        </motion.div>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="mb-12"
        >
          <p className="text-cyan-400 text-xs uppercase tracking-[0.4em] mb-3" style={{ fontFamily: "var(--font-display)" }}>
            Installation Guide
          </p>
          <h1 className="text-5xl font-black tracking-tight mb-4" style={{ fontFamily: "var(--font-display)" }}>
            Get Phantom Browser
          </h1>
          <p className="text-white/50 text-lg leading-relaxed">
            Follow all three steps in order. Each one is required before the next will work.
          </p>
        </motion.div>

        {/* Steps */}
        <div className="flex flex-col gap-6">

          {/* ── STEP 1: Tor ── */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="relative p-6 rounded-2xl border border-white/10 hover:border-cyan-400/25 transition-all duration-300"
            style={{ background: "linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(0,245,255,0.015) 100%)" }}
          >
            <span className="absolute top-4 right-4 px-2 py-0.5 rounded text-xs font-bold bg-red-500/20 border border-red-500/40 text-red-400 uppercase tracking-wider"
              style={{ fontFamily: "var(--font-display)" }}>
              Do This First
            </span>

            <div className="flex items-start gap-5">
              <div className="flex-shrink-0 flex flex-col items-center gap-1">
                <span className="text-3xl">🧅</span>
                <span className="text-xs text-white/20 font-mono">01</span>
              </div>
              <div className="flex-1 min-w-0">
                <h2 className="text-xl font-bold mb-2" style={{ fontFamily: "var(--font-display)" }}>
                  Install Tor Expert Bundle
                </h2>
                <p className="text-white/60 text-sm leading-relaxed mb-4">
                  Phantom Browser routes all traffic through Tor automatically. You must install the Tor Expert Bundle first — without it, Phantom cannot connect to the network.
                </p>
                <a
                  href="https://www.torproject.org/download/tor/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-bold uppercase tracking-wider border border-cyan-400/50 text-cyan-400 bg-cyan-400/10 hover:bg-cyan-400/20 transition-all duration-200"
                  style={{ fontFamily: "var(--font-display)" }}
                >
                  ↗ Download Tor Expert Bundle
                </a>
                <div className="mt-4 p-3 rounded-lg border border-white/8" style={{ background: "rgba(255,255,255,0.03)" }}>
                  <p className="text-white/40 text-xs leading-relaxed">
                    Download the <strong className="text-white/60">Tor Expert Bundle</strong> (not Tor Browser) from the official Tor Project website. Extract and run it before launching Phantom. Keep it running in the background at all times.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* ── STEP 2: PhantomClient ── */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.35 }}
            className="relative rounded-2xl border border-orange-500/30 overflow-hidden"
            style={{ background: "linear-gradient(135deg, rgba(249,115,22,0.06) 0%, rgba(255,255,255,0.02) 100%)" }}
          >
            {/* Windows Defender warning — prominent header bar */}
            <div className="flex items-start gap-3 px-6 py-4 border-b border-orange-500/20" style={{ background: "rgba(249,115,22,0.1)" }}>
              <span className="text-xl flex-shrink-0 mt-0.5">🛡️</span>
              <div>
                <p className="font-bold text-orange-400 text-sm uppercase tracking-widest mb-1" style={{ fontFamily: "var(--font-display)" }}>
                  Windows Defender Will Flag This File
                </p>
                <p className="text-orange-200/70 text-sm leading-relaxed">
                  Windows Defender (and some antivirus software) may quarantine or block <strong className="text-orange-300">PhantomClient.exe</strong> because it is unsigned software. You <strong className="text-orange-300">must temporarily disable Windows Defender</strong> or add an exclusion before downloading and running this file, otherwise it will be deleted on download.
                </p>
              </div>
            </div>

            {/* Defender disable instructions */}
            <div className="px-6 py-4 border-b border-white/8">
              <p className="text-xs font-bold uppercase tracking-widest text-white/40 mb-3" style={{ fontFamily: "var(--font-display)" }}>
                How to disable Windows Defender temporarily
              </p>
              <ol className="flex flex-col gap-2">
                {[
                  "Open Windows Security → Virus & threat protection",
                  'Click "Manage settings" under Virus & threat protection settings',
                  'Toggle "Real-time protection" OFF',
                  "Download and run PhantomClient.exe",
                  "Turn Real-time protection back ON when done",
                ].map((step, i) => (
                  <li key={i} className="flex items-start gap-3 text-xs text-white/50 leading-relaxed">
                    <span className="flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold"
                      style={{ background: "rgba(249,115,22,0.2)", color: "#fb923c", border: "1px solid rgba(249,115,22,0.3)" }}>
                      {i + 1}
                    </span>
                    {step}
                  </li>
                ))}
              </ol>
            </div>

            {/* Download section */}
            <div className="px-6 py-5">
              <div className="flex items-start gap-5">
                <div className="flex-shrink-0 flex flex-col items-center gap-1">
                  <span className="text-3xl">📦</span>
                  <span className="text-xs text-white/20 font-mono">02</span>
                </div>
                <div className="flex-1 min-w-0">
                  <h2 className="text-xl font-bold mb-2" style={{ fontFamily: "var(--font-display)" }}>
                    Download PhantomClient
                  </h2>
                  <p className="text-white/60 text-sm leading-relaxed mb-4">
                    PhantomClient is the companion utility that manages your Tor connection and privacy settings. Run it after disabling Windows Defender.
                  </p>
                  <a
                    href="/PhantomClient.exe"
                    download="PhantomClient.exe"
                    className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-bold uppercase tracking-wider border border-orange-400/50 text-orange-400 bg-orange-400/10 hover:bg-orange-400/20 transition-all duration-200"
                    style={{ fontFamily: "var(--font-display)" }}
                  >
                    ↓ Download PhantomClient.exe
                  </a>
                  <p className="mt-3 text-xs text-white/30 leading-relaxed">
                    Only download from this official page. Run as Administrator if prompted. Re-enable Windows Defender after installation.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* ── STEP 3: Phantom Browser ── */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
            className="relative p-6 rounded-2xl border border-white/10 hover:border-cyan-400/25 transition-all duration-300"
            style={{ background: "linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(0,245,255,0.015) 100%)" }}
          >
            <div className="flex items-start gap-5">
              <div className="flex-shrink-0 flex flex-col items-center gap-1">
                <span className="text-3xl">👻</span>
                <span className="text-xs text-white/20 font-mono">03</span>
              </div>
              <div className="flex-1 min-w-0">
                <h2 className="text-xl font-bold mb-2" style={{ fontFamily: "var(--font-display)" }}>
                  Download Phantom Browser
                </h2>
                <p className="text-white/60 text-sm leading-relaxed mb-4">
                  With Tor running and PhantomClient installed, download the main Phantom Browser. Run the installer and follow the setup wizard.
                </p>
                <a
                  href="/PhantomBrowser.exe"
                  download="PhantomBrowser.exe"
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-bold uppercase tracking-wider border border-cyan-400/50 text-cyan-400 bg-cyan-400/10 hover:bg-cyan-400/20 transition-all duration-200"
                  style={{ fontFamily: "var(--font-display)" }}
                >
                  ↓ Download PhantomBrowser.exe
                </a>
                <div className="mt-4 p-3 rounded-lg border border-white/8" style={{ background: "rgba(255,255,255,0.03)" }}>
                  <p className="text-white/40 text-xs leading-relaxed">
                    Launch Tor first, then PhantomClient, then open Phantom Browser. The browser will detect the Tor connection automatically. You'll see the Tor status indicator at the bottom of the browser window.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>

        </div>

        {/* System requirements */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.7 }}
          className="mt-10 p-6 rounded-2xl border border-white/8"
          style={{ background: "rgba(255,255,255,0.02)" }}
        >
          <h3 className="font-bold text-sm uppercase tracking-widest text-white/70 mb-4" style={{ fontFamily: "var(--font-display)" }}>
            System Requirements
          </h3>
          <div className="grid grid-cols-2 gap-3 text-sm">
            {[
              ["OS", "Windows 10 / 11 (64-bit)"],
              ["RAM", "2 GB minimum, 4 GB recommended"],
              ["Disk", "200 MB free space"],
              ["Network", "Active internet connection"],
              ["Dependencies", "Tor Expert Bundle + PhantomClient"],
              ["Architecture", "x86_64"],
            ].map(([label, value]) => (
              <div key={label} className="flex flex-col gap-0.5">
                <span className="text-white/30 text-xs uppercase tracking-wider" style={{ fontFamily: "var(--font-display)" }}>
                  {label}
                </span>
                <span className="text-white/70">{value}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Back to home */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.9 }}
          className="mt-10 text-center"
        >
          <Link
            to="/"
            className="text-white/30 hover:text-white/60 text-sm transition-colors"
            style={{ fontFamily: "var(--font-display)" }}
          >
            ← Back to Home
          </Link>
        </motion.div>
      </div>
    </div>
  );
}
