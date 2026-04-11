---
name: book-simplifier
description: Turn textbook or study PDF books, chapters, notes, answer keys, or revision material into interactive workshop decks with quizzes, extracted text, extracted images, page preview images, and mobile-friendly self-contained HTML output. Use when processing one or more local PDF files into simplified reading material, revision decks, or answer-check workshops stored in separate per-book folders.
---

# Book Simplifier

## Purpose

Convert local textbook-style PDF files into small, interactive workshop decks that are easier to read on mobile and easier to revise with quizzes.

The workflow must:

- extract text from each PDF
- extract embedded PDF images
- render full page preview images
- store every PDF's output in its own directory
- generate a self-contained HTML workshop
- generate a companion quiz JSON file
- preserve progress using browser localStorage
- keep the content friendly, short, readable, and interactive for the intended learner age group

## Generalization Rule

This skill must stay reusable.

Do not hardcode:

- specific PDF filenames
- specific chapter names
- specific subjects
- fixed module titles tied to one book
- quiz counts that assume every source has the same depth

Infer all of those from the current PDF batch.

The same workflow should work for:

- science books
- social studies books
- language books
- math books
- revision or answer keys
- short notes
- long textbook chapters

Adapt the tone, examples, and quiz style to the source subject and learner level.

## Required Behavior

### Input Expectations

- Work from local PDF files in the current workspace.
- Treat every PDF independently.
- Create a separate output folder for each PDF.
- Keep all generated code under `py/`.
- Keep dependency declarations in `requirements.txt`.
- Keep all generated outputs in the current workspace.

### Output Expectations Per PDF

For a PDF like `jescXYZ.pdf`, create:

- `output/jescXYZ/document.txt`
- `output/jescXYZ/metadata.json`
- `output/jescXYZ/pages/`
- `output/jescXYZ/images/`
- `output/jescXYZ/page_previews/`
- `output/jescXYZ/jescXYZ_workshop.html`
- `output/jescXYZ/jescXYZ_quiz.json`

### Content Expectations

- Never make the material sound like a dry textbook objective sheet.
- Do not tell the child to read another chapter or another PDF.
- Rewrite difficult wording into simpler child-friendly language when needed.
- Keep explanations short enough to read in tiny portions.
- Use additional subject knowledge when it improves clarity.
- Preserve subject correctness.
- Use images in the slides.
- Prefer readable page preview images when raw embedded PDF images are noisy, fragmented, decorative, or dominated by QR codes.
- Treat answer booklets or revision PDFs differently from full chapters; turn them into revision or answer-check workshops instead of pretending they are normal concept chapters.

## Detailed Workflow

### 1. Plan First

When starting a new batch, first write a markdown plan file in the workspace. The plan must include:

- which PDFs will be processed
- expected output folders
- extraction steps
- workshop generation steps
- verification steps

### 2. Extract PDF Content

For each PDF:

- extract page text into `pages/page_XXXX.txt`
- combine text into `document.txt`
- extract embedded images into `images/`
- render each page into `page_previews/page_XXXX.png`
- write summary metadata into `metadata.json`

### 3. Inspect Topic Structure

Read enough extracted pages to identify:

- the topic title
- the core subtopics
- whether the material is concept-heavy, story-heavy, diagram-heavy, equation-heavy, example-heavy, exercise-heavy, or revision-heavy
- whether the material is long enough for 4 modules or should be shorter

### 4. Generate Workshop Content

Create a kid-friendly workshop with:

- small lesson units
- short paragraphs
- friendly framing
- image-backed slides
- direct explanations
- simple checkpoints
- quizzes after each module or at regular intervals

Do not assume all subjects need the same workshop structure.

Examples:

- science may need concept plus diagram explanation
- math may need worked examples plus quick practice
- language may need passage explanation plus vocabulary checks
- history may need timeline slides plus cause-effect questions
- answer books may need correction logic and self-check prompts

### 5. Verify Outputs

Confirm for every generated workshop:

- HTML file exists
- quiz JSON exists
- page previews exist
- navigation works structurally
- localStorage support exists
- image references point to the local output folder

## Languages and Technologies Used

### Primary Authoring and Automation Language

Use Python for extraction and generation.

Expected runtime:

- Python 3.12 or compatible modern Python 3

### Output Languages

Use:

- HTML for the workshop document
- CSS for styling
- plain JavaScript for interactivity
- JSON for quiz data

### JavaScript Style

Use dependency-free client-side JavaScript.

Implement:

- slide navigation
- table of contents
- quiz flow
- retry flow
- localStorage save and restore
- progress tracking

## Libraries Used

### Required Python Library

Use:

- `PyMuPDF` for PDF text extraction, embedded image extraction, and page preview rendering

### Python Standard Library Used

Use only simple standard-library modules as needed, such as:

- `argparse`
- `json`
- `pathlib`
- `textwrap`
- `string`

## Libraries and Tooling Not Required

Do not require these unless there is a strong new reason:

- `PyPDF2`
- `pypdf`
- `pdfplumber`
- `Pillow`
- React
- Vue
- external CSS frameworks
- external JavaScript frameworks
- CDN-hosted assets
- external web fonts

These were not needed for the working workflow created here.

## NPM and NPX Guidance

`npm` or `npx` may be used only if a task truly needs them, but this workflow does not require them by default.

Prefer not to use them for this skill because:

- the workshop output is self-contained
- plain HTML/CSS/JS is enough
- fewer dependencies makes local execution more reliable

## Extraction Design Rules

### Why Page Previews Matter

Raw embedded PDF images can be poor slide assets because they may include:

- QR codes
- tiny decorative fragments
- cropped pieces of diagrams
- low-signal layout elements

Because of that, always generate full page preview images and prefer those for workshop visuals unless a specific embedded image is clearly better.

### Metadata Expectations

`metadata.json` should contain at least:

- source PDF path
- page count
- embedded image count
- page preview count
- image manifest with page number and relative path

## Workshop HTML Rules

### Format

Generate a single self-contained HTML file for each PDF.

The file must not depend on:

- external CSS
- external JavaScript
- external fonts
- network access

### Required Features

Every workshop should include:

- a visible progress indicator
- previous and next navigation
- a TOC or contents navigation mechanism
- quiz support
- a retry or retry-missed mechanism
- localStorage persistence
- mobile-friendly layout
- local image usage from that PDF's output folder

### Mobile Behavior

Optimize for phones and smaller screens:

- shorter text chunks
- generous spacing
- readable buttons
- responsive layout
- no desktop-only assumptions

### Persistence

Use browser localStorage so the learner can leave and come back later without losing progress.

At minimum save:

- current slide or module
- quiz answers
- quiz scores
- retry state if used

## Workshop Content Rules

### Tone

Write for the intended learner:

- clear
- friendly
- direct
- not patronizing
- not overly academic

### Explanation Style

Prefer:

- short paragraphs
- examples from daily life
- quick comparisons
- memory hooks
- callout boxes

Avoid:

- dense textbook phrasing
- repeating book headings without simplification
- telling the learner to read some other source

### Use of Images

Include images directly in slides where they help:

- opening context
- diagrams
- page figure overviews
- visual reinforcement

### Use of Additional Knowledge

It is acceptable to add small amounts of extra subject explanation when it improves understanding, as long as:

- it stays age-appropriate
- it stays accurate
- it does not drift away from the topic

## Quiz Rules

### Basic Structure

Generate a companion JSON quiz file for each workshop.

Each question must include:

- `id`
- `question`
- `options`
- `answer`
- `explanation`

### Answer Convention

Store the correct answer first in JSON and use `answer: 0`.

Shuffle in the UI only if desired, and do it deterministically when a shuffle system exists.

### Difficulty

Quizzes should test:

- concept understanding
- pattern recognition
- simple application
- diagram interpretation where useful
- worked-example understanding where useful
- recall and revision where useful

### Child-Friendly Quiz Design

Keep questions:

- short
- readable
- not trick-heavy
- confidence-building

## File Naming Rules

Use the current PDF stem as the folder slug and output base.

Examples:

- `jesc102.pdf` -> `output/jesc102/jesc102_workshop.html`
- `jesc102.pdf` -> `output/jesc102/jesc102_quiz.json`

## Python File Placement Rules

All Python files created for this workflow must live under `py/`.

Examples of acceptable script names:

- `py/extract_pdf.py`
- `py/generate_workshop.py`
- `py/generate_requirement1_workshops.py`
- batch- or group-specific helper scripts under `py/`

## Parallel Work Guidance

If the user explicitly allows sub-agents or parallel execution:

- split PDFs into non-overlapping groups
- give each worker clear ownership of specific output folders
- avoid shared-write conflicts
- keep shared generator edits to a minimum
- close workers after completion

Good split example:

- Worker A owns `output/jesc106/**`, `output/jesc107/**`, `output/jesc108/**`
- Worker B owns `output/jesc109/**`, `output/jesc110/**`, `output/jesc111/**`
- Worker C owns `output/jesc112/**`, `output/jesc113/**`, `output/jesc1an/**`

## Quality Bar

A finished batch should satisfy all of the following:

- every source PDF has its own output folder
- extraction completed successfully
- page previews were rendered
- HTML workshop exists
- quiz JSON exists
- workshop is readable on mobile
- localStorage is present
- navigation exists
- images are included
- text is simplified for the intended learner

## Minimal Dependency Install

`requirements.txt` can stay minimal:

```txt
PyMuPDF>=1.24,<1.27
```

If a newer working PyMuPDF version is already installed globally and works in the environment, that is acceptable in practice, but the skill should still keep the declared dependency simple and focused.

## Recommended Implementation Pattern

1. Write a plan markdown file.
2. Run the PDF extractor for each target PDF.
3. Inspect extracted page 1 and a few later pages to identify the topic structure.
4. Prefer page preview images for slide visuals.
5. Generate child-friendly HTML workshop and quiz JSON.
6. Verify existence and structure of all outputs.
7. If using sub-agents, validate all worker outputs at the end in one sweep.

## What Not to Do

- Do not store outputs outside the workspace.
- Do not merge multiple PDFs into one output folder.
- Do not depend on another markdown file for the operating rules.
- Do not rely on external web services for rendering the workshop.
- Do not force textbook wording when it is hard for children to read.
- Do not use raw embedded image scraps if page preview images are clearer.
- Do not omit localStorage persistence.
- Do not omit images from the slides.

## Final Deliverable Standard

For each PDF, the final result should feel like:

- a simplified digital mini-book for that subject
- a mobile workshop
- a revision tool
- a self-check quiz experience

The learner should be able to open one HTML file locally, read in small chunks, see visuals, answer questions, and come back later without losing progress.
