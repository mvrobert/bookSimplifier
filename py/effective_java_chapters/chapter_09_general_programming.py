from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Chapter 9: General Programming",
    "subtitle": "Effective Java, pages 282-313. Items 57-68: local scope, for-each, libraries, exact arithmetic, primitives vs boxed primitives, strings, concatenation, interfaces, reflection, native methods, optimization, and naming.",
    "modules": [
        module(
            "Local Scope and for-each",
            [
                (
                    "Declare local variables at the point of first use",
                    slide(
                        [
                            "The default rule is narrow scope: declare a local variable only when you have enough information to initialize it sensibly.",
                            "Premature declarations create visual clutter and keep names visible longer than necessary, which increases the chance of accidental reuse.",
                            "A try block is the main exception: if initialization can throw a checked exception, declare the variable before the try only when later use requires it.",
                        ],
                        image="../../page_previews/page_0282.png",
                        caption="Item 57 starts with scope minimization and the try-block exception, pages 282-283.",
                        source_pages=(282, 283),
                    ),
                ),
                (
                    "Prefer for-each unless you need explicit iteration control",
                    slide(
                        [
                            "The enhanced for statement removes iterator and index clutter for collections and arrays.",
                            "It has no performance penalty over the hand-written loop, and it makes nested iteration much less error-prone.",
                            "Use the traditional for loop only when you need destructive filtering, element replacement, or parallel traversal.",
                        ],
                        image="../../page_previews/page_0285.png",
                        caption="Item 58 explains why for-each is the normal choice, pages 285-287.",
                        source_pages=(285, 287),
                    ),
                ),
                (
                    "Keep loops and methods small so scope stays obvious",
                    slide(
                        [
                            "A for loop limits the lifetime of the loop variable to the loop body, which blocks copy-and-paste mistakes that are easy in while loops.",
                            "If a loop test depends on an invariant result, cache it in a second loop variable with the correct scope instead of recomputing it every iteration.",
                            "If a method has multiple unrelated phases, split it; local variables should not remain in scope just because the method is long.",
                        ],
                        image="../../page_previews/page_0284.png",
                        caption="Item 57's bug example and loop-scope techniques, pages 283-284.",
                        source_pages=(283, 284),
                    ),
                ),
            ],
            [
                q(
                    "What is the primary benefit of declaring a local variable at first use?",
                    "It minimizes scope and reduces clutter and accidental misuse.",
                    "It avoids the need for an initializer.",
                    "It makes the variable visible to later methods.",
                    "It guarantees the variable is final.",
                    "Narrow scope improves readability and reduces the chance that a variable is observed outside its intended region.",
                    question_id="chapter_09_m1_q1",
                ),
                q(
                    "When is a traditional for loop justified over for-each?",
                    "When you need the iterator, index, removal, replacement, or parallel traversal control.",
                    "Whenever the container is a collection rather than an array.",
                    "Whenever performance matters.",
                    "Whenever the body contains more than one statement.",
                    "For-each is the default; explicit control is for the few cases where the iterator or index is semantically required.",
                    question_id="chapter_09_m1_q2",
                ),
                q(
                    "Why are while loops more error-prone for simple iteration?",
                    "They leave the loop variable in scope longer and make copy-and-paste mistakes harder to catch.",
                    "They are slower than for loops.",
                    "They cannot iterate over arrays.",
                    "They require recursion behind the scenes.",
                    "The book's concern is scope and clarity, not raw execution speed.",
                    question_id="chapter_09_m1_q3",
                ),
                q(
                    "Why does the enhanced for statement not hurt performance?",
                    "The generated code is essentially identical to the hand-written iterator or index loop.",
                    "It uses a specialized JVM instruction.",
                    "It caches all elements automatically.",
                    "It disables bounds checks entirely.",
                    "The gain is readability and safety, not a special runtime optimization.",
                    question_id="chapter_09_m1_q4",
                ),
                q(
                    "When should you implement `Iterable` on a custom element group?",
                    "Whenever you want clients to use the for-each loop naturally.",
                    "Only when the type also implements `Collection`.",
                    "Only when the elements are primitive values.",
                    "Only when the type is immutable.",
                    "Any type that represents a group of elements should be iterable if possible.",
                    question_id="chapter_09_m1_q5",
                ),
            ],
        ),
        module(
            "Libraries and Exact Arithmetic",
            [
                (
                    "Use the standard libraries before writing ad hoc code",
                    slide(
                        [
                            "The library version is usually correct, battle-tested, and cheaper to maintain than a home-grown copy.",
                            "For random numbers, use the current library facility rather than `Math.abs(rnd.nextInt()) % n`, which is biased and can fail catastrophically.",
                            "Know the core packages well: `java.lang`, `java.util`, `java.io`, the collections framework, streams, and the concurrency utilities.",
                        ],
                        image="../../page_previews/page_0288.png",
                        caption="Item 59 argues for the standard libraries and current random-number APIs, pages 288-289.",
                        source_pages=(288, 289),
                    ),
                ),
                (
                    "Library code improves over time; so does your leverage",
                    slide(
                        [
                            "Standard libraries tend to gain functionality and performance across releases with no code change on your side.",
                            "If the platform library does not fit, try a high-quality third-party library before writing your own implementation.",
                            "The point is not dependency avoidance; it is not duplicating infrastructure that the ecosystem already maintains better than you will.",
                        ],
                        image="../../page_previews/page_0290.png",
                        caption="Item 59's practical advice: use common library types and naming carefully, pages 289-290.",
                        source_pages=(289, 290),
                    ),
                ),
                (
                    "Use exact arithmetic when the answer must be exact",
                    slide(
                        [
                            "`float` and `double` are binary floating-point types; they are for approximation, not exact decimal accounting.",
                            "For money and other exact decimal quantities, use `BigDecimal` when you need decimal-point tracking and controlled rounding.",
                            "If the scale is bounded and performance matters, use `int` or `long` and track the unit explicitly, such as cents instead of dollars.",
                        ],
                        image="../../page_previews/page_0291.png",
                        caption="Item 60 shows why floating-point is wrong for exact decimal answers, pages 291-293.",
                        source_pages=(291, 293),
                    ),
                ),
            ],
            [
                q(
                    "Why is `Math.abs(rnd.nextInt()) % n` a bad way to generate a bounded random integer?",
                    "It is biased and can fail catastrophically on `Integer.MIN_VALUE`.",
                    "It is too slow for small `n`.",
                    "It always returns negative values.",
                    "It only works for prime `n`.",
                    "Item 59 explicitly calls out bias and the `Integer.MIN_VALUE` edge case.",
                    question_id="chapter_09_m2_q1",
                ),
                q(
                    "What is the preferred modern random generator for most uses?",
                    "`ThreadLocalRandom`.",
                    "`Random`.",
                    "`Math.random()`.",
                    "`SplittableRandom` only, in all cases.",
                    "The book says `ThreadLocalRandom` is the usual choice, with `SplittableRandom` for fork-join and parallel work.",
                    question_id="chapter_09_m2_q2",
                ),
                q(
                    "Why should you use `BigDecimal` for exact money calculations?",
                    "Binary floating-point cannot represent decimal fractions like `0.1` exactly.",
                    "Because `BigDecimal` is always faster than primitives.",
                    "Because `BigDecimal` automatically rounds to cents.",
                    "Because `double` is always imprecise for all numbers.",
                    "The issue is exact decimal representation and controlled rounding, not general numeric validity.",
                    question_id="chapter_09_m2_q3",
                ),
                q(
                    "When is `int` or `long` a reasonable alternative to `BigDecimal`?",
                    "When the quantity can be represented as a scaled integer within the range you need.",
                    "Whenever exact answers are not required.",
                    "Only for scientific calculations.",
                    "Never; primitives are always unsafe.",
                    "Scaled integers are a deliberate exact-arithmetic strategy when the magnitude is bounded.",
                    question_id="chapter_09_m2_q4",
                ),
                q(
                    "What should you do if a standard library almost solves the problem but misses a feature?",
                    "Check for a high-quality third-party library before implementing it yourself.",
                    "Rewrite the entire standard library function.",
                    "Use reflection to patch the library class.",
                    "Ignore the gap and duplicate the missing piece in every project.",
                    "The book's order is: platform library, then third-party library, then custom code.",
                    question_id="chapter_09_m2_q5",
                ),
            ],
        ),
        module(
            "Primitives, Strings, and Interfaces",
            [
                (
                    "Prefer primitives unless you need reference semantics",
                    slide(
                        [
                            "Boxed primitives add identity, null, and allocation overhead; primitives have only values and are simpler and faster.",
                            "Mixed primitive/boxed operations auto-unbox, so `null` can trigger a `NullPointerException` in places that look harmless.",
                            "Use boxed primitives only where the language requires a reference type, such as collections, type parameters, or reflective APIs.",
                        ],
                        image="../../page_previews/page_0294.png",
                        caption="Item 61's boxed-primitive pitfalls: identity, null, and performance, pages 294-296.",
                        source_pages=(294, 296),
                    ),
                ),
                (
                    "Use strings for text, not for structure or capability",
                    slide(
                        [
                            "If the data is numeric, boolean, enum-like, or composite, represent it as that type instead of forcing it through a string.",
                            "Strings are a poor capability mechanism because they are forgeable and often share a global namespace.",
                            "A typesafe redesign usually moves the type parameter into the API itself, as with `ThreadLocal<T>`.",
                        ],
                        image="../../page_previews/page_0297.png",
                        caption="Item 62 replaces stringly typed APIs with proper types and capabilities, pages 297-299.",
                        source_pages=(297, 299),
                    ),
                ),
                (
                    "Repeated string concatenation is quadratic",
                    slide(
                        [
                            "The `+` operator is fine for a few strings, but repeated concatenation copies intermediate results and scales poorly.",
                            "Use `StringBuilder` for loops or any nontrivial accumulation; pre-size it when you can estimate the final length.",
                            "The rule is about asymptotic behavior, not stylistic preference.",
                        ],
                        image="../../page_previews/page_0300.png",
                        caption="Item 63 shows why `StringBuilder` beats repeated `+`, page 300.",
                        source_pages=(300, 300),
                    ),
                ),
                (
                    "Refer to objects by interfaces, not concrete classes",
                    slide(
                        [
                            "Use the least specific type that still exposes the operations you need, usually an interface.",
                            "This keeps implementations swappable and prevents client code from depending on incidental methods or iteration order.",
                            "Refer to a class directly only when no appropriate interface exists or when the class-specific behavior is required.",
                        ],
                        image="../../page_previews/page_0301.png",
                        caption="Item 64 keeps variables, fields, parameters, and returns interface-based when possible, pages 301-302.",
                        source_pages=(301, 302),
                    ),
                ),
            ],
            [
                q(
                    "Why is `Long sum = 0L` a problem in a tight accumulation loop?",
                    "It forces repeated boxing and unboxing and can be much slower than `long`.",
                    "It makes the sum exact when `long` would not.",
                    "It prevents the loop from compiling.",
                    "It disables integer overflow.",
                    "The issue is unnecessary object creation and auto-unboxing overhead.",
                    question_id="chapter_09_m3_q1",
                ),
                q(
                    "When is a boxed primitive appropriate?",
                    "In collections, type parameters, and other places where a reference type is required.",
                    "Whenever the value might be `null`.",
                    "Whenever a method has more than one parameter.",
                    "Whenever you want better performance.",
                    "Boxed primitives are sometimes necessary, but only because the type system requires references there.",
                    question_id="chapter_09_m3_q2",
                ),
                q(
                    "Why are strings a poor substitute for aggregate types?",
                    "They hide structure, require parsing, and cannot express invariants directly.",
                    "They cannot be compared for equality.",
                    "They are always slower than arrays.",
                    "They are mutable by default.",
                    "A dedicated type can expose the fields and contracts explicitly instead of encoding them in delimiters.",
                    question_id="chapter_09_m3_q3",
                ),
                q(
                    "What is the main reason to prefer an interface type for a variable or field?",
                    "It keeps the implementation swappable without changing client code.",
                    "It makes the code shorter.",
                    "It guarantees iteration order.",
                    "It forces the use of factory methods.",
                    "The point is decoupling from a concrete implementation choice.",
                    question_id="chapter_09_m3_q4",
                ),
                q(
                    "When is it acceptable to refer to an object by its concrete class?",
                    "When no suitable interface exists or when class-specific behavior is required.",
                    "Whenever the class is public.",
                    "Whenever you want better compile times.",
                    "Whenever the class is final.",
                    "The concrete class is appropriate only when the interface abstraction would be lossy or unavailable.",
                    question_id="chapter_09_m3_q5",
                ),
            ],
        ),
        module(
            "Reflection, Native Code, Optimization, and Naming",
            [
                (
                    "Treat reflection as a controlled escape hatch",
                    slide(
                        [
                            "Reflection discards compile-time type checking, produces verbose code, and is slower than ordinary invocation.",
                            "If you need to load a class unknown at compile time, reflect only to instantiate it and then use a known interface or superclass normally.",
                            "The technique is powerful, but the cost belongs in the smallest possible boundary layer.",
                        ],
                        image="../../page_previews/page_0303.png",
                        caption="Item 65 recommends reflection only at the boundary and normally through an interface, pages 303-305.",
                        source_pages=(303, 305),
                    ),
                ),
                (
                    "Use native methods only when the tradeoff is real",
                    slide(
                        [
                            "JNI can access platform-specific facilities or legacy native libraries, but it increases portability, debugging difficulty, and memory-management risk.",
                            "Use native code sparingly, and assume Java is fast enough until you have evidence otherwise.",
                            "If you must cross the boundary, keep the native surface area small and test it aggressively.",
                        ],
                        image="../../page_previews/page_0306.png",
                        caption="Item 66 explains the legitimate uses and risks of JNI, page 306.",
                        source_pages=(306, 306),
                    ),
                ),
                (
                    "Optimize only after measurement, and start at the algorithm level",
                    slide(
                        [
                            "Do not warp an API for speculative performance gains; design well first, then measure.",
                            "Use a profiler or `jmh` to find where time is really going, and fix algorithmic mistakes before micro-optimizing code paths.",
                            "Optimization must be iterative and evidence-driven because Java performance varies across VMs, releases, and hardware.",
                        ],
                        image="../../page_previews/page_0307.png",
                        caption="Item 67 ties optimization to profiling, measurement, and algorithm choice, pages 307-309.",
                        source_pages=(307, 309),
                    ),
                ),
                (
                    "Follow the platform's naming conventions",
                    slide(
                        [
                            "Package names are lowercase and hierarchical; class and interface names are PascalCase; methods and fields use lowerCamelCase.",
                            "Constant fields are the exception: use uppercase words separated by underscores, and reserve underscores for that purpose.",
                            "Type variables are short and conventional: `T`, `E`, `K`, `V`, `X`, `R`, and friends. The conventions are conventions, but they matter.",
                        ],
                        image="../../page_previews/page_0310.png",
                        caption="Item 68 summarizes typographical and grammatical naming rules, pages 310-313.",
                        source_pages=(310, 313),
                    ),
                ),
            ],
            [
                q(
                    "What is the main technical downside of reflection?",
                    "It bypasses compile-time type checking and is slower and more verbose than normal calls.",
                    "It cannot construct objects.",
                    "It only works for private members.",
                    "It makes code immutable.",
                    "Reflection is useful, but it shifts correctness checks from compile time to runtime.",
                    question_id="chapter_09_m4_q1",
                ),
                q(
                    "What is the preferred way to use a class found reflectively?",
                    "Instantiate it reflectively, then interact with it through a known interface or superclass.",
                    "Invoke all methods reflectively forever.",
                    "Cast it to `Object` and inspect fields manually.",
                    "Avoid constructors and use native code instead.",
                    "This keeps the reflective cost at the boundary and the rest of the code normal.",
                    question_id="chapter_09_m4_q2",
                ),
                q(
                    "When are native methods justified?",
                    "For platform-specific facilities or truly necessary native libraries, not as a default performance trick.",
                    "Whenever Java code allocates objects.",
                    "Whenever reflection feels verbose.",
                    "Only in test code.",
                    "Native code is a narrow interoperability tool, not a general optimization strategy.",
                    question_id="chapter_09_m4_q3",
                ),
                q(
                    "What is the correct first step in optimization?",
                    "Measure with a profiler or `jmh` and identify the real hot spots.",
                    "Replace all strings with `StringBuilder`.",
                    "Inline every method.",
                    "Convert everything to native code.",
                    "The book is explicit: don't guess, measure, then fix the right problem.",
                    question_id="chapter_09_m4_q4",
                ),
                q(
                    "Which naming rule is most conventional for a constant field?",
                    "Uppercase words separated by underscores.",
                    "lowerCamelCase.",
                    "PascalCase.",
                    "A single lowercase word.",
                    "Constant fields are the standard exception to the normal member-name casing rules.",
                    question_id="chapter_09_m4_q5",
                ),
            ],
        ),
    ],
}
