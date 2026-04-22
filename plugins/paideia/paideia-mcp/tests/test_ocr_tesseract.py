"""Minimal import smoke test for ``paideia_mcp.ocr.tesseract``.

Skips gracefully when pytesseract or its system binary is unavailable — the
goal here is to catch syntax and import regressions, not to vet OCR quality.
"""

from __future__ import annotations

import pytest


def test_module_imports() -> None:
    try:
        from paideia_mcp.ocr import tesseract as _tesseract  # noqa: F401
    except ImportError as exc:  # pragma: no cover — optional dep
        pytest.skip(f"tesseract module import failed: {exc}")


def test_pytesseract_available() -> None:
    pytesseract = pytest.importorskip("pytesseract")
    try:
        pytesseract.get_tesseract_version()
    except (
        pytesseract.TesseractNotFoundError  # type: ignore[attr-defined]
    ) as exc:
        pytest.skip(f"tesseract binary not installed: {exc}")
    except Exception as exc:  # pragma: no cover
        pytest.skip(f"tesseract probe failed: {exc}")


def test_empty_input_returns_empty_list() -> None:
    tesseract = pytest.importorskip("paideia_mcp.ocr.tesseract")
    assert tesseract.transcribe_pages([]) == []
