const { bundle } = require("@remotion/bundler");
const { renderMedia, selectComposition } = require("@remotion/renderer");
const path = require("path");
const fs = require("fs");

const QUEUE_DIR = path.join(__dirname, "queue/1_gambar_ready");
const OUTPUT_DIR = path.join(__dirname, "output/videos");

async function startRender() {
  if (!fs.existsSync(QUEUE_DIR)) return;
  const files = fs.readdirSync(QUEUE_DIR).filter((f) => f.endsWith(".json"));

  if (files.length === 0) {
    console.log("[Remotion] Tidak ada file antrean untuk dirender.");
    return;
  }

  console.log("[Remotion] Memulai bundling komponen React...");
  const bundled = await bundle(path.join(__dirname, "remotion/index.ts"));

  for (const file of files) {
    const jsonPath = path.join(QUEUE_DIR, file);
    const rawData = fs.readFileSync(jsonPath, "utf-8");
    const data = JSON.parse(rawData);

    const baseName = path.basename(file, ".json");
    const images = data.downloaded_images || [];
    const title = data.product_title || "PRODUK UNGGULAN";

    console.log(`[Remotion] Memproses render video untuk: ${file}`);

    const composition = await selectComposition({
      serveUrl: bundled,
      id: "PromoVideo",
      inputProps: { images, title },
    });

    if (!fs.existsSync(OUTPUT_DIR)) {
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    }

    const outputPath = path.join(OUTPUT_DIR, `${baseName}.mp4`);

    await renderMedia({
      composition,
      serveUrl: bundled,
      codec: "h264",
      outputLocation: outputPath,
      inputProps: { images, title },
    });

    console.log(`[Remotion] Berhasil merender video: ${outputPath}`);
  }
}

startRender().catch((err) => {
  console.error("[Remotion] Error saat rendering:", err);
  process.exit(1);
});
