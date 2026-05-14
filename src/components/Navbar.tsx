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
      <Link to="/" className="flex items-center gap-3">
        <span className="text-2xl">👻</span>
        <span
          className="font-bold tracking-widest text-white text-sm uppercase"
          style={{ fontFamily: "var(--font-display)" }}
        >
          Phantom
        </span>
      </Link>

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
