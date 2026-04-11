from __future__ import annotations

from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Classes and Interfaces",
    "subtitle": "Effective Java Chapter 4, Items 15-25",
    "modules": [
        module(
            "Encapsulation and public API shape",
            [
                (
                    "Item 15: Hide implementation details",
                    slide(
                        [
                            "Information hiding is the main difference between a clean API and a brittle one.",
                            "Make each class or member as inaccessible as possible, then raise the level only when the design actually requires it.",
                        ],
                        image="../../page_previews/page_0094.png",
                        caption="Chapter opening and Item 15: encapsulation is the first design gate.",
                        points=[
                            "Top-level types are only package-private or public.",
                            "Members can be private, package-private, protected, or public.",
                            "Package-private is usually better than public for helper types.",
                        ],
                        source_pages=(94, 95),
                    ),
                ),
                (
                    "Member access levels are not symmetric",
                    slide(
                        [
                            "Private is for implementation only.",
                            "Package-private is for package-local cooperation.",
                            "Protected is a public commitment for subclasses and package peers, so treat it as API surface, not an internal convenience.",
                        ],
                        image="../../page_previews/page_0095.png",
                        caption="Item 15: access control exists to minimize what the outside world can depend on.",
                        code="""private -> top-level class only
package-private -> any class in package
protected -> package + subclasses
public -> everywhere""",
                        box=(
                            "note",
                            "If a public class needs many package-private helpers, revisit the package split instead of leaking more access.",
                        ),
                        source_pages=(95, 96),
                    ),
                ),
                (
                    "Item 16: Prefer accessors to public fields",
                    slide(
                        [
                            "A public field freezes the representation into the API.",
                            "For public classes, use private fields plus accessors and mutators when mutation is actually needed.",
                            "Public fields are mostly tolerable only for package-private or private nested classes, or for public constants with immutable values.",
                        ],
                        image="../../page_previews/page_0099.png",
                        caption="Item 16: public fields destroy encapsulation for exported classes.",
                        points=[
                            "You lose invariant checking.",
                            "You lose the ability to change representation later.",
                            "You lose the chance to run logic on field access or update.",
                        ],
                        source_pages=(99, 100),
                    ),
                ),
                (
                    "Public fields, arrays, and constants",
                    slide(
                        [
                            "A public static final array is still mutable through its elements, so it is a security hole.",
                            "Expose an unmodifiable list or return a clone of a private array instead.",
                            "Public immutable fields are less harmful than mutable ones, but they are still an API commitment.",
                        ],
                        image="../../page_previews/page_0100.png",
                        caption="Item 16: the Time example shows that immutable fields are still a compromise, not a default.",
                        code="""private static final Thing[] VALUES = { ... };
public static final List<Thing> VIEW =
    Collections.unmodifiableList(Arrays.asList(VALUES));

public static Thing[] values() {
    return VALUES.clone();
}""",
                        box=(
                            "warn",
                            "Never return a direct reference to a mutable array field from a public API.",
                        ),
                        source_pages=(100, 100),
                    ),
                ),
            ],
            [
                q(
                    "For a public class, what is the preferred access level for a helper type that is only used inside the package?",
                    "package-private",
                    "public",
                    "protected",
                    "private",
                    "Package-private keeps the type usable inside the package without exporting it as part of the public API.",
                    question_id="chapter4_m1_q1",
                ),
                q(
                    "Why are public mutable fields discouraged in exported classes?",
                    "They freeze representation into the API and prevent invariant enforcement",
                    "They make the class abstract",
                    "They speed up serialization automatically",
                    "They improve binary compatibility",
                    "A public mutable field exposes implementation details and removes the class's ability to control updates.",
                    question_id="chapter4_m1_q2",
                ),
                q(
                    "What is wrong with a public static final array field?",
                    "Its reference is final, but the array contents remain mutable",
                    "Arrays cannot be final",
                    "The compiler rejects all array constants",
                    "It cannot be read from other classes",
                    "The array object itself can still be modified through the returned reference.",
                    question_id="chapter4_m1_q3",
                ),
                q(
                    "Which statement about protected members of exported classes is correct?",
                    "They are part of the exported API and should be rare",
                    "They are invisible outside the package",
                    "They are always safer than private members",
                    "They are only relevant to interfaces",
                    "Protected members are a long-term compatibility promise, so they should be used sparingly.",
                    question_id="chapter4_m1_q4",
                ),
            ],
        ),
        module(
            "Immutability and composition",
            [
                (
                    "Item 17: Make classes immutable when possible",
                    slide(
                        [
                            "An immutable object cannot be observed in more than one state.",
                            "The five rules are strict: no mutators, no subclassing, all fields final, all fields private, and no external access to mutable components.",
                            "Defensive copies belong in constructors, accessors, and deserialization hooks when mutable inputs or outputs are involved.",
                        ],
                        image="../../page_previews/page_0101.png",
                        caption="Item 17: the immutable Complex example uses pure operations instead of in-place mutation.",
                        points=[
                            "Immutable objects are easier to reason about.",
                            "They are inherently thread-safe.",
                            "They make failure atomicity easier because state never changes after construction.",
                        ],
                        source_pages=(101, 103),
                    ),
                ),
                (
                    "Immutability trades speed for simplicity",
                    slide(
                        [
                            "Immutability can be expensive for large values or multistep updates because each step may allocate a fresh object.",
                            "Use static factories and cached instances when it helps, and consider a mutable companion class only if you actually need the performance win.",
                            "Small value objects should usually be immutable; larger values should be immutable unless profiling shows a real problem.",
                        ],
                        image="../../page_previews/page_0103.png",
                        caption="Item 17: sharing immutable objects is safe, and caching becomes practical.",
                        box=(
                            "note",
                            "If a class cannot be fully immutable, keep its state space small and its fields private final unless there is a concrete reason not to.",
                        ),
                        source_pages=(103, 104),
                    ),
                ),
                (
                    "Item 18: Favor composition over inheritance",
                    slide(
                        [
                            "Implementation inheritance is fragile because subclasses depend on superclass internals.",
                            "Composition keeps the existing class as a private component, and forwarding methods expose only the behavior you choose.",
                            "Use inheritance only when the subclass is truly an is-a subtype and the superclass is designed for extension.",
                        ],
                        image="../../page_previews/page_0108.png",
                        caption="Item 18: the wrapper pattern replaces fragile extension with forwarding.",
                        code="""public class InstrumentedSet<E> extends ForwardingSet<E> {
    private int addCount;
    public InstrumentedSet(Set<E> s) { super(s); }
    @Override public boolean add(E e) {
        addCount++;
        return super.add(e);
    }
}""",
                        source_pages=(108, 110),
                    ),
                ),
                (
                    "Inheritance is a subtype test, not a convenience",
                    slide(
                        [
                            "Ask one blunt question: is every B really an A?",
                            "If the answer is no, inheritance is the wrong model even if it looks shorter.",
                            "Wrappers are usually more robust because they avoid superclass API surprises and preserve your own abstraction boundaries.",
                        ],
                        image="../../page_previews/page_0110.png",
                        caption="Item 18: tagged classes and fragile subclasses both leak implementation choices.",
                        points=[
                            "Stack is not a Vector.",
                            "Properties is not a Hashtable.",
                            "Wrapper classes can add behavior without depending on superclass internals.",
                        ],
                        source_pages=(110, 112),
                    ),
                ),
            ],
            [
                q(
                    "Which rule is part of making a class immutable?",
                    "Make all fields private and final, and do not expose mutable internals",
                    "Make every method static",
                    "Avoid constructors entirely",
                    "Use public setters for all fields",
                    "Immutability requires fixed state and no external mutation channel.",
                    question_id="chapter4_m2_q1",
                ),
                q(
                    "Why are immutable objects attractive for concurrent code?",
                    "They are inherently thread-safe and need no synchronization",
                    "They cannot be serialized",
                    "They always allocate less memory",
                    "They eliminate the need for equals",
                    "If state never changes, concurrent readers cannot observe a race on that state.",
                    question_id="chapter4_m2_q2",
                ),
                q(
                    "What is the main risk of implementation inheritance across package boundaries?",
                    "The subclass can break when superclass internals change",
                    "The subclass cannot compile at all",
                    "The JVM forbids it",
                    "It automatically duplicates all methods",
                    "A subclass can depend on superclass behavior that was never part of the public contract.",
                    question_id="chapter4_m2_q3",
                ),
                q(
                    "What is the best general replacement for fragile subclassing of a concrete class?",
                    "Composition plus forwarding methods",
                    "A public tag field",
                    "More protected methods",
                    "A larger abstract superclass",
                    "Composition lets you control the exposed API and avoids tight coupling to internals.",
                    question_id="chapter4_m2_q4",
                ),
            ],
        ),
        module(
            "Inheritance contracts and interface design",
            [
                (
                    "Item 19: Document or prohibit inheritance",
                    slide(
                        [
                            "If a class is meant to be subclassed, its documentation must describe self-use of overridable methods precisely.",
                            "Constructors, clone, and readObject must never invoke overridable methods directly or indirectly.",
                            "If the class is not designed for extension, make that explicit by preventing subclassing.",
                        ],
                        image="../../page_previews/page_0114.png",
                        caption="Item 19: overridable self-use is a contract, not an accident.",
                        box=(
                            "warn",
                            "A constructor calling an override can observe a partially initialized subclass and break before the subclass finishes constructing.",
                        ),
                        source_pages=(114, 117),
                    ),
                ),
                (
                    "Prohibit inheritance when you do not intend it",
                    slide(
                        [
                            "Declare the class final, or make constructors private or package-private and expose static factories instead.",
                            "If a concrete class is not meant for extension, do not leave it half-open just for convenience.",
                            "If you must allow inheritance, remove self-use of overridable methods and document the safe hooks very carefully.",
                        ],
                        image="../../page_previews/page_0115.png",
                        caption="Item 19: final is often the cleanest way to keep fragile subclasses out.",
                        source_pages=(117, 119),
                    ),
                ),
                (
                    "Item 20: Prefer interfaces to abstract classes",
                    slide(
                        [
                            "Interfaces let unrelated classes share a type without forcing a hierarchy.",
                            "Abstract classes constrain you to single inheritance, which is expensive when the type should be mixin-like or retrofitted onto existing code.",
                            "If you need reusable implementation, pair the interface with a skeletal implementation class or default methods where appropriate.",
                        ],
                        image="../../page_previews/page_0120.png",
                        caption="Item 20: interfaces scale better for multiple implementations and mixins.",
                        points=[
                            "Interfaces define type without ownership of state.",
                            "Skeletal implementations shift repeated logic out of client code.",
                            "Default methods help, but they are not a blank check.",
                        ],
                        source_pages=(120, 123),
                    ),
                ),
                (
                    "Items 21 and 22: design interfaces carefully",
                    slide(
                        [
                            "Default methods can break existing implementations if they assume behavior the old code never promised.",
                            "Test new interfaces with multiple independent implementations before release.",
                            "Use interfaces to define types, not to dump constants into the namespace; constants belong in classes or enums, not constant interfaces.",
                        ],
                        image="../../page_previews/page_0125.png",
                        caption="Item 21 and Item 22: interface design should survive future releases, not just compile today.",
                        code="""public class PhysicalConstants {
    private PhysicalConstants() { }
    public static final double AVOGADROS_NUMBER = 6.022_140_857e23;
}""",
                        source_pages=(125, 129),
                    ),
                ),
            ],
            [
                q(
                    "What must a class document if it is designed for inheritance?",
                    "Its self-use of overridable methods and the effects of overriding them",
                    "Only its package name",
                    "Only its private fields",
                    "Nothing, because inheritance is self-documenting",
                    "Subclass authors need to know exactly which overridable methods the superclass calls and when.",
                    question_id="chapter4_m3_q1",
                ),
                q(
                    "Why are default methods risky when added to an existing interface?",
                    "They can silently break preexisting implementations at runtime",
                    "They cannot be compiled by javac",
                    "They are always ignored by clients",
                    "They forbid all abstract methods",
                    "Existing classes may inherit behavior that does not preserve their invariants.",
                    question_id="chapter4_m3_q2",
                ),
                q(
                    "Which is the best use of an interface according to Item 22?",
                    "To define a type that clients can use to refer to instances",
                    "To export constants without qualification",
                    "To store instance fields",
                    "To replace every utility class",
                    "Interfaces should describe what a type is, not merely provide a bag of constants.",
                    question_id="chapter4_m3_q3",
                ),
                q(
                    "What is a skeletal implementation class for?",
                    "It supplies reusable method bodies while leaving the type as an interface",
                    "It prevents all subclassing",
                    "It replaces every default method",
                    "It is only for constants",
                    "Skeletal implementations reduce the work of implementing an interface without forcing inheritance for clients.",
                    question_id="chapter4_m3_q4",
                ),
            ],
        ),
        module(
            "Tagged classes, member classes, and source files",
            [
                (
                    "Item 23: Replace tagged classes with hierarchies",
                    slide(
                        [
                            "A tagged class hides multiple flavors behind a tag field and switch statements, which makes the code verbose and fragile.",
                            "Use a class hierarchy instead: one abstract root and one concrete subclass per flavor.",
                            "The compiler then checks that each flavor initializes only its own state and implements the required behavior.",
                        ],
                        image="../../page_previews/page_0130.png",
                        caption="Item 23: the Figure example is the warning sign; the hierarchy is the fix.",
                        points=[
                            "No irrelevant fields per instance.",
                            "No giant switch statement over tag values.",
                            "No runtime surprise when a new flavor is added.",
                        ],
                        source_pages=(130, 132),
                    ),
                ),
                (
                    "Item 24: Prefer static member classes",
                    slide(
                        [
                            "Use a static member class when the nested type does not need an enclosing instance.",
                            "A nonstatic member class carries an implicit reference to the outer instance, which costs space and can accidentally retain objects longer than intended.",
                            "Choose nonstatic only when the nested object truly needs the enclosing object.",
                        ],
                        image="../../page_previews/page_0133.png",
                        caption="Item 24: hidden outer-instance references are easy to miss and hard to debug.",
                        code="""private static class Entry {
    private final K key;
    private V value;
}""",
                        source_pages=(133, 134),
                    ),
                ),
                (
                    "Nested class forms and when to use them",
                    slide(
                        [
                            "Anonymous classes are for short, one-off uses; local classes are for named helpers that stay inside a method; member classes are for reusable nested types.",
                            "Lambdas usually replace anonymous classes when you only need a function object.",
                            "If the nested type is public or protected and belongs to an exported API, the static-versus-nonstatic choice becomes a compatibility commitment.",
                        ],
                        image="../../page_previews/page_0134.png",
                        caption="Item 24: anonymous and local classes have tight limits and should stay short.",
                        source_pages=(134, 135),
                    ),
                ),
                (
                    "Item 25: One top-level class per source file",
                    slide(
                        [
                            "Multiple top-level classes in one source file create brittle compiler-order behavior and allow accidental duplicate definitions.",
                            "If helper types belong to one owner, prefer private static member classes instead of packing unrelated top-level types together.",
                            "One source file, one top-level class or interface, is the stable rule.",
                        ],
                        image="../../page_previews/page_0136.png",
                        caption="Item 25: separate source files avoid order-dependent surprises.",
                        code="""// Good
public class Main { }

// Better for helpers
private static class Helper { }""",
                        source_pages=(136, 137),
                    ),
                ),
            ],
            [
                q(
                    "Why are tagged classes discouraged?",
                    "They force irrelevant fields and switch logic into one brittle type",
                    "They cannot be instantiated",
                    "They are illegal in Java",
                    "They always use abstract methods",
                    "A tagged class mixes multiple flavors in one type, which is verbose and error-prone.",
                    question_id="chapter4_m4_q1",
                ),
                q(
                    "What is the hidden cost of a nonstatic member class?",
                    "It stores an implicit reference to its enclosing instance",
                    "It cannot access private fields",
                    "It is always abstract",
                    "It cannot be serialized",
                    "That enclosing-instance reference consumes space and can extend object lifetime unintentionally.",
                    question_id="chapter4_m4_q2",
                ),
                q(
                    "When is an anonymous class appropriate?",
                    "For a short one-off use where naming the type is unnecessary",
                    "For implementing multiple interfaces at once",
                    "For defining a public API class",
                    "For replacing every nested class",
                    "Anonymous classes are limited and should stay small; lambdas are usually preferred for function objects.",
                    question_id="chapter4_m4_q3",
                ),
                q(
                    "What is the rule for top-level source files in this chapter?",
                    "Limit each source file to one top-level class or interface",
                    "Put all utility classes in one file",
                    "Use multiple files only for public classes",
                    "Keep every nested type top-level",
                    "One top-level type per file avoids duplicate-definition and order-dependent compiler behavior.",
                    question_id="chapter4_m4_q4",
                ),
            ],
        ),
    ],
}
