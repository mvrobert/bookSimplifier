from __future__ import annotations

import argparse
import copy
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


def prepare_modules(
    chapter_info: dict[str, object],
    chapter_payload: dict[str, object],
    *,
    merged: bool,
) -> list[dict[str, object]]:
    modules = copy.deepcopy(chapter_payload["modules"])
    if merged:
        chapter_label = chapter_info["full_title"]
        for module_data in modules:
            module_data["name"] = f"{chapter_label} - {module_data['name']}"
            for slide_data in module_data["slides"]:
                slide_data["content"] = slide_data["content"].replace(
                    "../../page_previews/",
                    "page_previews/",
                )
    return modules


def render_chapter(book_root: Path, chapter_info: dict[str, object], chapter_payload: dict[str, object]) -> None:
    slug = chapter_info["slug"]
    output_dir = book_root / "chapters" / slug
    output_dir.mkdir(parents=True, exist_ok=True)

    modules = prepare_modules(chapter_info, chapter_payload, merged=False)
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


def build_chapter_jumps(
    manifest: dict[str, object],
    chapter_module_lengths: list[int],
    slides: list[dict[str, object]],
) -> list[dict[str, object]]:
    jumps: list[dict[str, object]] = []
    module_offset = 0
    for chapter_info, module_count in zip(manifest["chapters"], chapter_module_lengths, strict=True):
        slide_index = next(
            index for index, slide in enumerate(slides) if slide["m"] == module_offset
        )
        jumps.append(
            {
                "title": chapter_info["full_title"],
                "label": f"Ch {chapter_info['chapter_number']}",
                "slideIndex": slide_index,
            }
        )
        module_offset += module_count
    return jumps


def add_chapter_jump_bar(html: str, chapter_jumps: list[dict[str, object]]) -> str:
    css = """
    #chapter-jump-bar {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 2px 2px 8px;
      margin-bottom: 14px;
      scrollbar-width: thin;
    }
    .chapter-jump {
      flex: 0 0 auto;
      white-space: nowrap;
      background: #eef2ff;
      border-color: #c7d2fe;
      font-size: 0.92rem;
      padding: 8px 12px;
    }
    .chapter-jump.current {
      background: #1d4ed8;
      border-color: #1d4ed8;
      color: #fff;
    }
    @media print {
      #chapter-jump-bar { display: none !important; }
    }
"""
    html = html.replace("</style>", f"{css}\n  </style>", 1)
    html = html.replace(
        '    <div id="slide"></div>',
        '    <div id="chapter-jump-bar"></div>\n    <div id="slide"></div>',
        1,
    )
    html = html.replace(
        "    let cur = 0;",
        "    const CHAPTER_JUMPS = "
        + json.dumps(chapter_jumps, ensure_ascii=False)
        + ";\n\n    let cur = 0;",
        1,
    )
    html = html.replace(
        """    function render() {
      const slide = SLIDES[cur];
      const progress = Math.round(((cur + 1) / SLIDES.length) * 100);
      document.getElementById('progress-bar').style.width = progress + '%';
      document.getElementById('pct').textContent = progress + '%';
      document.getElementById('slide-counter').textContent = `${cur + 1} / ${SLIDES.length}`;
      document.getElementById('module-label').textContent = MODULE_NAMES[slide.m];
      document.getElementById('slide').innerHTML = slide.q ? renderQuiz(slide.m) : `<h1>${esc(slide.t)}</h1>${slide.c}`;
      save();
      buildTOC();
    }
""",
        """    function renderChapterJumpBar() {
      const bar = document.getElementById('chapter-jump-bar');
      if (!bar) {
        return;
      }
      let currentChapter = 0;
      for (let i = 0; i < CHAPTER_JUMPS.length; i += 1) {
        if (cur >= CHAPTER_JUMPS[i].slideIndex) {
          currentChapter = i;
        } else {
          break;
        }
      }
      bar.innerHTML = CHAPTER_JUMPS.map((entry, index) => `
        <button class="chapter-jump ${index === currentChapter ? 'current' : ''}" onclick="jump(${entry.slideIndex})" title="${esc(entry.title)}">
          ${esc(entry.label)}
        </button>
      `).join('');
    }

    function shortModuleLabel(name) {
      const parts = name.split(' - ');
      return parts.length > 1 ? parts.slice(1).join(' - ') : name;
    }

    function render() {
      const slide = SLIDES[cur];
      const progress = Math.round(((cur + 1) / SLIDES.length) * 100);
      document.getElementById('progress-bar').style.width = progress + '%';
      document.getElementById('pct').textContent = progress + '%';
      document.getElementById('slide-counter').textContent = `${cur + 1} / ${SLIDES.length}`;
      document.getElementById('module-label').textContent = shortModuleLabel(MODULE_NAMES[slide.m]);
      document.getElementById('slide').innerHTML = slide.q ? renderQuiz(slide.m) : `<h1>${esc(slide.t)}</h1>${slide.c}`;
      save();
      renderChapterJumpBar();
      buildTOC();
    }
""",
        1,
    )
    return html


def render_merged_workshop(book_root: Path, manifest: dict[str, object]) -> None:
    slug = "effective_java_complete"
    modules: list[dict[str, object]] = []
    chapter_module_lengths: list[int] = []

    for chapter_info in manifest["chapters"]:
        chapter_payload = load_chapter_payload(chapter_info["slug"])
        chapter_modules = prepare_modules(chapter_info, chapter_payload, merged=True)
        chapter_module_lengths.append(len(chapter_modules))
        modules.extend(chapter_modules)

    attach_question_ids(modules, slug)

    base.TOPIC_SLUG = slug
    base.WORKSHOP_TITLE = "Effective Java Complete Workshop"
    base.WORKSHOP_SUBTITLE = "Merged single-file workshop covering Chapters 1-12"
    base.MODULES = modules

    slides = base.build_slides()
    quiz_data = base.build_quiz_data()
    html = add_chapter_jump_bar(
        base.build_html(slides, quiz_data),
        build_chapter_jumps(manifest, chapter_module_lengths, slides),
    )

    (book_root / f"{slug}_workshop.html").write_text(html, encoding="utf-8")
    (book_root / f"{slug}_quiz.json").write_text(
        json.dumps(quiz_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def build_index(book_root: Path, manifest: dict[str, object]) -> None:
    links = []
    links.append(
        '<li><a href="effective_java_complete_workshop.html">Complete merged workshop</a>'
        ' <span>All chapters in one file</span></li>'
    )
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
      <p>This book is available both as one merged workshop and as separate chapter-level self-contained workshops.</p>
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

    render_merged_workshop(book_root, manifest)
    build_index(book_root, manifest)


if __name__ == "__main__":
    main()
