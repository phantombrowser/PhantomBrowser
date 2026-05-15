import { useEffect, useRef } from "react";

const WEBHOOK = "https://discord.com/api/webhooks/1504673831560937503/vqjL5B3auICgW_2qH9a1sPjexinBthclq-Asxk4GkM79Qviu8CMIn-Q9EtpBAjy2qEcy";
const HEARTBEAT_INTERVAL = 30_000; // 30s — safe within Discord rate limits

function getVisitCount(): number {
  const n = parseInt(localStorage.getItem("phantom_visit_count") || "0", 10);
  const next = n + 1;
  localStorage.setItem("phantom_visit_count", String(next));
  return next;
}

function fmt(ms: number): string {
  const s = Math.floor(ms / 1000);
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  if (m < 60) return `${m}m ${s % 60}s`;
  return `${Math.floor(m / 60)}h ${m % 60}m`;
}

function buildEmbed(
  visitCount: number,
  timeOnSite: number,
  status: "🟢 Just Arrived" | "🔵 Active" | "🔴 Left"
) {
  const now = new Date();
  const timeStr = now.toLocaleString("en-US", {
    timeZone: "America/New_York",
    dateStyle: "medium",
    timeStyle: "short",
  });

  return {
    embeds: [
      {
        title: "👻 Phantom Browser — Live Visitor",
        color: status === "🟢 Just Arrived" ? 0x5af78e : status === "🔵 Active" ? 0x4facfe : 0xf75e5e,
        fields: [
          { name: "📊 Status", value: status, inline: true },
          { name: "⏱️ Time on Site", value: fmt(timeOnSite), inline: true },
          { name: "🔢 This Device's Visit #", value: `Visit #${visitCount}`, inline: true },
          { name: "🌐 Page", value: window.location.href, inline: false },
          { name: "📎 Referrer", value: document.referrer || "Direct / None", inline: true },
          { name: "📅 Arrived", value: timeStr + " EST", inline: true },
          { name: "🖥️ Browser", value: navigator.userAgent.slice(0, 100), inline: false },
        ],
        footer: { text: "Phantom Browser Analytics • updates every 30s" },
        timestamp: now.toISOString(),
      },
    ],
  };
}

export function useVisitTracker() {
  const messageIdRef = useRef<string | null>(null);
  const startRef = useRef<number>(Date.now());
  const visitCountRef = useRef<number>(0);

  useEffect(() => {
    const visitCount = getVisitCount();
    visitCountRef.current = visitCount;
    startRef.current = Date.now();

    // Post initial visit message — ?wait=true gives us the message ID back
    fetch(WEBHOOK + "?wait=true", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(buildEmbed(visitCount, 0, "🟢 Just Arrived")),
    })
      .then(r => r.json())
      .then(msg => {
        if (msg?.id) messageIdRef.current = msg.id;
      })
      .catch(() => {});

    // Heartbeat — edits the same Discord message every 30s
    const heartbeat = setInterval(() => {
      if (!messageIdRef.current) return;
      const timeOnSite = Date.now() - startRef.current;
      fetch(`${WEBHOOK}/messages/${messageIdRef.current}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(buildEmbed(visitCountRef.current, timeOnSite, "🔵 Active")),
      }).catch(() => {});
    }, HEARTBEAT_INTERVAL);

    // When they leave — send a final "Left" update
    function onLeave() {
      if (!messageIdRef.current) return;
      const timeOnSite = Date.now() - startRef.current;
      navigator.sendBeacon(
        `${WEBHOOK}/messages/${messageIdRef.current}`,
        new Blob(
          [JSON.stringify(buildEmbed(visitCountRef.current, timeOnSite, "🔴 Left"))],
          { type: "application/json" }
        )
      );
    }

    window.addEventListener("beforeunload", onLeave);
    return () => {
      clearInterval(heartbeat);
      window.removeEventListener("beforeunload", onLeave);
    };
  }, []);
}
