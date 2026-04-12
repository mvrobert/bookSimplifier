## JavaConcurrency Execution Plan

### Source PDF

- `JavaConcurrency.pdf`

### Expected Output Root

- `output/JavaConcurrency/`

### Expected Extraction Outputs

- `output/JavaConcurrency/document.txt`
- `output/JavaConcurrency/metadata.json`
- `output/JavaConcurrency/pages/`
- `output/JavaConcurrency/images/`
- `output/JavaConcurrency/page_previews/`

### Expected Workshop Outputs

- `output/JavaConcurrency/JavaConcurrency_workshop.html`
- `output/JavaConcurrency/JavaConcurrency_quiz.json`
- `output/JavaConcurrency/chapter_manifest.json` if the PDF exposes a usable table of contents
- additional chapter-level workshop output under `output/JavaConcurrency/chapters/` if the TOC structure is strong enough to support reliable splitting

### Extraction Steps

1. Run the existing PDF extractor against `JavaConcurrency.pdf`.
2. Extract page text into `pages/page_XXXX.txt`.
3. Combine extracted text into `document.txt`.
4. Extract embedded images into `images/`.
5. Render page preview PNGs into `page_previews/`.
6. Capture summary metadata in `metadata.json`.

### Structure Inspection Steps

1. Attempt to build a TOC manifest from the PDF bookmarks.
2. Inspect the extracted opening pages and a few later pages to determine the book title, chapter structure, and topic flow.
3. Decide whether the book should be rendered as:
   - a single full-book workshop, or
   - a chapter-aware set of workshops plus a merged entry point
4. Prefer chapter-aware output if the bookmark structure is reliable enough.

### Workshop Generation Steps

1. Reuse the existing local HTML/CSS/JS workshop shell so the output stays self-contained and mobile-friendly.
2. Build short modules based on the extracted Java concurrency topics instead of forcing the original school-science framing.
3. Use local page preview images where they improve comprehension.
4. Generate companion quiz JSON using the existing answer format.
5. Keep browser localStorage persistence for progress and quiz state.

### Verification Steps

1. Confirm extraction outputs exist under `output/JavaConcurrency/`.
2. Confirm the workshop HTML file exists.
3. Confirm the quiz JSON file exists.
4. Confirm page previews and extracted images exist.
5. Confirm the HTML remains local and self-contained with no network dependency.
6. Confirm localStorage support remains present in the generated workshop.
