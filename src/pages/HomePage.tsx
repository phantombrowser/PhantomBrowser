import { useRef } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Navbar } from "../components/Navbar";
import VideoTemplate from "../components/video/VideoTemplate";
import phantomScreenshot from "@assets/Screenshot_2026-05-14_175428_1778796471296.png";

const features = [
  {
    icon: "🧅",
    title: "Tor Network Built-In",
    desc: "Every request routes through Tor automatically. No extra setup, no leaks. Just open Phantom and browse.",
  },
  {
    icon: "🔍",
    title: "DuckDuckGo by Default",
    desc: "Search without being tracked or profiled. DuckDuckGo is baked in as the default engine — no switching required.",
  },
  {
    icon: "🍪",
    title: "Zero Cookies Saved",
    desc: "Cookies never persist between sessions. Every time you close Phantom, your trail vanishes completely.",
  },
  {
    icon: "🛡️",
    title: "Trackers Blocked",
    desc: "Built-in tracker blocking stops surveillance networks, fingerprinting scripts, and ad networks cold.",
  },
  {
    icon: "🧠",
    title: "In-Memory Cache",
    desc: "Nothing is written to disk. History, cache, and session data live only in RAM and disappear on exit.",
  },
  {
    icon: "🌐",
    title: ".onion Sites Supported",
    desc: "Natively browse hidden services and .onion addresses without any configuration or bridge setup.",
  },
];

export function HomePage() {
  const featuresRef = useRef<HTMLDivElement>(null);

  function scrollToFeatures() {
    featuresRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  return (
    <div className="min-h-screen bg-[#04040a] text-white overflow-x-hidden">
      <Navbar />

      {/* Hero — full-screen animated intro */}
      <section className="relative h-screen">
        <VideoTemplate />

        {/* Scroll CTA overlaid at the bottom */}
        <div className="absolute bottom-10 left-0 right-0 flex flex-col items-center gap-3 z-30">
          <motion.button
            onClick={scrollToFeatures}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 2, duration: 0.8 }}
            className="flex flex-col items-center gap-2 text-white/40 hover:text-white/70 transition-colors cursor-pointer group"
          >
            <span className="text-xs uppercase tracking-widest" style={{ fontFamily: "var(--font-display)" }}>
              Discover More
            </span>
            <motion.div
              animate={{ y: [0, 6, 0] }}
              transition={{ repeat: Infinity, duration: 1.6, ease: "easeInOut" }}
              className="text-cyan-400/60 group-hover:text-cyan-400"
            >
              ↓
            </motion.div>
          </motion.button>
        </div>
      </section>

      {/* Features section */}
      <section
        ref={featuresRef}
        className="relative py-32 px-6"
        style={{ background: "linear-gradient(to bottom, #04040a 0%, #080c14 100%)" }}
      >
        {/* Ambient glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] rounded-full blur-[120px] opacity-10"
          style={{ background: "radial-gradient(circle, #00f5ff, transparent)" }} />

        <div className="relative max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-20"
          >
            <p className="text-cyan-400 text-xs uppercase tracking-[0.4em] mb-4" style={{ fontFamily: "var(--font-display)" }}>
              Built for anonymity
            </p>
            <h2 className="text-5xl md:text-6xl font-black tracking-tight" style={{ fontFamily: "var(--font-display)" }}>
              Why Phantom?
            </h2>
            <p className="mt-6 text-white/50 text-lg max-w-xl mx-auto">
              Most browsers claim privacy. Phantom was built from the ground up to deliver it — no compromises, no toggles to flip.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: i * 0.08 }}
                className="relative p-6 rounded-xl border border-white/8 group hover:border-cyan-400/30 transition-all duration-300"
                style={{ background: "linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(0,245,255,0.02) 100%)" }}
              >
                <div className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"
                  style={{ background: "linear-gradient(135deg, rgba(0,245,255,0.04) 0%, transparent 100%)" }} />
                <span className="text-3xl mb-4 block">{f.icon}</span>
                <h3 className="font-bold text-lg mb-2 text-white" style={{ fontFamily: "var(--font-display)" }}>
                  {f.title}
                </h3>
                <p className="text-white/50 text-sm leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Screenshot showcase */}
      <section className="py-24 px-6" style={{ background: "#080c14" }}>
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl font-black tracking-tight" style={{ fontFamily: "var(--font-display)" }}>
              Clean. Dark. Focused.
            </h2>
            <p className="mt-4 text-white/50">A browser that gets out of your way.</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            whileInView={{ opacity: 1, scale: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 1, ease: [0.16, 1, 0.3, 1] }}
            className="relative rounded-2xl overflow-hidden border border-white/10 shadow-[0_0_80px_rgba(0,245,255,0.08)]"
          >
            <img src={phantomScreenshot} alt="Phantom Browser interface" className="w-full h-auto" />
            <div className="absolute inset-0 pointer-events-none"
              style={{ boxShadow: "inset 0 0 60px rgba(0,0,0,0.4)" }} />
          </motion.div>
        </div>
      </section>

      {/* CTA section */}
      <section className="py-32 px-6 text-center relative overflow-hidden" style={{ background: "#04040a" }}>
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="w-[800px] h-[400px] rounded-full blur-[150px] opacity-8"
            style={{ background: "radial-gradient(circle, #00f5ff, transparent)" }} />
        </div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="relative max-w-2xl mx-auto"
        >
          <p className="text-cyan-400 text-xs uppercase tracking-[0.4em] mb-4" style={{ fontFamily: "var(--font-display)" }}>
            Ready to disappear?
          </p>
          <h2 className="text-5xl md:text-6xl font-black tracking-tight mb-6" style={{ fontFamily: "var(--font-display)" }}>
            Start browsing<br />with confidence.
          </h2>
          <p className="text-white/40 mb-10 text-lg">
            Free. Open. Private. No accounts, no data collection, no compromise.
          </p>
          <Link
            to="/install"
            className="inline-flex items-center gap-3 px-8 py-4 rounded-xl font-bold text-sm uppercase tracking-widest bg-cyan-400 text-black hover:bg-cyan-300 transition-all duration-200 shadow-[0_0_40px_rgba(0,245,255,0.3)]"
            style={{ fontFamily: "var(--font-display)" }}
          >
            <span>👻</span>
            Get Phantom Browser
          </Link>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/8 py-8 px-6 text-center text-white/30 text-xs" style={{ fontFamily: "var(--font-display)" }}>
        <p>Phantom Browser — Privacy-First Browsing • Currently in Beta</p>
      </footer>
    </div>
  );
}
