import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import phantomScreenshot from "@assets/Screenshot_2026-05-14_175428_1778796471296.png";

export function Scene5() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 500),
      setTimeout(() => setPhase(2), 2000),
      setTimeout(() => setPhase(3), 5000),
    ];
    return () => timers.forEach(t => clearTimeout(t));
  }, []);

  return (
    <motion.div
      className="absolute inset-0 flex flex-col items-center justify-center bg-black z-10"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1 }}
    >
      <motion.div
        className="absolute inset-0 opacity-10"
        initial={{ scale: 1.2 }}
        animate={{ scale: 1 }}
        transition={{ duration: 5 }}
      >
        <img src={phantomScreenshot} alt="Background" className="w-full h-full object-cover" />
      </motion.div>

      <motion.h1
        className="text-[4.5vw] font-black font-['Inter'] text-center max-w-[80vw] leading-tight z-20"
        initial={{ opacity: 0, y: 30 }}
        animate={phase >= 1 ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
        transition={{ duration: 1 }}
      >
        "Privacy isn't a feature.
        <br />
        <span className="text-cyan-400">It's the foundation."</span>
      </motion.h1>

      <motion.div
        className="mt-12 text-[1.5vw] font-['JetBrains_Mono'] text-gray-400 z-20"
        initial={{ opacity: 0 }}
        animate={phase >= 2 ? { opacity: 1 } : { opacity: 0 }}
        transition={{ duration: 1 }}
      >
        Phantom Browser v2.0
      </motion.div>
    </motion.div>
  );
}
