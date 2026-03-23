"""PDF rendering for worksheets using WeasyPrint + Jinja2."""

from __future__ import annotations

from datetime import datetime, timezone
from itertools import groupby
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader

from backend.config import TEMPLATES_DIR

if TYPE_CHECKING:
    from backend.database import Chapter, Question, Worksheet

_jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))


def render_worksheet_pdf(
    worksheet: Worksheet,
    questions: list[Question],
    chapter: Chapter | None,
    show_answers: bool = False,
) -> bytes:
    """Render a worksheet to PDF bytes."""
    from weasyprint import HTML

    # Group questions by section
    sections: list[dict] = []
    for heading, group in groupby(questions, key=lambda q: q.section_heading):
        sections.append({"heading": heading, "questions": list(group)})

    template = _jinja_env.get_template("worksheet.html")
    html_str = template.render(
        worksheet=worksheet,
        chapter=chapter,
        sections=sections,
        show_answers=show_answers,
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    )

    return HTML(string=html_str).write_pdf()
