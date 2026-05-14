import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import phantomScreenshot from "@assets/Screenshot_2026-05-14_175428_1778796471296.png";

export function Scene2() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 200),
      setTimeout(() => setPhase(2), 800),
      setTimeout(() => setPhase(3), 4000),
    ];
    return () => timers.forEach(t => clearTimeout(t));
  }, []);

  return (
    <motion.div
      className="absolute inset-0 flex items-center justify-between px-[10vw] z-10"
      initial={{ opacity: 0, x: "10vw" }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: "-10vw", filter: "blur(10px)" }}
      transition={{ duration: 1, ease: "easeInOut" }}
    >
      <div className="w-1/2">
        <motion.h2
          className="text-[4vw] font-bold font-['JetBrains_Mono'] leading-tight mb-4"
          initial={{ opacity: 0, x: -50 }}
          animate={phase >= 1 ? { opacity: 1, x: 0 } : { opacity: 0, x: -50 }}
          transition={{ duration: 0.6 }}
        >
          Integrated Tor Routing
        </motion.h2>
        <motion.p
          className="text-[1.5vw] text-gray-400 max-w-lg"
          initial={{ opacity: 0 }}
          animate={phase >= 2 ? { opacity: 1 } : { opacity: 0 }}
          transition={{ duration: 0.6 }}
        >
          Invisible routing directly in your browser. No extra setup required.
        </motion.p>
      </div>

      <motion.div
        className="w-[40vw] rounded-xl overflow-hidden shadow-[0_0_40px_rgba(0,255,255,0.2)] border border-white/10"
        initial={{ opacity: 0, scale: 0.8, rotateY: 20 }}
        animate={phase >= 1 ? { opacity: 1, scale: 1, rotateY: 0 } : { opacity: 0, scale: 0.8, rotateY: 20 }}
        transition={{ type: "spring", stiffness: 100, damping: 20 }}
        style={{ perspective: 1000 }}
      >
        <img src={phantomScreenshot} alt="App Screenshot" className="w-full h-auto" />
      </motion.div>
    </motion.div>
  );
}
