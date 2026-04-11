## Effective Java Execution Plan

### Source PDF

- `EffectiveJava.pdf`

### Expected Output Root

- `output/EffectiveJava/`

### Expected Extraction Outputs

- `output/EffectiveJava/document.txt`
- `output/EffectiveJava/metadata.json`
- `output/EffectiveJava/pages/`
- `output/EffectiveJava/images/`
- `output/EffectiveJava/page_previews/`

### Expected Chapter Workshop Outputs

- `output/EffectiveJava/chapters/chapter_01_introduction/`
- `output/EffectiveJava/chapters/chapter_02_creating_and_destroying_objects/`
- `output/EffectiveJava/chapters/chapter_03_methods_common_to_all_objects/`
- `output/EffectiveJava/chapters/chapter_04_classes_and_interfaces/`
- `output/EffectiveJava/chapters/chapter_05_generics/`
- `output/EffectiveJava/chapters/chapter_06_enums_and_annotations/`
- `output/EffectiveJava/chapters/chapter_07_lambdas_and_streams/`
- `output/EffectiveJava/chapters/chapter_08_methods/`
- `output/EffectiveJava/chapters/chapter_09_general_programming/`
- `output/EffectiveJava/chapters/chapter_10_exceptions/`
- `output/EffectiveJava/chapters/chapter_11_concurrency/`
- `output/EffectiveJava/chapters/chapter_12_serialization/`

### Extraction Steps

1. Run the existing PDF extractor on `EffectiveJava.pdf`.
2. Extract page text into `pages/page_XXXX.txt`.
3. Combine extracted text into `document.txt`.
4. Extract embedded images into `images/`.
5. Render page preview PNGs into `page_previews/`.
6. Capture PDF table-of-contents structure and chapter boundaries in metadata for downstream chapter generation.

### Workshop Generation Steps

1. Build a chapter-aware Python generator under `py/`.
2. Read the PDF TOC and map each chapter to its item ranges and page spans.
3. Generate one output folder per chapter under `output/EffectiveJava/chapters/`.
4. Generate one self-contained HTML workshop per chapter with:
   - progress UI
   - previous / next navigation
   - TOC navigation
   - quiz flow
   - retry support
   - localStorage persistence
   - local page preview images
5. Generate one quiz JSON file per chapter.
6. Generate a root summary index for the book if useful for navigation.

### Parallel Execution Steps

1. Split chapter generation into non-overlapping groups across sub-agents.
2. Give each worker ownership of specific chapter output folders only.
3. Keep shared script edits centralized in the main agent.
4. Have workers only generate chapter content and outputs after the shared generator is ready.
5. Close workers after generation finishes.

### Verification Steps

1. Confirm extraction output exists for the book root.
2. Confirm all 12 chapter folders exist.
3. Confirm each chapter folder contains:
   - HTML workshop
   - quiz JSON
   - image references pointing at local page previews
4. Confirm each workshop contains structural support for:
   - TOC
   - progress tracking
   - retry flow
   - localStorage
5. Confirm chapter generation covers all TOC chapters from the PDF.
6. Syntax-check any new Python scripts.
