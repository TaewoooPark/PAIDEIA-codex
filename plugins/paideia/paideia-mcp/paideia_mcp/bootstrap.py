"""Dependency bootstrap for the PAIDEIA MCP server.

Codex can spawn this MCP server before a user has run ``$paideia-init-course``.
The server itself needs the ``mcp`` package to complete the stdio handshake, so
the launcher gets one small self-healing step before importing ``server.py``.
"""

from __future__ import annotations

import importlib
import importlib.util
import os
import site
import subprocess
import sys


REQUIRED_IMPORTS: tuple[tuple[str, str], ...] = (
    ("mcp.server", "mcp>=1.2.0"),
    ("httpx", "httpx"),
    ("pypdf", "pypdf"),
    ("PIL", "pillow"),
    ("pdf2image", "pdf2image"),
    ("pytesseract", "pytesseract"),
    ("reportlab", "reportlab"),
)

PIP_PACKAGES: tuple[str, ...] = tuple(pkg for _, pkg in REQUIRED_IMPORTS)
FALSEY = {"0", "false", "no", "off"}


def missing_imports() -> list[str]:
    """Return import names that are not currently importable."""

    missing = []
    for name, _ in REQUIRED_IMPORTS:
        try:
            spec = importlib.util.find_spec(name)
        except ModuleNotFoundError:
            spec = None
        if spec is None:
            missing.append(name)
    return missing


def missing_message(missing: list[str]) -> str:
    packages = ", ".join(missing)
    install = " ".join(
        f'"{pkg}"' if any(op in pkg for op in "<>=") else pkg
        for pkg in PIP_PACKAGES
    )
    return (
        f"paideia-mcp: missing Python packages: {packages}\n"
        "paideia-mcp: automatic dependency install is disabled or failed.\n"
        "paideia-mcp: run:\n"
        f"  {sys.executable} -m pip install --break-system-packages --user {install}\n"
    )


def _run_pip(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pip", "install", *args, *PIP_PACKAGES],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _install_missing() -> None:
    sys.stderr.write("paideia-mcp: installing missing Python dependencies...\n")
    result = _run_pip(["--user"])
    if result.returncode != 0:
        combined = f"{result.stdout}\n{result.stderr}"
        if "externally-managed-environment" in combined or "--break-system-packages" in combined:
            result = _run_pip(["--break-system-packages", "--user"])
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(missing_message(missing_imports()))

    importlib.invalidate_caches()
    try:
        user_site = site.getusersitepackages()
    except Exception:
        user_site = None
    if user_site and user_site not in sys.path:
        sys.path.append(user_site)


def ensure_dependencies() -> None:
    missing = missing_imports()
    if not missing:
        return

    auto_install = os.environ.get("PAIDEIA_MCP_AUTO_INSTALL", "1").strip().lower()
    if auto_install in FALSEY:
        raise SystemExit(missing_message(missing))

    _install_missing()
    still_missing = missing_imports()
    if still_missing:
        raise SystemExit(missing_message(still_missing))


def main() -> None:
    ensure_dependencies()
    from paideia_mcp.server import main as server_main

    server_main()


if __name__ == "__main__":
    main()
