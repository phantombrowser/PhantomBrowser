import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "path";
import { IncomingMessage, ServerResponse } from "http";
import { spawn } from "child_process";
import { mkdirSync, createWriteStream, existsSync } from "fs";
import { tmpdir } from "os";
import { join } from "path";
import { randomUUID } from "crypto";

const port = Number(process.env.PORT || 5000);
const basePath = process.env.BASE_PATH || "/";

function convertPlugin() {
  return {
    name: "mp4-convert",
    configureServer(server: any) {
      server.middlewares.use(
        "/api/convert-to-mp4",
        async (req: IncomingMessage, res: ServerResponse) => {
          if (req.method !== "POST") {
            res.statusCode = 405;
            res.end("Method Not Allowed");
            return;
          }

          const id = randomUUID();
          const tmpDir = join(tmpdir(), "phantom-export");
          mkdirSync(tmpDir, { recursive: true });
          const inputPath = join(tmpDir, `${id}.webm`);
          const outputPath = join(tmpDir, `${id}.mp4`);

          // Write incoming body to file
          await new Promise<void>((resolve, reject) => {
            const writeStream = createWriteStream(inputPath);
            req.pipe(writeStream);
            writeStream.on("finish", resolve);
            writeStream.on("error", reject);
          });

          // Convert with FFmpeg
          await new Promise<void>((resolve, reject) => {
            const ff = spawn("ffmpeg", [
              "-y",
              "-i", inputPath,
              "-c:v", "libx264",
              "-preset", "fast",
              "-crf", "18",
              "-pix_fmt", "yuv420p",
              "-movflags", "+faststart",
              outputPath,
            ]);
            ff.on("close", (code) => {
              if (code === 0) resolve();
              else reject(new Error(`FFmpeg exited with code ${code}`));
            });
          });

          // Stream MP4 back
          const { createReadStream, statSync } = await import("fs");
          const stat = statSync(outputPath);
          res.setHeader("Content-Type", "video/mp4");
          res.setHeader("Content-Disposition", 'attachment; filename="phantom-browser-ad.mp4"');
          res.setHeader("Content-Length", stat.size);
          createReadStream(outputPath).pipe(res);
        }
      );
    },
  };
}

export default defineConfig({
  base: basePath,
  plugins: [
    react(),
    tailwindcss(),
    convertPlugin(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "src"),
      "@assets": path.resolve(import.meta.dirname, "attached_assets"),
    },
    dedupe: ["react", "react-dom", "framer-motion"],
  },
  root: path.resolve(import.meta.dirname),
  build: {
    outDir: path.resolve(import.meta.dirname, "dist"),
    emptyOutDir: true,
  },
  server: {
    port,
    strictPort: true,
    host: "0.0.0.0",
    allowedHosts: true,
  },
  preview: {
    port,
    host: "0.0.0.0",
    allowedHosts: true,
  },
});
