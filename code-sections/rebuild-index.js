#!/usr/bin/env node
/**
 * Rebuilds index.html, test.html, and test/index.html from the modular files in code-sections/.
 * Runs once and exits immediately (no background processes).
 * Usage: node code-sections/rebuild-index.js
 */
const fs = require("fs");
const path = require("path");

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

const parts = sectionFiles.map((file) => {
  const raw = fs.readFileSync(path.join(sectionsDir, file), "utf8");
  // Strip the 10-line modular header comment added at the top of each section file
  return raw.replace(/^<!--[\s\S]*?============================================================================ -->\r?\n/, "");
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
const totalKB = (Buffer.byteLength(combined, "utf8") / 1024).toFixed(1);
console.log(`Successfully rebuilt ${targets.join(", ")} from code-sections/ (${totalLines.toLocaleString()} lines, ${totalKB} KB).`);
