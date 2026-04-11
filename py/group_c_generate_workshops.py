from __future__ import annotations

import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def ppath(page: int) -> str:
    return f"page_previews/page_{page:04d}.png"


def mk_preview(slug: str, pages: list[int]) -> str:
    return "".join(
        f'<figure class="preview"><img src="{ppath(page)}" alt="Page {page} preview"><figcaption>Page {page}</figcaption></figure>'
        for page in pages
    )


def build_html(workshop: dict) -> str:
    slides_html = []
    for idx, slide in enumerate(workshop["slides"]):
        bullets = "".join(f"<li>{escape(b)}</li>" for b in slide["bullets"])
        slides_html.append(
            f"""
            <section class="panel" data-slide="{idx}">
              <div class="eyebrow">{escape(slide["eyebrow"])}</div>
              <h2>{escape(slide["title"])}</h2>
              <p class="lede">{escape(slide["summary"])}</p>
              <div class="grid">
                <div class="card">
                  <h3>Key ideas</h3>
                  <ul>{bullets}</ul>
                  <div class="callout">{escape(slide["callout"])}</div>
                </div>
                <div class="card">
                  <h3>Page previews</h3>
                  <div class="previews">{mk_preview(workshop["slug"], slide["pages"])}</div>
                </div>
              </div>
            </section>
            """
        )

    quiz_modules_html = []
    for module in workshop["quiz"]["modules"]:
        questions_html = []
        for q in module["questions"]:
            options_html = "".join(
                f'<button class="opt" data-qid="{q["id"]}" data-choice="{i}"><span>{chr(65+i)}</span><em>{escape(opt)}</em></button>'
                for i, opt in enumerate(q["options"])
            )
            questions_html.append(
                f"""
                <div class="qcard" data-qid="{q["id"]}">
                  <div class="qtitle">{escape(q["question"])}</div>
                  <div class="opts">{options_html}</div>
                  <div class="feedback"></div>
                </div>
                """
            )
        quiz_modules_html.append(
            f"""
            <div class="qmodule">
              <h3>{escape(module["name"])}</h3>
              <p class="muted">{escape(module["focus"])}</p>
              {''.join(questions_html)}
            </div>
            """
        )

    toc_items = "".join(
        f'<button class="toc-item" data-jump="{i}">{i+1}. {escape(slide["title"])}</button>'
        for i, slide in enumerate(workshop["slides"] + [{"title": "Quiz"}])
    )

    total_questions = sum(len(m["questions"]) for m in workshop["quiz"]["modules"])
    data_json = json.dumps(workshop, indent=2)
    theme = workshop["theme"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(workshop["title"])}</title>
  <style>
    :root {{
      --bg:{theme["bg"]}; --surface:{theme["surface"]}; --text:{theme["text"]}; --muted:{theme["muted"]};
      --border:{theme["border"]}; --primary:{theme["primary"]}; --accent:{theme["accent"]}; --good:#15803d; --bad:#b91c1c;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Segoe UI, system-ui, sans-serif; color:var(--text);
      background:linear-gradient(180deg, var(--bg), color-mix(in srgb, var(--bg) 80%, white)); }}
    #bar {{ position:fixed; top:0; left:0; height:4px; width:0; background:linear-gradient(90deg,var(--primary),var(--accent)); z-index:50; }}
    #shell {{ max-width:1100px; margin:0 auto; padding:16px 14px 36px; }}
    #top {{ position:sticky; top:8px; z-index:30; display:flex; justify-content:space-between; gap:10px; align-items:center;
      padding:12px 14px; background:rgba(255,255,255,.9); border:1px solid var(--border); border-radius:18px; backdrop-filter:blur(10px); }}
    .brand strong {{ display:block; font-size:1.02rem; }}
    .brand span {{ color:var(--muted); font-size:.92rem; }}
    .actions {{ display:flex; gap:8px; flex-wrap:wrap; }}
    button {{ font:inherit; }}
    .btn {{ border:1px solid var(--border); background:#fff; padding:10px 14px; border-radius:12px; cursor:pointer; }}
    .btn.primary {{ background:linear-gradient(135deg,var(--primary),var(--accent)); color:#fff; border-color:transparent; }}
    #slide {{ margin-top:16px; background:rgba(255,255,255,.92); border:1px solid var(--border); border-radius:22px; overflow:hidden; box-shadow:0 16px 32px rgba(15,23,42,.12); }}
    .panel {{ display:none; padding:22px; }}
    .panel.active {{ display:block; }}
    .eyebrow {{ text-transform:uppercase; letter-spacing:.14em; color:var(--primary); font-size:.78rem; font-weight:800; margin-bottom:10px; }}
    h1,h2,h3 {{ margin:0 0 10px; line-height:1.15; }}
    h2 {{ font-size:clamp(1.7rem, 4vw, 2.8rem); }}
    .lede, p, li {{ line-height:1.65; font-size:1.02rem; }}
    .lede {{ color:var(--muted); max-width:70ch; }}
    .grid {{ display:grid; grid-template-columns:repeat(12, 1fr); gap:14px; margin-top:16px; }}
    .card {{ grid-column:span 6; padding:16px; border:1px solid var(--border); border-radius:18px; background:#fff; }}
    .callout {{ margin-top:12px; padding:12px 14px; border-radius:14px; background:color-mix(in srgb, var(--primary) 10%, white); border-left:4px solid var(--primary); }}
    .previews {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(140px,1fr)); gap:10px; }}
    .preview {{ margin:0; padding:10px; border:1px solid var(--border); border-radius:16px; background:#fff; }}
    .preview img {{ width:100%; display:block; border-radius:12px; }}
    .preview figcaption {{ color:var(--muted); font-size:.9rem; margin-top:6px; }}
    #toc {{ position:fixed; left:-350px; top:0; bottom:0; width:min(330px, 92vw); background:rgba(255,255,255,.96); border-right:1px solid var(--border);
      box-shadow:18px 0 32px rgba(15,23,42,.14); z-index:40; padding:16px; overflow:auto; transition:left .2s ease; }}
    #toc.open {{ left:0; }}
    .toc-item {{ width:100%; text-align:left; display:block; margin:0 0 8px; border:1px solid var(--border); background:#fff; padding:10px 12px; border-radius:12px; cursor:pointer; }}
    .toc-item.active {{ border-color:var(--primary); background:color-mix(in srgb, var(--primary) 10%, white); font-weight:700; }}
    .footer {{ display:flex; justify-content:space-between; gap:10px; margin-top:14px; flex-wrap:wrap; }}
    .qmodule {{ margin-top:14px; }}
    .qcard {{ margin-top:12px; border:1px solid var(--border); border-radius:18px; padding:14px; background:#fff; }}
    .qtitle {{ font-weight:700; margin-bottom:10px; }}
    .opts {{ display:grid; gap:10px; }}
    .opt {{ width:100%; display:flex; gap:10px; text-align:left; border:1px solid var(--border); border-radius:14px; background:#fff; padding:11px 12px; cursor:pointer; }}
    .opt span {{ width:26px; height:26px; border-radius:999px; display:inline-flex; align-items:center; justify-content:center; background:color-mix(in srgb, var(--primary) 12%, white); color:var(--primary); font-weight:800; flex:none; }}
    .opt.correct {{ border-color:#16a34a; background:#f0fdf4; }}
    .opt.wrong {{ border-color:#dc2626; background:#fef2f2; }}
    .opt.locked {{ pointer-events:none; opacity:.88; }}
    .feedback {{ display:none; margin-top:10px; padding:12px 14px; border-radius:14px; }}
    .feedback.show {{ display:block; }}
    .feedback.good {{ background:#f0fdf4; color:#166534; border:1px solid #86efac; }}
    .feedback.bad {{ background:#fef2f2; color:#991b1b; border:1px solid #fecaca; }}
    .summary {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(160px,1fr)); gap:12px; margin:16px 0; }}
    .stat {{ padding:14px; border:1px solid var(--border); border-radius:18px; background:#fff; }}
    .muted {{ color:var(--muted); }}
    @media (max-width:820px) {{ .card {{ grid-column:span 12; }} #top {{ flex-direction:column; align-items:flex-start; }} }}
  </style>
</head>
<body>
  <div id="bar"></div>
  <aside id="toc">
    <button class="btn" data-close>Close</button>
    <h3>{escape(workshop["title"])}</h3>
    <p class="muted">{escape(workshop["subtitle"])}</p>
    {toc_items}
  </aside>
  <div id="shell">
    <header id="top">
      <div class="brand"><strong>{escape(workshop["title"])}</strong><span>{escape(workshop["subtitle"])}</span></div>
      <div class="actions">
        <button class="btn" data-open>Menu</button>
        <button class="btn" data-home>Start</button>
        <button class="btn primary" data-end>Quiz</button>
        <span class="btn" id="counter">Slide 1 / {len(workshop["slides"]) + 1}</span>
      </div>
    </header>
    <main id="slide">
      {''.join(slides_html)}
      <section class="panel" data-slide="{len(workshop["slides"])}">
        <div class="eyebrow">Quiz time</div>
        <h2>Quick self-check</h2>
        <p class="lede">These questions are saved in this browser. Pick an answer, see the feedback, and use Try again to reset everything.</p>
        <div class="summary">
          <div class="stat"><div class="muted">Answered</div><strong id="answered">0</strong></div>
          <div class="stat"><div class="muted">Correct</div><strong id="correct">0</strong></div>
          <div class="stat"><div class="muted">Total</div><strong>{total_questions}</strong></div>
        </div>
        <button class="btn" id="retry">Try again</button>
        {''.join(quiz_modules_html)}
      </section>
      <div class="footer"><button class="btn" data-prev>Previous</button><button class="btn primary" data-next>Next</button></div>
    </main>
  </div>
  <script>
    const DATA = {data_json};
    const KEY = 'workshop:{workshop["slug"]}';
    const state = {{
      slide: Number(localStorage.getItem(KEY + ':slide') || 0),
      answers: JSON.parse(localStorage.getItem(KEY + ':answers') || '{{}}')
    }};
    const panels = [...document.querySelectorAll('.panel')];
    const bar = document.getElementById('bar');
    const toc = document.getElementById('toc');
    const counter = document.getElementById('counter');
    const answered = document.getElementById('answered');
    const correct = document.getElementById('correct');
    const total = DATA.quiz.totalQuestions || 1;
    function save() {{
      localStorage.setItem(KEY + ':slide', String(state.slide));
      localStorage.setItem(KEY + ':answers', JSON.stringify(state.answers));
    }}
    function show(n) {{
      state.slide = Math.max(0, Math.min(n, panels.length - 1));
      panels.forEach((p, i) => p.classList.toggle('active', i === state.slide));
      bar.style.width = ((state.slide + 1) / panels.length * 100) + '%';
      counter.textContent = `Slide ${{state.slide + 1}} / ${{panels.length}}`;
      document.querySelectorAll('.toc-item').forEach((b, i) => b.classList.toggle('active', i === state.slide));
      save();
    }}
    function score() {{
      let a = 0, c = 0;
      for (const m of DATA.quiz.modules) for (const q of m.questions) {{
        if (state.answers[q.id] !== undefined) {{
          a += 1;
          if (state.answers[q.id] === q.answer) c += 1;
        }}
      }}
      answered.textContent = a;
      correct.textContent = c;
    }}
    function lock(card, q, chosen) {{
      const fb = card.querySelector('.feedback');
      card.querySelectorAll('.opt').forEach(btn => {{
        btn.classList.add('locked');
        const c = Number(btn.dataset.choice);
        if (c === q.answer) btn.classList.add('correct');
        if (c === chosen && chosen !== q.answer) btn.classList.add('wrong');
      }});
      fb.classList.add('show');
      fb.classList.add(chosen === q.answer ? 'good' : 'bad');
      fb.innerHTML = '<strong>' + (chosen === q.answer ? 'Correct. ' : 'Not quite. ') + '</strong>' + q.explanation;
    }}
    document.querySelectorAll('.opt').forEach(btn => {{
      btn.addEventListener('click', () => {{
        const qid = btn.dataset.qid;
        const chosen = Number(btn.dataset.choice);
        const q = DATA.quiz.modules.flatMap(m => m.questions).find(item => item.id === qid);
        const card = btn.closest('.qcard');
        state.answers[qid] = chosen;
        save();
        lock(card, q, chosen);
        score();
      }});
    }});
    document.getElementById('retry').addEventListener('click', () => {{
      state.answers = {{}};
      localStorage.removeItem(KEY + ':answers');
      document.querySelectorAll('.qcard').forEach(card => {{
        card.querySelectorAll('.opt').forEach(btn => btn.classList.remove('correct', 'wrong', 'locked'));
        const fb = card.querySelector('.feedback');
        fb.className = 'feedback';
        fb.textContent = '';
      }});
      score();
      show(DATA.slides.length);
    }});
    document.querySelectorAll('[data-open]').forEach(btn => btn.addEventListener('click', () => toc.classList.add('open')));
    document.querySelectorAll('[data-close]').forEach(btn => btn.addEventListener('click', () => toc.classList.remove('open')));
    document.querySelectorAll('[data-home]').forEach(btn => btn.addEventListener('click', () => show(0)));
    document.querySelectorAll('[data-end]').forEach(btn => btn.addEventListener('click', () => show(panels.length - 1)));
    document.querySelectorAll('[data-prev]').forEach(btn => btn.addEventListener('click', () => show(state.slide - 1)));
    document.querySelectorAll('[data-next]').forEach(btn => btn.addEventListener('click', () => show(state.slide + 1)));
    document.querySelectorAll('[data-jump]').forEach(btn => btn.addEventListener('click', () => {{
      show(Number(btn.dataset.jump));
      toc.classList.remove('open');
    }}));
    window.addEventListener('keydown', e => {{
      if (e.key === 'Escape') toc.classList.remove('open');
      if (e.key === 'ArrowLeft') show(state.slide - 1);
      if (e.key === 'ArrowRight') show(state.slide + 1);
      if (e.key.toLowerCase() === 'm') toc.classList.toggle('open');
    }});
    DATA.quiz.modules.forEach(m => m.questions.forEach(q => {{
      if (state.answers[q.id] !== undefined) {{
        const card = document.querySelector(`.qcard[data-qid="${{q.id}}"]`);
        if (card) lock(card, q, state.answers[q.id]);
      }}
    }}));
    score();
    show(state.slide);
  </script>
</body>
</html>"""


def write_workshop(workshop: dict) -> None:
    out = ROOT / "output" / workshop["slug"]
    out.mkdir(parents=True, exist_ok=True)
    (out / f'{workshop["slug"]}_workshop.html').write_text(build_html(workshop), encoding="utf-8")
    quiz_payload = {
        "title": workshop["title"] + " - Kid-friendly workshop quiz",
        "version": "1.0",
        "totalQuestions": sum(len(m["questions"]) for m in workshop["quiz"]["modules"]),
        "modules": workshop["quiz"]["modules"],
    }
    (out / f'{workshop["slug"]}_quiz.json').write_text(json.dumps(quiz_payload, indent=2), encoding="utf-8")


WORKSHOPS = [
    {
        "slug": "jesc112",
        "title": "Magnetic Effects of Electric Current",
        "subtitle": "Kid-friendly workshop on current, magnetism, field lines, and circuit safety.",
        "theme": {"bg": "#f5f9ff", "surface": "#ffffff", "text": "#10213a", "muted": "#5c6f8a", "border": "#d7e4f5", "primary": "#2563eb", "accent": "#14b8a6"},
        "slides": [
            {"eyebrow": "Start here", "title": "Electricity can act like a magnet", "summary": "The chapter begins with a simple clue: current in a wire can move a compass needle.", "bullets": ["A current-carrying wire makes a magnetic effect.", "Oersted's experiment linked electricity and magnetism.", "A compass is the small magnet that reveals the change."], "callout": "Move through the slides first, then use the quiz to check what stuck.", "pages": [1, 2]},
            {"eyebrow": "Module 1", "title": "Current makes magnetism", "summary": "The first idea is easy to test: when current flows, the wire behaves like a magnet for nearby objects.", "bullets": ["The needle swing is evidence of a magnetic field.", "The effect happens around the wire, not inside the compass.", "Electricity and magnetism are connected ideas."], "callout": "If the compass moves, the wire is doing more than just carrying charge.", "pages": [1, 2, 3]},
            {"eyebrow": "Module 2", "title": "Reading magnetic field lines", "summary": "Field lines are drawings that show direction and strength around a magnet.", "bullets": ["Outside the magnet, lines go from north to south.", "Closer lines mean a stronger field.", "Field lines do not cross each other."], "callout": "Think of the lines as a map of magnetic push and pull.", "pages": [3, 4, 5]},
            {"eyebrow": "Module 3", "title": "Wires, coils, and electromagnets", "summary": "Different wire shapes make different field patterns, and a coil with soft iron becomes an electromagnet.", "bullets": ["A straight wire makes circles around it.", "A solenoid acts like a bar magnet.", "Soft iron helps make a stronger electromagnet."], "callout": "A coil plus iron core is the chapter's useful magnet trick.", "pages": [6, 7, 8, 9]},
            {"eyebrow": "Module 4", "title": "Circuit safety", "summary": "The last part of the chapter is about staying safe at home with fuses, earth wires, and careful use of power.", "bullets": ["A fuse protects against extra current.", "An earth wire helps stop shocks.", "Too many appliances can overload one circuit."], "callout": "Good wiring is about safety, not just about making things work.", "pages": [10, 11, 12, 13]},
        ],
        "quiz": {
            "modules": [
                {"name": "Current and magnetism", "focus": "A wire with current can behave like a magnet.", "questions": [
                    {"id": "j112_1", "question": "What happens when current flows through a wire?", "options": ["It creates a magnetic effect", "It becomes glass", "It stops all movement", "It loses all heat"], "answer": 0, "explanation": "A current-carrying wire creates a magnetic field around it."},
                    {"id": "j112_2", "question": "Which scientist showed the compass deflection near a wire?", "options": ["Oersted", "Newton", "Curie", "Galileo"], "answer": 0, "explanation": "Oersted connected electricity and magnetism in the experiment."},
                ]},
                {"name": "Magnetic field lines", "focus": "Lines help us picture direction and strength.", "questions": [
                    {"id": "j112_3", "question": "Outside a bar magnet, field lines go from", "options": ["north to south", "south to north", "top to bottom", "middle to edge"], "answer": 0, "explanation": "That is the direction used outside the magnet."},
                    {"id": "j112_4", "question": "When field lines are crowded together, the field is", "options": ["stronger", "weaker", "gone", "backwards"], "answer": 0, "explanation": "Crowded lines mean a stronger magnetic field."},
                ]},
                {"name": "Wires and coils", "focus": "Wire shape changes the magnetic pattern.", "questions": [
                    {"id": "j112_5", "question": "The field lines around a straight current-carrying wire are", "options": ["concentric circles", "straight stripes", "triangles", "random dots"], "answer": 0, "explanation": "A straight wire gives circular field lines."},
                    {"id": "j112_6", "question": "An electromagnet is made from a coil around", "options": ["soft iron", "rubber", "wood", "plastic"], "answer": 0, "explanation": "Soft iron helps the coil become a strong magnet."},
                ]},
                {"name": "Safety", "focus": "Protection against shocks, overloads, and short circuits.", "questions": [
                    {"id": "j112_7", "question": "Which part protects a circuit from too much current?", "options": ["A fuse", "A spoon", "A book", "A fan blade"], "answer": 0, "explanation": "A fuse breaks the circuit when current gets too high."},
                    {"id": "j112_8", "question": "What does the earth wire do?", "options": ["Carries leaking current safely to the ground", "Makes bulbs blue", "Stores food energy", "Changes wire colour"], "answer": 0, "explanation": "Earthing is a safety path for leakage current."},
                ]},
            ]
        },
    },
    {
        "slug": "jesc113",
        "title": "Our Environment",
        "subtitle": "Kid-friendly workshop on ecosystems, food chains, energy flow, and caring for nature.",
        "theme": {"bg": "#f4fbf6", "surface": "#ffffff", "text": "#11301d", "muted": "#587064", "border": "#d1e9d9", "primary": "#15803d", "accent": "#f59e0b"},
        "slides": [
            {"eyebrow": "Start here", "title": "Nature works as a connected system", "summary": "Living things and non-living parts work together in every ecosystem.", "bullets": ["Biotic means living.", "Abiotic means non-living.", "A garden, pond, forest, or aquarium can all be ecosystems."], "callout": "Look for the living parts and the non-living parts together.", "pages": [1, 2]},
            {"eyebrow": "Module 1", "title": "Ecosystems are living neighborhoods", "summary": "An ecosystem is a place where organisms and surroundings affect each other.", "bullets": ["An aquarium is a human-made ecosystem.", "Producers, consumers, and decomposers all matter.", "Food and shelter link the organisms together."], "callout": "The ecosystem works because many parts depend on one another.", "pages": [1, 2, 3]},
            {"eyebrow": "Module 2", "title": "Food chains and food webs", "summary": "Energy moves through feeding links. A food web is a connected set of many food chains.", "bullets": ["A food chain shows who eats whom.", "A food web is more realistic than one straight line.", "Trophic levels name each step in the chain."], "callout": "Nature usually looks more like a web than a straight line.", "pages": [3, 4, 5]},
            {"eyebrow": "Module 3", "title": "Energy flow", "summary": "Sunlight enters through plants, and only part of the energy moves on at each step.", "bullets": ["Plants capture only a small part of sunlight.", "About 10% of food energy moves to the next level.", "The lowest trophic level usually has the most organisms."], "callout": "Energy moves forward only. It does not circle back.", "pages": [5, 6, 7]},
            {"eyebrow": "Module 4", "title": "Waste, ozone, and better habits", "summary": "The chapter ends with practical care: reduce waste, protect the ozone layer, and choose cleaner habits.", "bullets": ["Biodegradable waste breaks down naturally.", "Non-biodegradable waste can build up and cause trouble.", "Cloth bags and turning off unused lights are helpful habits."], "callout": "Small actions matter when they are repeated every day.", "pages": [8, 9, 10]},
        ],
        "quiz": {
            "modules": [
                {"name": "Ecosystems", "focus": "Living and non-living parts interact in one place.", "questions": [
                    {"id": "j113_1", "question": "What is an ecosystem made of?", "options": ["Living things and non-living surroundings", "Only animals", "Only rocks", "Only one plant"], "answer": 0, "explanation": "Ecosystems include biotic and abiotic parts."},
                    {"id": "j113_2", "question": "An aquarium is a", "options": ["human-made ecosystem", "desert", "mountain", "machine"], "answer": 0, "explanation": "People set it up, so it is human-made."},
                ]},
                {"name": "Food chains and webs", "focus": "Food moves through linked eating relationships.", "questions": [
                    {"id": "j113_3", "question": "Which sequence is a food chain?", "options": ["Grass -> goat -> human", "Stone -> cloud -> chair", "Pen -> bag -> book", "Sun -> rain -> soil"], "answer": 0, "explanation": "It shows who eats whom."},
                    {"id": "j113_4", "question": "What does a food web show?", "options": ["Many connected food chains", "Only one animal", "A map of roads", "A weather chart"], "answer": 0, "explanation": "Food webs connect lots of chains together."},
                ]},
                {"name": "Energy flow", "focus": "Energy enters from the Sun and moves step by step.", "questions": [
                    {"id": "j113_5", "question": "About how much sunlight energy do plants capture?", "options": ["About 1%", "About 50%", "About 100%", "About 0%"], "answer": 0, "explanation": "The chapter says plants capture only a small part of sunlight."},
                    {"id": "j113_6", "question": "About how much food energy goes to the next level?", "options": ["About 10%", "About 90%", "About 50%", "Exactly 100%"], "answer": 0, "explanation": "The 10% rule is the chapter's easy memory trick."},
                ]},
                {"name": "Clean habits", "focus": "Waste, ozone, and better choices for nature.", "questions": [
                    {"id": "j113_7", "question": "Which item is biodegradable?", "options": ["Fruit peels", "Plastic bag", "Glass bottle", "Metal spoon"], "answer": 0, "explanation": "Fruit peels break down naturally."},
                    {"id": "j113_8", "question": "Why is the ozone layer important?", "options": ["It blocks harmful UV radiation", "It makes food sweeter", "It creates wind", "It stores water"], "answer": 0, "explanation": "The ozone layer protects living things from ultraviolet rays."},
                ]},
            ]
        },
    },
    {
        "slug": "jesc1an",
        "title": "Answer Key Revision Workshop",
        "subtitle": "A kid-friendly answer-check guide for self-marking and smart revision.",
        "theme": {"bg": "#fff8f1", "surface": "#ffffff", "text": "#3a2412", "muted": "#7b6149", "border": "#f1d5b7", "primary": "#c2410c", "accent": "#f97316"},
        "slides": [
            {"eyebrow": "Start here", "title": "This is a self-check helper, not a lesson chapter", "summary": "The source PDF is an answer resource, so this workshop turns it into a friendly revision tool.", "bullets": ["Use it after trying the questions yourself.", "Learn how chapter numbers, option letters, and short answers are shown.", "Turn mistakes into clues for what to revise next."], "callout": "Best habit: try first, check second, retry third.", "pages": [1, 2, 3]},
            {"eyebrow": "Module 1", "title": "Meet the answer key", "summary": "The answer pages are chapter-wise and compact. That makes them good for self-marking, not for copying.", "bullets": ["Chapter numbers help you find the right section quickly.", "Letters like a, b, c, and d show multiple-choice answers.", "Some answers are short phrases instead of letters."], "callout": "An answer key is a coach, not a shortcut.", "pages": [1]},
            {"eyebrow": "Module 2", "title": "How to read the answer patterns", "summary": "This resource shows several answer styles, so you can learn what kind of question each one belongs to.", "bullets": ["More than one letter can mean more than one correct option.", "True/False entries come from statement questions.", "Short answers show the key idea you should remember."], "callout": "Look for the pattern, then ask what the question might have been.", "pages": [2]},
            {"eyebrow": "Module 3", "title": "Check, fix, and retry", "summary": "The best revision happens after a mistake: compare, spot the gap, and try again.", "bullets": ["Mark your own attempt before opening the key.", "Circle the questions you missed.", "Retry after one more quick review."], "callout": "The goal is remembering it later, not just once.", "pages": [2, 3]},
            {"eyebrow": "Module 4", "title": "Fast revision habits", "summary": "A calm routine keeps revision honest and useful.", "bullets": ["Work chapter by chapter.", "Use the key to see what you know well.", "Keep a short list of ideas to revisit."], "callout": "Small, steady, honest revision works best.", "pages": [1, 2, 3]},
        ],
        "quiz": {
            "modules": [
                {"name": "Using the key", "focus": "This resource is for checking, not skipping practice.", "questions": [
                    {"id": "j1an_1", "question": "What is this PDF mostly for?", "options": ["Checking your own answers", "Watching cartoons", "Drawing maps", "Counting pencils"], "answer": 0, "explanation": "It is an answer resource for self-checking."},
                    {"id": "j1an_2", "question": "When should you use the answer key?", "options": ["After you try the work", "Before reading the question", "Instead of studying", "Only when bored"], "answer": 0, "explanation": "Trying first makes the check useful."},
                ]},
                {"name": "Reading patterns", "focus": "Different answer shapes tell you what kind of question it was.", "questions": [
                    {"id": "j1an_3", "question": "If the key shows more than one letter, that usually means", "options": ["More than one option may be correct", "The page is broken", "The chapter has no answers", "The pencil is dull"], "answer": 0, "explanation": "Multiple letters usually mean a multi-answer question."},
                    {"id": "j1an_4", "question": "If the key says True/False, the question was probably a", "options": ["statement to judge", "picture puzzle", "music task", "labelling race"], "answer": 0, "explanation": "True/False belongs to statement questions."},
                ]},
                {"name": "Fixing mistakes", "focus": "Mistakes are clues for what to revise next.", "questions": [
                    {"id": "j1an_5", "question": "What should you do after finding a wrong answer?", "options": ["Read the explanation and retry", "Hide the notebook", "Stop studying", "Ignore it"], "answer": 0, "explanation": "Retrying helps the idea stick."},
                    {"id": "j1an_6", "question": "Why is retrying helpful?", "options": ["It helps you remember later", "It changes the answer key", "It makes pages vanish", "It removes homework"], "answer": 0, "explanation": "A second attempt builds stronger memory."},
                ]},
                {"name": "Revision habits", "focus": "Use the key to learn, not to copy.", "questions": [
                    {"id": "j1an_7", "question": "What is the main job of a revision resource?", "options": ["Help you check and remember", "Decorate the desk", "Replace all practice", "Hide the syllabus"], "answer": 0, "explanation": "A revision resource supports honest study."},
                    {"id": "j1an_8", "question": "What is the best study habit here?", "options": ["Try first, check second, retry third", "Open answers first", "Skip revision", "Read once and stop"], "answer": 0, "explanation": "That routine keeps practice real."},
                ]},
            ]
        },
    },
]


def main() -> None:
    for workshop in WORKSHOPS:
        write_workshop(workshop)


if __name__ == "__main__":
    main()
