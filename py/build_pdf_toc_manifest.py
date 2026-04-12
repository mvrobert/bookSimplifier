from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import fitz


CHAPTER_PREFIX_RE = re.compile(r"^Chapter\s+(\d+)\s*(?:[.\-])\s+(.+)$", re.IGNORECASE)
CHAPTER_PLAIN_RE = re.compile(r"^(\d+)\s+(.+)$")
ITEM_RE = re.compile(r"^Item\s+(\d+):\s*(.+)$")
SECTION_RE = re.compile(r"^(\d+(?:\.\d+)+)\.?\s+(.+)$")


def safe_stem(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name)


def parse_chapter_title(title: str) -> tuple[int, str] | None:
    text = title.strip()
    prefixed = CHAPTER_PREFIX_RE.match(text)
    if prefixed:
        return int(prefixed.group(1)), prefixed.group(2).strip()

    plain = CHAPTER_PLAIN_RE.match(text)
    if plain:
        return int(plain.group(1)), plain.group(2).strip()

    return None


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

    chapter_toc_entries: list[tuple[int, str, int]] = []
    for level, title, page in toc:
        parsed = parse_chapter_title(title)
        if parsed is None:
            continue
        chapter_toc_entries.append((level, title, page))

    for index, (level, title, page) in enumerate(chapter_toc_entries):
        parsed = parse_chapter_title(title)
        if parsed is None:
            continue

        chapter_number, chapter_title = parsed
        next_chapter_page = document.page_count + 1
        if index + 1 < len(chapter_toc_entries):
            next_chapter_page = chapter_toc_entries[index + 1][2]

        chapter_entries.append(
            {
                "chapter_number": chapter_number,
                "title": chapter_title,
                "full_title": title.strip(),
                "start_page": page,
                "end_page": next_chapter_page - 1,
                "items": [],
                "_level": level,
            }
        )

    chapter_by_start = {int(chapter["start_page"]): chapter for chapter in chapter_entries}
    current_chapter: dict[str, object] | None = None

    for level, title, page in toc:
        if parse_chapter_title(title) is not None:
            current_chapter = chapter_by_start.get(page)
            continue

        if current_chapter is None:
            continue

        expected_item_level = int(current_chapter["_level"]) + 1
        if level != expected_item_level:
            continue

        item_match = ITEM_RE.match(title.strip())
        section_match = SECTION_RE.match(title.strip())
        if item_match:
            item_number: int | str = int(item_match.group(1))
            item_title = item_match.group(2).strip()
            item_slug = f"item_{int(item_number):02d}_{safe_stem(item_title.lower())}"
        elif section_match:
            item_number = section_match.group(1)
            item_title = section_match.group(2).strip()
            item_slug = f"section_{safe_stem(str(item_number))}_{safe_stem(item_title.lower())}"
        else:
            continue

        item_entry = {
            "item_number": item_number,
            "title": item_title,
            "full_title": title.strip(),
            "start_page": page,
            "end_page": int(current_chapter["end_page"]),
            "slug": item_slug,
        }

        items = current_chapter["items"]
        if items:
            items[-1]["end_page"] = page - 1
        items.append(item_entry)

    chapters_out = []
    for chapter in chapter_entries:
        chapter_slug = f"chapter_{chapter['chapter_number']:02d}_{safe_stem(str(chapter['title']).lower())}"
        chapter["slug"] = chapter_slug
        chapter["item_count"] = len(chapter["items"])
        chapter.pop("_level", None)
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
