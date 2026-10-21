#!/usr/bin/env node
/**
 * Rebuilds index.html, test.html, and test/index.html from the modular files in code-sections/.
 *
 * Modes:
 *   node code-sections/rebuild-index.js          -> Instant one-time rebuild
 *   node code-sections/rebuild-index.js --watch  -> Auto-rebuild whenever any section file changes
 *   node code-sections/rebuild-index.js --serve  -> Auto-watch + local HTTP trigger on 127.0.0.1:18514 for Rebuild-Index.html
 */
const fs = require("fs");
const path = require("path");
const http = require("http");

const sectionFiles = [
  "01-head-and-styles.html",
  "02-main-layout-and-modals.html",
  "03-embedded-plant-catalog-data.html",
  "04-state-utilities-and-invasive-species.html",
  "05-auth-rbac-and-text-scaling.html",
  "06-consultations-and-invasive-ui.html",
  "07-catalog-sync-and-admin-console.html",
  "08-filtering-plant-cards-and-staging.html",
  "09-reports-pdf-and-docx-generators.html",
  "10-events-and-garden-planner.html"
];

const sectionsDir = __dirname;
const rootDir = path.resolve(sectionsDir, "..");

function rebuildIndex() {
  const startMs = Date.now();
  const sectionsReport = [];
  const parts = sectionFiles.map((file, idx) => {
    const fullPath = path.join(sectionsDir, file);
    const stat = fs.statSync(fullPath);
    const raw = fs.readFileSync(fullPath, "utf8");
    const stripped = raw.replace(/^<!--[\s\S]*?============================================================================ -->\n/, "");
    const lines = stripped.split("\n").length;
    sectionsReport.push({
      index: idx + 1,
      file,
      lines,
      bytes: Buffer.byteLength(stripped, "utf8"),
      mtime: stat.mtime.toISOString()
    });
    return stripped;
  });

  const combined = parts.join("\n");
  const targets = ["index.html", "test.html"];
  fs.writeFileSync(path.join(rootDir, "index.html"), combined, "utf8");
  fs.writeFileSync(path.join(rootDir, "test.html"), combined, "utf8");
  if (fs.existsSync(path.join(rootDir, "test"))) {
    fs.writeFileSync(path.join(rootDir, "test", "index.html"), combined, "utf8");
    targets.push("test/index.html");
  }

  const totalLines = combined.split("\n").length;
  const totalBytes = Buffer.byteLength(combined, "utf8");
  const elapsedMs = Date.now() - startMs;
  const result = {
    ok: true,
    timestamp: new Date().toISOString(),
    elapsedMs,
    totalLines,
    totalBytes,
    targets,
    sections: sectionsReport
  };

  console.log(
    `[${result.timestamp}] Successfully rebuilt ${targets.join(", ")} from code-sections/ (${totalLines.toLocaleString()} lines, ${(totalBytes / 1024).toFixed(1)} KB in ${elapsedMs}ms).`
  );
  return result;
}

const args = process.argv.slice(2);
const isWatch = args.includes("--watch") || args.includes("--serve");
const isServe = args.includes("--serve");

// Always run an initial rebuild immediately
let lastResult = rebuildIndex();

if (isWatch) {
  let lastMtimes = new Map();
  const snapshotMtimes = () => {
    for (const file of sectionFiles) {
      try {
        const stat = fs.statSync(path.join(sectionsDir, file));
        lastMtimes.set(file, stat.mtimeMs);
      } catch (e) {}
    }
  };
  snapshotMtimes();

  setInterval(() => {
    let changedFile = null;
    for (const file of sectionFiles) {
      try {
        const stat = fs.statSync(path.join(sectionsDir, file));
        const prev = lastMtimes.get(file);
        if (prev !== undefined && stat.mtimeMs !== prev) {
          changedFile = file;
        }
        lastMtimes.set(file, stat.mtimeMs);
      } catch (e) {}
    }
    if (changedFile) {
      console.log(`Detected change in ${changedFile} — auto-rebuilding...`);
      try {
        lastResult = rebuildIndex();
      } catch (err) {
        console.error("Auto-rebuild error:", err.message);
      }
    }
  }, 1200);
  console.log("Watching code-sections/ for changes...");
}

if (isServe) {
  const PORT = Number(process.env.REBUILD_PORT || 18514);
  const server = http.createServer((req, res) => {
    res.setHeader("Access-Control-Allow-Origin", "*");
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    if (req.method === "OPTIONS") {
      res.writeHead(204);
      res.end();
      return;
    }
    if (req.url.startsWith("/rebuild") || req.url === "/") {
      try {
        lastResult = rebuildIndex();
        res.writeHead(200, { "Content-Type": "application/json" });
        res.end(JSON.stringify(lastResult));
      } catch (err) {
        res.writeHead(500, { "Content-Type": "application/json" });
        res.end(JSON.stringify({ ok: false, error: err.message }));
      }
      return;
    }
    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ ok: false, error: "Not found" }));
  });

  server.listen(PORT, "127.0.0.1", () => {
    console.log(`Local Rebuild Trigger Server listening on http://127.0.0.1:${PORT}/rebuild`);
  });
}
