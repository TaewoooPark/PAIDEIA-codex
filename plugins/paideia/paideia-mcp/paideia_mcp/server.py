"""paideia-mcp stdio entrypoint.

Registers four tools — ``ingest_pdfs``, ``grade_pdf``, ``build_course_index``,
``course_phase`` — and dispatches JSON-encoded results over the stdio MCP
channel. The Codex plugin loader launches this via ``python -m
paideia_mcp.server``.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from .analyze import build_course_index
from .grade import grade_pdf
from .ingest import ingest_pdfs
from .phase import course_phase

app: Server = Server("paideia-mcp")


_PROJECT_ROOT_PROP = {
    "type": "string",
    "description": (
        "Absolute path to the course project root. Defaults to the server's "
        "CWD when omitted; set this explicitly if the user has cd'd between "
        "courses within the same Codex session."
    ),
}


_INGEST_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "engine": {
            "type": "string",
            "enum": ["openai-vision", "qwen3-vl", "tesseract"],
            "default": "openai-vision",
            "description": (
                "OCR engine. openai-vision needs OPENAI_API_KEY; qwen3-vl "
                "needs a local Ollama with qwen3-vl:8b; tesseract needs "
                "pytesseract + eng+kor traineddata."
            ),
        },
        "force": {
            "type": "boolean",
            "default": False,
            "description": "Reconvert even if converted/<cat>/<stem>.md exists.",
        },
        "categories": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["lectures", "textbook", "homework", "solutions"],
            },
            "description": "Restrict to a subset of the materials subfolders.",
        },
        "project_root": _PROJECT_ROOT_PROP,
    },
    "additionalProperties": False,
}


_GRADE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "path": {
            "type": "string",
            "description": (
                "Answer PDF path. Absolute, or relative to project_root "
                "(typically answers/<stem>.pdf)."
            ),
        },
        "engine": {
            "type": "string",
            "enum": ["openai-vision", "qwen3-vl", "tesseract"],
            "description": (
                "Override the OCR engine. When omitted, falls back to "
                ".course-meta OCR_ENGINE, then to openai-vision."
            ),
        },
        "project_root": _PROJECT_ROOT_PROP,
    },
    "required": ["path"],
    "additionalProperties": False,
}


_ANALYZE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "weak_zones": {
            "type": "string",
            "description": "Free-form hints about weak areas; passed through.",
        },
        "project_root": _PROJECT_ROOT_PROP,
    },
    "additionalProperties": False,
}


_PHASE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "project_root": _PROJECT_ROOT_PROP,
    },
    "additionalProperties": False,
}


@app.list_tools()
async def _list_tools() -> list[Tool]:
    """Publish the four tools the plugin exposes."""

    return [
        Tool(
            name="ingest_pdfs",
            description=(
                "Render every materials/**/*.pdf to markdown via the selected "
                "OCR engine. Idempotent unless force=True."
            ),
            inputSchema=_INGEST_SCHEMA,
        ),
        Tool(
            name="grade_pdf",
            description=(
                "OCR a single hand-written answer PDF into "
                "answers/converted/<stem>.md with a confidence tier."
            ),
            inputSchema=_GRADE_SCHEMA,
        ),
        Tool(
            name="build_course_index",
            description=(
                "Return an inventory of converted/ markdown files for the "
                "analyze skill to reason over."
            ),
            inputSchema=_ANALYZE_SCHEMA,
        ),
        Tool(
            name="course_phase",
            description=(
                "Return the artifact-derived course phase (setup/diag/drill/"
                "mock/cram/cool), days_until_exam, and top_miss_pattern."
            ),
            inputSchema=_PHASE_SCHEMA,
        ),
    ]


_DISPATCH = {
    "ingest_pdfs": ingest_pdfs,
    "grade_pdf": grade_pdf,
    "build_course_index": build_course_index,
    "course_phase": course_phase,
}


@app.call_tool()
async def _call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[TextContent]:
    """Dispatch a tool call and return its JSON-encoded result."""

    handler = _DISPATCH.get(name)
    if handler is None:
        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {"error": f"unknown tool '{name}'"},
                    ensure_ascii=False,
                ),
            )
        ]
    kwargs = dict(arguments or {})
    try:
        result = handler(**kwargs)
    except TypeError as exc:
        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "error": f"bad arguments for '{name}': {exc}",
                        "arguments": kwargs,
                    },
                    ensure_ascii=False,
                ),
            )
        ]
    except Exception as exc:  # noqa: BLE001 — surface as structured error
        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "error": f"{type(exc).__name__}: {exc}",
                        "tool": name,
                    },
                    ensure_ascii=False,
                ),
            )
        ]
    return [
        TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2),
        )
    ]


async def _run() -> None:
    """Start the stdio server and run until the client disconnects."""

    async with stdio_server() as (reader, writer):
        await app.run(reader, writer, app.create_initialization_options())


def main() -> None:
    """Console-script entrypoint."""

    asyncio.run(_run())


if __name__ == "__main__":
    main()
