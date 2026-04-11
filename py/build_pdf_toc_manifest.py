from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import fitz


CHAPTER_RE = re.compile(r"^(\d+)\s+(.+)$")
ITEM_RE = re.compile(r"^Item\s+(\d+):\s*(.+)$")


def safe_stem(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a chapter and item manifest from a PDF table of contents.")
    parser.add_argument("pdf", type=Path, help="Path to a PDF file.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("output"),
        help="Root output directory where the manifest should be written.",
    )
    return parser.parse_args()


def build_manifest(pdf_path: Path, output_root: Path) -> Path:
    pdf_path = pdf_path.resolve()
    book_slug = safe_stem(pdf_path.stem)
    book_root = output_root / book_slug
    manifest_path = book_root / "chapter_manifest.json"

    document = fitz.open(pdf_path)
    toc = document.get_toc(simple=True)
    chapter_entries: list[dict[str, object]] = []

    for index, (level, title, page) in enumerate(toc):
        if level != 1:
            continue
        match = CHAPTER_RE.match(title.strip())
        if not match:
            continue

        chapter_number = int(match.group(1))
        chapter_title = match.group(2).strip()
        next_chapter_page = document.page_count + 1
        for next_level, next_title, next_page in toc[index + 1 :]:
            if next_level == 1 and CHAPTER_RE.match(next_title.strip()):
                next_chapter_page = next_page
                break

        chapter_entries.append(
            {
                "chapter_number": chapter_number,
                "title": chapter_title,
                "full_title": title.strip(),
                "start_page": page,
                "end_page": next_chapter_page - 1,
                "items": [],
            }
        )

    chapter_by_start = {int(chapter["start_page"]): chapter for chapter in chapter_entries}
    current_chapter: dict[str, object] | None = None
    pending_items: list[tuple[int, dict[str, object]]] = []

    for level, title, page in toc:
        chapter_match = CHAPTER_RE.match(title.strip())
        if level == 1 and chapter_match:
            current_chapter = chapter_by_start.get(page)
            pending_items = []
            continue

        if current_chapter is None or level != 2:
            continue

        item_match = ITEM_RE.match(title.strip())
        if not item_match:
            continue

        item_number = int(item_match.group(1))
        item_title = item_match.group(2).strip()
        item_entry = {
            "item_number": item_number,
            "title": item_title,
            "full_title": title.strip(),
            "start_page": page,
            "end_page": int(current_chapter["end_page"]),
        }

        items = current_chapter["items"]
        if items:
            items[-1]["end_page"] = page - 1
        items.append(item_entry)

    chapters_out = []
    for chapter in chapter_entries:
        chapter_slug = f"chapter_{chapter['chapter_number']:02d}_{safe_stem(str(chapter['title']).lower())}"
        chapter["slug"] = chapter_slug
        chapter["items"] = [
            {
                **item,
                "slug": f"item_{item['item_number']:02d}_{safe_stem(str(item['title']).lower())}",
            }
            for item in chapter["items"]
        ]
        chapter["item_count"] = len(chapter["items"])
        chapters_out.append(chapter)

    manifest = {
        "source_pdf": str(pdf_path),
        "book_slug": book_slug,
        "page_count": document.page_count,
        "chapter_count": len(chapters_out),
        "chapters": chapters_out,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def main() -> None:
    args = parse_args()
    manifest_path = build_manifest(args.pdf, args.output_root)
    print(manifest_path)


if __name__ == "__main__":
    main()
