import { motion, AnimatePresence } from "framer-motion";
import { useVideoPlayer } from "@/lib/video";
import { Scene1 } from "./video_scenes/Scene1";
import { Scene2 } from "./video_scenes/Scene2";
import { Scene3 } from "./video_scenes/Scene3";
import { Scene4 } from "./video_scenes/Scene4";
import { Scene5 } from "./video_scenes/Scene5";

const SCENE_DURATIONS = {
  intro: 5000,
  tor: 5000,
  duckduckgo: 5000,
  privacy: 5000,
  outro: 6000,
};

export default function VideoTemplate() {
  const { currentScene } = useVideoPlayer({ durations: SCENE_DURATIONS });

  return (
    <div className="relative w-full h-screen overflow-hidden bg-black text-white font-['Inter']">
      <div className="absolute inset-0 z-0">
        <video
          src={`${import.meta.env.BASE_URL}videos/tech-grid.mp4`}
          autoPlay
          loop
          muted
          playsInline
          className="w-full h-full object-cover opacity-30"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-black" />
      </div>

      <AnimatePresence mode="sync">
        {currentScene === 0 && <Scene1 key="intro" />}
        {currentScene === 1 && <Scene2 key="tor" />}
        {currentScene === 2 && <Scene3 key="ddg" />}
        {currentScene === 3 && <Scene4 key="privacy" />}
        {currentScene === 4 && <Scene5 key="outro" />}
      </AnimatePresence>
    </div>
  );
}
