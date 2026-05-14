import { useState, useEffect } from "react";
import { motion } from "framer-motion";

export function Scene3() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 300),
      setTimeout(() => setPhase(2), 1000),
      setTimeout(() => setPhase(3), 4000),
    ];
    return () => timers.forEach(t => clearTimeout(t));
  }, []);

  return (
    <motion.div
      className="absolute inset-0 flex flex-col items-center justify-center z-10"
      initial={{ opacity: 0, scale: 0.5, rotate: -5 }}
      animate={{ opacity: 1, scale: 1, rotate: 0 }}
      exit={{ opacity: 0, scale: 1.5, filter: "blur(20px)" }}
      transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
    >
      <motion.h2
        className="text-[5vw] font-black font-['JetBrains_Mono'] text-white"
        initial={{ y: 50, opacity: 0 }}
        animate={phase >= 1 ? { y: 0, opacity: 1 } : { y: 50, opacity: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      >
        DuckDuckGo
      </motion.h2>

      <motion.div
        className="flex gap-8 mt-8 text-[1.8vw] text-cyan-400 font-bold uppercase tracking-wider"
        initial={{ opacity: 0 }}
        animate={phase >= 2 ? { opacity: 1 } : { opacity: 0 }}
        transition={{ duration: 1 }}
      >
        <span>No Tracking</span>
        <span>•</span>
        <span>No Profiling</span>
      </motion.div>
    </motion.div>
  );
}
