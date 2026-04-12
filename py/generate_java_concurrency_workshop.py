from __future__ import annotations

import json
from pathlib import Path
import re

import generate_workshop as base

from effective_java_common import attach_question_ids, module, q, slide


TOPIC_SLUG = "JavaConcurrency"
WORKSHOP_TITLE = "Java Concurrency in Practice Workshop"
WORKSHOP_SUBTITLE = "Chapter-based workshop with 10 content slides per chapter"
BOOK_ROOT = Path("output") / TOPIC_SLUG


CHAPTER_GUIDES: dict[int, dict[str, object]] = {
    1: {
        "why": "The introduction explains why concurrency keeps showing up in real Java systems even though it makes correctness harder.",
        "through_line": "Treat threads as a design tool for overlap, responsiveness, and scaling, not as free performance magic.",
        "extra_focuses": ["Safety vs liveness trade-off", "Where concurrency shows up in real systems"],
        "pitfalls": ["Adding threads before identifying a bottleneck", "Ignoring liveness and performance risks", "Treating concurrency as an implementation detail instead of a design choice", "Assuming more threads automatically mean more speed"],
        "checklist": ["Name the problem concurrency is solving", "Separate benefits from hazards", "Notice where asynchronous work becomes simpler or riskier", "Use the later chapters as a map for the failure modes introduced here"],
        "principle": "Concurrency is justified only when the system gains a clear responsiveness, throughput, or modeling benefit.",
    },
    2: {
        "why": "This chapter defines thread safety as a behavior guarantee and anchors the rest of the book.",
        "through_line": "Shared mutable state is the real problem; locking and atomic operations are only mechanisms for controlling it.",
        "extra_focuses": ["Choosing a synchronization boundary"],
        "pitfalls": ["Exposing shared mutable state casually", "Leaving compound actions unprotected", "Using a lock without knowing which state it guards", "Treating thread safety as a keyword instead of a contract"],
        "checklist": ["List the mutable state", "Identify who may touch it concurrently", "Protect compound actions as one unit", "Prefer simpler designs such as statelessness when possible"],
        "principle": "The first concurrency question is always: what state is shared, and what invariant must survive concurrent access?",
    },
    3: {
        "why": "Chapter 3 adds visibility and publication, which are often the least intuitive concurrency rules for developers.",
        "through_line": "A program can fail even when no race is obvious if writes are not made visible to other threads safely.",
        "extra_focuses": ["Stale reads and reordering"],
        "pitfalls": ["Publishing objects before construction is complete", "Using volatile where a richer invariant needs locking", "Letting this escape during construction", "Assuming writes are seen immediately without synchronization"],
        "checklist": ["Prefer confinement when possible", "Use immutability aggressively", "Publish shared objects safely", "Treat visibility rules as first-class correctness rules"],
        "principle": "Correct concurrent code needs both atomicity and visibility; missing either one breaks the contract.",
    },
    4: {
        "why": "This chapter shows why composing thread-safe pieces is still a design problem, not an automatic outcome.",
        "through_line": "Thread-safe components only stay safe when the larger object preserves the right invariants and synchronization policy.",
        "extra_focuses": ["Lock ownership and policy documentation"],
        "pitfalls": ["Assuming thread-safe fields imply a thread-safe class", "Extending behavior without preserving invariants", "Mixing ownership rules across multiple components", "Leaving synchronization policy undocumented"],
        "checklist": ["Name the invariants that span fields", "Decide whether safety is delegated or owned locally", "Keep confinement boundaries explicit", "Document the lock and the state it guards"],
        "principle": "Composition works only when the synchronization policy is as carefully designed as the data model.",
    },
    5: {
        "why": "Chapter 5 is where the book starts leaning on platform building blocks instead of hand-rolled coordination.",
        "through_line": "Higher-level concurrent collections and synchronizers reduce bug surface by packaging coordination rules explicitly.",
        "extra_focuses": [],
        "pitfalls": ["Relying on synchronized wrappers for compound workflows", "Rebuilding producer-consumer coordination from scratch", "Ignoring blocking behavior and interruption", "Using caches or collections without thinking about contention"],
        "checklist": ["Start with JDK building blocks", "Prefer BlockingQueue for producer-consumer work", "Use concurrent collections where shared access is hot", "Let abstractions carry synchronization policy when they fit the problem"],
        "principle": "If the platform already has a concurrency abstraction that matches your problem, use it before inventing one.",
    },
    6: {
        "why": "Task-based design is one of the book's biggest architectural shifts away from raw thread management.",
        "through_line": "Define independent units of work first and then decide how an execution policy should run them.",
        "extra_focuses": ["Task boundaries", "Queueing and handoff", "Executor-driven design"],
        "pitfalls": ["Embedding execution policy inside business logic", "Choosing tasks that are too large or too dependent", "Creating raw threads where executor policy is needed", "Ignoring how exceptions and cancellation interact with task boundaries"],
        "checklist": ["Define sensible task boundaries", "Separate task logic from execution policy", "Use executors for lifecycle control", "Look for parallelism only after independence is clear"],
        "principle": "Good concurrent architecture starts with task design, not with thread creation.",
    },
    7: {
        "why": "Reliable cancellation and shutdown are what separate code that merely runs from services that can be operated safely.",
        "through_line": "Stopping concurrent work is cooperative and must be part of the design from the beginning.",
        "extra_focuses": ["Interruption discipline", "Service lifecycle boundaries"],
        "pitfalls": ["Trying to stop work forcibly", "Swallowing interrupts", "Leaving blocked producers or consumers stranded", "Failing to define startup and shutdown ownership"],
        "checklist": ["Use interruption deliberately", "Design services with explicit lifecycle methods", "Restore or propagate interrupt status correctly", "Test how cancellation behaves under partial progress"],
        "principle": "Shutdown behavior is part of the service contract, not cleanup code you can bolt on later.",
    },
    8: {
        "why": "Thread pools help only when their policy matches the workload and task dependencies.",
        "through_line": "Pool sizing, queue choice, and task coupling directly affect both throughput and liveness.",
        "extra_focuses": ["Rejected work and back-pressure", "Monitoring and tuning pools"],
        "pitfalls": ["Copying pool sizes from other systems", "Letting dependent tasks share a constrained pool carelessly", "Ignoring queue growth and rejection behavior", "Treating pools as a performance checkbox instead of a resource policy"],
        "checklist": ["Size pools from workload data", "Watch for blocked or dependent tasks", "Choose queues and rejection policies intentionally", "Use executor extension points for visibility and control"],
        "principle": "A thread pool is a resource-management policy; the right size depends on what the tasks actually do.",
    },
    9: {
        "why": "The GUI chapter is really a lesson in protecting responsiveness in any single-threaded subsystem.",
        "through_line": "Some threads own latency-sensitive work and must stay short, predictable, and isolated from long-running operations.",
        "extra_focuses": ["Foreground vs background work", "Safe model updates"],
        "pitfalls": ["Running long work on the event thread", "Blocking the owner thread while waiting for background work", "Updating shared models carelessly", "Forgetting that responsiveness is a correctness concern for users"],
        "checklist": ["Keep owner-thread tasks short", "Push heavy work to background execution", "Marshal results back carefully", "Treat responsiveness budgets as a real design constraint"],
        "principle": "Responsiveness improves when ownership of single-threaded subsystems is explicit and respected.",
    },
    10: {
        "why": "Liveness hazards are often the failures teams discover only after the system appears healthy but stops making progress.",
        "through_line": "Correct locking and bounded resources must still leave the program able to move forward.",
        "extra_focuses": ["Deadlock patterns", "Open calls and ordering rules", "Starvation and livelock"],
        "pitfalls": ["Acquiring multiple locks in inconsistent orders", "Calling unknown code while holding locks", "Starving work through unfair resource use", "Retrying eagerly without a progress strategy"],
        "checklist": ["Establish lock ordering", "Prefer open calls", "Diagnose wait cycles early", "Design retries with timeouts, randomness, or backoff when needed"],
        "principle": "A safe program that never makes progress is still broken.",
    },
    11: {
        "why": "This chapter reframes performance around contention, serialized work, and coordination cost instead of raw thread count.",
        "through_line": "Scalability comes from shrinking bottlenecks, not from assuming concurrency removes them.",
        "extra_focuses": ["Contention hotspots", "Amdahl-limited speedup"],
        "pitfalls": ["Holding locks longer than necessary", "Ignoring serialized fractions", "Adding threads without measuring contention", "Confusing local speedups with system scalability"],
        "checklist": ["Measure where work serializes", "Reduce lock hold time", "Choose data structures that lower contention", "Tune only after correctness and liveness are stable"],
        "principle": "Concurrency can overlap work, but it cannot repeal bottlenecks.",
    },
    12: {
        "why": "Testing concurrent programs requires more than ordinary unit tests because many failures are probabilistic and timing-sensitive.",
        "through_line": "Good tests make races, liveness failures, and performance regressions easier to expose and explain.",
        "extra_focuses": ["Stress and performance testing", "Observability of failure"],
        "pitfalls": ["Assuming a passing unit test proves concurrency safety", "Running tests too briefly for rare failures", "Ignoring liveness and throughput checks", "Writing code whose coordination rules are too hidden to test cleanly"],
        "checklist": ["Test safety and liveness separately", "Run stress tests long enough", "Measure performance under representative load", "Design code so concurrency rules are observable in tests"],
        "principle": "Concurrent tests succeed when they magnify nondeterministic failures instead of accidentally hiding them.",
    },
    13: {
        "why": "Explicit locks matter when intrinsic locking is correct but not expressive enough for the coordination problem.",
        "through_line": "Use ReentrantLock for capabilities such as timed, interruptible, or fairness-sensitive acquisition, not just because it looks advanced.",
        "extra_focuses": ["Timed and interruptible acquisition"],
        "pitfalls": ["Using explicit locks without a clear need", "Forgetting explicit unlock discipline", "Choosing fairness or read-write policies without workload evidence", "Replacing simple synchronized code with more complex lock code unnecessarily"],
        "checklist": ["Know why Lock is needed", "Pair every acquisition with explicit release discipline", "Use advanced features only when they solve a real problem", "Measure before claiming a lock strategy is better"],
        "principle": "Advanced locking earns its complexity only when its extra semantics solve a concrete design problem.",
    },
    14: {
        "why": "Custom synchronizers are powerful because they encode coordination around an explicit state model.",
        "through_line": "State dependence becomes safer when the waiting conditions, transitions, and release rules are all designed deliberately.",
        "extra_focuses": [],
        "pitfalls": ["Using wait or condition queues without a clear predicate", "Forgetting which lock guards which condition", "Building custom synchronizers before checking existing utilities", "Treating AQS as magic instead of a state machine framework"],
        "checklist": ["Define the condition predicate clearly", "Bind conditions to the right lock and state", "Prefer existing utilities when they fit", "Use AQS only with a clean acquisition and release model"],
        "principle": "A synchronizer is a state machine with concurrency semantics; if the state model is vague, the implementation will be fragile.",
    },
    15: {
        "why": "Atomic variables and non-blocking algorithms reduce some locking costs but narrow the kinds of invariants you can express directly.",
        "through_line": "Use atomics where state transitions are small and well-scoped; use locks when the invariant is larger.",
        "extra_focuses": ["CAS-style state updates", "Choosing lock-free only when it helps"],
        "pitfalls": ["Replacing locks with atomics without checking invariant scope", "Ignoring contention and retry cost in non-blocking algorithms", "Treating lock-free as automatically faster", "Forgetting that atomics still rely on memory-model guarantees"],
        "checklist": ["Use atomics for narrow transitions", "Keep retry loops bounded and measurable", "Compare lock-based and non-blocking behavior under real contention", "Choose the simplest primitive that preserves the invariant"],
        "principle": "Atomics are precise tools for precise state changes, not universal replacements for synchronization.",
    },
    16: {
        "why": "The memory model explains why the higher-level rules around publication, synchronization, and visibility actually work.",
        "through_line": "Ordering and visibility guarantees define what one thread is allowed to observe from another.",
        "extra_focuses": ["Visibility and ordering", "Publication and initialization", "Reordering intuition", "Practical JMM rules", "Safe publication habits"],
        "pitfalls": ["Assuming source-code order is what other threads observe", "Publishing partially constructed state", "Using low-level reasoning without a clear happens-before edge", "Treating the JMM as optional theory"],
        "checklist": ["Know what creates visibility guarantees", "Publish shared state safely", "Use synchronization edges intentionally", "Fall back to higher-level patterns when low-level reasoning gets fragile"],
        "principle": "The Java Memory Model is the ground truth for what concurrent reads and writes are allowed to mean.",
    },
}


def preview(page: int) -> str:
    return f"page_previews/page_{page:04d}.png"


def load_manifest() -> dict[str, object]:
    return json.loads((BOOK_ROOT / "chapter_manifest.json").read_text(encoding="utf-8"))


def midpoint(start_page: int, end_page: int) -> int:
    return (start_page + end_page) // 2


def chapter_progression(chapter: dict[str, object]) -> list[str]:
    items = [item["title"] for item in chapter["items"]]
    if items:
        return items
    return ["Core topic", "Key rule", "Practical interpretation"]


def choose_focuses(chapter: dict[str, object], guide: dict[str, object]) -> list[dict[str, object]]:
    focuses = [
        {
            "title": item["title"],
            "start_page": int(item["start_page"]),
            "end_page": int(item["end_page"]),
        }
        for item in chapter["items"]
    ]
    extra_focuses = list(guide["extra_focuses"])
    while len(focuses) < 6:
        offset = len(focuses) - len(chapter["items"])
        approx_page = min(int(chapter["end_page"]), int(chapter["start_page"]) + max(offset, 0))
        title = extra_focuses[offset] if offset < len(extra_focuses) else f"Chapter pattern {offset + 1}"
        focuses.append({"title": title, "start_page": approx_page, "end_page": approx_page})
    return focuses[:6]


def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)


def count_words(parts: list[str]) -> int:
    return len(re.findall(r"\b[\w'-]+\b", " ".join(strip_tags(part) for part in parts)))


def support_box(title: str, guide: dict[str, object], source_pages: tuple[int, int]) -> str:
    return (
        f"<strong>Definition:</strong> {title} is being used here as a study handle for the chapter's core rule: {guide['through_line']} "
        f"<br><strong>Pointers:</strong> Track the shared state, the coordination boundary, and the failure that appears when that boundary is weakened. "
        f"Ask whether the design is protecting correctness, visibility, progress, or throughput. "
        f"<br><strong>Notes:</strong> Read the cited source span as a worked example set rather than as isolated prose. "
        f"Pages {source_pages[0]}-{source_pages[1]} show how the book turns abstract concurrency ideas into concrete engineering decisions."
    )


def minimum_length_paragraphs(title: str, guide: dict[str, object], source_pages: tuple[int, int]) -> list[str]:
    return [
        f"This slide is intentionally longer than a quick caption because the goal is to make {title.lower()} readable even without the original page image. "
        f"When you study it, slow down and identify the state boundary, the coordination mechanism, and the cost of getting the rule wrong. "
        f"The book's argument is rarely just about one API call; it is usually about how a design choice affects safety, visibility, liveness, or scalability over time.",
        f"A practical way to use this section is to compare its rule with code you already know. "
        f"Ask whether the same pattern appears in request handling, background jobs, shared caches, GUI event handling, or shutdown logic. "
        f"If the answer is yes, the chapter is giving you a review lens, not just a one-off example. "
        f"That is why the source span {source_pages[0]}-{source_pages[1]} matters: it contains the narrative, examples, and warnings that make the design principle concrete.",
        f"Keep the chapter principle in mind while reading: {guide['principle']} "
        f"If a slide feels abstract, translate it into three questions. What state or resource is being coordinated? What guarantee is the code trying to provide? "
        f"What kind of bug or slowdown appears when that guarantee is dropped? Those three questions usually expose the real lesson quickly.",
    ]


def text_only_slide(
    title: str,
    paragraphs: list[str],
    *,
    points: list[str] | None = None,
    box_kind: str = "note",
    extra_box: str | None = None,
    guide: dict[str, object],
    source_pages: tuple[int, int],
) -> str:
    normalized_points = list(points or [])
    box_text = support_box(title, guide, source_pages)
    if extra_box:
        box_text = f"{extra_box}<br><br>{box_text}"

    all_parts = list(paragraphs) + normalized_points + [box_text]
    if count_words(all_parts) < 150:
        paragraphs = list(paragraphs) + minimum_length_paragraphs(title, guide, source_pages)

    all_parts = list(paragraphs) + normalized_points + [box_text]
    if count_words(all_parts) < 150:
        paragraphs.append(
            f"Final reminder: this slide is part of a chapter-level sequence, so do not treat the rule as isolated advice. "
            f"It links back to the chapter's through-line, which is {guide['through_line'].lower()}"
        )

    return slide(
        paragraphs,
        points=normalized_points,
        box=(box_kind, box_text),
        source_pages=source_pages,
    )


def describe_focus(chapter_title: str, focus_title: str) -> tuple[list[str], list[str]]:
    key = focus_title.lower()
    chapter_key = chapter_title.lower()

    if "history" in key:
        return (
            [
                "This section explains why systems moved from one-program execution toward concurrent execution as resource use and responsiveness became more important.",
                "The historical framing matters because it shows concurrency as a response to real system pressure, not just a language feature.",
            ],
            ["Track what resources were being wasted.", "Notice how waiting for external work pushes systems toward overlap.", "Connect the history to modern Java workloads."],
        )
    if "benefits" in key:
        return (
            [
                "The benefits slide is where the book argues that threads earn their cost when they improve overlap, responsiveness, or the shape of asynchronous code.",
                "Read the examples here as motivation for when concurrency changes the design for the better.",
            ],
            ["Parallel work can use more hardware.", "Background work can protect responsiveness.", "Sequential task code can simplify asynchronous workflows."],
        )
    if "risks" in key:
        return (
            [
                "This section groups concurrency hazards into safety, liveness, and performance failures.",
                "That split becomes the map for the rest of the book, so it is worth treating these categories as debugging tools.",
            ],
            ["Safety means wrong answers or broken invariants.", "Liveness means progress stops or stalls.", "Performance means the coordination cost cancels out the benefit."],
        )
    if "thread safety" in key or "what is thread safety" in key:
        return (
            [
                "This section defines thread safety as correct behavior under concurrent access without hidden caller-side rules.",
                "The important shift is from syntax to behavior: safety is a contract, not a keyword.",
            ],
            ["Name the shared mutable state.", "Name the invariant to preserve.", "Ask whether callers need extra undocumented coordination."],
        )
    if "atomicity" in key or "locking" in key or "guarding state" in key:
        return (
            [
                "This part of the chapter explains how compound actions and shared invariants need one coherent protection boundary.",
                "Read it by asking what could change in the middle of a multi-step action if the protection rule were removed.",
            ],
            ["Protect the whole action, not just one field.", "Map each lock to guarded state.", "Keep the invariant in mind while reading the example."],
        )
    if "visibility" in key or "publication" in key or "escape" in key or "immutability" in key or "confinement" in key:
        return (
            [
                "This section is about what other threads are allowed to observe and how state crosses thread boundaries safely.",
                "Visibility, publication, confinement, and immutability are all tools for making those observations predictable.",
            ],
            ["Stale reads are real bugs.", "Safe publication matters even for objects that look stable.", "Confinement and immutability shrink the coordination surface."],
        )
    if "composing" in key or "designing" in key or "delegating" in key or "documenting" in key:
        return (
            [
                "This focus area is about preserving invariants when a larger class is built from smaller pieces.",
                "The design question is whether safety is owned locally, delegated cleanly, or undermined by hidden cross-field rules.",
            ],
            ["A safe field does not guarantee a safe aggregate.", "Cross-field invariants need one clear policy.", "Documentation is part of the synchronization design."],
        )
    if "collections" in key or "queues" in key or "synchronizers" in key or "cache" in key:
        return (
            [
                "This section shows why stronger library abstractions usually beat hand-rolled coordination protocols.",
                "The point is to let a tested type carry the waiting rule, sharing rule, or access pattern instead of recreating it in application code.",
            ],
            ["Choose the abstraction that matches the coordination pattern.", "Notice where blocking and contention show up.", "Prefer explicit semantics over ad hoc signaling."],
        )
    if "task" in key or "executor" in key or "parallel" in key:
        return (
            [
                "This section reframes concurrency around units of work and the policy used to execute them.",
                "The main reading habit is to separate what the task does from how the runtime schedules, queues, or cancels it.",
            ],
            ["Define good task boundaries first.", "Keep execution policy visible.", "Exploit parallelism only when work is independent enough."],
        )
    if "cancellation" in key or "shutdown" in key or "interruption" in key or "termination" in key or "lifecycle" in key:
        return (
            [
                "This focus area is about how concurrent work stops, fails, or hands control back safely.",
                "The chapter treats shutdown as part of the service contract rather than as cleanup code at the end.",
            ],
            ["Interruption is cooperative.", "Blocked work still needs a response path.", "Service lifecycle boundaries should be explicit."],
        )
    if "pool" in key or "threadpoolexecutor" in key or "rejected" in key or "back-pressure" in key:
        return (
            [
                "This section turns executors into execution policy: queueing, sizing, overload behavior, and coupling between tasks all matter.",
                "The key is to read the pool as a resource budget instead of a generic performance booster.",
            ],
            ["Pool size depends on workload shape.", "Queue choice changes overload behavior.", "Dependent tasks can create liveness problems inside constrained pools."],
        )
    if "gui" in chapter_key or "single-threaded" in key or "background" in key or "model" in key:
        return (
            [
                "The lesson here is that some threads own responsiveness-critical work and must stay short and predictable.",
                "Long-running tasks belong elsewhere, with results marshaled back carefully to the owner thread.",
            ],
            ["Keep owner-thread work short.", "Move heavy work out of the latency-sensitive path.", "Preserve ownership rules when state comes back."],
        )
    if "deadlock" in key or "liveness" in key or "starvation" in key or "livelock" in key:
        return (
            [
                "This section studies ways a program can stop making useful progress even while it remains alive.",
                "Deadlock is the obvious case, but the broader lesson is to design for forward progress, not just mutual exclusion.",
            ],
            ["Look for waiting cycles.", "Reduce multi-lock or multi-resource coupling.", "Use ordering, openness, and retry strategies deliberately."],
        )
    if "performance" in key or "scalability" in key or "amdahl" in key or "contention" in key or "context switch" in key:
        return (
            [
                "This section is about the real limits on concurrent speedup: serialized work, contention, scheduling cost, and waiting overhead.",
                "The chapter's point is that concurrency helps only after those bottlenecks are understood and reduced.",
            ],
            ["Measure before tuning.", "Reduce shared hot spots.", "Treat extra threads as cost as well as opportunity."],
        )
    if "testing" in key or "observability" in key or "stress" in key:
        return (
            [
                "This focus area turns testing into a way to expose rare timing and coordination failures instead of accidentally hiding them.",
                "The aim is to make nondeterministic problems repeatable enough to diagnose.",
            ],
            ["Separate safety and liveness checks.", "Run long enough for rare failures to appear.", "Keep concurrency state observable in tests."],
        )
    if "lock" in key or "condition" in key or "synchronizer" in key or "aqs" in key:
        return (
            [
                "This section uses lower-level primitives only where their extra semantics solve a concrete coordination problem.",
                "Read it as a lesson in choosing stronger control only when the state model and waiting rules are already clear.",
            ],
            ["Name the state transition being protected.", "Keep acquisition and release rules explicit.", "Choose advanced primitives only when the invariant demands them."],
        )
    if "atomic" in key or "non-blocking" in key or "memory model" in chapter_key or "publication" in key or "reordering" in key:
        return (
            [
                "This section connects low-level guarantees to what other threads are allowed to observe.",
                "Atomics, publication, and ordering rules only help when the state change and visibility edge are understood precisely.",
            ],
            ["Atomics suit narrow transitions.", "Ordering guarantees matter for visibility.", "Use higher-level patterns when low-level reasoning becomes fragile."],
        )
    return (
        [
            f"This section uses {focus_title.lower()} to make the chapter's concurrency trade-offs concrete.",
            f"Read it by tracking the state, execution policy, or progress guarantee that {chapter_key} is trying to make explicit.",
        ],
        ["Identify the shared state or resource boundary.", "Notice what can go wrong if the rule is ignored.", "Connect the example back to the chapter's main design principle."],
    )


def build_chapter_slides(chapter: dict[str, object], guide: dict[str, object]) -> list[tuple[str, str]]:
    chapter_title = str(chapter["title"])
    chapter_number = int(chapter["chapter_number"])
    start_page = int(chapter["start_page"])
    end_page = int(chapter["end_page"])
    items = chapter_progression(chapter)
    focuses = choose_focuses(chapter, guide)

    slides: list[tuple[str, str]] = []
    slides.append(
        (
            "Chapter Map",
            text_only_slide(
                "Chapter Map",
                [
                    f"Chapter {chapter_number} focuses on {chapter_title.lower()} across source pages {start_page}-{end_page}.",
                    str(guide["why"]),
                    str(guide["through_line"]),
                ],
                points=[f"Section: {title}" for title in items[:6]],
                extra_box=f"<strong>Primary rule:</strong> {guide['principle']}",
                guide=guide,
                source_pages=(start_page, end_page),
            ),
        )
    )
    slides.append(
        (
            "What To Watch For",
            text_only_slide(
                "What To Watch For",
                [
                    f"This chapter matters because {str(guide['why']).rstrip('.')}.",
                    f"As you read the examples, keep this framing in mind: {guide['through_line']}",
                    "Most of the examples in this chapter are easiest to understand when you trace the state boundary, the execution policy, and the failure mode being prevented.",
                ],
                points=[
                    "Which state or resource is shared?",
                    "What coordination rule is being enforced?",
                    "What failure appears if that rule is dropped?",
                ],
                guide=guide,
                source_pages=(start_page, end_page),
            ),
        )
    )

    for focus in focuses:
        paragraphs, points = describe_focus(chapter_title, str(focus["title"]))
        slides.append(
            (
                str(focus["title"]),
                text_only_slide(
                    str(focus["title"]),
                    paragraphs,
                    points=points,
                    guide=guide,
                    source_pages=(int(focus["start_page"]), int(focus["end_page"])),
                ),
            )
        )

    slides.append(
        (
            "Common Traps",
            text_only_slide(
                "Common Traps",
                [
                    f"Chapter {chapter_number} is also a warning label. The examples are there to make the failure modes feel concrete before they appear in production code.",
                    "Use these traps as review prompts when you revisit your own code or compare alternative designs.",
                ],
                points=[str(item) for item in guide["pitfalls"]],
                box_kind="warn",
                extra_box="<strong>Review habit:</strong> if one of these traps sounds familiar in your codebase, revisit the full chapter examples before patching locally.",
                guide=guide,
                source_pages=(start_page, end_page),
            ),
        )
    )
    slides.append(
        (
            "Review Checklist",
            text_only_slide(
                "Review Checklist",
                [
                    f"Use this checklist to turn Chapter {chapter_number} into an engineering review lens instead of a one-time reading exercise.",
                    "If you can answer these questions cleanly, you usually understand what this chapter is trying to protect.",
                ],
                points=[str(item) for item in guide["checklist"]],
                box_kind="tip",
                extra_box=f"<strong>Keep in mind:</strong> {guide['principle']}",
                guide=guide,
                source_pages=(start_page, end_page),
            ),
        )
    )
    return slides


def build_chapter_questions(chapter: dict[str, object], guide: dict[str, object], all_titles: list[str]) -> list[dict[str, object]]:
    chapter_title = str(chapter["title"])
    item_titles = [str(item["title"]) for item in chapter["items"]]
    wrong_titles = [title for title in all_titles if title != chapter_title]
    wrong_item_titles = [title for title in all_titles if title not in item_titles]
    checklist = [str(item) for item in guide["checklist"]]
    pitfalls = [str(item) for item in guide["pitfalls"]]

    return [
        q(
            f"What is the main concern of Chapter {chapter['chapter_number']}?",
            chapter_title,
            wrong_titles[0],
            wrong_titles[1],
            wrong_titles[2],
            f"This chapter is specifically about {chapter_title.lower()}.",
        ),
        q(
            f"Which section belongs to the {chapter_title} chapter?",
            item_titles[0] if item_titles else str(guide["extra_focuses"][0]),
            wrong_item_titles[0],
            wrong_item_titles[1],
            wrong_item_titles[2],
            f"The chapter manifest lists this topic under {chapter_title}.",
        ),
        q(
            f"Which review habit best matches the {chapter_title} chapter?",
            checklist[0],
            wrong_titles[3],
            wrong_titles[4],
            wrong_titles[5],
            "The checklist slide turns the chapter into a practical review lens.",
        ),
        q(
            f"Which trap is explicitly called out for the {chapter_title} chapter?",
            pitfalls[0],
            checklist[1],
            checklist[2],
            checklist[3],
            "The Common Traps slide highlights recurring mistakes tied to this chapter's topic.",
        ),
    ]


def build_modules(manifest: dict[str, object]) -> list[dict[str, object]]:
    all_titles = [str(chapter["title"]) for chapter in manifest["chapters"]]
    modules: list[dict[str, object]] = []
    for chapter in manifest["chapters"]:
        chapter_number = int(chapter["chapter_number"])
        guide = CHAPTER_GUIDES[chapter_number]
        modules.append(
            module(
                f"Chapter {chapter_number}: {chapter['title']}",
                build_chapter_slides(chapter, guide),
                build_chapter_questions(chapter, guide, all_titles),
            )
        )
    return modules


def main() -> None:
    manifest = load_manifest()
    modules = build_modules(manifest)
    attach_question_ids(modules, TOPIC_SLUG.lower())

    base.TOPIC_SLUG = TOPIC_SLUG
    base.WORKSHOP_TITLE = WORKSHOP_TITLE
    base.WORKSHOP_SUBTITLE = WORKSHOP_SUBTITLE
    base.MODULES = modules

    slides = base.build_slides()
    quiz_data = base.build_quiz_data()
    html = base.build_html(slides, quiz_data)

    (BOOK_ROOT / f"{TOPIC_SLUG}_workshop.html").write_text(html, encoding="utf-8")
    (BOOK_ROOT / f"{TOPIC_SLUG}_quiz.json").write_text(
        json.dumps(quiz_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
