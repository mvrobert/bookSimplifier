from __future__ import annotations

from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Chapter 7: Lambdas and Streams",
    "subtitle": "Effective Java, pages 214-247. Items 42-48: lambdas, method references, functional interfaces, streams, side-effect-free functions, return types, and parallel stream caution.",
    "modules": [
        module(
            "Lambdas, anonymous classes, and method references",
            [
                (
                    "Item 42: lambdas replace most anonymous function objects",
                    slide(
                        [
                            "Anonymous classes were the historical way to create function objects, but they are verbose and visually noisy.",
                            "A lambda is the right tool when you need a function object and you do not need a named class, a distinct identity, or extra state beyond the captured variables.",
                            "Prefer lambdas for single-abstract-method interfaces such as `Comparator`, `Runnable`, and the standard `java.util.function` types.",
                        ],
                        image="../../page_previews/page_0214.png",
                        caption="Chapter opener and Item 42: lambdas formalize function objects for functional interfaces, pages 214-215.",
                        points=[
                            "Use lambdas for behavior, not for representing a rich object with state and methods.",
                            "A lambda captures effectively final variables from the enclosing scope.",
                            "If you need `this` to name the enclosing instance, prefer an anonymous class or refactor the code.",
                        ],
                        source_pages=(214, 215),
                    ),
                ),
                (
                    "Lambda bodies should stay short and local",
                    slide(
                        [
                            "A lambda should usually fit on one screen and do one thing.",
                            "If the body grows complex, extract it to a properly named method and use a method reference or a simpler lambda at the call site.",
                            "Do not use lambdas to smuggle imperative control flow into APIs that are designed around functional callbacks.",
                        ],
                        image="../../page_previews/page_0215.png",
                        caption="Item 42: keep lambda bodies small enough to read as behavior, not mini-methods, page 215.",
                        code="""Collections.sort(words, (s1, s2) -> Integer.compare(s1.length(), s2.length()));""",
                        source_pages=(215, 217),
                    ),
                ),
                (
                    "Item 43: method references are a clearer shorthand when they fit",
                    slide(
                        [
                            "Method references are just another way to express a function object, but they remove boilerplate when the lambda would only forward arguments.",
                            "Use them when they are shorter and clearer than the equivalent lambda, not as an aesthetic default.",
                            "If the parameter names in the lambda convey useful meaning, keep the lambda; the names can be documentation.",
                        ],
                        image="../../page_previews/page_0218.png",
                        caption="Item 43: method references trim ceremony when the lambda is only forwarding arguments, pages 218-219.",
                        code="""map.merge(key, 1, Integer::sum);
service.execute(GoshThisClassNameIsHumongous::action);""",
                        source_pages=(218, 219),
                    ),
                ),
            ],
            [
                q(
                    "When is a lambda usually preferable to an anonymous class?",
                    "When you need a concise implementation of a functional interface and do not need a separate named type",
                    "When you need to override `equals` and `hashCode`",
                    "When you want the class to be reusable through inheritance",
                    "When the callback must access private members of any object",
                    "Lambdas are the preferred syntax for function objects; anonymous classes are still useful when you need a distinct class body.",
                    question_id="chapter7_m1_q1",
                ),
                q(
                    "What is the main reason to extract a long lambda into a method?",
                    "It improves readability by giving the behavior a real name and documentation site",
                    "It makes the code parallel by default",
                    "It guarantees allocation-free execution",
                    "It changes the lambda into a singleton",
                    "The book favors small lambdas; complex behavior should move into named methods.",
                    question_id="chapter7_m1_q2",
                ),
                q(
                    "What is the normal advantage of a method reference over the equivalent lambda?",
                    "It is usually shorter and clearer when the lambda only forwards to an existing method",
                    "It can express more behavior than a lambda",
                    "It avoids type inference",
                    "It works only for static methods",
                    "Method references are a shorthand, not a new capability.",
                    question_id="chapter7_m1_q3",
                ),
                q(
                    "Why is `Integer::sum` better than `(count, incr) -> count + incr` in some contexts?",
                    "It removes boilerplate without losing meaning",
                    "It is the only legal syntax for `merge`",
                    "It avoids boxing overhead entirely",
                    "It makes the lambda stateful",
                    "Use the method reference when the intent is obviously simple forwarding to a known method.",
                    question_id="chapter7_m1_q4",
                ),
                q(
                    "What should make you hesitate before replacing a lambda with a method reference?",
                    "The lambda parameter names carry useful semantic documentation",
                    "The target type is a functional interface",
                    "The method reference compiles",
                    "The code is inside a stream pipeline",
                    "A lambda can be clearer when naming the parameters explains the computation better than the method name does.",
                    question_id="chapter7_m1_q5",
                ),
            ],
        ),
        module(
            "Functional interfaces and stream fundamentals",
            [
                (
                    "Item 44: prefer standard functional interfaces when they fit",
                    slide(
                        [
                            "Use the standard interfaces in `java.util.function` whenever their signatures and contracts match your need.",
                            "A purpose-built functional interface is justified only when the name adds real documentation, the contract is strong, or custom default methods are valuable.",
                            "A `@FunctionalInterface` annotation is not optional decoration; it documents intent and protects the single-abstract-method contract.",
                        ],
                        image="../../page_previews/page_0220.png",
                        caption="Item 44: standard functional interfaces should be the default API choice, pages 220-223.",
                        points=[
                            "Prefer `Function`, `Predicate`, `Supplier`, `Consumer`, `UnaryOperator`, `BinaryOperator`, and their primitive specializations.",
                            "Do not define a new interface just to avoid importing one.",
                            "Annotate true functional interfaces with `@FunctionalInterface`.",
                        ],
                        source_pages=(220, 223),
                    ),
                ),
                (
                    "Do not overload on incompatible functional interfaces at the same call site",
                    slide(
                        [
                            "Overloading methods on different functional interfaces in the same argument position invites ambiguity.",
                            "Executor-style APIs are the cautionary example: a lambda may fit more than one overload, forcing the client to cast.",
                            "If the overload set is likely to confuse the compiler or the reader, prefer distinct method names or a single well-chosen functional type.",
                        ],
                        image="../../page_previews/page_0222.png",
                        caption="Item 44: functional-interface overloads can create real ambiguity for lambda clients, page 222.",
                        source_pages=(222, 223),
                    ),
                ),
                (
                    "Item 45: streams are a pipeline abstraction, not a blanket replacement for iteration",
                    slide(
                        [
                            "A stream is a finite or infinite sequence of elements; a pipeline is a source, zero or more intermediate operations, and one terminal operation.",
                            "Intermediate operations are lazy and do not run until the terminal operation starts evaluation.",
                            "Streams are fluent and expressive, but they are not automatically better than loops or collections.",
                        ],
                        image="../../page_previews/page_0224.png",
                        caption="Item 45: stream pipelines are lazy and compositional, pages 224-230.",
                        code="""words.stream()
    .map(String::toLowerCase)
    .collect(groupingBy(Function.identity(), counting()));""",
                        source_pages=(224, 230),
                    ),
                ),
            ],
            [
                q(
                    "When should you prefer a standard functional interface over a custom one?",
                    "When the standard type matches the required signature and semantics",
                    "Only when the API is internal",
                    "Only if the interface has exactly two abstract methods",
                    "Only when you need generics",
                    "The standard interfaces are shared vocabulary; custom interfaces are for genuinely new contracts.",
                    question_id="chapter7_m2_q1",
                ),
                q(
                    "Why should a custom functional interface be annotated with `@FunctionalInterface`?",
                    "It enforces the single-abstract-method contract and documents intent",
                    "It makes the interface serializable",
                    "It guarantees lambda performance",
                    "It prevents the interface from being public",
                    "The annotation is a compile-time guard and an API signal.",
                    question_id="chapter7_m2_q2",
                ),
                q(
                    "What is the key evaluation rule for a stream pipeline?",
                    "Nothing runs until the terminal operation is invoked",
                    "Every stage runs immediately when it is declared",
                    "Only the source stage is lazy",
                    "Intermediate operations always materialize collections",
                    "Laziness is what makes stream pipelines compositional and sometimes able to handle infinite sources.",
                    question_id="chapter7_m2_q3",
                ),
                q(
                    "Why does Item 45 warn that streams are not a universal replacement for iteration?",
                    "Because some problems are clearer or simpler with loops, and some APIs still need iterable results",
                    "Because stream operations cannot filter data",
                    "Because streams are slower by definition",
                    "Because streams cannot be used on collections",
                    "The book treats streams as a tool with a strong fit for bulk transformations, not a mandate.",
                    question_id="chapter7_m2_q4",
                ),
                q(
                    "What is a terminal operation doing in a stream pipeline?",
                    "It forces evaluation and produces the final result",
                    "It only renames the pipeline",
                    "It converts the stream back to an array automatically",
                    "It makes all intermediate operations parallel",
                    "Without a terminal operation, a stream pipeline is a no-op.",
                    question_id="chapter7_m2_q5",
                ),
            ],
        ),
        module(
            "Side effects, return types, and parallelism",
            [
                (
                    "Item 46: stream functions should be side-effect-free",
                    slide(
                        [
                            "Stream pipelines work best when each stage is a pure transformation of the previous stage.",
                            "Function objects passed to stream operations should not mutate external state unless you are deliberately using a collector or other API designed for mutation.",
                            "A `forEach` that performs the computation, rather than reporting a completed computation, is a strong smell.",
                        ],
                        image="../../page_previews/page_0231.png",
                        caption="Item 46: frequency-table examples show why mutating external state is the wrong stream style, pages 231-236.",
                        points=[
                            "Use collectors such as `groupingBy`, `counting`, `toList`, `toSet`, and `toMap` for aggregation.",
                            "Side effects make stream code harder to reason about and harder to parallelize correctly.",
                            "Pure functions preserve the algebraic structure that streams rely on.",
                        ],
                        source_pages=(231, 236),
                    ),
                ),
                (
                    "Item 47: return a collection when clients may want both iteration and streaming",
                    slide(
                        [
                            "If a method naturally returns a finite sequence and you can realize it as a collection, prefer a standard collection return type.",
                            "A `Collection` gives clients both iteration and stream access, and it is usually the least surprising choice.",
                            "Return `Stream` only when a collection is impractical or when the result is naturally a pipeline rather than a reusable materialized sequence.",
                        ],
                        image="../../page_previews/page_0237.png",
                        caption="Item 47: collection return types are the default when a materialized sequence is feasible, pages 237-242.",
                        source_pages=(237, 242),
                    ),
                ),
                (
                    "Item 48: parallel streams need evidence, not optimism",
                    slide(
                        [
                            "Parallelism can help, but only when the source splits cheaply, the workload is substantial, and the terminal operation scales well.",
                            "Do not assume that `parallel()` is a free speedup; it can cause incorrect results, liveness failures, or slower execution.",
                            "Measure under realistic conditions before shipping parallel stream code, and prefer simple, splittable sources such as arrays and `ArrayList` when parallelism is justified.",
                        ],
                        image="../../page_previews/page_0243.png",
                        caption="Item 48: parallel streams are conditional, expensive to get wrong, and highly workload-dependent, pages 243-247.",
                        code="""return LongStream.rangeClosed(2, n)
    .parallel()
    .mapToObj(BigInteger::valueOf)
    .filter(i -> i.isProbablePrime(50))
    .count();""",
                        source_pages=(243, 247),
                    ),
                ),
            ],
            [
                q(
                    "What is wrong with using `forEach` to build a frequency table by mutating an external map?",
                    "It turns the pipeline into imperative code with side effects instead of a pure stream computation",
                    "It prevents compilation unless the map is immutable",
                    "It always executes in parallel",
                    "It cannot read lowercase words",
                    "Item 46 says the stream should compute the result, not merely drive mutation in a terminal action.",
                    question_id="chapter7_m3_q1",
                ),
                q(
                    "Which collector family best matches the idea of building results without side effects?",
                    "Collectors such as `groupingBy`, `counting`, `toList`, `toSet`, and `toMap`",
                    "Only `forEach` and `peek`",
                    "Only `parallel()`",
                    "Only `reduce` with mutable accumulators",
                    "Collectors are the intended mutable-reduction mechanism for stream pipelines.",
                    question_id="chapter7_m3_q2",
                ),
                q(
                    "What is the preferred return type when a method can naturally materialize its results and clients may want to iterate?",
                    "A standard collection such as `ArrayList`, `Set`, or `Collection`",
                    "Always `Stream`",
                    "Always `Iterable`",
                    "Always an array",
                    "Returning a collection supports both iteration and streaming and is usually the least surprising API.",
                    question_id="chapter7_m3_q3",
                ),
                q(
                    "When is `parallel()` most promising?",
                    "When the source splits cheaply and the computation is substantial and well-structured",
                    "Whenever the pipeline contains `filter`",
                    "Whenever the stream is infinite",
                    "Whenever the code is short",
                    "Parallel stream performance depends on splittability, locality, and terminal-operation behavior.",
                    question_id="chapter7_m3_q4",
                ),
                q(
                    "Why does Item 48 insist on measurements before enabling parallel streams in production?",
                    "Because parallelism can regress correctness or performance, and the effect is workload-specific",
                    "Because `parallel()` is deprecated",
                    "Because the JVM never uses more than one core",
                    "Because streams cannot run in parallel on collections",
                    "The book treats parallelism as a proof obligation, not a guess.",
                    question_id="chapter7_m3_q5",
                ),
            ],
        ),
    ],
}
