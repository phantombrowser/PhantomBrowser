import { Link, useLocation } from "react-router-dom";
import { motion } from "framer-motion";

const links = [
  { to: "/", label: "Home" },
  { to: "/preview", label: "Preview" },
  { to: "/install", label: "Install" },
];

export function Navbar() {
  const { pathname } = useLocation();

  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.3 }}
      className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-8 py-4"
      style={{ background: "linear-gradient(to bottom, rgba(0,0,0,0.85) 0%, transparent 100%)" }}
    >
      <Link to="/" className="flex items-center gap-3 group">
        <div className="relative flex items-center justify-center">
          {/* animated glow ring */}
          <span
            className="absolute inset-0 rounded-full"
            style={{
              background: "radial-gradient(circle, rgba(90,247,142,0.35) 0%, transparent 70%)",
              animation: "ghostPulse 2.4s ease-in-out infinite",
            }}
          />
          <img
            src="/ghost-logo.png"
            alt="Phantom"
            className="relative w-10 h-10 object-contain"
            style={{
              filter: "drop-shadow(0 0 8px rgba(90,247,142,0.7)) drop-shadow(0 0 2px rgba(0,245,255,0.4))",
              animation: "ghostFloat 3s ease-in-out infinite",
            }}
          />
        </div>
        <span
          className="font-bold tracking-widest text-white text-sm uppercase"
          style={{ fontFamily: "var(--font-display)" }}
        >
          Phantom
        </span>
      </Link>

      <style>{`
        @keyframes ghostFloat {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-3px); }
        }
        @keyframes ghostPulse {
          0%, 100% { transform: scale(0.9); opacity: 0.5; }
          50% { transform: scale(1.4); opacity: 1; }
        }
      `}</style>

      <div className="flex items-center gap-6">
        {links.map(({ to, label }) => (
          <Link
            key={to}
            to={to}
            className={`text-sm tracking-wider uppercase transition-colors ${
              pathname === to ? "text-cyan-400" : "text-white/50 hover:text-white"
            }`}
            style={{ fontFamily: "var(--font-display)" }}
          >
            {label}
          </Link>
        ))}
        <Link
          to="/install"
          className="px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-widest border border-cyan-400/60 text-cyan-400 bg-cyan-400/10 hover:bg-cyan-400/20 transition-all"
          style={{ fontFamily: "var(--font-display)" }}
        >
          Download
        </Link>
      </div>
    </motion.nav>
  );
}
