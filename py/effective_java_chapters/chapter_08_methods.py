from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Methods",
    "subtitle": "Effective Java, pages 248-281. Items 49-56: parameter validity, defensive copies, method signatures, overloading, varargs, empty results, optionals, and doc comments.",
    "modules": [
        module(
            "Parameter validity and object boundaries",
            [
                (
                    "Validate at the boundary",
                    slide(
                        [
                            "Check public and protected parameters at method entry, before any state change or expensive work. Invalid inputs should fail fast, with the exception the API documents, not with some later accident.",
                            "Use the narrowest check that proves the contract: `Objects.requireNonNull`, range checks, and explicit type/shape tests. If the computation itself naturally validates the inputs, a separate pre-check is optional, but only if you understand the failure mode.",
                        ],
                        image="../../page_previews/page_0248.png",
                        caption="Item 49: parameter validity, failure atomicity, and explicit preconditions.",
                        points=[
                            "Document restrictions, then enforce them immediately.",
                            "Prefer the documented exception to an arbitrary downstream failure.",
                            "Do not add checks that are pure overhead when the algorithm already validates naturally.",
                        ],
                        source_pages=(248, 251),
                    ),
                ),
                (
                    "Copy before you trust",
                    slide(
                        [
                            "If a method or constructor accepts a mutable object, copy it before storing or validating it. Otherwise a caller can mutate your internal state through an alias.",
                            "For mutable internals, return defensive copies, not direct references. That applies to arrays too: nonempty arrays are always mutable, so accessors must not expose them raw.",
                        ],
                        image="../../page_previews/page_0252.png",
                        caption="Item 50: the Period example, TOCTOU risk, and defensive accessors.",
                        code=(
                            "public Period(Date start, Date end) {\n"
                            "    this.start = new Date(start.getTime());\n"
                            "    this.end = new Date(end.getTime());\n"
                            "    if (this.start.compareTo(this.end) > 0) {\n"
                            "        throw new IllegalArgumentException();\n"
                            "    }\n"
                            "}\n"
                            "\n"
                            "public Date start() {\n"
                            "    return new Date(start.getTime());\n"
                            "}"
                        ),
                        points=[
                            "Copy mutable inputs before validation to close the TOCTOU window.",
                            "Do not use `clone` on a parameter whose runtime type may be a malicious subclass.",
                            "Prefer immutable value types so copies disappear from the design.",
                        ],
                        source_pages=(252, 255),
                    ),
                ),
            ],
            [
                q(
                    "Why should a public method validate bad parameters at entry?",
                    "So the method fails fast, preserves object invariants, and reports the documented exception.",
                    "So the method can avoid all documentation for its parameters.",
                    "So the method can always continue with a default value.",
                    "So the caller can inspect the object state after the failure.",
                    "Parameter checks are about contract enforcement and failure atomicity, not just defensive programming.",
                    question_id="chapter_08_m1_q1",
                ),
                q(
                    "When is a separate validity check not worth doing?",
                    "When the main computation will naturally validate the inputs and the extra check would be redundant or expensive.",
                    "Whenever the method is public.",
                    "Whenever the method returns void.",
                    "Whenever the input type is an interface.",
                    "The item allows implicit validation, but only if you understand the trade-off and the resulting exception behavior.",
                    question_id="chapter_08_m1_q2",
                ),
                q(
                    "Why should a constructor copy a mutable argument before storing it?",
                    "To prevent later caller mutations from corrupting the object's invariants.",
                    "To make the field final.",
                    "To avoid the need for Javadoc.",
                    "To allow the object to share state intentionally.",
                    "Storing the caller's object creates an alias into your representation; a defensive copy breaks that alias.",
                    question_id="chapter_08_m1_q3",
                ),
                q(
                    "Why do defensive copies on accessors matter even for immutable-looking classes?",
                    "Because returning a mutable internal reference hands callers a back door into the object's state.",
                    "Because accessors are slower than constructors.",
                    "Because `Date` cannot be returned from a method.",
                    "Because the JVM automatically copies every return value anyway.",
                    "Returning a live mutable object exposes the representation; returning a copy preserves encapsulation.",
                    question_id="chapter_08_m1_q4",
                ),
            ],
        ),
        module(
            "Signature shape and overloads",
            [
                (
                    "Keep signatures small and typed to interfaces",
                    slide(
                        [
                            "Method names should be short, consistent, and unsurprising. Parameter lists should usually stay at four or fewer arguments; beyond that, users cannot reliably remember the order.",
                            "When a repeated parameter cluster means a real concept, factor it into a helper type. When several parameters are optional, consider a builder-like parameter object. Accept interfaces such as `Map`, not concrete classes such as `HashMap`.",
                        ],
                        image="../../page_previews/page_0257.png",
                        caption="Item 51: name choice, parameter count, helper types, and interface parameters.",
                        points=[
                            "Use helper types when a parameter bundle represents one domain concept.",
                            "Use a builder-style object when optional parameters start to dominate the signature.",
                            "Prefer enums to boolean flags unless the meaning is already self-evident.",
                        ],
                        source_pages=(257, 258),
                    ),
                ),
                (
                    "Overload only when the call is obvious",
                    slide(
                        [
                            "Overload resolution is compile-time only. The runtime type of an argument does not select an overload the way it selects an override.",
                            "That is why overload sets with the same arity, autoboxing, varargs, or functional interfaces are easy to misuse. If two overloads can both accept the same actual arguments, the API is already fragile.",
                        ],
                        image="../../page_previews/page_0259.png",
                        caption="Item 52: compile-time overload selection and the `CollectionClassifier` trap.",
                        code=(
                            "public static String classify(Collection<?> c) {\n"
                            "    return c instanceof Set ? \"Set\"\n"
                            "         : c instanceof List ? \"List\"\n"
                            "         : \"Unknown Collection\";\n"
                            "}"
                        ),
                        points=[
                            "Overloading and overriding are not interchangeable.",
                            "Avoid same-arity overloads unless the type sets are radically different.",
                            "If overloads must coexist, make them behave identically on the same inputs.",
                        ],
                        source_pages=(259, 265),
                    ),
                ),
            ],
            [
                q(
                    "Why are long parameter lists a smell?",
                    "They are hard to remember, easy to transpose, and difficult to use without constant reference to docs.",
                    "Because Java forbids methods with more than four parameters.",
                    "Because they always allocate arrays at runtime.",
                    "Because they prevent JIT inlining.",
                    "The practical issue is API usability, not language restriction.",
                    question_id="chapter_08_m2_q1",
                ),
                q(
                    "Why prefer an interface type over a class type in a parameter list?",
                    "It keeps the API flexible and avoids forcing callers into a particular implementation.",
                    "It makes the method more abstract and slower.",
                    "It guarantees immutability.",
                    "It lets the compiler skip null checks.",
                    "Programming to the interface avoids unnecessary copying and needless coupling.",
                    question_id="chapter_08_m2_q2",
                ),
                q(
                    "Why is overloading with the same arity risky?",
                    "Because the compiler chooses based on compile-time types, so the obvious-looking call can bind to the wrong method.",
                    "Because the JVM randomly picks one overload at runtime.",
                    "Because overloaded methods cannot be public.",
                    "Because autoboxing eliminates all ambiguity.",
                    "This is the core lesson of `CollectionClassifier` and the `remove(int)` versus `remove(Integer)` problem.",
                    question_id="chapter_08_m2_q3",
                ),
                q(
                    "When is overload ambiguity least likely to confuse users?",
                    "When the parameter types are radically different and no actual argument can plausibly fit both signatures.",
                    "Whenever the methods have the same name.",
                    "Whenever one overload is static.",
                    "Whenever the return types differ.",
                    "Radically different types make the choice obvious; otherwise, prefer different method names.",
                    question_id="chapter_08_m2_q4",
                ),
            ],
        ),
        module(
            "Varargs and absence",
            [
                (
                    "Varargs are not free",
                    slide(
                        [
                            "A varargs call allocates and initializes an array on every invocation. That overhead is acceptable when you truly need a flexible arity, but it is still real work.",
                            "If the method requires at least one argument, put the required argument first and use a trailing varargs parameter. For hot paths, use fixed-arity overloads for the common cases and reserve varargs for the tail.",
                        ],
                        image="../../page_previews/page_0266.png",
                        caption="Item 53: varargs syntax, required leading arguments, and the fixed-arity fast path.",
                        code=(
                            "static int min(int firstArg, int... remainingArgs) {\n"
                            "    int min = firstArg;\n"
                            "    for (int arg : remainingArgs)\n"
                            "        if (arg < min)\n"
                            "            min = arg;\n"
                            "    return min;\n"
                            "}"
                        ),
                        points=[
                            "Use varargs when the flexibility is genuinely part of the contract.",
                            "Expect array allocation on each call.",
                            "Do not force callers to pass zero arguments when the method is ill-defined without one.",
                        ],
                        source_pages=(266, 267),
                    ),
                ),
                (
                    "Return empty containers, not null",
                    slide(
                        [
                            "If a method has no elements to return, return an empty collection or a zero-length array. Returning null shifts special-case handling onto every caller.",
                            "The usual implementation is simple: `new ArrayList<>(...)` for collections, `toArray(new T[0])` for arrays, and `Collections.emptyList()` only when profiling proves it matters.",
                        ],
                        image="../../page_previews/page_0268.png",
                        caption="Item 54: empty collection and array returns, plus the zero-length-array pattern.",
                        points=[
                            "Empty containers are clearer than null and are usually cheap enough.",
                            "Do not preallocate the `toArray` target array in hopes of a speedup.",
                            "Use cached empty arrays only when measurement says the allocation matters.",
                        ],
                        source_pages=(268, 269),
                    ),
                ),
                (
                    "Optional is for absent results",
                    slide(
                        [
                            "Use `Optional<T>` when the method conceptually returns a `T` but may not be able to produce one, and the caller should have to confront that possibility.",
                            "Do not return null from an `Optional`-returning method. Do not use `Optional` as a collection element, map value, or field unless you have a very specific reason. For primitives, prefer `OptionalInt`, `OptionalLong`, or `OptionalDouble` over boxed optionals.",
                        ],
                        image="../../page_previews/page_0270.png",
                        caption="Item 55: Optional as a return type, and nowhere else by default.",
                        points=[
                            "Choose `orElse`, `orElseGet`, or `orElseThrow` based on the cost of the fallback.",
                            "Use `map`, `flatMap`, and `filter` before falling back to `isPresent` and `get`.",
                            "Prefer an empty container when the logical result is a container.",
                        ],
                        source_pages=(270, 273),
                    ),
                ),
            ],
            [
                q(
                    "Why does every varargs invocation have a cost?",
                    "Because the compiler creates and initializes an array for the arguments at the call site.",
                    "Because varargs force reflection.",
                    "Because varargs disable inlining.",
                    "Because the JVM boxes every argument twice.",
                    "The flexibility is convenient, but it still compiles to array creation.",
                    question_id="chapter_08_m3_q1",
                ),
                q(
                    "What is the correct pattern for a method that needs at least one value and then any number more?",
                    "Take one normal argument first, then a trailing varargs parameter.",
                    "Take only a varargs parameter and check `args.length` at runtime.",
                    "Take an `Optional<T>` and a varargs parameter together.",
                    "Overload the method with a separate empty signature.",
                    "The leading required parameter makes the contract compile-time explicit.",
                    question_id="chapter_08_m3_q2",
                ),
                q(
                    "Why should an API return an empty collection or array instead of null?",
                    "It removes special-case client code and avoids null handling without real performance gain.",
                    "Because empty containers are always allocated on the stack.",
                    "Because null is illegal as a return value.",
                    "Because callers cannot test for null in Java.",
                    "Returning null for absence pushes avoidable complexity into every caller.",
                    question_id="chapter_08_m3_q3",
                ),
                q(
                    "When is `Optional<T>` the right return type?",
                    "When the method may not be able to return a value and the caller should be forced to think about that possibility.",
                    "Whenever a method returns a collection.",
                    "Whenever a field is optional.",
                    "Whenever you want to avoid exceptions entirely.",
                    "Optional is a return-value tool, not a general replacement for null everywhere.",
                    question_id="chapter_08_m3_q4",
                ),
            ],
        ),
        module(
            "Documentation",
            [
                (
                    "Doc comments are the contract",
                    slide(
                        [
                            "Every exported class, interface, constructor, method, and field needs a doc comment. The comment should describe the contract, not the implementation, and it should enumerate preconditions, postconditions, and side effects.",
                            "For methods, use third-person declarative wording and keep the summary sentence self-contained. For public/protected members, `@param`, `@return`, and `@throws` are part of the API surface, not decorative noise.",
                        ],
                        image="../../page_previews/page_0275.png",
                        caption="Item 56: method contracts, preconditions, postconditions, and side effects.",
                        points=[
                            "Document unchecked exceptions when they represent precondition violations.",
                            "Use `@throws` for the contract, not just checked exceptions.",
                            "Treat missing docs as a usability defect, not a style nit.",
                        ],
                        source_pages=(275, 276),
                    ),
                ),
                (
                    "Use Javadoc tags precisely",
                    slide(
                        [
                            "Use `{@code}` for code fragments, `{@literal}` when you need HTML metacharacters without code font, and `{@implSpec}` when documenting self-use and subclass contracts.",
                            "The summary description must stand on its own, which is why overloads should not reuse the same first sentence. Generics, enums, and annotations need their own documentation conventions: type parameters, constants, and annotation members all need comments.",
                        ],
                        image="../../page_previews/page_0277.png",
                        caption="Item 56: summary text, tags, type parameters, enums, annotations, and inherited docs.",
                        points=[
                            "Document generic type parameters with `@param <T>` style tags.",
                            "Document enum constants and annotation members, not just the type itself.",
                            "Use `{@inheritDoc}` only when reusing inherited contract text is actually correct.",
                        ],
                        source_pages=(277, 280),
                    ),
                ),
                (
                    "Document the whole API surface",
                    slide(
                        [
                            "Package-level comments live in `package-info.java`; module-level comments live in `module-info.java`. If a class is serializable or a type has a thread-safety guarantee, say so explicitly.",
                            "Javadoc is only useful when you read the generated output. That is the final check for readability, HTML correctness, and whether the summary sentence actually communicates the API.",
                        ],
                        image="../../page_previews/page_0281.png",
                        caption="Item 56 closes with package/module docs, serializability, and thread safety.",
                        points=[
                            "Document thread-safety and serialized form when they matter.",
                            "Use external architecture docs when the API surface alone is not enough.",
                            "Generated docs should be read, not merely produced.",
                        ],
                        source_pages=(281, 281),
                    ),
                ),
            ],
            [
                q(
                    "What is the main purpose of a doc comment on an exported API element?",
                    "To specify the contract a client relies on, including preconditions, postconditions, and side effects.",
                    "To restate the implementation line by line.",
                    "To replace code review.",
                    "To satisfy the compiler.",
                    "Documentation is part of the API, not a paraphrase of the source code.",
                    question_id="chapter_08_m4_q1",
                ),
                q(
                    "Which tags are expected for a normal method contract?",
                    "`@param`, `@return`, and `@throws`.",
                    "`@implSpec`, `@index`, and `@literal`.",
                    "`@override`, `@serial`, and `@code`.",
                    "Only `@return`.",
                    "Those three tags are the standard way to document parameters, results, and exception conditions.",
                    question_id="chapter_08_m4_q2",
                ),
                q(
                    "When should `{@implSpec}` be used?",
                    "When documenting the self-use contract for subclasses or overriding code.",
                    "Whenever a method is public.",
                    "Whenever the method is generic.",
                    "Whenever you want to hide implementation details from callers.",
                    "It is for inheritance contracts, not for client-facing behavior descriptions.",
                    question_id="chapter_08_m4_q3",
                ),
                q(
                    "What should you document for generic types, enums, annotations, and packages?",
                    "Type parameters, constants, annotation members, and package/module-level comments where appropriate.",
                    "Only the public constructors.",
                    "Only the top-level class summary.",
                    "Nothing extra, because Javadoc infers it.",
                    "Those elements have API meaning and need explicit documentation to stay usable.",
                    question_id="chapter_08_m4_q4",
                ),
            ],
        ),
    ],
}
