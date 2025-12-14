"""Tests to ensure all documentation notebooks execute without errors."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

# Get all notebooks in the docs directory
DOCS_DIR = Path(__file__).parent.parent / "docs"
NOTEBOOKS = list(DOCS_DIR.glob("**/*.ipynb"))


def get_notebook_id(notebook_path: Path) -> str:
    """Generate a readable test ID from notebook path."""
    return str(notebook_path.relative_to(DOCS_DIR))


@pytest.mark.parametrize("notebook_path", NOTEBOOKS, ids=get_notebook_id)
def test_notebook_executes(notebook_path: Path, tmp_path: Path):
    """Test that a notebook executes without errors.

    Uses nbconvert to execute the notebook in a subprocess.
    This ensures each notebook runs in a clean environment.
    """
    output_notebook = tmp_path / notebook_path.name

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--output",
            str(output_notebook),
            str(notebook_path),
        ],
        capture_output=True,
        text=True,
        timeout=300,  # 5 minute timeout per notebook
    )

    if result.returncode != 0:
        # Read the notebook to find which cell failed
        error_msg = f"Notebook {notebook_path.name} failed to execute.\n"
        error_msg += f"STDOUT:\n{result.stdout}\n"
        error_msg += f"STDERR:\n{result.stderr}\n"
        pytest.fail(error_msg)


def test_notebooks_exist():
    """Ensure we found notebooks to test."""
    assert len(NOTEBOOKS) > 0, f"No notebooks found in {DOCS_DIR}"

    # Check we have the expected guide notebooks
    guide_notebooks = [nb for nb in NOTEBOOKS if "guide" in str(nb)]
    assert len(guide_notebooks) >= 7, f"Expected at least 7 guide notebooks, found {len(guide_notebooks)}"
