#!/usr/bin/env node
/* Capture Plotly notebook charts as PNGs with Playwright managed Chromium. */

const fs = require("fs");
const path = require("path");
const { pathToFileURL } = require("url");
const { chromium } = require("playwright");

function parseArgs(argv) {
  const args = {};
  for (let index = 2; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) {
      throw new Error(`Unexpected argument: ${key}`);
    }
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for ${key}`);
    }
    args[key.slice(2)] = value;
    index += 1;
  }
  for (const required of ["manifest", "png-dir", "gallery", "viewport"]) {
    if (!args[required]) {
      throw new Error(`Missing --${required}`);
    }
  }
  return args;
}

function parseViewport(value) {
  const match = /^(\d+)x(\d+)$/.exec(value);
  if (!match) {
    throw new Error(`Viewport must be WIDTHxHEIGHT, got: ${value}`);
  }
  return { width: Number(match[1]), height: Number(match[2]) };
}

function fileUrl(value) {
  return pathToFileURL(path.resolve(value)).href;
}

function safeName(value) {
  return value.replace(/[^A-Za-z0-9_.-]+/g, "-").replace(/^-+|-+$/g, "") || "chart";
}

function relativeLink(fromFile, targetFile) {
  return path.relative(path.dirname(fromFile), targetFile).split(path.sep).join("/");
}

async function chartMetadata(page) {
  return page.evaluate(() => {
    const nodes = Array.from(document.body.querySelectorAll("h1,h2,h3,.plotly-graph-div"));
    const labels = [];
    let heading = "";
    for (const node of nodes) {
      if (/^H[1-3]$/.test(node.tagName)) {
        heading = node.textContent.trim();
        continue;
      }
      labels.push({ heading });
    }
    return labels;
  });
}

function writeGallery(galleryPath, rows) {
  const cards = rows.map((row) => {
    const imageHref = relativeLink(galleryPath, row.png);
    const htmlHref = relativeLink(galleryPath, row.html);
    return `
      <article class="chart">
        <h2>${escapeHtml(row.notebookTitle)}</h2>
        <h3>${escapeHtml(row.heading || `Chart ${row.index}`)}</h3>
        <p><a href="${htmlHref}">Rendered notebook HTML</a> · ${escapeHtml(row.fileName)}</p>
        <img src="${imageHref}" alt="${escapeHtml(row.heading || `Chart ${row.index}`)}">
        <dl>
          <dt>Intent check</dt>
          <dd>Confirm the chart semantics match the notebook heading and code, not merely that the image is non-blank.</dd>
          <dt>Observed issue</dt>
          <dd></dd>
        </dl>
      </article>`;
  }).join("\n");

  const html = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>ggplotly Notebook Visual Review</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 24px; color: #202124; }
    header { max-width: 960px; margin-bottom: 24px; }
    .chart { border-top: 1px solid #d0d7de; padding: 20px 0 28px; }
    h1 { margin: 0 0 8px; }
    h2 { margin: 0 0 4px; font-size: 20px; }
    h3 { margin: 0 0 8px; font-size: 16px; color: #4b5563; }
    p, dd, dt { font-size: 14px; }
    img { display: block; max-width: 100%; border: 1px solid #d0d7de; background: white; }
    dl { display: grid; grid-template-columns: 120px 1fr; gap: 8px 16px; max-width: 960px; }
    dt { font-weight: 700; }
    dd { margin: 0; min-height: 20px; }
  </style>
</head>
<body>
  <header>
    <h1>ggplotly Notebook Visual Review</h1>
    <p>Review each PNG against chart intent. Empty, plausible, or merely rendered is not sufficient.</p>
  </header>
  ${cards}
</body>
</html>
`;
  fs.writeFileSync(galleryPath, html, "utf8");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

async function main() {
  const args = parseArgs(process.argv);
  const manifest = JSON.parse(fs.readFileSync(args.manifest, "utf8"));
  const pngDir = path.resolve(args["png-dir"]);
  const galleryPath = path.resolve(args.gallery);
  const viewport = parseViewport(args.viewport);
  fs.mkdirSync(pngDir, { recursive: true });
  fs.mkdirSync(path.dirname(galleryPath), { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport });
  const rows = [];

  for (const item of manifest.items) {
    const htmlPath = path.resolve(item.html);
    await page.goto(fileUrl(htmlPath), { waitUntil: "networkidle" });
    await page.waitForTimeout(750);
    const charts = page.locator(".plotly-graph-div");
    const count = await charts.count();
    const labels = await chartMetadata(page);
    const notebookStem = safeName(path.basename(item.notebook, ".ipynb"));

    for (let index = 0; index < count; index += 1) {
      const locator = charts.nth(index);
      await locator.scrollIntoViewIfNeeded();
      const pngName = `${notebookStem}-chart-${String(index + 1).padStart(2, "0")}.png`;
      const pngPath = path.join(pngDir, pngName);
      await locator.screenshot({ path: pngPath });
      rows.push({
        notebookTitle: item.title,
        heading: labels[index] ? labels[index].heading : "",
        index: index + 1,
        fileName: pngName,
        png: pngPath,
        html: htmlPath,
      });
    }
  }

  await browser.close();
  writeGallery(galleryPath, rows);
  fs.writeFileSync(
    path.join(pngDir, "manifest.tsv"),
    ["notebook\theading\tpng\thtml"].concat(rows.map((row) => [
      row.notebookTitle,
      row.heading,
      row.png,
      row.html,
    ].map((value) => String(value).replace(/\t/g, " ")).join("\t"))).join("\n") + "\n",
    "utf8",
  );
  console.log(`Captured ${rows.length} chart PNGs`);
  console.log(`Gallery: ${galleryPath}`);
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
