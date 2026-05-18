# Notebook Visual Review Workflow

Use this workflow whenever a change can affect notebook output. Execution
passing is not enough: inspect the PNGs against the chart intent.

## One-Time Setup

Install the Node Playwright dependency and its managed Chromium browser:

```bash
npm install
npm run playwright:install
```

This follows the official Playwright npm workflow
(https://playwright.dev/docs/intro) and avoids using the installed macOS Chrome
application.

## Run A Review

Review the gallery notebooks:

```bash
npm run visual-review:notebooks
```

Review specific notebooks:

```bash
npm run visual-review:notebooks -- docs/gallery/visual-regression-edge-cases.ipynb
```

Write output to a stable location:

```bash
npm run visual-review:notebooks -- docs/gallery/basic.ipynb --output-dir /private/tmp/ggplotly-basic-review
```

Render without executing cells first:

```bash
npm run visual-review:notebooks -- docs/gallery/basic.ipynb --no-execute
```

## Output

The workflow writes:

- `html/`: executed notebook HTML.
- `png/`: one PNG per Plotly chart plus `manifest.tsv`.
- `manifest.json`: source notebook to rendered HTML mapping.
- `index.html`: review gallery containing every PNG and a prompt to record
  intent-based issues.

Generated review artifacts should stay under `/private/tmp` unless there is a
specific reason to track them.

## Review Standard

For each chart:

- Confirm the chart type, axes, grouping, labels, scales, legends, facets, and
  annotations match the notebook code and section heading.
- Confirm the image is not clipped, overlapped, blank, detached from map
  projections, or missing expected traces.
- Do not accept "plausible" or "non-blank" as passing.
- If an issue is found, record the PNG filename, notebook section, expected
  behavior, observed behavior, and likely package surface.

## Troubleshooting

- If `node` cannot find `playwright`, rerun `npm install`.
- If Chromium is missing, run `npm run playwright:install`.
- If notebook execution cannot bind local Jupyter kernel ports in the sandbox,
  rerun the same command with approval/escalation rather than changing notebook
  code.
- Do not use Kaleido or desktop Chrome for batch notebook review.
