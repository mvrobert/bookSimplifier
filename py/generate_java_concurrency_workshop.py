from __future__ import annotations

import json
from pathlib import Path

import generate_workshop as base

from effective_java_common import attach_question_ids, module, q, slide


TOPIC_SLUG = "JavaConcurrency"
WORKSHOP_TITLE = "Java Concurrency in Practice Workshop"
WORKSHOP_SUBTITLE = "Developer-friendly overview built from JavaConcurrency.pdf"


def preview(page: int) -> str:
    return f"page_previews/page_{page:04d}.png"


MODULES = [
    module(
        "M0: Orientation",
        [
            (
                "How the Book Is Organized",
                slide(
                    [
                        "This deck turns `JavaConcurrency.pdf` into a shorter study route.",
                        "The book moves from thread-safety basics into executors, cancellation, liveness, performance, testing, and advanced synchronization tools.",
                        "Use the source spans to jump back into the PDF when you want the fuller code examples.",
                    ],
                    image=preview(18),
                    caption="Chapter 1 opening page.",
                    points=[
                        "Part I: safety, visibility, composition, building blocks",
                        "Part II: tasks, cancellation, pools, GUI responsiveness",
                        "Part III: liveness, scalability, testing",
                        "Part IV: explicit locks, custom synchronizers, atomics, memory model",
                    ],
                    box=("tip", "<strong>Reading rule:</strong> classify problems as safety, visibility, liveness, or performance issues before choosing a fix."),
                    source_pages=(18, 27),
                ),
            ),
            (
                "Why Concurrency Helps and Hurts",
                slide(
                    [
                        "Threads help overlap work, use multiple cores, and keep blocking operations from freezing the whole application.",
                        "They also introduce shared-state races, stale reads, deadlock risk, and coordination overhead.",
                        "The book's message is to use concurrency deliberately, not by default.",
                    ],
                    image=preview(20),
                    caption="Introduction pages summarizing benefits and risks.",
                    source_pages=(19, 25),
                ),
            ),
        ],
        [
            q("Why does the book front-load thread safety?", "Because later concurrency techniques depend on shared state being managed correctly", "Because GUI code always comes first", "Because performance tuning must happen before correctness", "Because thread pools remove safety bugs", "The preface treats safety as the base layer for everything else."),
            q("Which pair matches the introduction?", "Threads can improve overlap and responsiveness, but they add coordination risk", "Threads remove the need for synchronization", "Threads only matter for GUIs", "Threads always improve performance linearly", "The book balances benefits against hazards from the start."),
            q("What is the best first step when a concurrency bug feels vague?", "Classify it as safety, visibility, liveness, or performance", "Increase thread priority", "Replace all collections", "Disable interrupts", "The workshop uses the book's structure as a debugging map."),
            q("What are the source page spans for?", "To jump back into the original PDF for full examples and detail", "To skip the PDF entirely", "To find only figures", "To choose pool sizes", "The deck is a guide, not a full replacement for the book."),
        ],
    ),
    module(
        "M1: Safety and Visibility",
        [
            (
                "Thread Safety in Practice",
                slide(
                    [
                        "A class is thread-safe when it behaves correctly under concurrent access without forcing callers to add hidden extra locking.",
                        "Most failures come from shared mutable state, compound actions, and undocumented invariants.",
                        "The book repeatedly asks: what state exists, who mutates it, and what rule protects it?",
                    ],
                    image=preview(28),
                    caption="Chapter 2 on thread safety.",
                    points=[
                        "Stateless objects are easiest to make safe.",
                        "Check-then-act and read-modify-write sequences need real protection.",
                        "Thread safety is a behavior guarantee, not just a keyword.",
                    ],
                    source_pages=(28, 39),
                ),
            ),
            (
                "Visibility, Confinement, and Publication",
                slide(
                    [
                        "Chapter 3 adds the subtle problem: one thread may not see another thread's writes when you expect.",
                        "Synchronization is therefore about visibility as well as atomicity. Volatile, locking, and safe publication patterns tell the runtime what must become visible across threads.",
                        "Confinement and immutability shrink the amount of state that needs coordination in the first place.",
                    ],
                    image=preview(40),
                    caption="Chapter 3 on visibility and safe publication.",
                    box=("warn", "<strong>Common mistake:</strong> code that 'usually works' is not evidence that visibility or publication is correct."),
                    source_pages=(40, 53),
                ),
            ),
        ],
        [
            q("What best defines a thread-safe class?", "It behaves correctly under concurrent access without extra caller-side synchronization", "It contains a synchronized method", "It avoids object allocation", "It uses only final methods", "The book defines thread safety as a behavioral property."),
            q("Why are check-then-act sequences risky?", "Another thread can change state between the check and the action", "They always throw InterruptedException", "The JVM forbids them in threads", "They disable caching", "Compound actions become races unless protected as one unit."),
            q("What extra job does synchronization do besides atomicity?", "It provides visibility of writes across threads", "It increases queue capacity", "It schedules garbage collection", "It changes thread priority", "Chapter 3 emphasizes visibility strongly."),
            q("When is volatile most appropriate?", "For simple visibility-based state protocols, not rich multi-step invariants", "As a replacement for every lock", "For iterating collections safely", "For blocking I/O", "Volatile helps, but it is not a universal substitute for locking."),
        ],
    ),
    module(
        "M2: Composition and Building Blocks",
        [
            (
                "Composing Safe Classes",
                slide(
                    [
                        "A class built from thread-safe parts is not automatically thread-safe as a whole.",
                        "Composition can introduce cross-field invariants and compound operations that the parts do not protect together.",
                        "That is why Chapter 4 pushes hard on documenting synchronization policy and ownership of state.",
                    ],
                    image=preview(54),
                    caption="Chapter 4 on composition and delegation.",
                    source_pages=(54, 67),
                ),
            ),
            (
                "Prefer Library Building Blocks",
                slide(
                    [
                        "Chapter 5 argues for using concurrent collections, blocking queues, futures, latches, and semaphores instead of hand-rolled wait/notify protocols whenever possible.",
                        "These abstractions package concurrency policies more clearly and usually more safely than custom coordination code.",
                        "The broad lesson is to move upward in abstraction before reaching for lower-level primitives.",
                    ],
                    image=preview(68),
                    caption="Chapter 5 on concurrent collections and synchronizers.",
                    points=[
                        "BlockingQueue simplifies producer-consumer work.",
                        "Concurrent collections improve shared-access patterns.",
                        "Synchronizers express coordination directly.",
                    ],
                    source_pages=(68, 88),
                ),
            ),
        ],
        [
            q("Why are thread-safe parts not enough by themselves?", "Because the full object may have invariants that span multiple operations or fields", "Because thread-safe classes cannot be reused", "Because composition disables locking", "Because Java forbids nested objects", "Composition can create new correctness requirements."),
            q("What is a major message of Chapter 5?", "Use JDK concurrent collections and synchronizers before inventing your own coordination protocol", "Avoid all collection classes", "Use polling loops instead of blocking", "Replace queues with volatile arrays", "The book consistently favors stronger built-in abstractions."),
            q("Why can synchronized collections still surprise callers?", "Compound actions like iteration or put-if-absent may still need extra coordination", "They cannot store mutable objects", "They stop working on multicore CPUs", "They disable exceptions", "Method-level thread safety is not the same as workflow-level safety."),
            q("When is BlockingQueue especially helpful?", "In producer-consumer designs with natural blocking behavior", "For replacing immutable objects", "For keeping UI work on the event thread", "For safe publication of final fields", "It directly models a common coordination pattern."),
        ],
    ),
    module(
        "M3: Tasks, Cancellation, and Pools",
        [
            (
                "Think in Tasks, Not Raw Threads",
                slide(
                    [
                        "Chapter 6 reframes concurrency around units of work. Define tasks and hand them to an execution policy instead of micromanaging thread creation everywhere.",
                        "That separation lets task logic evolve separately from queueing, sizing, reuse, shutdown, and monitoring.",
                        "Executor, Callable, and Future are central because they decouple what work is done from how it runs.",
                    ],
                    image=preview(89),
                    caption="Chapter 6 on task execution.",
                    source_pages=(89, 101),
                ),
            ),
            (
                "Cancellation and Pool Policy",
                slide(
                    [
                        "Chapter 7 treats cancellation as part of service design, not a side feature. Interruption is the standard cooperative signal and code has to honor it consistently.",
                        "Chapter 8 adds that thread pools are resource-management policies. Size, queue choice, task dependencies, and blocking behavior all affect throughput and liveness.",
                        "A pool is not just a performance trick. It is a concurrency contract.",
                    ],
                    image=preview(121),
                    caption="Chapters 7 and 8 on shutdown, interruption, and pool design.",
                    box=("warn", "<strong>Pool sizing:</strong> base it on workload shape and blocking behavior, not copied defaults."),
                    source_pages=(102, 133),
                ),
            ),
        ],
        [
            q("What is the benefit of separating tasks from thread management?", "Task logic and execution policy can change independently", "It makes all code lock-free", "It removes the need for shutdown", "It guarantees perfect CPU usage", "Chapter 6 treats executors as separation of concerns."),
            q("Which abstractions fit the book's preferred execution style?", "Executor, Callable, and Future", "stop, suspend, and ThreadGroup", "Vector, Hashtable, and Timer", "clone, finalize, and notify", "The book strongly steers work toward executor-based execution."),
            q("Why is cancellation a design problem?", "Because tasks, blocking points, shutdown boundaries, and recovery behavior all have to cooperate", "Because Java cannot interrupt threads", "Because only GUIs cancel work", "Because cancellation is handled by the garbage collector", "Robust cancellation depends on protocol and structure."),
            q("Why can a thread pool hurt liveness?", "Tasks can block, depend on each other, or exhaust the limited execution budget", "Pools always create too many threads", "Pools disable queueing", "Pools break memory visibility", "Chapter 8 focuses on hidden coupling between tasks and policy."),
        ],
    ),
    module(
        "M4: Responsiveness, Liveness, and Performance",
        [
            (
                "Protecting Responsiveness",
                slide(
                    [
                        "Chapter 9 uses GUI work to show that some threads own responsiveness-critical work and must stay fast and predictable.",
                        "Long-running work belongs on background threads, but coordination back to the owning thread has to stay disciplined.",
                        "This lesson applies outside GUIs too: some subsystems have a latency budget that background work must respect.",
                    ],
                    image=preview(134),
                    caption="Chapter 9 on responsiveness in single-threaded subsystems.",
                    source_pages=(134, 144),
                ),
            ),
            (
                "Deadlock to Scalability",
                slide(
                    [
                        "Chapter 10 covers deadlock, starvation, and livelock: different ways a program can stop making useful progress.",
                        "Chapter 11 adds the performance view: more threads do not guarantee more throughput. Contention, serialized sections, and context switching cap scalability.",
                        "Amdahl's Law is the reminder that a small serialized bottleneck can dominate the speedup ceiling.",
                    ],
                    image=preview(154),
                    caption="Chapters 10 and 11 on liveness and scalability.",
                    points=[
                        "Deadlock: progress stops in a waiting cycle.",
                        "Livelock: work keeps reacting but never finishes.",
                        "Scalability depends on reducing contention and serialized work.",
                    ],
                    source_pages=(145, 169),
                ),
            ),
        ],
        [
            q("What is the broad lesson from the GUI chapter?", "Some threads own responsiveness-critical work and must stay short and predictable", "Every background task should run on the UI thread", "GUI code never needs synchronization", "Thread pools should not touch models", "Chapter 9 generalizes to any latency-sensitive subsystem."),
            q("What best separates deadlock from livelock?", "Deadlock blocks progress in a cycle, while livelock keeps reacting without useful completion", "Deadlock affects syntax, livelock affects memory", "They are identical", "Livelock happens only with semaphores", "Chapter 10 distinguishes blocked progress from endless useless activity."),
            q("What does Amdahl's Law highlight?", "A serialized fraction can cap speedup from added parallelism", "Every workload scales linearly", "More locks always improve throughput", "Thread pools remove bottlenecks", "Chapter 11 uses Amdahl's Law to set realistic scalability expectations."),
            q("What change is most likely to improve scalability?", "Reducing contention at a shared hotspot", "Adding threads without measuring", "Making more fields global", "Holding locks longer", "The book focuses on narrowing the serialized and contended parts."),
        ],
    ),
    module(
        "M5: Testing and Advanced Topics",
        [
            (
                "Testing Concurrent Code",
                slide(
                    [
                        "Chapter 12 explains why normal unit tests are not enough for concurrent code. Timing-sensitive failures may appear only under specific interleavings or stress levels.",
                        "Testing therefore has to mix correctness checks, stress, performance checks, and designs that make concurrency errors easier to provoke and observe.",
                        "Poorly structured concurrent code is harder to test because its coordination rules are hidden.",
                    ],
                    image=preview(170),
                    caption="Chapter 12 on testing correctness and performance.",
                    source_pages=(170, 187),
                ),
            ),
            (
                "Locks, Atomics, and the Memory Model",
                slide(
                    [
                        "Chapters 13 and 14 introduce explicit locks and custom synchronizers for cases where intrinsic locking or existing utilities are not expressive enough.",
                        "Chapters 15 and 16 show where atomics shine and why the Java Memory Model still governs visibility, ordering, and safe publication underneath every higher-level abstraction.",
                        "Advanced primitives do not remove the need to reason carefully about invariants. They raise the bar for precision.",
                    ],
                    image=preview(224),
                    caption="Chapters 13-16 on advanced synchronization tools and memory semantics.",
                    box=("tip", "<strong>Decision rule:</strong> use atomics for narrow state changes; use locks when you must preserve richer invariants across multiple variables or operations."),
                    source_pages=(188, 235),
                ),
            ),
        ],
        [
            q("Why are ordinary unit tests often weak for concurrent code?", "Many bugs depend on rare timing and interleaving conditions", "Concurrent code cannot be tested", "The JVM disables assertions in threads", "Only production traffic can exercise it", "Chapter 12 emphasizes how hard timing-sensitive failures are to expose."),
            q("When are explicit locks especially useful?", "When you need timed acquisition, interruptible acquisition, or multiple condition queues", "When synchronized is illegal", "Only for immutable classes", "Only for GUI code", "Chapter 13 explains why explicit locks exist beyond intrinsic locking."),
            q("What do atomic variables do well?", "They support narrow state transitions with low coordination overhead", "They preserve arbitrary multi-object invariants automatically", "They eliminate publication concerns", "They make blocking code non-blocking", "Chapter 15 treats atomics as precise tools, not universal replacements."),
            q("Why does the Java Memory Model still matter?", "Because visibility, ordering, and publication guarantees determine what other threads can observe", "Because it only affects legacy JVMs", "Because it applies only to GUIs", "Because it replaces thread safety", "The memory model underlies all the visibility rules the book relies on."),
        ],
    ),
]


def main() -> None:
    output_dir = Path("output") / TOPIC_SLUG
    output_dir.mkdir(parents=True, exist_ok=True)

    modules = json.loads(json.dumps(MODULES))
    attach_question_ids(modules, TOPIC_SLUG.lower())

    base.TOPIC_SLUG = TOPIC_SLUG
    base.WORKSHOP_TITLE = WORKSHOP_TITLE
    base.WORKSHOP_SUBTITLE = WORKSHOP_SUBTITLE
    base.MODULES = modules

    slides = base.build_slides()
    quiz_data = base.build_quiz_data()
    html = base.build_html(slides, quiz_data)

    (output_dir / f"{TOPIC_SLUG}_workshop.html").write_text(html, encoding="utf-8")
    (output_dir / f"{TOPIC_SLUG}_quiz.json").write_text(json.dumps(quiz_data, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
