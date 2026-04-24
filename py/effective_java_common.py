from __future__ import annotations

import html
import re
from typing import Iterable


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def image_block(path: str, caption: str) -> str:
    safe_caption = html.escape(caption)
    return (
        f'<div style="margin:18px 0 10px;">'
        f'<img src="{html.escape(path, quote=True)}" alt="{safe_caption}" '
        f'style="width:100%;max-height:420px;object-fit:contain;border:1px solid #e2e8f0;'
        f'border-radius:12px;background:#f8fafc;">'
        f'<p style="font-size:0.95rem;color:#475569;margin-top:8px;">{safe_caption}</p>'
        f"</div>"
    )


IMAGE_BLOCK_RE = re.compile(
    r'<div style="margin:18px 0 10px;"><img\b[^>]*><p style="font-size:0\.95rem;color:#475569;margin-top:8px;">.*?</p></div>',
    re.DOTALL,
)


def strip_image_blocks(content: str) -> str:
    return IMAGE_BLOCK_RE.sub("", content)


def callout(kind: str, text: str) -> str:
    return f'<div class="{html.escape(kind, quote=True)}">{text}</div>'


def bullets(items: Iterable[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def code_block(code: str) -> str:
    return f"<pre><code>{html.escape(code)}</code></pre>"


def page_label(start_page: int, end_page: int) -> str:
    if start_page == end_page:
        return f"Source page {start_page}"
    return f"Source pages {start_page}-{end_page}"


def slide(
    paragraphs: list[str],
    *,
    image: str | None = None,
    caption: str | None = None,
    points: list[str] | None = None,
    box: tuple[str, str] | None = None,
    code: str | None = None,
    source_pages: tuple[int, int] | None = None,
) -> str:
    parts = [f"<p>{text}</p>" for text in paragraphs]
    if points:
        parts.append(bullets(points))
    if code:
        parts.append(code_block(code))
    if image and caption:
        parts.append(image_block(image, caption))
    if source_pages:
        parts.append(
            callout(
                "note",
                f"<strong>Source span:</strong> {html.escape(page_label(*source_pages))}.",
            )
        )
    if box:
        parts.append(callout(box[0], box[1]))
    return "\n".join(parts)


def q(
    prompt: str,
    correct: str,
    wrong_1: str,
    wrong_2: str,
    wrong_3: str,
    explanation: str,
    *,
    question_id: str | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "question": prompt,
        "options": [correct, wrong_1, wrong_2, wrong_3],
        "answer": 0,
        "explanation": explanation,
    }
    if question_id:
        payload["id"] = question_id
    return payload


def module(
    name: str,
    slide_defs: list[tuple[str, str]],
    questions: list[dict[str, object]],
) -> dict[str, object]:
    slides = [{"title": title, "content": content} for title, content in slide_defs]
    return {"name": name, "slides": slides, "questions": questions}


def attach_question_ids(modules: list[dict[str, object]], prefix: str) -> None:
    for module_index, module_data in enumerate(modules):
        for question_index, question in enumerate(module_data["questions"], start=1):
            question.setdefault("id", f"{prefix}_m{module_index}_q{question_index}")
