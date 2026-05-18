#!/usr/bin/env python3
"""Render notebooks to HTML, capture chart PNGs, and build a review gallery."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import nbformat


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")
    return slug or "notebook"


def notebook_title(path: Path) -> str:
    notebook = nbformat.read(path, as_version=4)
    for cell in notebook.cells:
        if cell.cell_type != "markdown":
            continue
        for line in cell.source.splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def expand_notebooks(root: Path, inputs: list[str]) -> list[Path]:
    paths = inputs or ["docs/gallery"]
    notebooks: list[Path] = []
    for raw_path in paths:
        path = (root / raw_path).resolve() if not Path(raw_path).is_absolute() else Path(raw_path)
        if path.is_dir():
            notebooks.extend(sorted(path.rglob("*.ipynb")))
        elif path.suffix == ".ipynb":
            notebooks.append(path)
        else:
            raise SystemExit(f"Expected a notebook or directory, got: {raw_path}")

    unique = []
    seen = set()
    for path in notebooks:
        resolved = path.resolve()
        if resolved in seen:
            continue
        if not resolved.exists():
            raise SystemExit(f"Notebook does not exist: {path}")
        seen.add(resolved)
        unique.append(resolved)
    if not unique:
        raise SystemExit("No notebooks matched the requested inputs.")
    return unique


def default_output_dir() -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return Path(tempfile.gettempdir()) / f"ggplotly-notebook-review-{stamp}"


def render_notebook(
    root: Path,
    notebook: Path,
    html_dir: Path,
    execute: bool,
    timeout: int,
) -> Path:
    rel = notebook.relative_to(root) if notebook.is_relative_to(root) else notebook.name
    output_stem = slugify(str(rel).removesuffix(".ipynb"))
    html_path = html_dir / f"{output_stem}.html"

    cmd = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "html",
        "--output",
        output_stem,
        "--output-dir",
        str(html_dir),
        str(notebook),
    ]
    if execute:
        cmd.insert(4, "--execute")
        cmd.insert(5, f"--ExecutePreprocessor.timeout={timeout}")

    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(root) if not existing_pythonpath else f"{root}{os.pathsep}{existing_pythonpath}"

    subprocess.run(cmd, cwd=root, env=env, check=True)
    return html_path


def require_node_playwright(root: Path) -> None:
    probe = ["node", "-e", "require.resolve('playwright'); console.log('playwright ok')"]
    result = subprocess.run(probe, cwd=root, text=True, capture_output=True)
    if result.returncode == 0:
        return
    raise SystemExit(
        "Node Playwright is not installed for this repo.\n"
        "Run:\n"
        "  npm install\n"
        "  npm run playwright:install\n"
        "Then rerun the visual review command."
    )


def capture_pngs(root: Path, manifest: Path, png_dir: Path, gallery: Path, viewport: str) -> None:
    require_node_playwright(root)
    subprocess.run(
        [
            "node",
            str(root / "scripts" / "capture_notebook_pngs.js"),
            "--manifest",
            str(manifest),
            "--png-dir",
            str(png_dir),
            "--gallery",
            str(gallery),
            "--viewport",
            viewport,
        ],
        cwd=root,
        check=True,
    )


def write_manifest(root: Path, output_dir: Path, items: list[dict[str, str]]) -> Path:
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo": str(root),
        "items": items,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render ggplotly notebooks, capture Plotly chart PNGs, and build a review gallery.",
    )
    parser.add_argument(
        "notebooks",
        nargs="*",
        help="Notebook files or directories. Defaults to docs/gallery.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Review output directory. Defaults to a timestamped directory under the system temp dir.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="Per-notebook execution timeout in seconds.",
    )
    parser.add_argument(
        "--no-execute",
        action="store_true",
        help="Convert notebooks without executing cells first.",
    )
    parser.add_argument(
        "--skip-capture",
        action="store_true",
        help="Render HTML only; do not run Playwright PNG capture.",
    )
    parser.add_argument(
        "--viewport",
        default="1440x1100",
        help="Playwright viewport as WIDTHxHEIGHT.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    notebooks = expand_notebooks(root, args.notebooks)
    output_dir = (args.output_dir or default_output_dir()).resolve()
    html_dir = output_dir / "html"
    png_dir = output_dir / "png"
    gallery = output_dir / "index.html"
    html_dir.mkdir(parents=True, exist_ok=True)
    png_dir.mkdir(parents=True, exist_ok=True)

    items = []
    for notebook in notebooks:
        html = render_notebook(
            root=root,
            notebook=notebook,
            html_dir=html_dir,
            execute=not args.no_execute,
            timeout=args.timeout,
        )
        items.append({
            "notebook": str(notebook),
            "title": notebook_title(notebook),
            "html": str(html),
        })

    manifest = write_manifest(root, output_dir, items)
    if not args.skip_capture:
        capture_pngs(root, manifest, png_dir, gallery, args.viewport)

    print(f"Review output: {output_dir}")
    print(f"Manifest: {manifest}")
    if not args.skip_capture:
        print(f"Gallery: {gallery}")
        print(f"PNGs: {png_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
