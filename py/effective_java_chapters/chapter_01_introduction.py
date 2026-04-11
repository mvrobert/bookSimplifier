from effective_java_common import module, q, slide


MODULE_1 = module(
    "Purpose and audience",
    [
        (
            "Why this book exists",
            slide(
                [
                    "Effective Java is a rules book for Java developers who already know the language and want to write better code with less ambiguity.",
                    "Its core scope is the standard platform libraries the author expects you to use in practice: `java.lang`, `java.util`, `java.io`, plus subpackages such as `java.util.concurrent` and `java.util.function`.",
                    "The book is intentionally practical, not theoretical: it focuses on reusable rules that improve design and implementation quality.",
                ],
                image="../../page_previews/page_0022.png",
                caption="Chapter 1, page 22: the book states its purpose and library scope explicitly.",
                source_pages=(22, 22),
            ),
        ),
        (
            "Who it is for",
            slide(
                [
                    "This is not an introductory Java text.",
                    "The target reader is already comfortable with Java syntax, libraries, and everyday programming, and wants guidance that is still useful for advanced work.",
                    "The book is designed to remain readable for experienced developers, but it assumes you can follow code examples without hand-holding.",
                ],
                box=(
                    "note",
                    "<strong>Pedantic reading:</strong> treat the book as a design manual for practicing Java developers, not as a language primer.",
                ),
                source_pages=(22, 22),
            ),
        ),
        (
            "Rule-based structure",
            slide(
                [
                    "The book contains ninety items, and each item expresses one rule.",
                    "The items are grouped into eleven chapters by broad design concern, but the intended reading path is non-linear.",
                    "Each item stands on its own, and the cross references are there so you can navigate by topic instead of reading cover to cover.",
                ],
                image="../../page_previews/page_0023.png",
                caption="Chapter 1, page 23: the book is organized around independent items, not a linear narrative.",
                source_pages=(23, 23),
            ),
        ),
    ],
    [
        q(
            "What audience does the book target?",
            "Java developers who already know the language and want practical guidance for better design",
            "Absolute beginners learning their first programming language",
            "Only library authors working on the JDK itself",
            "Only engineers writing concurrency-heavy systems",
            "The introduction says the book is not for beginners and assumes working knowledge of Java.",
            question_id="intro_m1_q1",
        ),
        q(
            "How is the book structured?",
            "Ninety independent items grouped into eleven chapters",
            "Twelve chapters, each split into exactly eight items",
            "A single continuous tutorial meant to be read in order",
            "One chapter per Java release",
            "The text explicitly says the book consists of ninety items loosely grouped into eleven chapters.",
            question_id="intro_m1_q2",
        ),
        q(
            "What is the recommended reading model?",
            "Read items selectively and follow cross references as needed",
            "Read strictly from the first page to the last page",
            "Skip all code examples and focus on prose only",
            "Treat the items as exhaustive formal proofs",
            "The introduction says each item stands on its own and the cross references help you plot your own course.",
            question_id="intro_m1_q3",
        ),
        q(
            "What kind of examples does the book emphasize?",
            "Code examples, including patterns and idioms that can be adapted directly",
            "Only mathematical proofs of correctness",
            "Only UML diagrams with no Java code",
            "Only contrived toy examples with no production relevance",
            "The book says it is heavily illustrated with code examples and design patterns/idioms.",
            question_id="intro_m1_q4",
        ),
    ],
)


MODULE_2 = module(
    "Edition updates and release map",
    [
        (
            "New platform features in the third edition",
            slide(
                [
                    "The edition reflects platform features added after the previous edition, especially Java 7, Java 8, and Java 9 features.",
                    "The introduction names several features by item and release so readers can find the primary coverage quickly.",
                    "Lambdas, streams, optionals, default methods, try-with-resources, `@SafeVarargs`, and modules are all explicitly mapped.",
                ],
                image="../../page_previews/page_0023.png",
                caption="Chapter 1, page 23: the book maps major language and platform features to the relevant items.",
                source_pages=(23, 23),
            ),
        ),
        (
            "Release names are normalized",
            slide(
                [
                    "When referring to platform versions, the book prefers nicknames over official release names for readability.",
                    "That choice is editorial, not technical: the goal is to reduce friction when the same release is referenced repeatedly across items.",
                    "The book includes a mapping from official JDK and Java SE names to the nicknames used throughout the text.",
                ],
                image="../../page_previews/page_0024.png",
                caption="Chapter 1, page 24: release names are normalized to short nicknames for the rest of the book.",
                source_pages=(24, 24),
            ),
        ),
        (
            "Technical vocabulary",
            slide(
                [
                    "The book aligns mostly with the Java Language Specification, but it also defines some terms in a more practical way.",
                    "It distinguishes reference types, primitive values, objects, class members, and method signatures with precise meanings.",
                    "It uses `package-private` rather than the formal but less common `package access`, and it treats inheritance as subclassing when talking about classes.",
                ],
                box=(
                    "note",
                    "<strong>Implementation detail:</strong> the terminology is intentionally consistent with how Java developers discuss APIs in practice, not just with the JLS phrasing.",
                ),
                source_pages=(24, 24),
            ),
        ),
    ],
    [
        q(
            "Why does the book prefer release nicknames?",
            "To make repeated version references easier to read",
            "To avoid discussing any Java versions by number",
            "To hide the fact that the book covers Java 8 and Java 9 features",
            "To replace all technical terminology with informal language",
            "The introduction says nicknames are used in preference to official names for convenience.",
            question_id="intro_m2_q1",
        ),
        q(
            "Which feature is explicitly associated with Java 9?",
            "Modules",
            "Streams",
            "Lambdas",
            "try-with-resources",
            "The release table maps modules to Java 9.",
            question_id="intro_m2_q2",
        ),
        q(
            "What is the book's stance on terminology?",
            "Mostly JLS-aligned, with a few pragmatic terms used consistently throughout",
            "It invents a new vocabulary unrelated to the JLS",
            "It avoids all formal terminology",
            "It uses only vendor-specific terms from one IDE",
            "The introduction says most terms follow the JLS, but some are adjusted for clarity and convention.",
            question_id="intro_m2_q3",
        ),
        q(
            "What does the book mean by an API?",
            "The exported classes, interfaces, constructors, members, and serialized forms a programmer uses",
            "Any internal helper method in a class",
            "Only public static methods",
            "Only a package's source files",
            "The introduction defines exported API and API elements explicitly.",
            question_id="intro_m2_q4",
        ),
    ],
)


MODULE_3 = module(
    "How to read the rules",
    [
        (
            "Examples and antipatterns",
            slide(
                [
                    "Most items include program examples, and the examples are intentionally realistic enough to show design tradeoffs rather than toy syntax.",
                    "When a bad pattern is shown, it is clearly labeled as something to avoid and is followed by an alternative approach.",
                    "The book also references established design literature when an example benefits from prior art.",
                ],
                image="../../page_previews/page_0024.png",
                caption="Chapter 1, page 24: bad examples are labeled so the item can explain the failure mode and the replacement.",
                source_pages=(24, 24),
            ),
        ),
        (
            "Principles behind the rules",
            slide(
                [
                    "The rules are grounded in a small set of design principles: clarity, simplicity, minimal surprise, small components, code reuse, low coupling, and early error detection.",
                    "Those principles are descriptive of the book's method, not optional motivational language.",
                    "A component here can be anything reusable from a single method to a large framework spanning multiple packages.",
                ],
                image="../../page_previews/page_0025.png",
                caption="Chapter 1, page 25: the introduction states the design principles that justify the rules that follow.",
                source_pages=(25, 25),
            ),
        ),
        (
            "Performance in context",
            slide(
                [
                    "Performance is not the primary subject of the book.",
                    "The priority is clear, correct, usable, robust, flexible, and maintainable code; performance should usually be addressed after those qualities are in place.",
                    "Where performance numbers appear, they are explicitly framed as approximate and machine-specific, not as universal constants.",
                ],
                box=(
                    "note",
                    "<strong>Reading rule:</strong> treat every optimization claim as conditional unless the item explicitly proves otherwise.",
                ),
                source_pages=(25, 25),
            ),
        ),
    ],
    [
        q(
            "What is the main purpose of the examples in the book?",
            "To illustrate design patterns, idioms, and mistakes with concrete Java code",
            "To provide complete production-ready source files for reuse",
            "To avoid any discussion of implementation details",
            "To compare Java against unrelated languages",
            "The introduction says the book is heavily illustrated with code examples and anti-examples.",
            question_id="intro_m3_q1",
        ),
        q(
            "What is the book's position on performance?",
            "It is secondary to clarity, correctness, usability, robustness, flexibility, and maintainability",
            "It is the only concern that matters",
            "It is ignored entirely",
            "It replaces all other design goals",
            "The introduction says the book is mostly not about performance.",
            question_id="intro_m3_q2",
        ),
        q(
            "How should the rules be applied?",
            "Generally, but not slavishly; violate them only occasionally and with good reason",
            "Always, even when the rule conflicts with the problem",
            "Never, because they are only historical notes",
            "Only after consulting external style guides",
            "The introduction explicitly warns that the rules are best practices, not absolute laws.",
            question_id="intro_m3_q3",
        ),
        q(
            "What is the book's definition of a component?",
            "Any reusable software element, from a method to a multi-package framework",
            "Only a Maven artifact",
            "Only a class file",
            "Only a user interface widget",
            "The introduction defines component broadly so the same rules can apply at different levels of reuse.",
            question_id="intro_m3_q4",
        ),
    ],
)


CHAPTER = {
    "title": "Introduction",
    "subtitle": "Purpose, scope, notation, and reading strategy for Effective Java",
    "modules": [MODULE_1, MODULE_2, MODULE_3],
}
