"""``build_course_index`` MCP tool.

Builds a machine-generated baseline ``course-index/`` from ``converted/**`` so
the higher-level analyze skill has a concrete draft to refine instead of
starting from an empty folder. The output is intentionally heuristic-driven,
not authoritative: it produces a usable first pass for summary/patterns/
coverage and returns the inventory it used.
"""

from __future__ import annotations

import datetime
import os
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

_CATEGORIES = ("lectures", "textbook", "homework", "solutions")
_INDEX_FILES = ("summary.md", "patterns.md", "coverage.md")
_STOPWORDS = {
    "and",
    "are",
    "but",
    "for",
    "from",
    "into",
    "that",
    "the",
    "this",
    "with",
    "using",
    "use",
    "your",
    "their",
    "then",
    "than",
    "when",
    "where",
    "have",
    "has",
    "had",
    "been",
    "will",
    "would",
    "about",
    "through",
    "under",
    "problem",
    "solution",
    "lecture",
    "chapter",
    "section",
    "example",
    "notes",
    "homework",
}


@dataclass(frozen=True)
class ConvertedDoc:
    """One converted markdown source file."""

    category: str
    path: Path
    rel: str
    text: str
    headings: list[str]
    tokens: set[str]


@dataclass(frozen=True)
class Section:
    """One inferred course section/topic."""

    label: str
    title: str
    source: str
    tokens: set[str]


@dataclass(frozen=True)
class PatternSpec:
    """Keyword-driven recurring pattern detector."""

    name: str
    regexes: tuple[str, ...]
    recognition: str
    move: str


_PATTERN_SPECS: tuple[PatternSpec, ...] = (
    PatternSpec(
        name="Residue evaluation",
        regexes=(r"\bresidue(s)?\b", r"\bpole(s)?\b", r"잔여", r"유수"),
        recognition="Poles, singularities, or a contour integral show up.",
        move="Locate the poles, compute the relevant residues, and sum them.",
    ),
    PatternSpec(
        name="Contour deformation",
        regexes=(r"\bcontour\b", r"\bkeyhole\b", r"\bsemicircle\b", r"경로 적분"),
        recognition="The integral is easier after choosing or deforming a contour.",
        move="Pick the contour that kills the unwanted arc and isolates the target term.",
    ),
    PatternSpec(
        name="Partial fraction split",
        regexes=(r"partial fraction", r"부분분수"),
        recognition="A rational expression needs to be decomposed before integrating or inverting.",
        move="Split the rational form into elementary pieces and solve term-by-term.",
    ),
    PatternSpec(
        name="Integration by parts",
        regexes=(r"integration by parts", r"부분적분"),
        recognition="A product of terms gets simpler when one factor is differentiated.",
        move="Choose the factor to differentiate/integrate so the remainder is easier.",
    ),
    PatternSpec(
        name="Change of variable",
        regexes=(r"\bsubstitut", r"change of variable", r"치환"),
        recognition="A substitution can normalize the integrand, bounds, or algebraic structure.",
        move="Introduce the natural variable, rewrite the measure, then simplify.",
    ),
    PatternSpec(
        name="Fourier representation",
        regexes=(r"\bfourier\b", r"푸리에"),
        recognition="Periodic structure, frequency decomposition, or transform language appears.",
        move="Project onto the Fourier basis or transform to frequency space and solve there.",
    ),
    PatternSpec(
        name="Laplace transform",
        regexes=(r"\blaplace\b", r"라플라스"),
        recognition="An ODE or convolution becomes algebraic after transforming.",
        move="Transform, solve algebraically, then invert back to the time domain.",
    ),
    PatternSpec(
        name="Separation of variables",
        regexes=(r"separation of variables", r"variables are separable", r"변수분리"),
        recognition="The equation separates into independent single-variable factors.",
        move="Split variables, integrate each side, and apply the boundary conditions.",
    ),
    PatternSpec(
        name="Eigenvalue / diagonalization",
        regexes=(r"\beigen(value|vector)\b", r"\bdiagonal", r"고유값", r"고유벡터"),
        recognition="Linear dynamics or quadratic forms simplify in an eigenbasis.",
        move="Find the eigen-structure, diagonalize, and solve in the decoupled basis.",
    ),
    PatternSpec(
        name="Taylor / perturbation expansion",
        regexes=(r"\btaylor\b", r"\bseries expansion\b", r"perturb", r"테일러"),
        recognition="A small parameter or local approximation controls the answer.",
        move="Expand to the required order, keep the dominant terms, and track the remainder.",
    ),
    PatternSpec(
        name="Convolution",
        regexes=(r"\bconvolution\b", r"합성곱"),
        recognition="Signals, kernels, or product-of-transforms structure appears.",
        move="Convert between product and convolution in the domain that simplifies the task.",
    ),
    PatternSpec(
        name="Green's function",
        regexes=(r"green'?s function", r"그린 함수"),
        recognition="A forcing term is handled via the response to a point source.",
        move="Build the Green's function for the operator and integrate against the source.",
    ),
    PatternSpec(
        name="Flux theorem",
        regexes=(r"\bstokes\b", r"divergence theorem", r"gauss theorem", r"발산 정리", r"스토크스"),
        recognition="A line, surface, or volume integral wants to be converted across dimensions.",
        move="Switch to the theorem that matches the geometry and orientation of the domain.",
    ),
    PatternSpec(
        name="Lagrange multiplier",
        regexes=(r"lagrange multiplier", r"라그랑주 승수"),
        recognition="Optimization is constrained by one or more equations.",
        move="Augment the objective with constraints, then solve the stationarity system.",
    ),
    PatternSpec(
        name="Recurrence / induction",
        regexes=(r"\binduction\b", r"\brecurrence\b", r"점화", r"귀납"),
        recognition="The solution is built from a relation between adjacent indices or cases.",
        move="Establish the base case, derive the recursive step, and close the loop.",
    ),
    PatternSpec(
        name="Characteristic equation",
        regexes=(r"characteristic equation", r"특성방정식"),
        recognition="A linear recurrence or differential equation reduces to an algebraic polynomial.",
        move="Solve the characteristic polynomial, then assemble the general solution from its roots.",
    ),
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _list_category(converted: Path, category: str) -> list[str]:
    """Return sorted relative paths for every ``.md`` in a category dir."""

    category_dir = converted / category
    if not category_dir.exists():
        return []
    return sorted(str(path.relative_to(converted)) for path in category_dir.rglob("*.md"))


def _clean_heading(text: str) -> str:
    """Normalize one markdown heading line."""

    cleaned = text.strip().strip("#").strip()
    cleaned = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", cleaned)
    cleaned = re.sub(r"[`*_~]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def _extract_headings(text: str) -> list[str]:
    """Return cleaned markdown headings, in file order."""

    headings: list[str] = []
    for raw in re.findall(r"(?m)^(#{1,6})\s+(.+)$", text):
        heading = _clean_heading(raw[1])
        if not heading:
            continue
        if heading.lower().startswith("page "):
            continue
        headings.append(heading)
    return headings


def _title_from_stem(stem: str) -> str:
    return re.sub(r"[-_]+", " ", stem).strip().title() or stem


def _tokenize(text: str) -> set[str]:
    tokens = re.findall(r"[A-Za-z][A-Za-z0-9\-']{2,}", text.lower())
    return {tok for tok in tokens if tok not in _STOPWORDS}


def _extract_label_and_title(heading: str, index: int) -> tuple[str, str]:
    """Derive a human-facing section label from a heading."""

    patterns = (
        re.compile(r"^(§\s*\d+(?:\.\d+)*)\s*[-:.)]?\s*(.*)$", re.I),
        re.compile(r"^(Ch(?:apter)?\.?\s*\d+(?:\.\d+)*)\s*[-:.)]?\s*(.*)$", re.I),
        re.compile(r"^(Lecture\s*\d+)\s*[-:.)]?\s*(.*)$", re.I),
        re.compile(r"^(\d+(?:\.\d+)*)\s+(.+)$"),
    )
    for pattern in patterns:
        match = pattern.match(heading)
        if not match:
            continue
        label = match.group(1)
        if pattern is patterns[3]:
            label = f"§{label}"
        title = match.group(2).strip() or heading.strip()
        return label, title
    return f"§{index}", heading.strip()


def _load_docs(root: Path) -> tuple[dict[str, list[str]], dict[str, int], list[ConvertedDoc]]:
    """Load every converted markdown file."""

    converted = root / "converted"
    inventory = {category: _list_category(converted, category) for category in _CATEGORIES}
    totals = {category: len(files) for category, files in inventory.items()}
    docs: list[ConvertedDoc] = []
    for category in _CATEGORIES:
        for rel in inventory[category]:
            path = converted / rel
            text = _read_text(path)
            headings = _extract_headings(text)
            tokens = _tokenize("\n".join(headings) + "\n" + text)
            docs.append(
                ConvertedDoc(
                    category=category,
                    path=path,
                    rel=rel,
                    text=text,
                    headings=headings,
                    tokens=tokens,
                )
            )
    return inventory, totals, docs


def _build_sections(docs: list[ConvertedDoc]) -> list[Section]:
    """Infer a topic list from lecture/textbook headings, then other sources."""

    ordered_docs = [
        doc
        for category in ("lectures", "textbook", "solutions", "homework")
        for doc in docs
        if doc.category == category
    ]
    sections: list[Section] = []
    seen: set[tuple[str, str]] = set()
    next_index = 1
    for doc in ordered_docs:
        candidates = doc.headings or [_title_from_stem(doc.path.stem)]
        for heading in candidates:
            label, title = _extract_label_and_title(heading, next_index)
            key = (label.lower(), title.lower())
            if key in seen:
                continue
            seen.add(key)
            sections.append(
                Section(
                    label=label,
                    title=title,
                    source=f"converted/{doc.rel}",
                    tokens=_tokenize(title),
                )
            )
            next_index += 1
    return sections


def _section_score(tokens: set[str], section: Section) -> int:
    overlap = tokens & section.tokens
    return len(overlap)


def _topic_labels_for_doc(doc: ConvertedDoc, sections: list[Section]) -> list[str]:
    """Find the best matching section labels for a converted file."""

    scored = sorted(
        (
            (_section_score(doc.tokens, section), section.label)
            for section in sections
        ),
        reverse=True,
    )
    labels = [label for score, label in scored if score > 0]
    return labels[:2]


def _scope_statement(docs: list[ConvertedDoc]) -> str:
    """Produce a one-paragraph draft scope statement."""

    source_docs = [doc for doc in docs if doc.category in {"lectures", "textbook"}]
    counter: Counter[str] = Counter()
    for doc in source_docs:
        for heading in doc.headings[:6]:
            counter.update(_tokenize(heading))
    themes = [token for token, _ in counter.most_common(4)]
    if not themes:
        return (
            "Draft baseline generated from the converted course materials. "
            "Refine section names and emphasis manually if the course uses local notation."
        )
    return (
        "Draft baseline generated from the converted course materials. Dominant "
        f"themes inferred from the lecture/textbook headings: {', '.join(themes)}."
    )


def _render_summary(
    created_at: str,
    docs: list[ConvertedDoc],
    sections: list[Section],
) -> str:
    """Render ``course-index/summary.md``."""

    lines = [
        "# Summary",
        "",
        f"_Generated {created_at} from {len(docs)} converted source files._",
        "",
        "## Scope",
        _scope_statement(docs),
        "",
        "## Topic tree",
    ]
    if sections:
        for section in sections:
            lines.append(f"- {section.label}. {section.title} — `{section.source}`")
    else:
        lines.append("- No headings detected. Run `$paideia-ingest --force` after checking the source materials.")

    if sections:
        chunk = max(1, len(sections) // 3)
        foundations = ", ".join(section.label for section in sections[:chunk])
        middle = ", ".join(section.label for section in sections[chunk : chunk * 2]) or foundations
        late = ", ".join(section.label for section in sections[chunk * 2 :]) or middle
        lines.extend(
            [
                "",
                "## Difficulty ordering",
                f"1. Foundations: {foundations}",
                f"2. Mid-course machinery: {middle}",
                f"3. Late-course applications: {late}",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def _collect_pattern_records(
    docs: list[ConvertedDoc],
    sections: list[Section],
) -> tuple[list[dict], list[dict]]:
    """Collect recurring vs one-off pattern hits."""

    searchable = [doc for doc in docs if doc.category in {"lectures", "textbook", "solutions"}]
    recurring: list[dict] = []
    one_off: list[dict] = []
    for spec in _PATTERN_SPECS:
        matched_docs = []
        for doc in searchable:
            lowered = doc.text.lower()
            if any(re.search(regex, lowered, re.I) for regex in spec.regexes):
                matched_docs.append(doc)
        if not matched_docs:
            continue
        sources = sorted({f"converted/{doc.rel}" for doc in matched_docs})
        topics = sorted({label for doc in matched_docs for label in _topic_labels_for_doc(doc, sections)})
        appears_in = sorted({Path(doc.rel).stem for doc in matched_docs})
        record = {
            "name": spec.name,
            "recognition": spec.recognition,
            "move": spec.move,
            "sources": sources,
            "topics": topics,
            "appears_in": appears_in,
        }
        target = recurring if len(sources) >= 2 else one_off
        target.append(record)

    recurring.sort(key=lambda item: (-len(item["sources"]), item["name"]))
    one_off.sort(key=lambda item: item["name"])
    return recurring, one_off


def _render_patterns(
    created_at: str,
    recurring: list[dict],
    one_off: list[dict],
) -> str:
    """Render ``course-index/patterns.md``."""

    lines = [
        "# Patterns",
        "",
        f"_Generated {created_at}. Recurring patterns are keyword-backed draft cards; refine names and examples as needed._",
        "",
        "## Recurring patterns",
    ]
    if recurring:
        for i, record in enumerate(recurring, 1):
            lines.extend(
                [
                    "",
                    f"### P{i}. {record['name']}",
                    f"**Recognition.** {record['recognition']}",
                    f"**Move.** {record['move']}",
                    f"**Appears in.** {', '.join(record['appears_in'])}",
                    f"**Topic.** {', '.join(record['topics']) if record['topics'] else 'unmapped'}",
                    f"**Sources.** {', '.join(f'`{src}`' for src in record['sources'])}",
                ]
            )
    else:
        lines.append("")
        lines.append("No recurring patterns were detected from the current converted sources.")

    lines.extend(["", "## One-off techniques"])
    if one_off:
        for record in one_off:
            lines.append(
                f"- {record['name']} — {', '.join(f'`{src}`' for src in record['sources'])}"
            )
    else:
        lines.append("- No one-off techniques detected.")

    return "\n".join(lines).rstrip() + "\n"


def _tier_for(count: int) -> str:
    if count >= 3:
        return "🔥🔥 Exam-primary"
    if count == 2:
        return "🔥 Exam-likely"
    if count == 1:
        return "🟡 Exam-possible"
    return "⚪ Low-risk"


def _best_section_for_homework(
    doc: ConvertedDoc,
    sections: list[Section],
) -> Section | None:
    if not sections:
        return None
    scored = sorted(
        ((section, _section_score(doc.tokens, section)) for section in sections),
        key=lambda item: item[1],
        reverse=True,
    )
    if not scored or scored[0][1] <= 0:
        return None
    return scored[0][0]


def _parse_weak_zones(weak_zones: str | None) -> list[str]:
    if not weak_zones:
        return []
    return [item.strip() for item in weak_zones.split(",") if item.strip()]


def _render_coverage(
    created_at: str,
    docs: list[ConvertedDoc],
    sections: list[Section],
    weak_zones: str | None,
) -> str:
    """Render ``course-index/coverage.md``."""

    hints = _parse_weak_zones(weak_zones)
    hint_tokens = [_tokenize(item) for item in hints]
    assignments: dict[str, list[str]] = {section.label: [] for section in sections}
    unmapped: list[str] = []
    for doc in (doc for doc in docs if doc.category == "homework"):
        section = _best_section_for_homework(doc, sections)
        if section is None:
            unmapped.append(f"converted/{doc.rel}")
            continue
        assignments[section.label].append(f"converted/{doc.rel}")

    lines = [
        "# Coverage",
        "",
        f"_Generated {created_at}. Asterisked sections overlap with declared weak zones: {', '.join(hints) if hints else 'none'}._",
        "",
        "## Section coverage",
        "",
        "| Section | Title | HW count | Tier | HW sources | Source |",
        "|---|---|---:|---|---|---|",
    ]

    ranked: list[tuple[int, int, Section]] = []
    for section in sections:
        weak_overlap = int(any(section.tokens & tokens for tokens in hint_tokens))
        hw_sources = assignments[section.label]
        count = len(hw_sources)
        title = section.title + (" *" if weak_overlap else "")
        hw_text = "<br>".join(f"`{source}`" for source in hw_sources) if hw_sources else "-"
        lines.append(
            f"| {section.label} | {title} | {count} | {_tier_for(count)} | {hw_text} | `{section.source}` |"
        )
        ranked.append((count, weak_overlap, section))

    if unmapped:
        lines.extend(["", "## Unmapped homework", ""])
        for source in unmapped:
            lines.append(f"- `{source}`")

    ranked.sort(key=lambda item: (item[0], item[1], item[2].label), reverse=True)
    lines.extend(["", "## Recommended drill priority", ""])
    chosen = [item for item in ranked if item[0] > 0 or item[1] > 0][:6]
    if chosen:
        for i, (count, weak_overlap, section) in enumerate(chosen, 1):
            drill = (
                "$paideia-blind"
                if count >= 3
                else "$paideia-twin"
                if count == 2
                else "$paideia-pattern"
            )
            emphasis = " + weak-zone" if weak_overlap else ""
            lines.append(
                f"{i}. {section.label}. {section.title} — {_tier_for(count)} ({count} HW{emphasis}) -> {drill}"
            )
    else:
        lines.append("1. No homework-to-section matches detected yet. Review the converted homework titles manually.")

    return "\n".join(lines).rstrip() + "\n"


def build_course_index(
    weak_zones: str | None = None,
    project_root: str | None = None,
    force: bool = False,
) -> dict:
    """Inventory ``converted/**`` and write a draft ``course-index/``."""

    root = Path(project_root or os.getcwd()).resolve()
    converted = root / "converted"
    if not converted.exists():
        return {
            "project_root": str(root),
            "converted_root": str(converted),
            "inventory": {category: [] for category in _CATEGORIES},
            "totals": {category: 0 for category in _CATEGORIES},
            "weak_zones": weak_zones,
            "ready": False,
            "wrote_index": False,
            "written": [],
            "message": (
                "converted/ is missing. Run ingest_pdfs (or the paideia-ingest skill) first."
            ),
        }

    inventory, totals, docs = _load_docs(root)
    ready = any(totals.values())
    if not ready:
        return {
            "project_root": str(root),
            "converted_root": str(converted),
            "inventory": inventory,
            "totals": totals,
            "weak_zones": weak_zones,
            "ready": False,
            "wrote_index": False,
            "written": [],
            "message": "converted/ is empty. Run ingest_pdfs first.",
        }

    course_index = root / "course-index"
    existing = [str(course_index / name) for name in _INDEX_FILES if (course_index / name).exists()]
    if existing and not force:
        return {
            "project_root": str(root),
            "converted_root": str(converted),
            "inventory": inventory,
            "totals": totals,
            "weak_zones": weak_zones,
            "ready": True,
            "wrote_index": False,
            "written": [],
            "existing": existing,
            "message": "course-index already exists. Re-run with force=True to regenerate.",
        }

    course_index.mkdir(parents=True, exist_ok=True)
    created_at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    sections = _build_sections(docs)
    recurring, one_off = _collect_pattern_records(docs, sections)

    summary_path = course_index / "summary.md"
    patterns_path = course_index / "patterns.md"
    coverage_path = course_index / "coverage.md"
    summary_path.write_text(_render_summary(created_at, docs, sections), encoding="utf-8")
    patterns_path.write_text(
        _render_patterns(created_at, recurring, one_off),
        encoding="utf-8",
    )
    coverage_path.write_text(
        _render_coverage(created_at, docs, sections, weak_zones),
        encoding="utf-8",
    )

    return {
        "project_root": str(root),
        "converted_root": str(converted),
        "inventory": inventory,
        "totals": totals,
        "weak_zones": weak_zones,
        "ready": True,
        "wrote_index": True,
        "written": [
            str(summary_path),
            str(patterns_path),
            str(coverage_path),
        ],
        "sections": len(sections),
        "recurring_patterns": len(recurring),
        "one_off_patterns": len(one_off),
    }


__all__ = ["build_course_index"]
