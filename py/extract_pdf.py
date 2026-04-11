from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz


def safe_stem(name: str) -> str:
    return "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in name)


def extract_pdf(pdf_path: Path, output_root: Path) -> None:
    pdf_path = pdf_path.resolve()
    doc_slug = safe_stem(pdf_path.stem)
    doc_root = output_root / doc_slug
    text_dir = doc_root / "pages"
    image_dir = doc_root / "images"
    preview_dir = doc_root / "page_previews"

    text_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)
    preview_dir.mkdir(parents=True, exist_ok=True)

    document = fitz.open(pdf_path)
    combined_pages: list[str] = []
    image_manifest: list[dict[str, str | int]] = []

    for page_index in range(document.page_count):
        page = document.load_page(page_index)
        page_number = page_index + 1
        page_text = page.get_text("text").strip()
        page_text_path = text_dir / f"page_{page_number:04d}.txt"
        page_text_path.write_text(page_text, encoding="utf-8")

        preview_path = preview_dir / f"page_{page_number:04d}.png"
        page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(preview_path)

        combined_pages.append(f"--- Page {page_number} ---\n{page_text}\n")

        for image_number, image in enumerate(page.get_images(full=True), start=1):
            xref = image[0]
            base_image = document.extract_image(xref)
            extension = base_image.get("ext", "bin")
            image_filename = f"page_{page_number:04d}_img_{image_number:02d}.{extension}"
            image_path = image_dir / image_filename
            image_path.write_bytes(base_image["image"])
            image_manifest.append(
                {
                    "page": page_number,
                    "image_index": image_number,
                    "xref": xref,
                    "path": str(image_path.relative_to(doc_root)),
                }
            )

    (doc_root / "document.txt").write_text("\n".join(combined_pages), encoding="utf-8")
    (doc_root / "metadata.json").write_text(
        json.dumps(
            {
                "source_pdf": str(pdf_path),
                "page_count": document.page_count,
                "image_count": len(image_manifest),
                "page_preview_count": document.page_count,
                "images": image_manifest,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract text and embedded images from a PDF into a structured output folder."
    )
    parser.add_argument("pdf", type=Path, help="Path to the source PDF file.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("output"),
        help="Folder where extracted assets will be written.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    extract_pdf(args.pdf, args.output_root)


if __name__ == "__main__":
    main()
