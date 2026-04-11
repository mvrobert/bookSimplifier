from __future__ import annotations

from effective_java_common import module, q, slide


CHAPTER = {
    "title": "Chapter 12: Serialization",
    "subtitle": "Effective Java, pages 360-413. Items 85-90: avoid Java serialization when possible, treat Serializable as a serious API commitment, design a custom serialized form when needed, defend readObject like a constructor, prefer enum instance control over readResolve, and use the serialization proxy pattern for robust deserialization.",
    "modules": [
        module(
            "Avoid Java serialization unless you are forced into it",
            [
                (
                    "Item 85: the default advice is to use something else",
                    slide(
                        [
                            "Java serialization is not a neutral persistence format. It is an object-construction protocol with a large attack surface.",
                            "The safe default is to avoid it in new systems and use cross-platform structured-data formats such as JSON or protobuf instead.",
                            "If you inherit a legacy boundary that still uses serialization, treat every byte stream as hostile until proven otherwise.",
                        ],
                        image="../../page_previews/page_0360.png",
                        caption="Item 85 opens with the core warning: Java serialization is risky, broad, and easy to misuse, pages 360-361.",
                        points=[
                            "Never deserialize untrusted data.",
                            "Prefer JSON or protobuf for new protocols and persistence boundaries.",
                            "Treat deserialization as code execution against the class path, not as passive parsing.",
                        ],
                        source_pages=(360, 361),
                    ),
                ),
                (
                    "Gadgets, gadget chains, and deserialization bombs",
                    slide(
                        [
                            "The attack surface includes every serializable type that can be reached during deserialization, including platform classes and third-party libraries.",
                            "A gadget is a method that is triggered during deserialization and does something dangerous; a gadget chain combines several such methods into an exploit.",
                            "Even without gadgets, a short stream can cause extreme work or memory pressure. A deserialization bomb is still a denial-of-service attack.",
                        ],
                        image="../../page_previews/page_0361.png",
                        caption="Item 85 emphasizes gadget chains and deserialization bombs as practical exploit mechanisms, page 361.",
                        points=[
                            "RMI, JMX, and JMS can expose serialization indirectly.",
                            "A class does not need to be badly written to become part of an exploit chain.",
                            "A tiny input stream can expand into an enormous amount of work.",
                        ],
                        source_pages=(361, 363),
                    ),
                ),
                (
                    "If you cannot avoid it, filter and whitelist",
                    slide(
                        [
                            "If you are forced to deserialize, use `ObjectInputFilter` so the stream is checked before objects are materialized.",
                            "Prefer whitelisting over blacklisting. A blacklist only knows the threats you already recognize.",
                            "Filtering helps with class selection, deep graphs, and excessive size, but it is not a proof of safety.",
                        ],
                        image="../../page_previews/page_0363.png",
                        caption="Item 85 closes by recommending migration away from serialization and, if needed, filtering as a damage-control measure, pages 362-363.",
                        code="""ObjectInputFilter filter = ObjectInputFilter.Config.createFilter("com.example.**;java.base/*;!com.bad.**");
ObjectInputStream in = new ObjectInputStream(input);
in.setObjectInputFilter(filter);""",
                        source_pages=(362, 363),
                    ),
                ),
            ],
            [
                q(
                    "What is the safest default stance toward Java serialization in a new system?",
                    "Avoid it and use a cross-platform structured-data format instead",
                    "Use it for every boundary because it is built into the JDK",
                    "Use it only with public fields",
                    "Use it only if the class has a serialVersionUID",
                    "Item 85 says to prefer alternatives such as JSON or protobuf.",
                    question_id="chapter12_m1_q1",
                ),
                q(
                    "Why is Java deserialization dangerous even when the code does not look obviously broken?",
                    "It can invoke code in many reachable classes during object reconstruction",
                    "It automatically encrypts the payload",
                    "It only works for final classes",
                    "It refuses to run if the stream is short",
                    "The class path itself becomes part of the attack surface.",
                    question_id="chapter12_m1_q2",
                ),
                q(
                    "What is a deserialization bomb?",
                    "A small stream that expands into very expensive work or deep recursion during deserialization",
                    "A stream that always throws `ClassNotFoundException`",
                    "A stream that only works on arrays",
                    "A stream that can only be produced by `ObjectOutputStream` in debug mode",
                    "The danger is denial of service, not necessarily gadget-based code execution.",
                    question_id="chapter12_m1_q3",
                ),
                q(
                    "Why is whitelisting preferred over blacklisting when filtering input streams?",
                    "Because blacklists only block known bad cases, while whitelists start from an explicit safe set",
                    "Because blacklists are slower in every JVM",
                    "Because whitelists always prevent bombs",
                    "Because blacklists only work with enums",
                    "Item 85 treats whitelist-first filtering as the more defensible policy.",
                    question_id="chapter12_m1_q4",
                ),
            ],
        ),
        module(
            "Serializable is an exported API, not a private implementation detail",
            [
                (
                    "Item 86: implementing Serializable is a long-term commitment",
                    slide(
                        [
                            "Adding `implements Serializable` is easy, but the serialized form becomes part of the exported API of the class.",
                            "If you accept the default form, private and package-private fields are no longer just implementation details.",
                            "The price of serializability is reduced freedom to change the class later.",
                        ],
                        image="../../page_previews/page_0364.png",
                        caption="Item 86 explains that the serialized form becomes part of the public contract, pages 364-365.",
                        points=[
                            "A generated serialized form is tied to the current internal representation.",
                            "The serialized form must be supported across releases if instances already exist in the wild.",
                            "Changing a class structure can break compatibility at runtime.",
                        ],
                        source_pages=(364, 365),
                    ),
                ),
                (
                    "serialVersionUID, hidden constructors, and inheritance cost",
                    slide(
                        [
                            "Declare an explicit `serialVersionUID` in every serializable class. Do not let the runtime invent one for you.",
                            "Deserialization is a hidden constructor, so it must preserve invariants just like any other constructor.",
                            "Classes designed for inheritance and interfaces should rarely implement `Serializable`, because subclasses inherit the burden.",
                        ],
                        image="../../page_previews/page_0365.png",
                        caption="Item 86 also warns about hidden constructors, version compatibility, and inheritance costs, pages 365-366.",
                        code="""private static final long serialVersionUID = 1L;""",
                        source_pages=(365, 366),
                    ),
                ),
            ],
            [
                q(
                    "Why does implementing `Serializable` affect future class evolution?",
                    "Because the serialized form becomes part of the class's exported API",
                    "Because it prevents adding methods",
                    "Because it disables generics",
                    "Because it forces all fields to be public",
                    "The serialized form must remain compatible with deployed data.",
                    question_id="chapter12_m2_q1",
                ),
                q(
                    "What is the main practical reason to declare an explicit `serialVersionUID`?",
                    "To control compatibility instead of relying on a runtime-generated hash",
                    "To make serialization encrypt the stream",
                    "To force all subclasses to share the same stream",
                    "To make `readResolve` unnecessary",
                    "An explicit value avoids accidental incompatibility from unrelated source changes.",
                    question_id="chapter12_m2_q2",
                ),
                q(
                    "Why does the book call deserialization a hidden constructor?",
                    "Because object creation happens without an ordinary constructor call and still must establish invariants",
                    "Because it always invokes the no-arg constructor first",
                    "Because it only works for records",
                    "Because it can never fail",
                    "The point is that the class must defend itself even though construction is extralinguistic.",
                    question_id="chapter12_m2_q3",
                ),
                q(
                    "Which kinds of classes should rarely implement `Serializable`?",
                    "Extendable classes and active entities such as thread pools",
                    "Only final value objects",
                    "Only nested classes",
                    "Only enums",
                    "Item 86 says inheritance makes serialization much harder to support safely.",
                    question_id="chapter12_m2_q4",
                ),
            ],
        ),
        module(
            "Design the serialized form, then defend readObject",
            [
                (
                    "Item 87: choose logical state over physical representation",
                    slide(
                        [
                            "The default serialized form mirrors the object's physical representation. That is only acceptable when physical structure and logical content are nearly identical.",
                            "A class like `Name` is a good fit for the default form. A linked structure like `StringList` is not.",
                            "If you choose a custom serialized form, design it deliberately and document it with `@serial` and `@serialData`.",
                        ],
                        image="../../page_previews/page_0364.png",
                        caption="Item 87 contrasts a good default form with a bad one and pushes designers toward logical state.",
                        points=[
                            "Do not accept the default form by habit.",
                            "Use `transient` for fields that are derived or VM-specific.",
                            "Preserve the logical sequence, not the in-memory structure.",
                        ],
                        source_pages=(367, 373),
                    ),
                ),
                (
                    "Custom forms still need the serialization protocol methods",
                    slide(
                        [
                            "Even if every field is transient, call `defaultWriteObject` and `defaultReadObject` to preserve compatibility for future fields.",
                            "Serialize logical content explicitly in `writeObject` and rebuild it explicitly in `readObject`.",
                            "If the class is synchronized, `writeObject` must honor the same locking discipline as other whole-object operations.",
                        ],
                        image="../../page_previews/page_0365.png",
                        caption="Item 87 shows the `StringList` custom form with explicit writeObject/readObject logic.",
                        code="""private void writeObject(ObjectOutputStream s) throws IOException {
    s.defaultWriteObject();
    s.writeInt(size);
    for (Entry e = head; e != null; e = e.next)
        s.writeObject(e.data);
}""",
                        source_pages=(367, 373),
                    ),
                ),
                (
                    "Always declare an explicit serialVersionUID",
                    slide(
                        [
                            "An explicit `serialVersionUID` removes one more source of accidental incompatibility and avoids runtime computation.",
                            "If you want compatibility with an old serialized form, you must preserve the old value.",
                            "If you want to break compatibility intentionally, changing the value is the clean way to do it.",
                        ],
                        image="../../page_previews/page_0366.png",
                        caption="Item 87 closes by requiring an explicit `serialVersionUID` for every serializable class.",
                        source_pages=(367, 373),
                    ),
                ),
            ],
            [
                q(
                    "When is the default serialized form usually acceptable?",
                    "When the physical representation is already a good description of the logical state",
                    "Whenever the class has many methods",
                    "Only when the class is final",
                    "Only when the class has no constructors",
                    "Item 87 says the default form is fine only if it matches the logical data closely.",
                    question_id="chapter12_m3_q1",
                ),
                q(
                    "Why should derived or JVM-specific fields usually be declared `transient`?",
                    "They are not part of the logical serialized state and should not be persisted",
                    "They make `Serializable` compile faster",
                    "They are automatically encrypted otherwise",
                    "They are required for `readResolve`",
                    "Transient fields should not leak implementation details into the stream.",
                    question_id="chapter12_m3_q2",
                ),
                q(
                    "Why must `defaultWriteObject` and `defaultReadObject` still be called in a custom form?",
                    "To preserve compatibility if nontransient fields are added later",
                    "Because the JVM rejects custom forms without them",
                    "Because they serialize transient fields too",
                    "Because they make the stream human-readable",
                    "Skipping them breaks backward and forward compatibility expectations.",
                    question_id="chapter12_m3_q3",
                ),
                q(
                    "What is the most important rule for synchronization inside `writeObject`?",
                    "It must follow the same lock-ordering and whole-object consistency rules as other methods",
                    "It should never use a lock",
                    "It must always be static",
                    "It should only synchronize on `this` if the class is immutable",
                    "Serialization must respect the class's concurrency discipline.",
                    question_id="chapter12_m3_q4",
                ),
            ],
        ),
        module(
            "Defensive deserialization, readResolve, and serialization proxies",
            [
                (
                    "Item 88: readObject must act like a constructor with adversarial input",
                    slide(
                        [
                            "A `readObject` method must validate invariants and make defensive copies before exposing any mutable component.",
                            "Treat the byte stream as untrusted input, even if the class was originally serialized by your own code.",
                            "Do not call overridable methods from `readObject`, directly or indirectly, because the object is not fully formed yet.",
                        ],
                        image="../../page_previews/page_0360.png",
                        caption="Item 88 treats readObject as a public constructor that must defend invariants.",
                        points=[
                            "Copy mutable fields before checking invariants.",
                            "Throw `InvalidObjectException` when validation fails.",
                            "Never assume the stream came from a real instance of the class.",
                        ],
                        source_pages=(374, 379),
                    ),
                ),
                (
                    "Defensive copying closes the MutablePeriod-style attack",
                    slide(
                        [
                            "If a serializable immutable class contains private mutable components, the deserialized object can be attacked unless those components are copied defensively.",
                            "Validation must happen after the copy, not before it.",
                            "Final fields are inconvenient here: the defense may require removing `final` so the copied values can be reassigned safely during deserialization.",
                        ],
                        image="../../page_previews/page_0361.png",
                        caption="Item 88 shows how rogue object references can steal mutable components unless readObject defends them.",
                        code="""private void readObject(ObjectInputStream s)
        throws IOException, ClassNotFoundException {
    s.defaultReadObject();
    start = new Date(start.getTime());
    end = new Date(end.getTime());
    if (start.compareTo(end) > 0)
        throw new InvalidObjectException(start + " after " + end);
}""",
                        source_pages=(374, 379),
                    ),
                ),
                (
                    "Item 89 and Item 90: enum first, proxy second",
                    slide(
                        [
                            "If you need instance control, prefer an enum. `readResolve` works, but it is fragile and can be bypassed if you are careless with fields or subclassing.",
                            "A serialization proxy is safer still: `writeReplace` emits a nested proxy, `readObject` rejects direct deserialization, and the proxy's `readResolve` rebuilds the object through the public API.",
                            "Use the proxy pattern for non-extendable classes with real invariants. It is the cleanest way to make serialization behave like ordinary construction.",
                        ],
                        image="../../page_previews/page_0363.png",
                        caption="Items 89 and 90 contrast fragile `readResolve` tricks with the serialization proxy pattern.",
                        points=[
                            "Enums guarantee one instance per constant in ordinary use.",
                            "`readResolve` must be carefully scoped on nonfinal classes.",
                            "Serialization proxies are not for extendable classes or circular object graphs.",
                        ],
                        source_pages=(380, 413),
                    ),
                ),
            ],
            [
                q(
                    "Why must `readObject` behave like a constructor?",
                    "Because it creates an instance from attacker-controlled bytes and must establish all invariants",
                    "Because it is always invoked before fields are allocated",
                    "Because it can skip validation if `Serializable` is present",
                    "Because it only runs for enums",
                    "Item 88 says to validate and copy just as a real constructor would.",
                    question_id="chapter12_m4_q1",
                ),
                q(
                    "What is the point of defensively copying mutable components during `readObject`?",
                    "To prevent outsiders from retaining references to private mutable state",
                    "To reduce the number of serialized fields",
                    "To make the stream shorter",
                    "To avoid `defaultReadObject`",
                    "Without the copy, an attacker can keep aliases to the object's internals.",
                    question_id="chapter12_m4_q2",
                ),
                q(
                    "Why is an enum the preferred tool for a serializable singleton?",
                    "It gives the JVM a built-in instance-control guarantee that `readResolve` cannot match as safely",
                    "It automatically makes all fields transient",
                    "It removes the need for constructors in every class",
                    "It allows any number of runtime instances",
                    "Item 89 recommends enums over fragile `readResolve` tricks whenever possible.",
                    question_id="chapter12_m4_q3",
                ),
                q(
                    "What is the key benefit of the serialization proxy pattern?",
                    "It reconstructs the object through the public API instead of exposing raw internal state",
                    "It makes the object serializable without `Serializable`",
                    "It eliminates the need for a nested class",
                    "It works best only for extendable classes",
                    "The proxy shifts deserialization back into ordinary, validated object construction.",
                    question_id="chapter12_m4_q4",
                ),
            ],
        ),
    ],
}
