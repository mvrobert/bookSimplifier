from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Chapter 5: Generics",
    "subtitle": "Effective Java, pages 138-177. Items 26-33: raw types, unchecked warnings, arrays vs lists, generic types and methods, bounded wildcards, varargs, and typesafe heterogeneous containers.",
    "modules": [
        module(
            "Raw Types and Unchecked Warnings",
            [
                (
                    "Raw types are legacy compatibility, not an API design choice",
                    slide(
                        [
                            "A raw type is the erased name of a generic type, such as `List` instead of `List<String>`.",
                            "Raw types exist for pre-generics compatibility, so they behave as if all type parameters were removed.",
                            "Using a raw type throws away compile-time checking and pushes failures to runtime.",
                        ],
                        image="../../page_previews/page_0138.png",
                        caption="Chapter 5 opener and the definition of raw types, page 138.",
                        source_pages=(138, 138),
                    ),
                ),
                (
                    "Unchecked warnings are evidence, not noise",
                    slide(
                        [
                            "Unchecked cast, method-invocation, and conversion warnings mean the compiler cannot prove type safety.",
                            "Do not suppress them globally. First fix the declaration, then suppress only the smallest provably safe scope.",
                            "If you cannot prove safety, the warning is telling you something real about possible heap pollution or `ClassCastException`.",
                        ],
                        image="../../page_previews/page_0144.png",
                        caption="Unchecked warnings and narrow `@SuppressWarnings` scope, page 144.",
                        source_pages=(144, 146),
                    ),
                ),
                (
                    "Use unbounded wildcards when the element type is unknown",
                    slide(
                        [
                            "If you only need to read from a generic type and do not care about the element type, use `?` instead of a raw type.",
                            "For example, `Set<?>` is typesafe and flexible, while `Set` is neither.",
                            "This is the correct way to express an unknown type argument in an API.",
                        ],
                        image="../../page_previews/page_0144.png",
                        caption="Replace raw types with `<?>` when the element type is irrelevant, page 144.",
                        source_pages=(144, 146),
                    ),
                ),
            ],
            [
                q(
                    "Why is `List<?>` preferable to a raw `List` when the element type is unknown?",
                    "It preserves compile-time type safety while still accepting any element type.",
                    "It allows inserting any object into the list without warnings.",
                    "It erases fewer runtime checks than a raw list.",
                    "It makes the list reifiable at runtime.",
                    "A wildcard expresses unknown type information without discarding generic checking; a raw type discards checking entirely.",
                    question_id="chapter_05_m1_q1",
                ),
                q(
                    "What should you do first when you see an unchecked warning?",
                    "Try to eliminate the warning by fixing the declaration or implementation.",
                    "Add `@SuppressWarnings(\"unchecked\")` to the class.",
                    "Ignore it because the compiler already accepted the code.",
                    "Convert the code to use raw types so the warning disappears.",
                    "Unchecked warnings are defects until you can prove the code is actually safe.",
                    question_id="chapter_05_m1_q2",
                ),
                q(
                    "What is the danger of using a raw collection type in client code?",
                    "It can let an invalid element through and defer the failure to runtime.",
                    "It automatically makes the collection immutable.",
                    "It prevents the collection from compiling with any methods.",
                    "It forces all elements to become `Object` references at runtime.",
                    "Raw types suppress generic checking, so a bad insertion can surface later as a `ClassCastException`.",
                    question_id="chapter_05_m1_q3",
                ),
                q(
                    "Where should `@SuppressWarnings(\"unchecked\")` normally be placed?",
                    "On the smallest declaration or statement scope that you can prove is safe.",
                    "On the entire package so all related warnings are silenced.",
                    "On the whole class to keep the source file clean.",
                    "On every method that uses generics.",
                    "The book’s rule is narrow scope only; broad suppression hides new problems.",
                    question_id="chapter_05_m1_q4",
                ),
                q(
                    "Why are raw types retained in the language at all?",
                    "To preserve binary and source compatibility with pre-generics code.",
                    "Because generic types cannot interoperate with old libraries.",
                    "Because the compiler requires raw types for all inheritance hierarchies.",
                    "Because raw types are more efficient than parameterized types.",
                    "Raw types are a compatibility escape hatch, not a recommended style.",
                    question_id="chapter_05_m1_q5",
                ),
            ],
        ),
        module(
            "Generic Types and Generic Methods",
            [
                (
                    "Generify the type, then push casts to the boundary",
                    slide(
                        [
                            "A generic class should expose its type parameter in the API instead of forcing clients to cast on every read.",
                            "When an array-backed generic class needs an `E[]`, create an `Object[]`, cast once, and suppress the warning only after proving the cast is safe.",
                            "The runtime array will still be `Object[]`; the generic type information exists only at compile time.",
                        ],
                        image="../../page_previews/page_0148.png",
                        caption="Generic arrays are illegal; collections are often the safer backing store, page 148.",
                        source_pages=(148, 150),
                    ),
                ),
                (
                    "Generic methods remove client-side casts",
                    slide(
                        [
                            "A generic method declares its own type parameter list before the return type, such as `<E> Set<E> union(...)`.",
                            "Use the same type variable consistently across parameters and the return type when they must match.",
                            "A generic method should compile without warnings and should not force callers to cast its result.",
                        ],
                        image="../../page_previews/page_0151.png",
                        caption="Generic method pattern and the typesafe heterogeneous container idea begin here, page 151.",
                        source_pages=(151, 155),
                    ),
                ),
                (
                    "Recursive type bounds express mutual comparability",
                    slide(
                        [
                            "The bound `<E extends Comparable<E>>` says that elements must be comparable to values of their own type.",
                            "Use this when the algorithm depends on a natural ordering that is defined by the elements themselves.",
                            "This is a precise constraint, not a guess: it tells the compiler which operations are legal on `E`.",
                        ],
                        image="../../page_previews/page_0151.png",
                        caption="Recursive type bounds and the `max` method, pages 151-177 summary region.",
                        source_pages=(151, 177),
                    ),
                ),
            ],
            [
                q(
                    "Why is `public static <E> Set<E> union(Set<E> s1, Set<E> s2)` better than a raw version?",
                    "It preserves the element type and eliminates unchecked warnings for callers.",
                    "It allows any set type to be passed without compile-time checks.",
                    "It removes the need for a return type.",
                    "It makes the method usable only with `Set<Object>`.",
                    "A generic method ties the inputs and output to a single type parameter.",
                    question_id="chapter_05_m2_q1",
                ),
                q(
                    "What does `<E extends Comparable<E>>` mean in practice?",
                    "Values of `E` can be compared to other values of the same `E`.",
                    "Values of `E` can be compared to any `Object`.",
                    "Values of `E` must be arrays.",
                    "Values of `E` must implement `Serializable`.",
                    "This recursive bound captures the usual self-comparable case used by `max`.",
                    question_id="chapter_05_m2_q2",
                ),
                q(
                    "When generifying a class backed by an array, what is the usual safe pattern?",
                    "Store an `Object[]`, cast once to `E[]`, and prove the cast is safe locally.",
                    "Create a `new E[]` array and suppress the compiler error.",
                    "Use a raw `List` internally to avoid warnings.",
                    "Expose the backing array so callers can manage typing.",
                    "The book’s preferred approach is a narrow, justified unchecked cast plus local suppression.",
                    question_id="chapter_05_m2_q3",
                ),
                q(
                    "Why are generic methods important even when the class itself is not generic?",
                    "They let utility APIs preserve type relationships without forcing casts.",
                    "They make every class automatically thread-safe.",
                    "They disable type inference so callers must specify everything explicitly.",
                    "They are only useful for collections libraries.",
                    "Many algorithms are naturally method-level generic, not class-level generic.",
                    question_id="chapter_05_m2_q4",
                ),
                q(
                    "What is the benefit of a recursive type bound over an unchecked cast?",
                    "The compiler can verify the intended ordering constraint at compile time.",
                    "It makes the type non-reifiable.",
                    "It allows raw types to compile faster.",
                    "It turns runtime errors into warnings.",
                    "A recursive bound encodes the contract directly instead of relying on comments or casts.",
                    question_id="chapter_05_m2_q5",
                ),
            ],
        ),
        module(
            "Lists, Arrays, and Wildcards",
            [
                (
                    "Arrays and generics enforce type safety differently",
                    slide(
                        [
                            "Arrays are covariant and reified, so their element type is checked at runtime.",
                            "Generics are invariant and erased, so their type arguments are enforced at compile time only.",
                            "That is why arrays can fail later with `ArrayStoreException`, while lists usually fail earlier with a compile-time error.",
                        ],
                        image="../../page_previews/page_0147.png",
                        caption="Arrays versus generics and the generic-array restriction, page 147.",
                        source_pages=(147, 150),
                    ),
                ),
                (
                    "Prefer `List<E>` to `E[]` when the API needs type safety",
                    slide(
                        [
                            "If a generic array creation error or an unchecked array cast appears, a list is often the better abstraction.",
                            "You may lose some compactness, but you gain type safety and smoother interaction with generic APIs.",
                            "The book treats the list substitution as the normal escape hatch for generic-array problems.",
                        ],
                        image="../../page_previews/page_0148.png",
                        caption="Use lists instead of generic arrays when the type system starts fighting you, page 148.",
                        source_pages=(147, 150),
                    ),
                ),
                (
                    "PECS is the rule for wildcard input parameters",
                    slide(
                        [
                            "Use `? extends T` for producers and `? super T` for consumers.",
                            "A producer gives you values of type `T` or a subtype; a consumer accepts values of type `T` or a supertype.",
                            "If a parameter both produces and consumes the same type, wildcards usually do not help.",
                        ],
                        image="../../page_previews/page_0160.png",
                        caption="Bounded wildcards and the PECS rule, page 160.",
                        source_pages=(160, 166),
                    ),
                ),
                (
                    "Capture wildcards with a private helper when necessary",
                    slide(
                        [
                            "A public `List<?>` API can be simple and flexible, even when the implementation needs a precise element type.",
                            "Use a private generic helper to capture the wildcard and let the compiler reason about the exact `E` internally.",
                            "This is how you keep the public API general without resorting to raw types or unsafe casts.",
                        ],
                        image="../../page_previews/page_0165.png",
                        caption="Wildcard capture and helper methods, page 165.",
                        source_pages=(164, 166),
                    ),
                ),
            ],
            [
                q(
                    "Why is `List<String>` not a subtype of `List<Object>`?",
                    "Because generic types are invariant.",
                    "Because `String` is not a subtype of `Object`.",
                    "Because lists are reified at runtime.",
                    "Because wildcards are required only for arrays.",
                    "Generics do not inherit subtype relationships the way arrays do.",
                    question_id="chapter_05_m3_q1",
                ),
                q(
                    "What is the most important difference between arrays and generics?",
                    "Arrays are reified and checked at runtime; generics are erased and checked at compile time.",
                    "Arrays are immutable; generics are mutable.",
                    "Generics support covariance; arrays do not.",
                    "Arrays never throw runtime exceptions.",
                    "The runtime type information that arrays keep is exactly why they behave differently.",
                    question_id="chapter_05_m3_q2",
                ),
                q(
                    "What does PECS stand for?",
                    "Producer-extends, consumer-super.",
                    "Parameter-equals-class structure.",
                    "Public APIs need capture-safe signatures.",
                    "Prefer erased collections over specialized collections.",
                    "It is the book’s mnemonic for choosing bounded wildcards.",
                    question_id="chapter_05_m3_q3",
                ),
                q(
                    "Why should return types generally not use bounded wildcards?",
                    "They force callers to deal with wildcards instead of giving them a precise result type.",
                    "They make the method less generic.",
                    "They disable type inference.",
                    "They always require a raw cast internally.",
                    "Wildcards are for input flexibility; return types should be as specific as possible.",
                    question_id="chapter_05_m3_q4",
                ),
                q(
                    "What is wildcard capture used for?",
                    "To let a private helper recover the exact type hidden behind `?`.",
                    "To convert any raw type into a parameterized type automatically.",
                    "To make arrays reified.",
                    "To eliminate the need for type parameters.",
                    "Capture lets implementation code regain precision without exposing it in the public API.",
                    question_id="chapter_05_m3_q5",
                ),
            ],
        ),
        module(
            "Varargs and Heterogeneous Containers",
            [
                (
                    "Generic varargs are legal, but they are a sharp edge",
                    slide(
                        [
                            "A varargs parameter is implemented as an array, so generic varargs can expose heap pollution if misused.",
                            "If a method stores into the varargs array or leaks that array to untrusted code, it is not safe.",
                            "A safe generic varargs method must treat the array as a read-only transport mechanism.",
                        ],
                        image="../../page_previews/page_0167.png",
                        caption="Generic varargs, heap pollution, and why the array matters, page 167.",
                        source_pages=(167, 171),
                    ),
                ),
                (
                    "@SafeVarargs is a promise, not decoration",
                    slide(
                        [
                            "Annotate only methods that cannot be overridden and that you have proven safe.",
                            "The annotation exists to silence client warnings for methods that are genuinely typesafe.",
                            "If a better API shape exists, a `List` parameter often avoids the problem entirely.",
                        ],
                        image="../../page_previews/page_0169.png",
                        caption="Safe generic varargs and `@SafeVarargs`, page 169.",
                        source_pages=(167, 171),
                    ),
                ),
                (
                    "Typesafe heterogeneous containers move the type parameter to the key",
                    slide(
                        [
                            "Normal containers parameterize the container itself; a heterogeneous container parameterizes the key instead.",
                            "Using `Class<T>` as a key lets one map hold values of many unrelated types without losing type safety.",
                            "This is the `Favorites` pattern: `putFavorite(Class<T>, T)` and `getFavorite(Class<T>)`.",
                        ],
                        image="../../page_previews/page_0172.png",
                        caption="Typesafe heterogeneous containers and `Class<T>` type tokens, page 172.",
                        source_pages=(172, 177),
                    ),
                ),
                (
                    "Bounded type tokens and `asSubclass` preserve runtime safety",
                    slide(
                        [
                            "A bounded type token restricts which `Class` objects can be used as keys or reflective selectors.",
                            "`Class.asSubclass` performs the checked narrowing from `Class<?>` to `Class<? extends Annotation>` or a similar bound.",
                            "That lets reflection-heavy APIs keep compile-time and runtime type information aligned.",
                        ],
                        image="../../page_previews/page_0176.png",
                        caption="Bounded type tokens and `Class.asSubclass`, page 176.",
                        source_pages=(175, 177),
                    ),
                ),
            ],
            [
                q(
                    "What is heap pollution in the context of generic varargs?",
                    "A parameterized type reference points to an object that is not actually of that type.",
                    "Any array created by the JVM at runtime.",
                    "A warning emitted whenever `List` is used.",
                    "A situation where `@SafeVarargs` is missing.",
                    "Heap pollution is the mismatch between the variable’s declared generic type and the object it refers to.",
                    question_id="chapter_05_m4_q1",
                ),
                q(
                    "When is `@SafeVarargs` appropriate?",
                    "Only when the method cannot be overridden and you have proven the varargs usage is safe.",
                    "On any method that takes at least one array parameter.",
                    "On every generic method automatically.",
                    "Only on methods that return arrays.",
                    "The annotation is a trust statement about a specific generic-varargs implementation.",
                    question_id="chapter_05_m4_q2",
                ),
                q(
                    "Why is `List` often a better API shape than a generic varargs parameter?",
                    "It avoids the array-backed varargs mechanism and the related heap-pollution warnings.",
                    "It makes the method reifiable.",
                    "It always performs better than arrays.",
                    "It removes the need for generics entirely.",
                    "A list parameter is often the simplest way to keep the API typesafe and warning-free.",
                    question_id="chapter_05_m4_q3",
                ),
                q(
                    "What is the key idea behind the `Favorites` pattern?",
                    "Use a parameterized key, usually `Class<T>`, to store and retrieve values of many types safely.",
                    "Store everything in a raw `Map` and cast at every call site.",
                    "Use arrays so the runtime can enforce the key type.",
                    "Use wildcard return types to maximize flexibility.",
                    "The container stays heterogeneous, while each access remains typechecked through the key.",
                    question_id="chapter_05_m4_q4",
                ),
                q(
                    "Why can `Favorites` safely call `type.cast(...)` on retrieval?",
                    "Because `Class.cast` performs a checked dynamic cast tied to the key’s runtime type.",
                    "Because `cast` is just syntactic sugar for a raw cast.",
                    "Because the map stores only primitive values.",
                    "Because all `Class` objects are reifiable wildcards.",
                    "The cast reestablishes the key/value type linkage at the point of use.",
                    question_id="chapter_05_m4_q5",
                ),
            ],
        ),
    ],
}
