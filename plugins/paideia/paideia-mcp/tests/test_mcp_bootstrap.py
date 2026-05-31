"""Regression tests for the MCP dependency bootstrapper."""

from __future__ import annotations

import pytest

from paideia_mcp import bootstrap


def test_missing_message_includes_manual_install_command() -> None:
    message = bootstrap.missing_message(["mcp.server"])

    assert "missing Python packages: mcp.server" in message
    assert "pip install" in message
    assert '"mcp>=1.2.0"' in message


def test_ensure_dependencies_can_be_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bootstrap, "missing_imports", lambda: ["mcp.server"])
    monkeypatch.setenv("PAIDEIA_MCP_AUTO_INSTALL", "0")

    with pytest.raises(SystemExit) as exc:
        bootstrap.ensure_dependencies()

    assert "automatic dependency install is disabled" in str(exc.value)


def test_ensure_dependencies_installs_then_rechecks(monkeypatch: pytest.MonkeyPatch) -> None:
    probes = iter([["mcp.server"], []])
    installs: list[bool] = []
    monkeypatch.setattr(bootstrap, "missing_imports", lambda: next(probes))
    monkeypatch.setattr(bootstrap, "_install_missing", lambda: installs.append(True))

    bootstrap.ensure_dependencies()

    assert installs == [True]
