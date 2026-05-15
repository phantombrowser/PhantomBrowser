import { useEffect } from "react";

const WEBHOOK = "https://discord.com/api/webhooks/1504673831560937503/vqjL5B3auICgW_2qH9a1sPjexinBthclq-Asxk4GkM79Qviu8CMIn-Q9EtpBAjy2qEcy";
const SESSION_KEY = "phantom_visited";

export function useVisitTracker() {
  useEffect(() => {
    if (sessionStorage.getItem(SESSION_KEY)) return;
    sessionStorage.setItem(SESSION_KEY, "1");

    const isReturning = !!localStorage.getItem(SESSION_KEY);
    if (!isReturning) localStorage.setItem(SESSION_KEY, "1");

    const now = new Date();
    const timeStr = now.toLocaleString("en-US", {
      timeZone: "America/New_York",
      dateStyle: "medium",
      timeStyle: "short",
    });

    const payload = {
      embeds: [
        {
          title: "👻 New Phantom Browser Visit",
          color: 0x5af78e,
          fields: [
            { name: "🌐 Page", value: window.location.href, inline: false },
            { name: "📅 Time", value: timeStr + " EST", inline: true },
            { name: "🔁 Visitor", value: isReturning ? "Returning" : "New", inline: true },
            { name: "📎 Referrer", value: document.referrer || "Direct / None", inline: false },
            { name: "🖥️ Browser", value: navigator.userAgent.slice(0, 120), inline: false },
          ],
          footer: { text: "Phantom Browser Analytics" },
          timestamp: now.toISOString(),
        },
      ],
    };

    fetch(WEBHOOK, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).catch(() => {});
  }, []);
}
