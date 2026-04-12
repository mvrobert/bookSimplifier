from __future__ import annotations

import json
import re
from pathlib import Path

import generate_workshop as base

from effective_java_common import attach_question_ids, module, q, slide


SCIENCE_ROOT = Path("science") / "output"
OUTPUT_DIR = SCIENCE_ROOT / "workshop"
TOPIC_SLUG = "science_complete"
WORKSHOP_TITLE = "Science Complete Workshop"
WORKSHOP_SUBTITLE = "Merged workshop built from completed science outputs in science/output"


def parse_js_array(source: str, name: str) -> list[dict[str, object]] | list[str]:
    match = re.search(rf"const {name} = (\[.*?\]);", source, re.S)
    if not match:
        raise ValueError(f"Could not find {name} in workshop HTML")
    return json.loads(match.group(1))


def parse_data_object(source: str) -> dict[str, object]:
    match = re.search(r"const DATA = (\{.*?\});\s*const KEY", source, re.S)
    if not match:
        raise ValueError("Could not find DATA object in workshop HTML")
    return json.loads(match.group(1))


def rewrite_asset_paths(html: str, slug: str) -> str:
    html = html.replace('src="page_previews/', f'src="../{slug}/page_previews/')
    html = html.replace('src="images/', f'src="../{slug}/images/')
    return html


def extract_static_modules(source: str) -> list[list[dict[str, str]]]:
    modules: list[list[dict[str, str]]] = []
    for section_html in re.findall(r'<section class="module"[^>]*>(.*?)</section>', source, re.S):
        slides: list[dict[str, str]] = []
        for article_html in re.findall(r'<article class="slide"[^>]*>(.*?)</article>', section_html, re.S):
            title_match = re.search(r"<h3>(.*?)</h3>", article_html, re.S)
            title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else "Slide"
            body = re.sub(r"<h3>.*?</h3>", "", article_html, count=1, flags=re.S).strip()
            slides.append({"title": title, "content": body})
        modules.append(slides)
    return modules


def load_completed_books() -> list[dict[str, object]]:
    books: list[dict[str, object]] = []
    for quiz_path in sorted(SCIENCE_ROOT.rglob("*_quiz.json")):
        slug = quiz_path.parent.name
        workshop_path = quiz_path.parent / f"{slug}_workshop.html"
        if not workshop_path.exists():
            continue

        quiz_data = json.loads(quiz_path.read_text(encoding="utf-8"))
        workshop_html = workshop_path.read_text(encoding="utf-8")
        data_object = parse_data_object(workshop_html) if "const DATA =" in workshop_html else None
        slides = parse_js_array(workshop_html, "SLIDES") if "const SLIDES =" in workshop_html else None
        module_names = parse_js_array(workshop_html, "MODULE_NAMES") if "const MODULE_NAMES =" in workshop_html else None
        static_modules = extract_static_modules(workshop_html) if slides is None and data_object is None else None

        books.append(
            {
                "slug": slug,
                "title": str(quiz_data["title"]).split(" - ")[0],
                "quiz_data": quiz_data,
                "data_object": data_object,
                "slides": slides,
                "module_names": module_names,
                "static_modules": static_modules,
            }
        )
    return books


def build_intro_module(books: list[dict[str, object]]) -> dict[str, object]:
    completed_titles = [str(book["title"]) for book in books]
    return module(
        "Merged Overview",
        [
            (
                "What This Deck Includes",
                slide(
                    [
                        "This merged workshop combines the completed science workshop outputs already present under `science/output` into one reading and revision deck.",
                        "It keeps the original module content, quizzes, and local asset usage, but places everything under one HTML file so a learner can move across topics without opening each workshop separately.",
                        "The source path also contains `jesc101`, but that folder is extraction-only in this location and does not currently have its own workshop HTML or quiz JSON, so it is not included in this merged deck.",
                    ],
                    points=[f"Included: {title}" for title in completed_titles],
                    box=("note", "<strong>Merge scope:</strong> this deck includes completed workshop outputs only, so it merges `jesc102` through `jesc113` plus `jesc1an`."),
                ),
            ),
            (
                "How To Use The Merged Deck",
                slide(
                    [
                        "Use the table of contents to jump by topic, or use the chapter jump bar to move across the merged science books quickly.",
                        "Each module still ends with its own quiz slide, so progress and retry behavior continue to work the same way as in the original workshop files.",
                        "The content remains local and self-contained. Images are referenced from the existing per-book output folders, and your progress is stored in browser localStorage using a merged store key.",
                    ],
                    points=[
                        "Read one topic at a time or use it as a revision deck.",
                        "Use Retry to revisit missed quiz questions.",
                        "Open source-specific modules from the TOC when revising one chapter family.",
                    ],
                    box=("tip", "<strong>Recommended flow:</strong> study a topic block, complete its quiz, then jump to the next science unit from the top jump bar."),
                ),
            ),
        ],
        [
            q(
                "Which science output is not included in this merged workshop because it lacks a completed workshop HTML in `science/output`?",
                "jesc101",
                "jesc102",
                "jesc112",
                "jesc1an",
                "The `science/output/jesc101` folder contains extraction output, but not a finished workshop HTML and quiz JSON.",
            ),
            q(
                "What is the main purpose of this merged deck?",
                "To let the learner study all completed science workshops from one HTML file",
                "To delete the original workshop folders",
                "To convert the PDFs again from scratch",
                "To remove quiz slides from the science content",
                "The merged deck preserves the completed workshop content while giving it a single entry point.",
            ),
        ],
    )


def build_book_modules(book: dict[str, object]) -> list[dict[str, object]]:
    quiz_modules = list(book["quiz_data"]["modules"])
    data_object = book["data_object"]
    slides = list(book["slides"]) if book["slides"] is not None else None
    static_modules = list(book["static_modules"]) if book["static_modules"] is not None else None
    slug = str(book["slug"])
    title = str(book["title"])
    modules: list[dict[str, object]] = []

    for module_index, quiz_module in enumerate(quiz_modules):
        module_slides: list[dict[str, object]] = []
        if data_object is not None:
            data_slides = list(data_object["slides"])
            total_modules = len(quiz_modules)
            total_slides = len(data_slides)
            base_count = total_slides // total_modules
            remainder = total_slides % total_modules
            start = 0
            for index in range(module_index):
                start += base_count + (1 if index < remainder else 0)
            count = base_count + (1 if module_index < remainder else 0)
            for slide_info in data_slides[start : start + count]:
                pages = list(slide_info.get("pages", []))
                preview_html = ""
                if pages:
                    figures = "".join(
                        f'<figure class="preview"><img src="../{slug}/page_previews/page_{page:04d}.png" alt="Page {page} preview"><figcaption>Page {page}</figcaption></figure>'
                        for page in pages[:3]
                    )
                    preview_html = f'<div class="previews">{figures}</div>'
                body = (
                    f'<p class="lede">{slide_info.get("summary", "")}</p>'
                    f'{base.bullets(slide_info.get("bullets", [])) if False else ""}'
                )
                bullets = "<ul>" + "".join(f"<li>{item}</li>" for item in slide_info.get("bullets", [])) + "</ul>"
                content = (
                    f"<div class=\"note\"><strong>{slide_info.get('eyebrow', 'Slide')}:</strong> {slide_info.get('callout', '')}</div>"
                    f"<p>{slide_info.get('summary', '')}</p>"
                    f"{bullets}"
                    f"{preview_html}"
                )
                module_slides.append({"title": str(slide_info["title"]), "content": content})
        elif slides is not None:
            for slide_data in slides:
                if int(slide_data["m"]) != module_index or slide_data.get("q"):
                    continue
                module_slides.append(
                    {
                        "title": str(slide_data["t"]),
                        "content": rewrite_asset_paths(str(slide_data["c"]), slug),
                    }
                )
        else:
            for slide_data in static_modules[module_index]:
                module_slides.append(
                    {
                        "title": str(slide_data["title"]),
                        "content": rewrite_asset_paths(str(slide_data["content"]), slug),
                    }
                )

        modules.append(
            {
                "name": f"{title} - {quiz_module['name']}",
                "slides": module_slides,
                "questions": list(quiz_module["questions"]),
            }
        )
    return modules


def build_book_jumps(book_counts: list[tuple[str, int]], slides: list[dict[str, object]]) -> list[dict[str, object]]:
    jumps: list[dict[str, object]] = []
    module_offset = 0
    for title, count in book_counts:
        slide_index = next(index for index, slide in enumerate(slides) if int(slide["m"]) == module_offset)
        jumps.append({"title": title, "label": title, "slideIndex": slide_index})
        module_offset += count
    return jumps


def rewrite_question_ids(modules: list[dict[str, object]], prefix: str) -> None:
    for module_index, module_data in enumerate(modules):
        for question_index, question in enumerate(module_data["questions"], start=1):
            question["id"] = f"{prefix}_m{module_index}_q{question_index}"


def add_book_jump_bar(html: str, jumps: list[dict[str, object]]) -> str:
    css = """
    #book-jump-bar {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 2px 2px 8px;
      margin-bottom: 14px;
      scrollbar-width: thin;
    }
    .book-jump {
      flex: 0 0 auto;
      white-space: nowrap;
      background: #ecfccb;
      border-color: #bef264;
      font-size: 0.92rem;
      padding: 8px 12px;
    }
    .book-jump.current {
      background: #3f6212;
      border-color: #3f6212;
      color: #fff;
    }
    @media print {
      #book-jump-bar { display: none !important; }
    }
"""
    html = html.replace("</style>", f"{css}\n  </style>", 1)
    html = html.replace('    <div id="slide"></div>', '    <div id="book-jump-bar"></div>\n    <div id="slide"></div>', 1)
    html = html.replace(
        "    let cur = 0;",
        "    const BOOK_JUMPS = " + json.dumps(jumps, ensure_ascii=False) + ";\n\n    let cur = 0;",
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
        """    function renderBookJumpBar() {
      const bar = document.getElementById('book-jump-bar');
      if (!bar) {
        return;
      }
      let currentBook = 0;
      for (let i = 0; i < BOOK_JUMPS.length; i += 1) {
        if (cur >= BOOK_JUMPS[i].slideIndex) {
          currentBook = i;
        } else {
          break;
        }
      }
      bar.innerHTML = BOOK_JUMPS.map((entry, index) => `
        <button class="book-jump ${index === currentBook ? 'current' : ''}" onclick="jump(${entry.slideIndex})" title="${esc(entry.title)}">
          ${esc(entry.label)}
        </button>
      `).join('');
    }

    function render() {
      const slide = SLIDES[cur];
      const progress = Math.round(((cur + 1) / SLIDES.length) * 100);
      document.getElementById('progress-bar').style.width = progress + '%';
      document.getElementById('pct').textContent = progress + '%';
      document.getElementById('slide-counter').textContent = `${cur + 1} / ${SLIDES.length}`;
      document.getElementById('module-label').textContent = MODULE_NAMES[slide.m];
      document.getElementById('slide').innerHTML = slide.q ? renderQuiz(slide.m) : `<h1>${esc(slide.t)}</h1>${slide.c}`;
      save();
      renderBookJumpBar();
      buildTOC();
    }
""",
        1,
    )
    return html


def main() -> None:
    books = load_completed_books()
    merged_modules = [build_intro_module(books)]
    book_counts: list[tuple[str, int]] = [("Overview", 1)]

    for book in books:
        modules = build_book_modules(book)
        merged_modules.extend(modules)
        book_counts.append((str(book["title"]), len(modules)))

    rewrite_question_ids(merged_modules, TOPIC_SLUG)

    base.TOPIC_SLUG = TOPIC_SLUG
    base.WORKSHOP_TITLE = WORKSHOP_TITLE
    base.WORKSHOP_SUBTITLE = WORKSHOP_SUBTITLE
    base.MODULES = merged_modules

    slides = base.build_slides()
    quiz_data = base.build_quiz_data()
    html = add_book_jump_bar(base.build_html(slides, quiz_data), build_book_jumps(book_counts, slides))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / f"{TOPIC_SLUG}_workshop.html").write_text(html, encoding="utf-8")
    (OUTPUT_DIR / f"{TOPIC_SLUG}_quiz.json").write_text(
        json.dumps(quiz_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
