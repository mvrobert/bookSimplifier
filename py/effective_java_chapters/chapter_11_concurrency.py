from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Chapter 11: Concurrency",
    "subtitle": "Effective Java, pages 332-359. Items 78-84: synchronization, excessive synchronization, executors and tasks, concurrency utilities, thread-safety documentation, lazy initialization, and scheduler dependence.",
    "modules": [
        module(
            "Synchronize shared mutable state",
            [
                (
                    "Shared mutable data needs a happens-before edge",
                    slide(
                        [
                            "If multiple threads can read and write the same state, you need a synchronization strategy. Otherwise updates can be lost, reads can be stale, and invariants can be observed half-updated.",
                            "The book's rule is blunt: synchronize every access to shared mutable data unless the object is safely published and immutable, or you use a higher-level concurrent utility that provides the same ordering guarantees.",
                            "Thread safety is not about being fast enough on your laptop. It is about establishing the visibility and atomicity that the Java Memory Model requires.",
                        ],
                        image="../../page_previews/page_0332.png",
                        caption="Item 78 begins with the basic rule for shared mutable state: every access must be coordinated.",
                        source_pages=(332, 334),
                    ),
                ),
                (
                    "Unsynchronized increment is not a minor bug",
                    slide(
                        [
                            "A read-modify-write sequence such as `count++` is not atomic. Two threads can both read the same value and then overwrite each other's updates.",
                            "Using `volatile` alone does not fix this. `volatile` gives visibility, not mutual exclusion or compound atomicity.",
                            "If you need a count, use `AtomicLong`, `LongAdder`, or a lock around the entire critical section. Pick the abstraction that matches the invariant, not the one that merely compiles.",
                        ],
                        image="../../page_previews/page_0334.png",
                        caption="Visibility and atomicity are different concerns; compound actions need a real synchronization boundary.",
                        source_pages=(334, 337),
                    ),
                ),
                (
                    "Synchronization protects invariants, not just fields",
                    slide(
                        [
                            "The point of synchronization is usually to preserve an invariant over several fields, not to protect one field in isolation.",
                            "If a method updates one field and then another, the entire update should usually be inside one synchronized region so observers never see the object in an impossible intermediate state.",
                            "When a class has a documented thread-safety policy, callers can reason about whether they need external locking or can use it concurrently as-is.",
                        ],
                        image="../../page_previews/page_0336.png",
                        caption="Item 78 ties synchronization to object invariants and published thread-safety policy.",
                        source_pages=(334, 337),
                    ),
                ),
            ],
            [
                q(
                    "Why is `count++` unsafe when multiple threads share the same counter?",
                    "It is a read-modify-write sequence, so updates can be lost without synchronization.",
                    "Because `int` values cannot be shared between threads.",
                    "Because `++` is always compiled as a loop.",
                    "Because `count` becomes immutable after the first increment.",
                    "Compound operations need mutual exclusion or an atomic class; otherwise two threads can overwrite each other's work.",
                    question_id="chapter_11_m1_q1",
                ),
                q(
                    "What does `volatile` guarantee, and what does it not guarantee?",
                    "It guarantees visibility of writes, but not mutual exclusion or atomicity of compound actions.",
                    "It guarantees both mutual exclusion and atomicity.",
                    "It makes every method in the class thread-safe automatically.",
                    "It prevents all reordering everywhere in the JVM.",
                    "A volatile field can still be involved in a race if you perform compound updates.",
                    question_id="chapter_11_m1_q2",
                ),
                q(
                    "What is the real target of synchronization in a mutable class?",
                    "The object invariant and the visibility of state transitions, not just individual fields.",
                    "Only the public methods.",
                    "Only the constructor.",
                    "Only the fields marked private.",
                    "Synchronizing the invariant boundary is what keeps readers from seeing a half-updated object.",
                    question_id="chapter_11_m1_q3",
                ),
                q(
                    "When is a shared object usually safe without external synchronization?",
                    "When it is immutable and safely published, or when it is internally thread-safe by design.",
                    "Whenever it has only one mutable field.",
                    "Whenever its methods are `final`.",
                    "Whenever the code passes all unit tests on one machine.",
                    "Thread safety comes from a documented policy and the memory-ordering guarantees behind it.",
                    question_id="chapter_11_m1_q4",
                ),
            ],
        ),
        module(
            "Avoid excessive synchronization",
            [
                (
                    "Do not hold a lock while calling alien code",
                    slide(
                        [
                            "Excessive synchronization is not just a performance problem. It can cause deadlock, contention, and surprise reentrancy when a callback runs while your lock is held.",
                            "The dangerous pattern is an open call: invoke an overridable method, client callback, or foreign object method while still inside a synchronized region.",
                            "Copy the data you need, drop the lock, and then call out if the callback does not require the lock. The rule is simpler than the edge cases it prevents.",
                        ],
                        image="../../page_previews/page_0338.png",
                        caption="Item 79 warns against open calls and holding locks across foreign code.",
                        source_pages=(338, 340),
                    ),
                ),
                (
                    "Synchronizing every method is often too blunt",
                    slide(
                        [
                            "A blanket `synchronized` modifier on every method can turn one object's lock into a throughput bottleneck.",
                            "It also increases the chance of deadlock if methods call each other across object boundaries or if client code tries to compose several locked objects.",
                            "Lock only the critical section needed to preserve the invariant, and keep the synchronized region as small and simple as correctness allows.",
                        ],
                        image="../../page_previews/page_0340.png",
                        caption="Item 79 prefers tight critical sections over class-wide locking by habit.",
                        source_pages=(339, 343),
                    ),
                ),
                (
                    "Inheritance and synchronization interact badly",
                    slide(
                        [
                            "A synchronized base class can be fragile if subclasses override methods and the base class calls them while holding its lock.",
                            "The safer design is often composition or a private helper method that is never overridden. That keeps the lock protocol under one author's control.",
                            "If a class needs to be extensible, document the synchronization policy explicitly or prohibit overriding altogether.",
                        ],
                        image="../../page_previews/page_0342.png",
                        caption="Excessive synchronization becomes much riskier when overridable methods enter the picture.",
                        source_pages=(340, 343),
                    ),
                ),
            ],
            [
                q(
                    "Why are open calls dangerous inside synchronized methods?",
                    "Because foreign or overridable code can run while your lock is held, causing deadlock or invariant violations.",
                    "Because they prevent the JVM from compiling the method.",
                    "Because they automatically make the method recursive.",
                    "Because synchronized blocks cannot contain method calls.",
                    "Calling out while holding a lock gives control to code you do not own, which is exactly where lock-order bugs appear.",
                    question_id="chapter_11_m2_q1",
                ),
                q(
                    "What is the best default when a synchronized region is larger than it needs to be?",
                    "Shrink it to the minimal section required to preserve the invariant.",
                    "Add more synchronized methods to compensate.",
                    "Replace the lock with `volatile`.",
                    "Move the lock to the caller automatically.",
                    "Excessive synchronization hurts correctness and performance, so minimize the locked scope rather than masking the design flaw.",
                    question_id="chapter_11_m2_q2",
                ),
                q(
                    "Why can inheritance make synchronization fragile?",
                    "Because overridden methods may run under a lock that the subclass does not control.",
                    "Because inheritance disables thread safety completely.",
                    "Because subclasses cannot access synchronized methods.",
                    "Because locks are inherited but monitors are not.",
                    "A superclass cannot safely assume what subclass code will do if it invokes overridable methods while locked.",
                    question_id="chapter_11_m2_q3",
                ),
                q(
                    "What is the practical benefit of copying state before calling foreign code?",
                    "It lets you release the lock before the callback executes.",
                    "It turns the method into a nonblocking algorithm automatically.",
                    "It makes the object immutable.",
                    "It removes the need for thread-safety documentation.",
                    "A local copy narrows the critical section and avoids holding a lock across unpredictable code.",
                    question_id="chapter_11_m2_q4",
                ),
            ],
        ),
        module(
            "Executors, utilities, and documentation",
            [
                (
                    "Prefer executors, tasks, and streams to raw threads",
                    slide(
                        [
                            "Raw thread management is low-level and brittle. An executor decouples task submission from task execution, which gives you pooling, scheduling, and policy control in one abstraction.",
                            "Tasks are the unit of work; threads are an implementation detail. Streams can also express bulk work more clearly than hand-managed thread farms when the problem is data-oriented.",
                            "If the work is structured as independent units, start with an executor before inventing ad hoc thread control.",
                        ],
                        image="../../page_previews/page_0344.png",
                        caption="Item 80 recommends executors and task abstractions over direct thread management.",
                        source_pages=(344, 345),
                    ),
                ),
                (
                    "Use concurrent utilities instead of wait and notify",
                    slide(
                        [
                            "Low-level `wait` and `notify` are easy to misuse because they require the caller to manage condition predicates, missed signals, and spurious wakeups correctly.",
                            "Prefer `BlockingQueue`, `CountDownLatch`, `Semaphore`, `CyclicBarrier`, `Exchanger`, and other utilities that package the protocol into a tested abstraction.",
                            "If you are writing your own monitor protocol, that is usually a signal that the JDK already has a better fit.",
                        ],
                        image="../../page_previews/page_0346.png",
                        caption="Item 81 moves most coordination problems out of handwritten monitor code.",
                        source_pages=(346, 350),
                    ),
                ),
                (
                    "Document thread safety explicitly",
                    slide(
                        [
                            "Clients cannot safely guess whether a class is thread-safe, conditionally thread-safe, or not thread-safe. The API must say so.",
                            "Document which lock, if any, guards the object state, whether the class is immutable, whether instances are externally synchronized, and which methods may be called concurrently.",
                            "Without that contract, even correct code becomes hard to compose because callers have no idea what concurrency assumptions are valid.",
                        ],
                        image="../../page_previews/page_0351.png",
                        caption="Item 82 treats thread-safety documentation as part of the API contract.",
                        source_pages=(351, 353),
                    ),
                ),
                (
                    "Lazy initialization and scheduler dependence are edge cases",
                    slide(
                        [
                            "Lazy initialization is only worth the complexity when initialization is genuinely expensive or may never be needed. Otherwise, eager initialization is simpler and usually safer.",
                            "If you do use lazy initialization, prefer the static holder pattern or a correctly synchronized/volatile-based approach. Do not invent a racy double-checked solution unless you can prove it.",
                            "For scheduler dependence, the lesson is the same: do not write concurrency that only works when the thread scheduler happens to be kind.",
                        ],
                        image="../../page_previews/page_0354.png",
                        caption="Items 83 and 84 push you toward simple initialization and scheduler-independent design.",
                        source_pages=(354, 359),
                    ),
                ),
            ],
            [
                q(
                    "Why does Effective Java prefer executors over manually managed threads?",
                    "Executors separate task submission from execution policy and make pooling and scheduling explicit.",
                    "Because threads are illegal in modern Java.",
                    "Because executors always outperform threads in every workload.",
                    "Because executor tasks cannot block.",
                    "An executor gives you a higher-level abstraction with fewer error-prone details to manage yourself.",
                    question_id="chapter_11_m3_q1",
                ),
                q(
                    "Why are `wait` and `notify` discouraged for most application code?",
                    "Because higher-level concurrency utilities already encode the coordination protocol more safely.",
                    "Because they do not work on synchronized objects.",
                    "Because they are slower than every other API by definition.",
                    "Because they can only be used in daemon threads.",
                    "Monitor protocols are easy to get wrong; utilities such as latches and queues reduce that risk.",
                    question_id="chapter_11_m3_q2",
                ),
                q(
                    "What should thread-safety documentation tell clients?",
                    "Whether the class is thread-safe, conditionally thread-safe, immutable, or externally synchronized, and what lock or rule governs use.",
                    "Only whether the class uses `synchronized` internally.",
                    "Only whether the class has a `main` method.",
                    "Nothing, because thread safety should be obvious from the code.",
                    "The thread-safety contract belongs in the API docs, not in guesswork.",
                    question_id="chapter_11_m3_q3",
                ),
                q(
                    "When is lazy initialization usually justified?",
                    "When construction is expensive or may never be needed, and the lazy path can be implemented safely.",
                    "Whenever a field is private.",
                    "Whenever you want to avoid writing a constructor.",
                    "Whenever the class is public.",
                    "Lazy init is a tradeoff, not a default. Simpler eager initialization is often the better design.",
                    question_id="chapter_11_m3_q4",
                ),
            ],
        ),
    ],
}
