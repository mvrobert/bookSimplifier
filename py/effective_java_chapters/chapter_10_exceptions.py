from __future__ import annotations

from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Exceptions",
    "subtitle": "Effective Java, Chapter 10: pages 314-331, Items 69-77",
    "modules": [
        module(
            "Exceptional conditions and throwable choice",
            [
                (
                    "Item 69: exceptions are for exceptional conditions",
                    slide(
                        [
                            "Do not use exceptions as an alternative loop construct or as a substitute for ordinary control flow.",
                            "The canonical test is semantic, not syntactic: if the caller is expected to hit the condition routinely, the condition is not exceptional.",
                            "For iteration and other state-sensitive APIs, prefer an explicit state-test method, an optional result, or a distinguished return value.",
                        ],
                        image="../../page_previews/page_0314.png",
                        caption="Item 69 rejects exception-based loops and prefers explicit state testing, pages 314-316.",
                        points=[
                            "Exception-driven iteration is misleading and usually slower.",
                            "A state-testing method is only safe when the object cannot change between the test and the action.",
                            "Optional results and distinguished values are better when concurrency or duplicate work makes testing unsafe.",
                        ],
                        source_pages=(314, 316),
                    ),
                ),
                (
                    "Item 70: checked versus unchecked is a recovery question",
                    slide(
                        [
                            "Use checked exceptions only when the caller can reasonably recover and the API should force recovery handling.",
                            "Use runtime exceptions for programming errors and precondition violations; use errors for VM-level conditions, not for application design.",
                            "If recovery is plausible, the exception should expose information that helps the caller recover rather than force string parsing.",
                        ],
                        image="../../page_previews/page_0317.png",
                        caption="Item 70 separates recoverable conditions from programming errors, pages 317-318.",
                        points=[
                            "Do not define new `Error` subclasses.",
                            "Do not define throwables outside `Exception`, `RuntimeException`, or `Error`.",
                            "Checked exceptions should provide accessors for recovery-relevant data when possible.",
                        ],
                        source_pages=(317, 318),
                    ),
                ),
                (
                    "Throwable design must preserve API clarity",
                    slide(
                        [
                            "When the right classification is unclear, default to unchecked unless a caller can clearly take corrective action.",
                            "Never hide recoverability behind a vague string; expose structured data with typed accessors.",
                            "Exception objects are full-fledged objects, so they should carry machine-readable information, not just prose.",
                        ],
                        image="../../page_previews/page_0318.png",
                        caption="Item 70 emphasizes typed recovery information and disciplined throwable design, page 318.",
                        source_pages=(318, 318),
                    ),
                ),
            ],
            [
                q(
                    "Why should exceptions not be used for ordinary loop control?",
                    "Because the condition is expected and should be expressed directly",
                    "Because exceptions cannot be caught inside loops",
                    "Because loop control requires checked exceptions",
                    "Because iteration with exceptions is always faster",
                    "An ordinary loop should spell out its termination condition; exceptions are for genuinely unusual failure.",
                    question_id="chapter10_m1_q1",
                ),
                q(
                    "When is a checked exception justified?",
                    "When the caller can reasonably recover and should be forced to handle the condition",
                    "Whenever the method is public",
                    "Whenever the code is performance-critical",
                    "Whenever a return value would be inconvenient",
                    "The checked/unchecked choice is about recoverability and caller burden, not style.",
                    question_id="chapter10_m1_q2",
                ),
                q(
                    "What should you throw for a programming error such as an invalid argument or illegal state?",
                    "A runtime exception appropriate to the violation",
                    "A checked exception so callers must catch it",
                    "An Error subclass",
                    "A Throwable subclass unrelated to Exception",
                    "Runtime exceptions model contract violations; checked exceptions model recoverable conditions.",
                    question_id="chapter10_m1_q3",
                ),
                q(
                    "What is wrong with defining a new Error subclass for application failure?",
                    "Errors are reserved for unrecoverable VM-level conditions and should not be part of normal API design",
                    "Errors cannot carry detail messages",
                    "Errors are always checked",
                    "Errors cannot be thrown from Java code",
                    "Application code should not invent new errors; it should use runtime exceptions or checked exceptions as appropriate.",
                    question_id="chapter10_m1_q4",
                ),
                q(
                    "What should a checked exception provide if recovery is expected?",
                    "Typed accessors that expose the data needed to recover",
                    "Only a stack trace",
                    "A localized user message",
                    "A private constructor",
                    "Callers should not need to parse exception text to recover from a known failure mode.",
                    question_id="chapter10_m1_q5",
                ),
            ],
        ),
        module(
            "Checked exceptions, standard exceptions, and abstraction",
            [
                (
                    "Item 71: avoid unnecessary checked exceptions",
                    slide(
                        [
                            "Checked exceptions are valuable when they improve reliability, but they make APIs harder to use because every caller must handle or declare them.",
                            "The burden is especially high when a method throws only one checked exception and therefore cannot be used directly in stream pipelines.",
                            "If callers cannot do anything useful at the call site, the checked exception is probably a design mistake.",
                        ],
                        image="../../page_previews/page_0319.png",
                        caption="Item 71 warns that checked exceptions create real caller burden, pages 319-320.",
                        points=[
                            "Prefer `Optional` when the failure is representable as absence.",
                            "Prefer an unchecked exception if callers cannot improve the outcome.",
                            "A separate state-test method is sometimes a cleaner API than a checked exception.",
                        ],
                        source_pages=(319, 320),
                    ),
                ),
                (
                    "Item 72: reuse standard exceptions first",
                    slide(
                        [
                            "Prefer the standard exceptions that already encode the right semantics: they are familiar, compact, and easier to read than custom types.",
                            "The choice should be based on documented meaning, not on class names alone.",
                            "Treat `Exception`, `RuntimeException`, `Throwable`, and `Error` as if they were abstract; do not throw them directly as catch-all placeholders.",
                        ],
                        image="../../page_previews/page_0321.png",
                        caption="Item 72 maps common failure modes to standard exception classes, pages 321-322.",
                        points=[
                            "`IllegalArgumentException` for bad argument values.",
                            "`IllegalStateException` for illegal object state.",
                            "`NullPointerException` and `IndexOutOfBoundsException` for the conventional null and index cases.",
                        ],
                        source_pages=(321, 322),
                    ),
                ),
                (
                    "Item 73: translate exceptions to match the abstraction",
                    slide(
                        [
                            "If a lower-level exception leaks through a higher-level API, the abstraction boundary is broken and the implementation detail becomes part of the contract.",
                            "Catch low-level exceptions and translate them into exceptions that make sense in terms of the higher-level abstraction.",
                            "When the original cause is useful for debugging, chain it rather than discard it.",
                        ],
                        image="../../page_previews/page_0323.png",
                        caption="Item 73 uses exception translation and chaining to preserve abstraction and cause, pages 323-324.",
                        code=(
                            "try {\n"
                            "    return i.next();\n"
                            "} catch (NoSuchElementException cause) {\n"
                            "    throw new IndexOutOfBoundsException(\"Index: \" + index);\n"
                            "}"
                        ),
                        source_pages=(323, 324),
                    ),
                ),
            ],
            [
                q(
                    "Why can a checked exception make an API unpleasant to use?",
                    "Because every caller must catch it or declare it, even when recovery is awkward",
                    "Because checked exceptions are always slower at runtime",
                    "Because checked exceptions cannot be documented",
                    "Because they cannot be translated",
                    "A checked exception is a deliberate API burden, so it should be reserved for useful recovery scenarios.",
                    question_id="chapter10_m2_q1",
                ),
                q(
                    "When should `Optional` be preferred over a checked exception?",
                    "When the failure can be represented as absence and no extra failure data is needed",
                    "When the caller needs a stack trace",
                    "When the method is private",
                    "When the exception is recoverable",
                    "Optional is a cleaner replacement when the failure mode is simply “no result.”",
                    question_id="chapter10_m2_q2",
                ),
                q(
                    "Which exception best matches an illegal argument value?",
                    "`IllegalArgumentException`",
                    "`IllegalStateException`",
                    "`ConcurrentModificationException`",
                    "`UnsupportedOperationException`",
                    "Bad parameter values should map to `IllegalArgumentException` unless a more specific standard exception applies.",
                    question_id="chapter10_m2_q3",
                ),
                q(
                    "What is the purpose of exception translation?",
                    "To convert a low-level failure into an exception that matches the higher-level abstraction",
                    "To hide all failures from callers",
                    "To avoid using stack traces",
                    "To force all exceptions to become checked",
                    "Translation keeps implementation details out of the public contract while preserving useful diagnostics.",
                    question_id="chapter10_m2_q4",
                ),
                q(
                    "Why is chaining useful in translated exceptions?",
                    "It preserves the original cause and its stack trace for debugging",
                    "It eliminates the need for documentation",
                    "It makes the exception unchecked",
                    "It guarantees recovery",
                    "Chaining gives you the higher-level exception the API needs plus the lower-level cause you may need later.",
                    question_id="chapter10_m2_q5",
                ),
            ],
        ),
        module(
            "Documentation, diagnostics, and failure atomicity",
            [
                (
                    "Item 74: document all thrown exceptions",
                    slide(
                        [
                            "Public APIs must document both checked and unchecked exceptions; the former with `throws` and `@throws`, the latter with `@throws` only.",
                            "Documenting unchecked exceptions is not optional trivia: it is how you communicate preconditions and expected failure modes.",
                            "Interface documentation matters especially because it becomes part of the contract shared by all implementations.",
                        ],
                        image="../../page_previews/page_0325.png",
                        caption="Item 74 treats exception documentation as part of the API contract, pages 325-326.",
                        points=[
                            "Do not hide behind `Exception` or `Throwable` in declarations.",
                            "Document preconditions through the exceptions they imply.",
                            "Use `@throws` even when the exception is unchecked.",
                        ],
                        source_pages=(325, 326),
                    ),
                ),
                (
                    "Item 75: detail messages should capture failure data",
                    slide(
                        [
                            "The detail message is for debugging, not for end users, so it should maximize diagnostic value and minimize fluff.",
                            "Include the parameter and field values that explain the failure, especially when the message will be the only evidence in a production stack trace.",
                            "Do not leak secrets or other sensitive data into exception messages that may be widely visible.",
                        ],
                        image="../../page_previews/page_0327.png",
                        caption="Item 75 says the message should capture the failure, not narrate it, pages 327-328.",
                        points=[
                            "For bounds failures, record the lower bound, upper bound, and failing index.",
                            "Prefer structured data in the exception object when the caller may need it.",
                            "Keep prose short; the stack trace and source code already provide context.",
                        ],
                        source_pages=(327, 328),
                    ),
                ),
                (
                    "Item 76: strive for failure atomicity",
                    slide(
                        [
                            "A failed method should leave the object in the same state it had before the call whenever practical.",
                            "Immutable objects get failure atomicity for free; mutable objects usually need prevalidation or careful ordering of state changes.",
                            "If an operation can fail in the middle, consider performing it on a temporary copy and committing only after success.",
                        ],
                        image="../../page_previews/page_0329.png",
                        caption="Item 76 explains how to preserve object state when operations fail, pages 329-330.",
                        points=[
                            "Validate before mutating when you can.",
                            "Order work so that likely failures happen before state changes.",
                            "Document any residual inconsistent state if atomicity cannot be provided.",
                        ],
                        source_pages=(329, 330),
                    ),
                ),
                (
                    "Item 77: never silently ignore exceptions",
                    slide(
                        [
                            "An empty catch block is usually a defect, not a simplification.",
                            "If ignoring an exception is truly correct, the catch block should explain why and the variable should be named `ignored`.",
                            "Logging is often better than silence because it preserves evidence without forcing recovery when recovery is unnecessary.",
                        ],
                        image="../../page_previews/page_0331.png",
                        caption="Item 77 rejects empty catch blocks and requires an explicit justification when ignoring is acceptable, page 331.",
                        points=[
                            "The rule applies to checked and unchecked exceptions alike.",
                            "Swallowing an exception can defer failure to a unrelated location and time.",
                            "If the exception is ignorable, write that reason down in code.",
                        ],
                        source_pages=(331, 331),
                    ),
                ),
            ],
            [
                q(
                    "What is the best way to document a checked exception?",
                    "With a precise `throws` declaration and a Javadoc `@throws` description of when it occurs",
                    "Only in the class-level comment",
                    "Only by naming the exception type well",
                    "By omitting it so callers discover it from stack traces",
                    "The declaration and the Javadoc should tell clients exactly when the exception is expected.",
                    question_id="chapter10_m3_q1",
                ),
                q(
                    "What belongs in an exception detail message?",
                    "The values that explain the failure, such as offending indexes or bounds",
                    "A long prose narrative for end users",
                    "Sensitive secrets so support can diagnose faster",
                    "Only the exception class name",
                    "The detail message should capture the failure facts, not tell a story.",
                    question_id="chapter10_m3_q2",
                ),
                q(
                    "What is failure atomicity?",
                    "A failed operation leaves the object in the same usable state it had before the call",
                    "A method never throws exceptions",
                    "A method always rolls back the heap",
                    "A catch block always repairs every invariant automatically",
                    "Failure atomicity is about preserving object state when an operation aborts.",
                    question_id="chapter10_m3_q3",
                ),
                q(
                    "When is it acceptable to ignore an exception?",
                    "Only when the code comments explicitly explain why ignoring it is safe or expected",
                    "Whenever the exception is checked",
                    "Whenever the catch block is empty but short",
                    "Whenever the program is not in debug mode",
                    "Ignoring an exception without explanation is a silent failure mode.",
                    question_id="chapter10_m3_q4",
                ),
                q(
                    "Why can swallowing an exception make debugging harder?",
                    "It can defer the visible failure to a later location that no longer obviously relates to the root cause",
                    "It forces the VM to crash immediately",
                    "It always improves throughput",
                    "It prevents stack traces from being generated",
                    "An ignored exception removes the evidence that would otherwise point at the original fault.",
                    question_id="chapter10_m3_q5",
                ),
            ],
        ),
    ],
}
