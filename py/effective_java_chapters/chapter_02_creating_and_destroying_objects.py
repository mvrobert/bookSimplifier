from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Creating and Destroying Objects",
    "subtitle": "Items 1-9: construction, ownership, reuse, cleanup, and resource safety",
    "modules": [
        module(
            "Construction APIs",
            [
                (
                    "Item 1: Static factories",
                    slide(
                        [
                            "Static factory methods give the creator a name, which is often the first clue about intent when constructor parameters are not self-describing.",
                            "They can return cached instances, hide implementation classes, and even return a subtype of the declared return type.",
                            "They are not the GoF Factory Method pattern; this item is about public static creation entry points.",
                        ],
                        image="../../page_previews/page_0026.png",
                        caption="Item 1: static factories as a named alternative to constructors",
                        points=[
                            "Use names such as `of`, `from`, `valueOf`, `getInstance`, or `newInstance` when they clarify construction semantics.",
                            "Prefer interface return types when the implementation class should stay hidden.",
                            "Do not assume a static factory must allocate a new object; instance control is often the point.",
                        ],
                        box=(
                            "note",
                            "Pedantic point: static factories trade discoverability for flexibility, so document them aggressively in API docs.",
                        ),
                        code="Boolean yes = Boolean.valueOf(true);\nBigInteger prime = BigInteger.valueOf(17);",
                        source_pages=(26, 30),
                    ),
                ),
                (
                    "Item 2: Builders for many parameters",
                    slide(
                        [
                            "Telescoping constructors scale poorly because callers must supply long positional argument lists and cannot see which values are optional.",
                            "JavaBeans improve readability but allow inconsistent intermediate state and make immutability awkward.",
                            "A builder restores readability and safety by collecting optional values first and constructing the target object only at `build()` time.",
                        ],
                        image="../../page_previews/page_0031.png",
                        caption="Item 2: builder pattern for required and optional parameters",
                        points=[
                            "Use builders when a constructor or static factory would need many parameters, especially when several are optional or same-typed.",
                            "Validate cheap invariants in the builder and cross-field invariants in the target constructor or `build()` path.",
                            "For hierarchies, use recursive generic builders plus a `self()` method to preserve fluent chaining.",
                        ],
                        box=(
                            "tip",
                            "Once a class is likely to accrete more optional parameters, starting with a builder is often less painful than migrating later.",
                        ),
                        code="NutritionFacts cocaCola = new NutritionFacts.Builder(240, 8)\n    .calories(100)\n    .sodium(35)\n    .carbohydrate(27)\n    .build();",
                        source_pages=(31, 37),
                    ),
                ),
            ],
            [
                q(
                    "Which is the clearest reason to prefer a static factory over a constructor when the creation path needs a descriptive name?",
                    "The name can encode the construction semantics directly.",
                    "Constructors cannot return objects.",
                    "Constructors cannot be public.",
                    "Static factories are always faster than constructors.",
                    "A static factory can communicate intent with a name such as `valueOf` or `of`, which is more readable than a bare constructor signature.",
                    question_id="chapter02_m1_q1",
                ),
                q(
                    "Why can a static factory be more flexible than a constructor?",
                    "It can return any subtype of the declared return type.",
                    "It must always allocate a fresh object.",
                    "It cannot be overloaded.",
                    "It cannot hide implementation classes.",
                    "The returned object may vary by subtype, by input, or by release, which is impossible with a constructor.",
                    question_id="chapter02_m1_q2",
                ),
                q(
                    "What is the main failure mode of telescoping constructors for many optional parameters?",
                    "Callers must pass long positional lists of identically typed values.",
                    "They cannot be made public.",
                    "They force all fields to be mutable.",
                    "They cannot validate parameters.",
                    "The core problem is readability and the risk of swapping same-typed arguments without compiler help.",
                    question_id="chapter02_m1_q3",
                ),
                q(
                    "What is the main technical drawback of the JavaBeans pattern for object construction?",
                    "The object can be observed in an inconsistent intermediate state.",
                    "It prevents the use of setters.",
                    "It requires private constructors.",
                    "It forbids optional parameters.",
                    "Construction is split across multiple calls, so invariants cannot be enforced atomically and immutability becomes awkward.",
                    question_id="chapter02_m1_q4",
                ),
            ],
        ),
        module(
            "Controlled Instantiation",
            [
                (
                    "Item 3: Singleton control",
                    slide(
                        [
                            "A singleton is a class that has exactly one instance, and the implementation must prevent any other instance from being created.",
                            "The traditional forms are a public static final instance field or a private static instance accessor; an enum singleton gives the strongest guarantee in modern Java.",
                            "If you need to defend against reflection or serialization attacks, the constructor must actively reject second-instance creation.",
                        ],
                        image="../../page_previews/page_0038.png",
                        caption="Item 3: singleton control with a private constructor",
                        points=[
                            "Use a private constructor plus a single exported instance path.",
                            "Prefer an enum singleton when you want the strongest built-in instance guarantee.",
                            "Singletons make testing harder when clients cannot substitute a mock implementation.",
                        ],
                        box=(
                            "warning",
                            "A singleton is instance control, not convenience. If the object has real state or resource dependencies, treat it as a design smell until proven otherwise.",
                        ),
                        code="public enum Elvis {\n    INSTANCE;\n}",
                        source_pages=(38, 39),
                    ),
                ),
                (
                    "Item 4: Noninstantiable utility classes",
                    slide(
                        [
                            "A utility class groups stateless helpers or static factories, but it should not be instantiable because an instance would be meaningless.",
                            "Marking such a class abstract is wrong because the class can still be subclassed and instantiated through the subclass.",
                            "The standard idiom is a private constructor that throws `AssertionError`; this prevents accidental construction and also blocks subclassing.",
                        ],
                        image="../../page_previews/page_0040.png",
                        caption="Item 4: private constructor for a utility class",
                        points=[
                            "Use this pattern for collections of static methods and fields, not as a substitute for object design.",
                            "The explicit constructor exists only to make construction impossible outside the class.",
                            "A comment is appropriate here because the pattern is intentionally counterintuitive.",
                        ],
                        code="public final class UtilityClass {\n    private UtilityClass() {\n        throw new AssertionError();\n    }\n}",
                        source_pages=(40, 40),
                    ),
                ),
                (
                    "Item 5: Dependency injection",
                    slide(
                        [
                            "If a class depends on an external resource whose behavior matters, do not hardwire that resource inside the class.",
                            "Inject the dependency through the constructor, a static factory, or a builder so the class can be tested and reused with different implementations.",
                            "If the dependency is itself a factory, `Supplier<? extends T>` is a natural input type because it allows subtype creation without losing flexibility.",
                        ],
                        image="../../page_previews/page_0041.png",
                        caption="Item 5: inject resources instead of baking them in",
                        points=[
                            "Dependency injection preserves flexibility, reusability, and testability.",
                            "It works for one dependency or many, and it composes well with immutable classes.",
                            "Large systems often hide the wiring behind a DI framework, but the manual API should still be clean.",
                        ],
                        box=(
                            "note",
                            "Do not use a singleton or static utility class for behavior that varies by resource, such as a spell checker bound to different dictionaries.",
                        ),
                        code="public class SpellChecker {\n    private final Lexicon dictionary;\n\n    public SpellChecker(Lexicon dictionary) {\n        this.dictionary = Objects.requireNonNull(dictionary);\n    }\n}",
                        source_pages=(41, 42),
                    ),
                ),
            ],
            [
                q(
                    "What is the strongest modern choice for a singleton that also needs serialization and reflection resistance by default?",
                    "An enum singleton.",
                    "A public constructor.",
                    "An abstract class with one instance field.",
                    "A static utility class.",
                    "An enum singleton gives the strongest built-in instance-control guarantee in Java.",
                    question_id="chapter02_m2_q1",
                ),
                q(
                    "Why is making a utility class abstract not a valid way to prevent instantiation?",
                    "A subclass can still be instantiated.",
                    "The compiler removes all constructors.",
                    "Abstract classes cannot have static methods.",
                    "Abstract classes cannot be final.",
                    "Abstract only blocks direct instantiation; it does not prevent subclass construction.",
                    question_id="chapter02_m2_q2",
                ),
                q(
                    "What is the purpose of throwing `AssertionError` in a private utility-class constructor?",
                    "It prevents accidental construction even from inside the class.",
                    "It makes the class serializable.",
                    "It enables dependency injection.",
                    "It avoids the need for a private constructor.",
                    "The exception is a defensive backstop in case the constructor is invoked by mistake during maintenance or reflection.",
                    question_id="chapter02_m2_q3",
                ),
                q(
                    "What is the core benefit of dependency injection for resource-dependent classes?",
                    "It lets clients supply the dependency they actually need.",
                    "It forces the resource to be static.",
                    "It makes the class impossible to test.",
                    "It eliminates constructors.",
                    "Injecting the resource gives the class flexibility, makes tests deterministic, and avoids hardwired global state.",
                    question_id="chapter02_m2_q4",
                ),
                q(
                    "Why is `Supplier<? extends Tile>` a good input type for a factory dependency?",
                    "It allows the client to provide any factory that creates a Tile subtype.",
                    "It forces the factory to return `null` on failure.",
                    "It prevents lambdas from being used.",
                    "It requires the factory to be a singleton.",
                    "The bounded wildcard preserves subtype flexibility while still expressing a factory contract.",
                    question_id="chapter02_m2_q5",
                ),
            ],
        ),
        module(
            "Allocation Discipline",
            [
                (
                    "Item 6: Avoid unnecessary objects",
                    slide(
                        [
                            "Do not create a new object when an existing immutable object, cached instance, or reusable mutable object will do the same job.",
                            "String literals, cached factory results, precompiled regular expressions, and view objects are the standard reuse opportunities in this chapter.",
                            "Autoboxing can silently allocate massive numbers of wrapper objects when a primitive would have been faster and clearer.",
                        ],
                        image="../../page_previews/page_0043.png",
                        caption="Item 6: reuse immutable and expensive objects",
                        points=[
                            "Prefer literals or cached factory results to `new` when the object has no stateful identity requirement.",
                            "Cache expensive objects such as `Pattern` instances when a method is invoked repeatedly.",
                            "Do not build your own object pool for cheap objects; modern JVM garbage collectors already optimize that path well.",
                        ],
                        code="private static final Pattern ROMAN = Pattern.compile(\n    \"^(?=.)M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$\"\n);\n\nstatic boolean isRomanNumeral(String s) {\n    return ROMAN.matcher(s).matches();\n}",
                        source_pages=(43, 46),
                    ),
                ),
                (
                    "Item 7: Eliminate obsolete references",
                    slide(
                        [
                            "Garbage collection only helps when objects are no longer reachable; a container that retains stale references is leaking memory even in a managed language.",
                            "When a custom data structure owns its own storage, it must null out references as soon as those slots become inactive.",
                            "Caches and listener registries are the two classic places where forgotten references quietly keep large object graphs alive.",
                        ],
                        image="../../page_previews/page_0047.png",
                        caption="Item 7: clear stale references in custom containers",
                        points=[
                            "Null out references when an element leaves the active portion of a custom storage structure.",
                            "Use `WeakHashMap` only when cache lifetime should track external references to the key.",
                            "A heap profiler is often how this bug is found after the code has shipped.",
                        ],
                        box=(
                            "note",
                            "Do not null every reference eagerly. The rule applies to references that are genuinely obsolete, not to variables that can simply fall out of scope.",
                        ),
                        code="Object result = elements[--size];\nelements[size] = null;\nreturn result;",
                        source_pages=(47, 49),
                    ),
                ),
            ],
            [
                q(
                    "Which allocation is most clearly unnecessary?",
                    "Creating `new String(\"bikini\")` instead of reusing the string literal.",
                    "Creating a small immutable value object once.",
                    "Using a builder for a complex object.",
                    "Returning an interface from a factory.",
                    "The string literal is already an object and can be reused directly.",
                    question_id="chapter02_m3_q1",
                ),
                q(
                    "Why is caching a compiled `Pattern` often better than calling `String.matches` repeatedly?",
                    "The regular expression compilation is expensive and can be reused.",
                    "`String.matches` is not part of the JDK.",
                    "A `Pattern` cannot be immutable.",
                    "Caching only helps for boxed primitives.",
                    "Repeatedly compiling the same regex creates avoidable work; a cached `Pattern` avoids that cost.",
                    question_id="chapter02_m3_q2",
                ),
                q(
                    "What is the best general response when a custom stack or array-backed container removes an element?",
                    "Null out the now-obsolete slot.",
                    "Leave the reference in place for debugging.",
                    "Clone the entire array on every pop.",
                    "Convert the array to a `WeakHashMap`.",
                    "The slot is no longer part of the active set, so clearing it lets the GC reclaim the object graph behind it.",
                    question_id="chapter02_m3_q3",
                ),
                q(
                    "When is `WeakHashMap` the right cache implementation?",
                    "When entry lifetime should follow external references to the key.",
                    "When entries must stay forever.",
                    "When all values are primitives.",
                    "When the cache is only used once.",
                    "Weak references are useful only when the cache entry is relevant for as long as the key is externally reachable.",
                    question_id="chapter02_m3_q4",
                ),
            ],
        ),
        module(
            "Cleanup and Resource Safety",
            [
                (
                    "Item 8: Finalizers and cleaners",
                    slide(
                        [
                            "Finalizers and cleaners are not normal cleanup mechanisms. They are unpredictable, slow, and unsuitable for time-critical or correctness-critical work.",
                            "A finalizer may never run, may run very late, may run on the wrong thread, and may silently hide exceptions.",
                            "Cleaners are less dangerous than finalizers, but they are still only background safety nets, not reliable resource management.",
                        ],
                        image="../../page_previews/page_0050.png",
                        caption="Item 8: finalizers and cleaners are a last resort",
                        points=[
                            "Do not depend on finalizers or cleaners for closing files, releasing locks, or updating persistent state.",
                            "The main legitimate uses are safety nets and noncritical native peer cleanup.",
                            "Finalizers also create attack surface because they can run on partially constructed objects.",
                        ],
                        box=(
                            "warning",
                            "If the object owns a resource that must be released promptly, the class should expose `close()` and make clients call it explicitly.",
                        ),
                        source_pages=(50, 51),
                    ),
                ),
                (
                    "Item 8: Cleaner as a safety net only",
                    slide(
                        [
                            "If you use a cleaner, keep the cleaning state separate from the owner object and make the state a static nested class so it cannot accidentally retain the owner.",
                            "The owner should still implement `AutoCloseable`; the cleaner exists only to cover client mistakes.",
                            "For native peers, a cleaner may be acceptable when the resource is not critical and performance costs are tolerable.",
                        ],
                        image="../../page_previews/page_0053.png",
                        caption="Item 8: cleaner safety-net pattern",
                        points=[
                            "The cleaner action must not capture the owning object.",
                            "A `close()` method should trigger cleanup explicitly and mark the object invalid.",
                            "Treat the cleaner as insurance, not as part of the normal control path.",
                        ],
                        code="public class Room implements AutoCloseable {\n    private static final Cleaner cleaner = Cleaner.create();\n    private static class State implements Runnable {\n        @Override public void run() { /* cleanup */ }\n    }\n}",
                        source_pages=(52, 54),
                    ),
                ),
                (
                    "Item 9: Try-with-resources",
                    slide(
                        [
                            "Try-with-resources is the correct way to close closeable resources in Java 7 and later.",
                            "It preserves the primary exception and suppresses later close failures, which makes debugging far better than the old try-finally pattern.",
                            "The resource type must implement `AutoCloseable`, and multiple resources can be declared in one resource specification.",
                        ],
                        image="../../page_previews/page_0055.png",
                        caption="Item 9: try-with-resources instead of try-finally",
                        points=[
                            "Use try-with-resources for anything with a `close()` method that must be called.",
                            "You can still attach `catch` clauses to handle failures without nested try blocks.",
                            "The compiler-generated suppression behavior keeps the most useful exception visible.",
                        ],
                        code="static String firstLineOfFile(String path) throws IOException {\n    try (BufferedReader br = new BufferedReader(new FileReader(path))) {\n        return br.readLine();\n    }\n}",
                        source_pages=(55, 57),
                    ),
                ),
            ],
            [
                q(
                    "Why are finalizers and cleaners poor choices for ordinary resource management?",
                    "They are not guaranteed to run promptly or at all.",
                    "They are required by every closeable type.",
                    "They run only on the main thread.",
                    "They cannot be used with native resources.",
                    "The timing and even execution of cleanup are not reliable enough for correctness or resource limits.",
                    question_id="chapter02_m4_q1",
                ),
                q(
                    "What is the best modern pattern for a class that owns a resource requiring explicit termination?",
                    "Implement `AutoCloseable` and require clients to call `close()`.",
                    "Rely on a finalizer as the primary cleanup path.",
                    "Make the resource static.",
                    "Hide the resource inside a singleton.",
                    "The class should expose explicit closure and, if desired, keep a cleaner only as a fallback safety net.",
                    question_id="chapter02_m4_q2",
                ),
                q(
                    "What happens when both the body of a try-finally block and the `close()` call throw?",
                    "The later exception can obscure the earlier one.",
                    "Both exceptions are always printed equally.",
                    "The compiler rewrites it as try-with-resources.",
                    "The close exception is ignored by definition.",
                    "Old try-finally code often loses the primary failure, which is one of the reasons try-with-resources was introduced.",
                    question_id="chapter02_m4_q3",
                ),
                q(
                    "Which interface must a resource implement to be usable in try-with-resources?",
                    "`AutoCloseable`.",
                    "`Serializable`.",
                    "`CloseableFactory`.",
                    "`Runnable`.",
                    "`AutoCloseable` is the contract that gives the compiler a resource to close automatically.",
                    question_id="chapter02_m4_q4",
                ),
                q(
                    "Can a try-with-resources statement also have a catch clause?",
                    "Yes, it can handle exceptions without extra nesting.",
                    "No, the syntax forbids it.",
                    "Only if the resource is finalizable.",
                    "Only inside a loop.",
                    "A catch clause may follow the resource specification exactly as it can follow a try-finally statement.",
                    question_id="chapter02_m4_q5",
                ),
            ],
        ),
    ],
}
