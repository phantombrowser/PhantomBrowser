import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Navbar } from "../components/Navbar";

const steps = [
  {
    num: "01",
    icon: "🧅",
    title: "Install Tor First",
    required: true,
    desc: "Phantom Browser integrates directly with Tor to route all traffic anonymously. You must install the Tor Expert Bundle before Phantom can connect.",
    action: {
      label: "Download Tor Expert Bundle",
      href: "https://www.torproject.org/download/tor/",
      external: true,
    },
    note: "Download the Tor Expert Bundle (not Tor Browser) from the official Tor Project website. Run it before launching Phantom Browser.",
  },
  {
    num: "02",
    icon: "👻",
    title: "Download Phantom Browser",
    required: false,
    desc: "Download the Phantom Browser installer for Windows. Run the .exe and follow the setup wizard to complete installation.",
    action: {
      label: "Download PhantomBrowser.exe",
      href: "/PhantomBrowser.exe",
      external: false,
      download: "PhantomBrowser.exe",
    },
    note: "Windows only at this time. macOS and Linux builds are in development.",
  },
  {
    num: "03",
    icon: "▶️",
    title: "Launch & Browse",
    required: false,
    desc: "Start Tor first, then open Phantom Browser. It will detect the Tor connection automatically and route all traffic through it.",
    note: "Make sure Tor is running in the background before you open Phantom. You'll see the Tor status indicator in the bottom right of the browser.",
  },
];

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
          className="mb-10 p-4 rounded-xl border border-yellow-500/40 bg-yellow-500/8 flex items-start gap-4"
        >
          <span className="text-2xl flex-shrink-0 mt-0.5">⚠️</span>
          <div>
            <p className="font-bold text-yellow-400 text-sm uppercase tracking-widest mb-1" style={{ fontFamily: "var(--font-display)" }}>
              Beta Software — Expect Bugs
            </p>
            <p className="text-yellow-200/70 text-sm leading-relaxed">
              Phantom Browser is currently in <strong className="text-yellow-300">public beta</strong>. You may encounter crashes, incomplete features, or unexpected behavior. We recommend not using it as your primary browser yet. Bug reports and feedback are welcome.
            </p>
          </div>
        </motion.div>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          className="mb-16"
        >
          <p className="text-cyan-400 text-xs uppercase tracking-[0.4em] mb-3" style={{ fontFamily: "var(--font-display)" }}>
            Installation Guide
          </p>
          <h1 className="text-5xl font-black tracking-tight mb-4" style={{ fontFamily: "var(--font-display)" }}>
            Get Phantom Browser
          </h1>
          <p className="text-white/50 text-lg leading-relaxed">
            Phantom Browser requires Tor to be installed and running to function. Follow these steps in order.
          </p>
        </motion.div>

        {/* Steps */}
        <div className="flex flex-col gap-6">
          {steps.map((step, i) => (
            <motion.div
              key={step.num}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 + i * 0.15 }}
              className="relative p-6 rounded-2xl border border-white/10 hover:border-cyan-400/25 transition-all duration-300"
              style={{ background: "linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(0,245,255,0.015) 100%)" }}
            >
              {/* Required badge */}
              {step.required && (
                <span className="absolute top-4 right-4 px-2 py-0.5 rounded text-xs font-bold bg-red-500/20 border border-red-500/40 text-red-400 uppercase tracking-wider"
                  style={{ fontFamily: "var(--font-display)" }}>
                  Required First
                </span>
              )}

              <div className="flex items-start gap-5">
                <div className="flex-shrink-0 flex flex-col items-center gap-1">
                  <span className="text-3xl">{step.icon}</span>
                  <span className="text-xs text-white/20 font-mono">{step.num}</span>
                </div>

                <div className="flex-1 min-w-0">
                  <h2 className="text-xl font-bold mb-2" style={{ fontFamily: "var(--font-display)" }}>
                    {step.title}
                  </h2>
                  <p className="text-white/60 text-sm leading-relaxed mb-4">
                    {step.desc}
                  </p>

                  {step.action && (
                    <a
                      href={step.action.href}
                      target={step.action.external ? "_blank" : undefined}
                      rel={step.action.external ? "noopener noreferrer" : undefined}
                      download={step.action.download}
                      className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-bold uppercase tracking-wider border border-cyan-400/50 text-cyan-400 bg-cyan-400/10 hover:bg-cyan-400/20 transition-all duration-200"
                      style={{ fontFamily: "var(--font-display)" }}
                    >
                      {step.action.external ? "↗" : "↓"} {step.action.label}
                    </a>
                  )}

                  <div className="mt-4 p-3 rounded-lg bg-white/3 border border-white/8">
                    <p className="text-white/40 text-xs leading-relaxed">{step.note}</p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
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
              ["Dependency", "Tor Expert Bundle (required)"],
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
