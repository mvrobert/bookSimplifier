from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Methods Common to All Objects",
    "subtitle": "Items 10-14: equals, hashCode, toString, clone, and Comparable",
    "modules": [
        module(
            "Equality and hash codes",
            [
                (
                    "Why Object methods matter",
                    slide(
                        [
                            "Object supplies five overridable methods with explicit contracts: equals, hashCode, toString, clone, and finalize.",
                            "This chapter focuses on the four that still matter for everyday library code, plus Comparable because it behaves like a companion contract for ordering.",
                            "If a class participates in collections, logging, or sorting, these methods are not cosmetic. They define observable behavior.",
                        ],
                        image="../../page_previews/page_0058.png",
                        caption="Chapter 3 opens by tying object methods to collection behavior and method contracts.",
                        box=(
                            "note",
                            "The practical failure mode is simple: once a contract is wrong, HashMap, HashSet, TreeMap, and TreeSet can misbehave in ways that are hard to diagnose.",
                        ),
                        source_pages=(58, 58),
                    ),
                ),
                (
                    "Equals contract and inheritance traps",
                    slide(
                        [
                            "Override equals only when the class has logical equality that differs from object identity.",
                            "The contract requires reflexive, symmetric, transitive, consistent behavior, and null must never compare equal.",
                            "Use instanceof for most value types; a getClass test breaks substitutability and usually makes subclasses stop behaving as their supertype.",
                        ],
                        image="../../page_previews/page_0043.png",
                        caption="The chapter shows why getClass-based equality and mixed-type equality both fail in real code.",
                        points=[
                            "Do not try one-way interoperability with a foreign type.",
                            "Do not extend an instantiable value class and add a new equality component unless you can accept the contract tradeoffs.",
                            "Favor composition when you need to add state and still preserve equality semantics.",
                        ],
                        code=(
                            "public final class CaseInsensitiveString {\n"
                            "    private final String s;\n"
                            "    @Override public boolean equals(Object o) {\n"
                            "        return o instanceof CaseInsensitiveString\n"
                            "                && ((CaseInsensitiveString) o).s.equalsIgnoreCase(s);\n"
                            "    }\n"
                            "}"
                        ),
                        source_pages=(38, 44),
                    ),
                ),
                (
                    "Hash codes that actually match equals",
                    slide(
                        [
                            "Every class that overrides equals must override hashCode as well.",
                            "Equal objects must produce the same hash code. Unequal objects may collide, but a good hash function should spread them out well enough to keep hash tables fast.",
                            "A constant hash code is legal but disastrous because it collapses every entry into one bucket and turns expected linear-time behavior into quadratic-time behavior.",
                        ],
                        image="../../page_previews/page_0051.png",
                        caption="Item 11 gives a field-based recipe and explains why 31 is the traditional multiplier.",
                        points=[
                            "Use only significant fields, meaning the fields that participate in equals.",
                            "Ignore derived fields that can be computed from those significant fields.",
                            "Cache the hash code only when the object is immutable and computing it is genuinely expensive.",
                        ],
                        code=(
                            "@Override public int hashCode() {\n"
                            "    int result = Short.hashCode(areaCode);\n"
                            "    result = 31 * result + Short.hashCode(prefix);\n"
                            "    result = 31 * result + Short.hashCode(lineNum);\n"
                            "    return result;\n"
                            "}"
                        ),
                        box=(
                            "warning",
                            "Do not hard-code the exact hash code in the API contract. That locks you into an implementation detail and makes future improvements painful.",
                        ),
                        source_pages=(50, 54),
                    ),
                ),
            ],
            [
                q(
                    "When is it reasonable to leave equals inherited from Object?",
                    "When each instance is inherently unique or the class has no logical equality concept",
                    "Whenever the class has many fields",
                    "Only when the class is final and public",
                    "Only when the class also overrides hashCode",
                    "Object identity is the right semantics for active entities and for classes that do not need logical equality.",
                    question_id="m1_q1",
                ),
                q(
                    "Which equals property is violated by one-way comparisons against String?",
                    "Symmetry",
                    "Reflexivity",
                    "Consistency",
                    "Null handling",
                    "If cis.equals(s) can be true while s.equals(cis) is false, the two objects do not agree on equality.",
                    question_id="m1_q2",
                ),
                q(
                    "Why does a getClass-based equals method often fail for subclasses?",
                    "It prevents a subtype from being equal to a valid supertype view of the same value",
                    "It makes hash codes slower to compute",
                    "It violates reflexivity for final classes",
                    "It forces every object to be mutable",
                    "A subclass is still an instance of the supertype, but getClass equality rejects that relationship outright.",
                    question_id="m1_q3",
                ),
                q(
                    "What is the main problem with a constant hashCode such as 42?",
                    "It is legal but collapses all entries into one bucket and destroys hash table performance",
                    "It makes equal objects unequal",
                    "It breaks reflexivity",
                    "It prevents compilation on modern JDKs",
                    "The contract allows collisions, but one bucket for everything is effectively a denial of service for hash tables.",
                    question_id="m1_q4",
                ),
                q(
                    "Which fields should participate in hashCode?",
                    "Only the significant fields used by equals",
                    "Every field, including transient and derived fields",
                    "Only primitive fields",
                    "Only fields declared final",
                    "hashCode must mirror equals, so it should be built from the same state that determines logical equality.",
                    question_id="m1_q5",
                ),
            ],
        ),
        module(
            "String form and copying",
            [
                (
                    "Why toString matters",
                    slide(
                        [
                            "Object.toString is usually not what clients want. A useful string should be concise, informative, and readable by a person.",
                            "toString is invoked implicitly by println, printf, concatenation, assert, and debuggers, so bad output leaks into logs whether you call it directly or not.",
                            "For value classes, document the exact format if you expect the string to be used as a stable human-readable representation or for round-tripping.",
                        ],
                        image="../../page_previews/page_0055.png",
                        caption="Item 12 argues for a readable diagnostic form and explains when to document the exact format.",
                        points=[
                            "Return all interesting state when that is practical.",
                            "Use a summary when the object is large or the state is not suitable for a literal dump.",
                            "If you specify a format, document it precisely and provide a matching parser, constructor, or factory when appropriate.",
                        ],
                        box=(
                            "note",
                            "If you do not override toString, every log message and debugger display that reaches your object will usually be far less useful than it should be.",
                        ),
                        source_pages=(55, 56),
                    ),
                ),
                (
                    "Clone is a protocol, not a constructor",
                    slide(
                        [
                            "Cloneable is unusual: it changes the behavior of Object.clone even though the interface declares no methods.",
                            "A well-behaved public clone should call super.clone first, return the concrete type, and then repair any mutable internal structure that the shallow copy leaves shared.",
                            "clone is fragile around mutable state, final fields, and overridable methods, so it behaves more like a special runtime protocol than a normal API.",
                        ],
                        image="../../page_previews/page_0060.png",
                        caption="The chapter shows the required super.clone pattern and why shallow copies become dangerous with mutable internals.",
                        code=(
                            "@Override public Stack clone() {\n"
                            "    try {\n"
                            "        Stack result = (Stack) super.clone();\n"
                            "        result.elements = elements.clone();\n"
                            "        return result;\n"
                            "    } catch (CloneNotSupportedException e) {\n"
                            "        throw new AssertionError();\n"
                            "    }\n"
                            "}"
                        ),
                        points=[
                            "Arrays are the one place where clone is usually the right copy mechanism.",
                            "If a clone method calls an overridable method during construction, the subclass can observe or corrupt a half-fixed object.",
                            "Public clone methods should not expose CloneNotSupportedException.",
                        ],
                        source_pages=(59, 64),
                    ),
                ),
                (
                    "Prefer copy constructors and factories",
                    slide(
                        [
                            "For almost every class, copy constructors or copy factories are safer than clone.",
                            "They avoid unchecked conventions, avoid checked exceptions, preserve final fields, and let the caller choose the implementation type in conversion constructors and factories.",
                            "A new interface should not extend Cloneable, and a new extendable class should usually not implement it.",
                        ],
                        image="../../page_previews/page_0065.png",
                        caption="Item 13 ends by recommending constructors or factories over Cloneable for most copy operations.",
                        points=[
                            "Use clone mainly when you inherit it from an existing Cloneable superclass or when copying arrays.",
                            "If the class is immutable, clone is usually pointless and should not be advertised as a normal copying path.",
                            "A class that needs deep copies of internal mutable structure must rebuild that structure explicitly.",
                        ],
                        box=(
                            "warning",
                            "Cloneable is not a general-purpose object-copying abstraction. Treat it as a legacy escape hatch, not a design default.",
                        ),
                        source_pages=(65, 65),
                    ),
                ),
            ],
            [
                q(
                    "What should a good toString method provide?",
                    "A concise but informative representation that a person can read",
                    "The exact hash code in hexadecimal",
                    "A full binary dump of every field",
                    "A string that cannot be parsed or logged",
                    "The contract explicitly favors human readability and useful diagnostics.",
                    question_id="m2_q1",
                ),
                q(
                    "When is it most useful to document the exact toString format?",
                    "For value classes where the string may be used as stable human-readable input and output",
                    "Only for private helper classes",
                    "Only when the class is mutable",
                    "Never, because formats should always be hidden",
                    "A precise format is helpful when the string representation is intended to be a standard representation.",
                    question_id="m2_q2",
                ),
                q(
                    "What is the required first step in a well-behaved clone implementation?",
                    "Call super.clone",
                    "Allocate the copy with new",
                    "Serialize the object to bytes",
                    "Throw CloneNotSupportedException immediately",
                    "The Object contract and the chapter both emphasize super.clone as the field-by-field base copy.",
                    question_id="m2_q3",
                ),
                q(
                    "Why can a shallow clone be dangerous for mutable internals?",
                    "The clone and the original may share mutable subobjects",
                    "It always violates equals",
                    "It makes the object non-final",
                    "It removes all constructors",
                    "If both objects point at the same mutable array or list, changes in one leak into the other.",
                    question_id="m2_q4",
                ),
                q(
                    "What is the preferred copy mechanism for most new classes?",
                    "A copy constructor or copy factory",
                    "A public clone method",
                    "A protected finalize method",
                    "A custom readObject method",
                    "The chapter treats constructors and factories as simpler, safer, and more flexible than Cloneable.",
                    question_id="m2_q5",
                ),
            ],
        ),
        module(
            "Comparable and ordering",
            [
                (
                    "Natural ordering and the compareTo contract",
                    slide(
                        [
                            "Comparable advertises a natural ordering for instances of the class.",
                            "compareTo is generic and is the single method that drives sorting, searching, and ordered collections such as TreeSet and TreeMap.",
                            "The contract is close to equals: antisymmetry, transitivity, and consistency across comparisons all matter, and consistency with equals is strongly recommended.",
                        ],
                        image="../../page_previews/page_0066.png",
                        caption="Item 14 frames Comparable as the ordered companion to equals.",
                        points=[
                            "If compareTo is inconsistent with equals, sorted collections may behave differently from hash-based collections.",
                            "The class should clearly document that inconsistency when it is intentional.",
                            "Cross-type comparisons usually fail with ClassCastException, and that is acceptable.",
                        ],
                        source_pages=(66, 68),
                    ),
                ),
                (
                    "Implement compareTo lexicographically",
                    slide(
                        [
                            "For multiple fields, compare from the most significant field to the least significant field and stop as soon as you find a nonzero result.",
                            "For primitive types, use the static compare methods. Do not subtract values and hope for the best.",
                            "For object fields, use their compareTo method or a Comparator when you need a nonstandard ordering.",
                        ],
                        image="../../page_previews/page_0069.png",
                        caption="The chapter recommends field-by-field lexicographic comparison and warns against subtraction-based order tests.",
                        code=(
                            "public int compareTo(PhoneNumber pn) {\n"
                            "    int result = Short.compare(areaCode, pn.areaCode);\n"
                            "    if (result == 0) {\n"
                            "        result = Short.compare(prefix, pn.prefix);\n"
                            "        if (result == 0)\n"
                            "            result = Short.compare(lineNum, pn.lineNum);\n"
                            "    }\n"
                            "    return result;\n"
                            "}"
                        ),
                        points=[
                            "Use Integer.compare, Long.compare, Double.compare, or their boxed equivalents instead of arithmetic subtraction.",
                            "Comparator.comparingInt and thenComparingInt make fluent lexicographic comparators easy to read.",
                            "Java 8 and later give you the comparator construction methods for all primitive and reference key types.",
                        ],
                        source_pages=(69, 71),
                    ),
                ),
                (
                    "Consistency with equals and BigDecimal",
                    slide(
                        [
                            "The chapter strongly recommends that compareTo return zero exactly when equals returns true, but that is a recommendation rather than a strict requirement.",
                            "BigDecimal is the standard example of a class whose natural ordering is inconsistent with equals, which means a HashSet and a TreeSet can report different sizes for the same inputs.",
                            "If you use a difference-based comparator, integer overflow and floating point artifacts can break transitivity and make the ordering wrong.",
                        ],
                        image="../../page_previews/page_0072.png",
                        caption="The closing advice is to use compare helpers and document any ordering that is intentionally inconsistent with equals.",
                        points=[
                            "Use static compare helpers or comparator construction methods instead of subtraction.",
                            "Document inconsistent natural orderings explicitly.",
                            "Remember that ordered collections consult compareTo, not equals, when deciding whether two elements are duplicates.",
                        ],
                        box=(
                            "warning",
                            "If two values compare as equal but are not equal according to equals, TreeSet and TreeMap will still treat them as duplicates.",
                        ),
                        source_pages=(71, 72),
                    ),
                ),
            ],
            [
                q(
                    "What does implementing Comparable advertise about a class?",
                    "That its instances have a natural ordering",
                    "That its instances are immutable",
                    "That its instances can be cloned safely",
                    "That its instances always have unique hash codes",
                    "Comparable is the marker for a class whose instances can be ordered without an external comparator.",
                    question_id="m3_q1",
                ),
                q(
                    "Why should you avoid subtracting one field value from another in compareTo?",
                    "Overflow and floating point edge cases can break the ordering",
                    "It cannot compile for any primitive type",
                    "It always returns zero",
                    "It makes the method abstract",
                    "The chapter calls difference-based comparison broken because arithmetic overflow can reverse the sign.",
                    question_id="m3_q2",
                ),
                q(
                    "Which statement about compareTo and equals is correct?",
                    "Consistency with equals is recommended but not required",
                    "They must always return the same result for every pair of objects",
                    "compareTo must never throw ClassCastException",
                    "equals is ignored by all sorted collections",
                    "The contract allows inconsistency, but the class should document it clearly when it exists.",
                    question_id="m3_q3",
                ),
                q(
                    "What do TreeSet and TreeMap use to decide element equality?",
                    "The ordering imposed by compareTo",
                    "Only object identity",
                    "Only hashCode",
                    "The finalize method",
                    "Sorted collections rely on ordering, so compareTo takes the role that equals plays in hash-based collections.",
                    question_id="m3_q4",
                ),
                q(
                    "Which helper is preferred for primitive comparisons inside compareTo?",
                    "The static compare methods such as Integer.compare and Short.compare",
                    "The minus operator",
                    "The instanceof operator",
                    "The clone method",
                    "Static compare helpers are clearer, safer, and less error-prone than subtraction.",
                    question_id="m3_q5",
                ),
            ],
        ),
    ],
}
