import { useState, useEffect } from "react";
import { motion } from "framer-motion";

export function Scene1() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 500),
      setTimeout(() => setPhase(2), 1500),
      setTimeout(() => setPhase(3), 4000),
    ];
    return () => timers.forEach(t => clearTimeout(t));
  }, []);

  return (
    <motion.div
      className="absolute inset-0 flex flex-col items-center justify-center z-10"
      initial={{ opacity: 0, scale: 1.1 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9, filter: "blur(10px)" }}
      transition={{ duration: 1 }}
    >
      <motion.div
        className="w-[20vw] h-[2px] bg-cyan-400 mb-8 shadow-[0_0_15px_#00ffff]"
        initial={{ scaleX: 0 }}
        animate={phase >= 1 ? { scaleX: 1 } : { scaleX: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      />
      
      <h1 className="text-[6vw] font-black tracking-tighter uppercase font-['JetBrains_Mono'] text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-500">
        Phantom Browser
      </h1>
      
      <motion.p
        className="text-[2vw] text-cyan-400 mt-4 tracking-widest uppercase font-bold"
        initial={{ opacity: 0, y: 20 }}
        animate={phase >= 2 ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
        transition={{ duration: 0.8 }}
      >
        Explore the Dark Web Safely
      </motion.p>
    </motion.div>
  );
}
