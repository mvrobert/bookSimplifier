from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Enums and Annotations",
    "subtitle": "Effective Java, Chapter 6: pages 178-213, Items 34-41",
    "modules": [
        module(
            "Enums are real types",
            [
                (
                    "Why int constants fail",
                    slide(
                        [
                            "Before enum types, the int-enum pattern encoded a closed set of constants as public static final ints. That buys syntax, not type safety.",
                            "The failure modes are predictable: namespace collisions, accidental arithmetic on values, brittle client binaries, and debugger output that is just a number.",
                        ],
                        image="../../page_previews/page_0178.png",
                        caption="Item 34 begins by contrasting int constants with real enum types.",
                        points=[
                            "A constant group has no namespace, so names must be prefixed manually.",
                            "The compiler cannot stop you from mixing unrelated constant groups.",
                            "Changing an int constant can require recompiling clients.",
                        ],
                        source_pages=(178, 179),
                    ),
                ),
                (
                    "Enum types are classes",
                    slide(
                        [
                            "An enum constant is a singleton instance exported by the enum class. The type is effectively final, instance-controlled, and much more than a glorified integer.",
                            "Enums can declare fields, constructors, methods, and interfaces. Use private final state and expose behavior through accessors, not ordinals.",
                        ],
                        image="../../page_previews/page_0180.png",
                        caption="A rich enum can carry data and behavior, not just names.",
                        points=[
                            "values() returns constants in declaration order.",
                            "toString() defaults to the constant name but can be overridden.",
                            "Enum constructors cannot access mutable static state during initialization.",
                        ],
                        code=(
                            "public enum Planet {\n"
                            "    EARTH(5.975e+24, 6.378e6);\n"
                            "    private final double mass;\n"
                            "    private final double radius;\n"
                            "    private final double surfaceGravity;\n"
                            "}"
                        ),
                        source_pages=(180, 183),
                    ),
                ),
                (
                    "Constant-specific behavior",
                    slide(
                        [
                            "If each enum constant has different behavior, prefer constant-specific class bodies over a switch that dispatches on this.",
                            "The switch style is fragile: adding a constant compiles cleanly and then fails at runtime if you forget to update the switch.",
                        ],
                        image="../../page_previews/page_0182.png",
                        caption="Constant-specific method implementations push behavior next to the constant.",
                        points=[
                            "Abstract methods in an enum force every constant to provide an implementation.",
                            "A strategy enum is useful when multiple constants share a behavior family.",
                            "Use a switch on an enum only when augmenting an enum you do not control.",
                        ],
                        source_pages=(182, 187),
                    ),
                ),
            ],
            [
                q(
                    "Why is the int-enum pattern inferior to a real enum type?",
                    "It provides type safety, a namespace, and stable binaries for clients.",
                    "It is faster than enums in every case.",
                    "It supports inheritance better than enums.",
                    "It automatically gives you set operations.",
                    "Int constants are brittle: they can be mixed accidentally, collide by name, and are compiled into client code. Real enums are type-safe classes.",
                ),
                q(
                    "What is the main reason to prefer instance fields over ordinal() for associated data?",
                    "Ordinal changes when constants are reordered; a stored field does not.",
                    "Ordinal is always slower than a stored field.",
                    "Ordinal cannot be called on enums with methods.",
                    "Stored fields cannot be final.",
                    "An enum's ordinal is only the declaration position, so it is not a semantic value and must not drive program logic.",
                ),
                q(
                    "When should you use a switch on an enum?",
                    "When you are augmenting an enum you do not control, or the logic does not belong in the enum itself.",
                    "Whenever you want compile-time checking for missing constants.",
                    "Whenever the enum has instance fields.",
                    "Whenever you need constant-specific behavior.",
                    "A switch is appropriate as a client-side adapter, not as the primary way to model per-constant behavior inside the enum.",
                ),
                q(
                    "What does an enum constructor give you that int constants cannot?",
                    "A place to bind per-constant data and compute derived state once.",
                    "A way to create multiple instances per constant.",
                    "Access to mutable static fields before initialization.",
                    "A namespace shared across unrelated enums.",
                    "Each enum constant can carry its own state and behavior, which is impossible with bare ints.",
                ),
            ],
        ),
        module(
            "EnumSet and EnumMap",
            [
                (
                    "EnumSet replaces bit fields",
                    slide(
                        [
                            "If a set of enum constants is being represented as a bit field, stop. EnumSet gives you the compactness of bit vectors with the API and safety of Set.",
                            "The client sees a normal Set<Style>; the implementation can still be bit-vector fast for small enums.",
                        ],
                        image="../../page_previews/page_0190.png",
                        caption="Item 36 replaces manual bit twiddling with EnumSet.",
                        points=[
                            "Use Set<Style> in signatures, not EnumSet<Style>.",
                            "Bulk operations remain efficient because EnumSet is internally bit based.",
                            "You do not need to precompute bit masks or choose int versus long up front.",
                        ],
                        code=(
                            "public void applyStyles(Set<Style> styles) {\n"
                            "    ...\n"
                            "}\n"
                            "text.applyStyles(EnumSet.of(Style.BOLD, Style.ITALIC));"
                        ),
                        source_pages=(190, 191),
                    ),
                ),
                (
                    "EnumMap replaces ordinal indexing",
                    slide(
                        [
                            "If an array is really a map from enum key to value, use EnumMap. It is type-safe, self-documenting, and comparable in speed to ordinal-indexed arrays.",
                            "EnumMap hides the array implementation detail and makes the key type explicit via the Class token.",
                        ],
                        image="../../page_previews/page_0192.png",
                        caption="Item 37 shows how EnumMap eliminates unchecked casts and index math.",
                        points=[
                            "Use Map<EnumType, V> in APIs, not ordinal-based arrays.",
                            "The constructor takes the enum Class object as a bounded type token.",
                            "For multidimensional relationships, use nested EnumMap instances.",
                        ],
                        source_pages=(192, 196),
                    ),
                ),
                (
                    "Nested EnumMap for enum pairs",
                    slide(
                        [
                            "A two-dimensional enum relationship should usually be represented as Map<A, Map<B, V>> backed by EnumMap at each level.",
                            "This is safer than an array-of-arrays indexed by ordinals, and it is far easier to extend when the enum grows.",
                        ],
                        image="../../page_previews/page_0194.png",
                        caption="The phase-transition example shows how nested EnumMap scales to enum pairs.",
                        points=[
                            "Adding a new enum constant should not require reshaping a 2D array manually.",
                            "Let the map-of-maps be initialized from the enum values.",
                            "Use groupingBy(..., mapFactory, ...) if stream collectors should produce EnumMap.",
                        ],
                        source_pages=(194, 196),
                    ),
                ),
            ],
            [
                q(
                    "Why is EnumSet preferred over a manual bit field?",
                    "It preserves Set semantics and type safety while keeping bit-vector performance.",
                    "It uses more memory than any other Set implementation.",
                    "It can represent sets with more than 64 elements in one long.",
                    "It is immutable by default.",
                    "EnumSet gives you compact representation and normal Set operations without manual bit masks.",
                ),
                q(
                    "Why should public APIs take Set<Style> instead of EnumSet<Style>?",
                    "So callers are not forced to use one specific implementation.",
                    "Because EnumSet cannot be passed to methods.",
                    "Because Set is always faster than EnumSet.",
                    "Because EnumSet is not a valid parameter type.",
                    "Program to the interface. Accepting Set keeps the API flexible even if EnumSet is the best implementation choice.",
                ),
                q(
                    "What is the main advantage of EnumMap over ordinal-indexed arrays?",
                    "It is type-safe and self-describing while staying close to array speed.",
                    "It supports non-enum keys better than HashMap.",
                    "It avoids the need for a key type token.",
                    "It is automatically immutable.",
                    "EnumMap hides the ordinal arithmetic and still uses array-backed storage internally.",
                ),
                q(
                    "When should you specify a map factory with groupingBy?",
                    "When you care that the collector produce EnumMap rather than an implementation chosen by the library.",
                    "Whenever the stream has more than one element.",
                    "Only when collecting to a Set.",
                    "Only when the source is already a map.",
                    "The default groupingBy collector may choose a different Map implementation; provide a factory if EnumMap behavior matters.",
                ),
            ],
        ),
        module(
            "Extensible enums and annotations",
            [
                (
                    "Extensible enums use interfaces",
                    slide(
                        [
                            "Java enums are not extensible, and that is usually correct. If you need an extensible opcode-like family, define an interface and let enums implement it.",
                            "Clients should depend on the interface type, not on a concrete base enum.",
                        ],
                        image="../../page_previews/page_0197.png",
                        caption="Item 38 replaces enum inheritance with an interface plus implementations.",
                        points=[
                            "The interface is the stable API surface.",
                            "A base enum can implement the interface, and extension enums can implement the same interface.",
                            "Use bounded type tokens when you want to iterate over a specific enum class.",
                        ],
                        code=(
                            "public interface Operation {\n"
                            "    double apply(double x, double y);\n"
                            "}\n"
                            "public enum BasicOperation implements Operation { ... }"
                        ),
                        source_pages=(197, 199),
                    ),
                ),
                (
                    "Annotations encode intent",
                    slide(
                        [
                            "Naming patterns are fragile. An annotation makes the intent machine-readable, type-checked, and less likely to fail silently.",
                            "For runtime tools, combine RetentionPolicy.RUNTIME with an appropriate Target meta-annotation.",
                        ],
                        image="../../page_previews/page_0201.png",
                        caption="Item 39 moves special handling from naming conventions to annotations.",
                        points=[
                            "Marker annotations carry no parameters; they simply mark an element.",
                            "A parameterized annotation can carry a Class<? extends Throwable> token.",
                            "Repeatable annotations are syntactic sugar over a synthetic container annotation.",
                        ],
                        source_pages=(201, 208),
                    ),
                ),
                (
                    "Repeatable annotations are not free",
                    slide(
                        [
                            "Repeatable annotations improve source readability when you need multiple logical instances on one element, but the processing rules are easy to get wrong.",
                            "isAnnotationPresent sees the annotation or the container, not both. getAnnotationsByType is the API that normalizes the repeated form.",
                        ],
                        image="../../page_previews/page_0206.png",
                        caption="The repeatable annotation form requires explicit handling in the processor.",
                        points=[
                            "Repeated annotations generate a synthetic container annotation.",
                            "Processors must not assume isAnnotationPresent covers both forms.",
                            "Use repeatable annotations only when the source form really reads better.",
                        ],
                        source_pages=(186, 187),
                    ),
                ),
            ],
            [
                q(
                    "Why are annotations better than naming patterns for framework hooks?",
                    "They are checked by the compiler and can carry structured metadata.",
                    "They execute faster at runtime.",
                    "They automatically fix invalid code.",
                    "They are only available for methods.",
                    "Annotations avoid silent typos and let tools inspect explicit metadata instead of parsing names.",
                ),
                q(
                    "What does @Retention(RetentionPolicy.RUNTIME) do for a test annotation?",
                    "It keeps the annotation visible to reflection at runtime.",
                    "It makes the annotation compile faster.",
                    "It allows the annotation only on types.",
                    "It forces the annotation to be repeatable.",
                    "Without runtime retention, a reflection-based test runner cannot see the annotation.",
                ),
                q(
                    "What is the main point of a bounded type token like Class<? extends Throwable>?",
                    "It lets the annotation accept only class literals for throwable subtypes.",
                    "It forces the value to be a String at runtime.",
                    "It makes annotation processing unnecessary.",
                    "It allows any unrelated class to be passed in.",
                    "The wildcard constrains the class literal to a Throwable subtype and keeps the API type-safe.",
                ),
                q(
                    "Why can repeated annotations be easy to process incorrectly?",
                    "Because the repeated form is represented through a synthetic container annotation.",
                    "Because Java forbids runtime reflection on annotations.",
                    "Because repeated annotations cannot carry parameters.",
                    "Because repeatable annotations are not retained.",
                    "A processor must look for the direct annotation and its container, or use getAnnotationsByType.",
                ),
            ],
        ),
        module(
            "Override and marker interfaces",
            [
                (
                    "Override catches overloads",
                    slide(
                        [
                            "Use @Override everywhere you believe a method overrides a supertype declaration. It turns accidental overloads into compiler errors.",
                            "The classic failure mode is equals(Bigram) instead of equals(Object): the code compiles, but the method does not override anything.",
                        ],
                        image="../../page_previews/page_0209.png",
                        caption="Item 40 shows how @Override turns a subtle bug into a compiler error.",
                        points=[
                            "It applies to superclass and interface methods.",
                            "In concrete classes, overriding an abstract superclass method is already compiler-enforced, but the annotation is still useful for clarity.",
                            "IDE warnings can complement compiler checks when the annotation is used consistently.",
                        ],
                        source_pages=(209, 211),
                    ),
                ),
                (
                    "Marker interfaces define a type",
                    slide(
                        [
                            "A marker interface does more than mark. It creates a real type that compile-time checks can use, which is impossible with a marker annotation alone.",
                            "Serializable is the canonical example: it denotes a capability that can be enforced by type checking if APIs choose to use it that way.",
                        ],
                        image="../../page_previews/page_0210.png",
                        caption="Item 41 argues that a marker interface is still the right tool when the marker is a type.",
                        points=[
                            "Use a marker interface when clients may want methods that accept only marked instances.",
                            "Use a marker interface to restrict a marker to a specific family of subtypes.",
                            "Use a marker annotation when the marker must apply to non-type program elements or fit an annotation framework.",
                        ],
                        source_pages=(191, 193),
                    ),
                ),
                (
                    "Choosing between annotation and interface",
                    slide(
                        [
                            "If the marker is part of a type relationship, prefer an interface. If it is just metadata on a class, method, field, or parameter, prefer an annotation.",
                            "The question is not whether annotations are newer. The question is whether the marker should participate in the type system.",
                        ],
                        image="../../page_previews/page_0212.png",
                        caption="The decision rule is simple: type system first, metadata second.",
                        points=[
                            "Use interfaces for compile-time filtering on accepted argument types.",
                            "Use annotations for frameworks that scan program elements.",
                            "If a TYPE-targeted annotation feels like a type, re-check the design.",
                        ],
                        source_pages=(212, 213),
                    ),
                ),
            ],
            [
                q(
                    "What bug does @Override most directly prevent?",
                    "Accidentally overloading a method when you intended to override it.",
                    "Using final fields in enums.",
                    "Missing import statements for superclasses.",
                    "Unchecked generic casts.",
                    "It forces the compiler to confirm that the signature actually matches a supertype method.",
                ),
                q(
                    "What is the key advantage of a marker interface over a marker annotation?",
                    "It creates a real type that APIs can require in method signatures.",
                    "It can be applied to methods and fields.",
                    "It is always shorter to write.",
                    "It does not require any inheritance relationship.",
                    "A marker interface can be used for compile-time type checking and subtype restriction.",
                ),
                q(
                    "When is a marker annotation the better choice?",
                    "When the marker applies to non-type elements or fits an annotation-driven framework.",
                    "Whenever you need subtype checking at compile time.",
                    "Whenever the marker should be inherited by default.",
                    "Whenever the marker adds methods.",
                    "Annotations are the right fit for metadata on methods, fields, parameters, and framework hooks.",
                ),
                q(
                    "Why is Serializable a marker interface rather than a marker annotation?",
                    "Because serialization is a capability that is naturally modeled as a type.",
                    "Because annotations did not exist when serialization was invented.",
                    "Because marker annotations cannot have runtime retention.",
                    "Because interfaces cannot be checked by the compiler.",
                    "The interface lets APIs express and enforce a type-level contract for serializability.",
                ),
            ],
        ),
    ],
}
