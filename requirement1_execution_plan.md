# Requirement 1 Execution Plan

## Scope

Process these source PDFs in `C:\Users\Robert\Downloads\jesc1dd\`:

- `jesc102.pdf`
- `jesc103.pdf`
- `jesc104.pdf`
- `jesc105.pdf`

For each PDF, produce a separate output directory containing:

- extracted page text
- extracted images in an `images/` folder
- metadata about the extraction
- a kid-friendly mobile-friendly workshop HTML file
- a companion quiz JSON file

## Constraints From `requirement1.md`

- All Python code must live under `py/`
- Keep outputs inside this workspace
- Each PDF must have its own output directory
- Workshop content should be interactive, kid-friendly, and readable in small portions
- Avoid framing the deck as a dry “chapter objective”
- Do not refer learners to other PDFs or chapters
- Use local storage so learners can continue later on mobile
- Include images in the slides
- If source wording is not reader-friendly, rewrite it more clearly
- Additional science knowledge may be added where it helps understanding

## Execution Steps

1. Review the existing extraction and workshop-generation code already created for `jesc101.pdf`.
2. Upgrade the tooling so it works cleanly for multiple PDFs and stores all generated files inside each PDF’s own output folder.
3. Extend the workshop generator so slides can include extracted images and remain mobile-friendly.
4. Run extraction for:
   - `jesc102.pdf`
   - `jesc103.pdf`
   - `jesc104.pdf`
   - `jesc105.pdf`
5. Inspect extracted text from each PDF to identify the science topic and the main subtopics to turn into modules.
6. Generate a separate workshop HTML and quiz JSON for each PDF, using:
   - kid-friendly language
   - short interactive explanations
   - deterministic quiz shuffling
   - localStorage progress persistence
   - extracted images embedded in content slides
7. Verify outputs exist for all four PDFs and that each workshop includes:
   - TOC
   - keyboard navigation
   - quiz flow
   - retry support
   - local storage state tracking
   - mobile-appropriate layout
8. Summarize results with file locations and note any limitations if a PDF’s extracted text is noisy.

## Output Layout Target

For each PDF `jescXYZ.pdf`, target a folder like:

- `output/jescXYZ/`

Inside that folder:

- `document.txt`
- `metadata.json`
- `pages/`
- `images/`
- `jescXYZ_workshop.html`
- `jescXYZ_quiz.json`

## Notes

- Existing dependencies in `requirements.txt` will be reused unless a new dependency becomes necessary.
- Preference is to reuse extracted PDF images rather than fetch external assets, unless local material is insufficient.
- Verification will include a quick structural check of generated HTML and quiz JSON for each PDF.
