import { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";

const VIDEO_DURATION_MS = 26000;

type State = "idle" | "picking" | "recording" | "converting" | "done" | "error";

export function ExportButton() {
  const [state, setState] = useState<State>("idle");
  const [progress, setProgress] = useState(0);
  const [errorMsg, setErrorMsg] = useState("");
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  async function startExport() {
    setState("picking");
    chunksRef.current = [];

    let stream: MediaStream;
    try {
      stream = await navigator.mediaDevices.getDisplayMedia({
        video: { frameRate: 30 },
        audio: false,
        // @ts-expect-error non-standard Chrome hint
        preferCurrentTab: true,
      });
    } catch {
      setState("idle");
      return;
    }

    const mimeType = MediaRecorder.isTypeSupported("video/webm;codecs=vp9")
      ? "video/webm;codecs=vp9"
      : "video/webm";

    const recorder = new MediaRecorder(stream, { mimeType });
    recorderRef.current = recorder;

    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunksRef.current.push(e.data);
    };

    recorder.onstop = async () => {
      stream.getTracks().forEach((t) => t.stop());
      clearInterval(timerRef.current!);
      setState("converting");
      setProgress(0);

      const blob = new Blob(chunksRef.current, { type: mimeType });

      try {
        const res = await fetch("/api/convert-to-mp4", {
          method: "POST",
          headers: { "Content-Type": mimeType },
          body: blob,
        });

        if (!res.ok) throw new Error(`Server error: ${res.status}`);

        const mp4Blob = await res.blob();
        const url = URL.createObjectURL(mp4Blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "phantom-browser-ad.mp4";
        a.click();
        URL.revokeObjectURL(url);
        setState("done");
        setTimeout(() => setState("idle"), 3000);
      } catch (err: any) {
        setErrorMsg(err.message || "Conversion failed");
        setState("error");
        setTimeout(() => setState("idle"), 4000);
      }
    };

    recorder.start(200);
    setState("recording");
    setProgress(0);

    const startTime = Date.now();
    timerRef.current = setInterval(() => {
      const elapsed = Date.now() - startTime;
      setProgress(Math.min((elapsed / VIDEO_DURATION_MS) * 100, 100));
      if (elapsed >= VIDEO_DURATION_MS) {
        clearInterval(timerRef.current!);
        recorder.stop();
      }
    }, 100);
  }

  function cancelRecording() {
    if (recorderRef.current && recorderRef.current.state === "recording") {
      recorderRef.current.stream.getTracks().forEach((t) => t.stop());
      recorderRef.current.stop();
    }
    clearInterval(timerRef.current!);
    setState("idle");
  }

  const label: Record<State, string> = {
    idle: "Export MP4",
    picking: "Select this tab...",
    recording: "Recording...",
    converting: "Converting...",
    done: "Downloaded!",
    error: "Failed — retry?",
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
      <AnimatePresence>
        {state === "recording" && (
          <motion.div
            key="progress"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="flex flex-col items-end gap-2"
          >
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
              <span className="text-xs text-white/70 font-mono">
                {Math.round(progress)}% — {Math.round((VIDEO_DURATION_MS - (progress / 100) * VIDEO_DURATION_MS) / 1000)}s left
              </span>
            </div>
            <div className="w-48 h-1 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-cyan-400 rounded-full"
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.1 }}
              />
            </div>
            <button
              onClick={cancelRecording}
              className="text-xs text-white/40 hover:text-white/70 transition-colors"
            >
              Cancel
            </button>
          </motion.div>
        )}

        {state === "converting" && (
          <motion.div
            key="converting"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-xs text-cyan-400 font-mono flex items-center gap-2"
          >
            <motion.div
              className="w-3 h-3 border border-cyan-400 border-t-transparent rounded-full"
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 0.8, ease: "linear" }}
            />
            Converting to MP4...
          </motion.div>
        )}

        {state === "error" && (
          <motion.div
            key="error"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-xs text-red-400 font-mono max-w-48 text-right"
          >
            {errorMsg}
          </motion.div>
        )}
      </AnimatePresence>

      <motion.button
        onClick={state === "idle" || state === "error" ? startExport : undefined}
        disabled={state === "picking" || state === "recording" || state === "converting"}
        whileHover={state === "idle" ? { scale: 1.05 } : {}}
        whileTap={state === "idle" ? { scale: 0.97 } : {}}
        className={`
          px-4 py-2 rounded-lg text-sm font-mono font-bold
          border transition-all duration-200 select-none
          ${state === "idle" || state === "error"
            ? "bg-cyan-400/10 border-cyan-400/60 text-cyan-400 hover:bg-cyan-400/20 cursor-pointer"
            : state === "done"
              ? "bg-green-400/10 border-green-400/60 text-green-400 cursor-default"
              : "bg-white/5 border-white/20 text-white/40 cursor-default"
          }
        `}
      >
        {state === "done" ? "✓ Downloaded!" : label[state]}
      </motion.button>

      {state === "idle" && (
        <p className="text-[10px] text-white/25 font-mono text-right max-w-44">
          When prompted, select this tab to record
        </p>
      )}
    </div>
  );
}
