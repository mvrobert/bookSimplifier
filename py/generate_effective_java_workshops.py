from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path

import generate_workshop as base

from effective_java_common import attach_question_ids


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate chapter workshops for EffectiveJava from chapter modules.")
    parser.add_argument(
        "--book-root",
        type=Path,
        default=Path("output") / "EffectiveJava",
        help="Root extracted book directory containing chapter_manifest.json.",
    )
    return parser.parse_args()


def load_manifest(book_root: Path) -> dict[str, object]:
    return json.loads((book_root / "chapter_manifest.json").read_text(encoding="utf-8"))


def load_chapter_payload(module_name: str) -> dict[str, object]:
    module = importlib.import_module(f"effective_java_chapters.{module_name}")
    return module.CHAPTER


def render_chapter(book_root: Path, chapter_info: dict[str, object], chapter_payload: dict[str, object]) -> None:
    slug = chapter_info["slug"]
    output_dir = book_root / "chapters" / slug
    output_dir.mkdir(parents=True, exist_ok=True)

    modules = chapter_payload["modules"]
    attach_question_ids(modules, slug)

    base.TOPIC_SLUG = slug
    base.WORKSHOP_TITLE = chapter_payload["title"]
    base.WORKSHOP_SUBTITLE = chapter_payload["subtitle"]
    base.MODULES = modules

    slides = base.build_slides()
    quiz_data = base.build_quiz_data()
    html = base.build_html(slides, quiz_data)

    (output_dir / f"{slug}_workshop.html").write_text(html, encoding="utf-8")
    (output_dir / f"{slug}_quiz.json").write_text(
        json.dumps(quiz_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def build_index(book_root: Path, manifest: dict[str, object]) -> None:
    links = []
    for chapter in manifest["chapters"]:
        slug = chapter["slug"]
        links.append(
            f'<li><a href="chapters/{slug}/{slug}_workshop.html">{chapter["full_title"]}</a>'
            f' <span>Pages {chapter["start_page"]}-{chapter["end_page"]}</span></li>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Effective Java Chapter Index</title>
  <style>
    body {{
      margin: 0;
      font-family: "Segoe UI", system-ui, sans-serif;
      background: linear-gradient(180deg, #f4f7fb 0%, #eef2ff 100%);
      color: #172033;
    }}
    main {{
      max-width: 920px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #d8e2f0;
      border-radius: 16px;
      padding: 24px;
      box-shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
    }}
    h1 {{
      margin-top: 0;
      font-size: 2rem;
    }}
    ul {{
      padding-left: 1.2rem;
      line-height: 1.8;
    }}
    li {{
      margin: 10px 0;
    }}
    a {{
      color: #1d4ed8;
      text-decoration: none;
      font-weight: 700;
    }}
    span {{
      color: #475569;
      margin-left: 6px;
    }}
  </style>
</head>
<body>
  <main>
    <div class="card">
      <h1>Effective Java Workshop Index</h1>
      <p>This book was extracted into chapter-level self-contained workshops. Open any chapter below.</p>
      <ul>
        {"".join(links)}
      </ul>
    </div>
  </main>
</body>
</html>
"""
    (book_root / "effective_java_index.html").write_text(html, encoding="utf-8")


def main() -> None:
    args = parse_args()
    book_root = args.book_root.resolve()
    manifest = load_manifest(book_root)

    for chapter_info in manifest["chapters"]:
        chapter_payload = load_chapter_payload(chapter_info["slug"])
        render_chapter(book_root, chapter_info, chapter_payload)

    build_index(book_root, manifest)


if __name__ == "__main__":
    main()
