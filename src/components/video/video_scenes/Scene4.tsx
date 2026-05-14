import { useState, useEffect } from "react";
import { motion } from "framer-motion";

export function Scene4() {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 200),
      setTimeout(() => setPhase(2), 600),
      setTimeout(() => setPhase(3), 1000),
      setTimeout(() => setPhase(4), 4000),
    ];
    return () => timers.forEach(t => clearTimeout(t));
  }, []);

  return (
    <motion.div
      className="absolute inset-0 flex flex-col items-start justify-center pl-[15vw] z-10"
      initial={{ opacity: 0, x: "-10vw" }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: "10vw", filter: "blur(10px)" }}
      transition={{ duration: 0.8, ease: "easeInOut" }}
    >
      <div className="space-y-6">
        {[
          "Zero Cookies Saved",
          "Trackers Blocked",
          "History In-Session Only",
        ].map((text, i) => (
          <motion.div
            key={text}
            className="flex items-center gap-6"
            initial={{ opacity: 0, x: -30 }}
            animate={phase >= i + 1 ? { opacity: 1, x: 0 } : { opacity: 0, x: -30 }}
            transition={{ type: "spring", stiffness: 300, damping: 25 }}
          >
            <div className="w-[3vw] h-[3vw] rounded-full border-2 border-cyan-400 flex items-center justify-center bg-cyan-400/10 shadow-[0_0_15px_#00ffff_inset]">
              <div className="w-[1vw] h-[1vw] bg-cyan-400 rounded-full" />
            </div>
            <h3 className="text-[3vw] font-['JetBrains_Mono'] font-bold text-white">
              {text}
            </h3>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
