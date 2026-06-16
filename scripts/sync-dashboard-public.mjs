import { cp, mkdir, rm } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(projectRoot, "public");

const itemsToCopy = [
  "assets",
  "data",
  "asset_reports",
  "tag_reports",
  "DASHBOARD_PREVIEW.html",
  "index.html",
  "REPORTS.html",
  "PROGRAMS_REPORT.html",
  "EXECUTIVE_REPORT.html",
  "BOARD_REPORT.html",
  "SOCIAL_LISTENING.html",
  "SETTINGS.html",
  "HELP.html",
  "manifest.webmanifest",
  "sw.js",
  "app-icon.svg",
];

await mkdir(publicRoot, { recursive: true });

for (const item of itemsToCopy) {
  const source = resolve(projectRoot, item);
  const target = resolve(publicRoot, item);
  await rm(target, { recursive: true, force: true });
  await cp(source, target, { recursive: true });
}
