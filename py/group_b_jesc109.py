from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

import generate_workshop as base


def clean(text: str) -> str:
    return dedent(text).strip()


def image_block(path: str, caption: str) -> str:
    return (
        f'<div style="margin:18px 0 10px;">'
        f'<img src="{path}" alt="{caption}" '
        f'style="width:100%;max-height:420px;object-fit:contain;border:1px solid #e2e8f0;'
        f'border-radius:12px;background:#f8fafc;">'
        f'<p style="font-size:0.95rem;color:#475569;margin-top:8px;">{caption}</p>'
        f"</div>"
    )


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def box(kind: str, text: str) -> str:
    return f'<div class="{kind}">{text}</div>'


def slide(paragraphs: list[str], image: str, caption: str, points: list[str], callout: tuple[str, str]) -> str:
    html = [f"<p>{p}</p>" for p in paragraphs]
    html.append(bullets(points))
    html.append(image_block(image, caption))
    html.append(box(callout[0], callout[1]))
    return base.clean_html("\n".join(html))


def q(prompt: str, correct: str, wrong_1: str, wrong_2: str, wrong_3: str, explanation: str) -> dict[str, object]:
    return {
        "question": prompt,
        "options": [correct, wrong_1, wrong_2, wrong_3],
        "answer": 0,
        "explanation": explanation,
    }


def module(name: str, slide_defs: list[tuple[str, str]], questions: list[dict[str, object]]) -> dict[str, object]:
    return {"name": name, "slides": [{"title": title, "content": content} for title, content in slide_defs], "questions": questions}


WORKSHOP = {
    "slug": "jesc109",
    "title": "Light - Reflection and Refraction",
    "subtitle": "Kid-friendly science workshop with tiny lessons and quick quizzes",
    "modules": [
        module(
            "M0: Light Helps Us See",
            [
                (
                    "Seeing Needs Light",
                    slide(
                        [
                            "We see objects when light reaches our eyes after bouncing off them or passing through them.",
                            "The chapter begins with a simple idea: in a dark room, objects are hard to see because no useful light is reaching the eye.",
                        ],
                        "page_previews/page_0001.png",
                        "The opening source page introduces straight-line travel of light and the first ideas about reflection.",
                        ["Light helps us see objects.", "Reflection happens when light bounces from a surface.", "A shadow or a mirror clue can tell us how light is moving."],
                        ("note", "<strong>Big idea:</strong> light is the messenger that lets us see other things.")
                    ),
                ),
                (
                    "The Two Laws of Reflection",
                    slide(
                        [
                            "The chapter states two simple rules for reflection: angle of incidence equals angle of reflection, and the incident ray, normal, and reflected ray all lie in the same plane.",
                            "Those rules explain why mirror images are so regular. A surface does not guess where to send light. It follows the same pattern every time.",
                        ],
                        "page_previews/page_0002.png",
                        "The early source pages list the laws of reflection and introduce image properties in a plane mirror.",
                        ["Angle of incidence = angle of reflection.", "The incident ray, normal, and reflected ray stay in one plane.", "Plane-mirror images are virtual, erect, and laterally inverted."],
                        ("tip", "<strong>Memory trick:</strong> the mirror is fair. It gives the same angle back that it receives.")
                    ),
                ),
            ],
            [
                q("How do we usually see an object?", "Light from the object reaches our eyes", "The object makes sound only", "The object always glows by itself", "The object turns into air", "We see because reflected or transmitted light enters the eye."),
                q("What is reflection of light?", "Light bouncing from a surface", "Light melting into water", "Light disappearing completely", "Light becoming a sound wave", "Reflection is the bouncing back of light from a surface."),
                q("Which law says the incoming angle equals the outgoing angle?", "Angle of incidence equals angle of reflection", "Angle of incidence is always zero", "The normal is a mirror", "The reflected ray bends toward the mirror", "This is one of the two laws of reflection."),
                q("What do the incident ray, normal, and reflected ray do?", "They lie in the same plane", "They make a triangle only", "They must be parallel", "They cannot touch the mirror", "The chapter states this as the second law of reflection."),
                q("What kind of image is formed by a plane mirror?", "Virtual and erect", "Real and upside down only", "Always tiny and black", "Only a shadow", "A plane mirror forms a virtual, erect image."),
                q("What does lateral inversion mean?", "Left and right appear swapped", "The image becomes invisible", "Top and bottom disappear", "The mirror changes color", "Plane mirrors reverse left-right appearance."),
                q("Why is a dark room hard to see in?", "Not enough light reaches the eyes", "The walls become liquid", "Sound stops working", "The mirror laws change", "Visibility depends on light reaching the eye."),
                q("Which word best matches light bouncing off a polished surface?", "Reflection", "Evaporation", "Freezing", "Filtration", "Reflection is the correct term."),
            ],
        ),
        module(
            "M1: Curved Mirrors and Images",
            [
                (
                    "Spoon Shapes and Spherical Mirrors",
                    slide(
                        [
                            "A shiny spoon can behave a little like a curved mirror. The inward-curved side acts like a concave mirror, while the outward-curved side acts like a convex mirror.",
                            "The chapter names the pole, centre of curvature, principal axis, and focus so we can talk about curved mirrors precisely.",
                        ],
                        "page_previews/page_0003.png",
                        "The source pages introduce spherical mirrors and the key points used to describe them.",
                        ["Concave mirrors curve inward.", "Convex mirrors curve outward.", "The pole, focus, and centre of curvature help describe the mirror shape."],
                        ("real", "<strong>Kid picture:</strong> one spoon side can make things look bigger; the other can give a wider view.")
                    ),
                ),
                (
                    "What Mirror Formula and Magnification Say",
                    slide(
                        [
                            "Concave mirrors can bring parallel rays together at a focus. Convex mirrors spread rays out as if they came from a point behind the mirror.",
                            "The chapter gives the mirror formula and magnification so you can predict image position and size. For spherical mirrors, 1/v + 1/u = 1/f, and magnification is m = -v/u.",
                        ],
                        "page_previews/page_0005.png",
                        "Later pages in the mirror section show image formation, sign convention, and the mirror formula.",
                        ["Concave mirrors can form real or virtual images.", "Convex mirrors usually give virtual, upright, smaller images.", "Magnification compares image height with object height."],
                        ("note", "<strong>Rule of thumb:</strong> if a mirror lets you see more of the world behind you, it is usually convex.")
                    ),
                ),
            ],
            [
                q("Which curved mirror bends inward like the inside of a spoon?", "Concave mirror", "Convex mirror", "Flat mirror", "Broken mirror", "A concave mirror curves inward."),
                q("Which curved mirror bends outward like the back of a spoon?", "Convex mirror", "Concave mirror", "Plane mirror", "Polished stone", "A convex mirror curves outward."),
                q("What is the point at the middle of a spherical mirror called?", "Pole", "Pupil", "Pixel", "Prism", "The pole is the centre point of the mirror surface."),
                q("What does a concave mirror do to rays parallel to its axis?", "It can bring them together at the focus", "It always sends them straight through", "It makes them stop", "It turns them into sound", "A concave mirror can converge parallel rays."),
                q("Why are convex mirrors used as rear-view mirrors?", "They give a wider field of view", "They make everything huge", "They reverse electricity", "They remove reflections", "Convex mirrors help drivers see more behind them."),
                q("What does magnification compare?", "Image height with object height", "Mirror size with room size", "Light speed with sound speed", "Colour with temperature", "Magnification is the ratio of image height to object height."),
                q("Which mirror usually forms a virtual and smaller image?", "Convex mirror", "Concave mirror", "Plane mirror", "Water surface", "Convex mirrors usually form virtual, erect, diminished images."),
                q("In the mirror formula 1/v + 1/u = 1/f, what does f mean?", "Focal length", "Field length", "Final angle", "Frame size", "f stands for focal length."),
            ],
        ),
        module(
            "M2: Refraction in Glass",
            [
                (
                    "Why Light Bends at a Boundary",
                    slide(
                        [
                            "Refraction happens when light moves from one transparent medium to another and changes direction.",
                            "A pencil in water can look bent, and text under a glass slab can look raised because light takes a different path in the new medium.",
                        ],
                        "page_previews/page_0013.png",
                        "The refraction section starts with common examples such as a pencil in water and a raised-looking line under glass.",
                        ["Refraction means bending at a boundary.", "Air to glass: bend toward the normal.", "Glass to air: bend away from the normal."],
                        ("tip", "<strong>Easy picture:</strong> light changes lanes when the material changes.")
                    ),
                ),
                (
                    "Glass Slabs and Refractive Index",
                    slide(
                        [
                            "A rectangular glass slab gives a neat result: the emergent ray is parallel to the incident ray, although it is shifted sideways.",
                            "The chapter also introduces refractive index, which compares the speed of light in vacuum with the speed of light in a medium.",
                        ],
                        "page_previews/page_0014.png",
                        "The source pages explain refraction through a glass slab and how the ray shifts sideways.",
                        ["A glass slab produces lateral displacement.", "The emergent ray stays parallel to the incident ray.", "Refractive index helps compare how strongly a medium bends light."],
                        ("real", "<strong>Think like a detective:</strong> if a pencil looks broken in water, the pencil did not actually break.")
                    ),
                ),
            ],
            [
                q("What is refraction?", "Bending of light when it enters a new medium", "Light turning into heat only", "Light vanishing completely", "Light stopping at the surface", "Refraction is the bending of light at a boundary."),
                q("When light goes from air to glass, it usually bends", "Toward the normal", "Away from the normal", "Into a circle", "It does not bend at all", "Air to glass is from rarer to denser, so the ray bends toward the normal."),
                q("When light goes from glass to air, it usually bends", "Away from the normal", "Toward the normal", "Only upward", "Only downward", "Glass to air is from denser to rarer, so the ray bends away from the normal."),
                q("What does a rectangular glass slab do to the emergent ray?", "It makes it parallel to the incident ray", "It makes it always perpendicular", "It turns it into a shadow", "It removes the ray", "The emergent ray is parallel, but laterally displaced."),
                q("Why does a pencil in water look bent?", "Light from the submerged part changes direction", "The pencil becomes soft", "Water pushes the pencil", "The eye closes one side", "Refraction makes the underwater part appear shifted."),
                q("What is lateral displacement?", "A sideways shift of the emergent ray", "A change in colour", "A change in mass", "A change in sound", "A glass slab shifts the ray sideways."),
                q("What does refractive index help compare?", "How strongly different media bend light", "How loud different media are", "How hot different media are", "How fast a pencil floats", "Refractive index is tied to how much a medium slows light."),
                q("Why do different materials bend light by different amounts?", "Because their refractive indices differ", "Because all light is the same everywhere", "Because mirrors are inside them", "Because temperature is always zero", "Different media have different refractive indices."),
            ],
        ),
        module(
            "M3: Lenses and Focus",
            [
                (
                    "How Lenses Form Images",
                    slide(
                        [
                            "A lens is a transparent material with at least one curved surface. Convex lenses bring rays together, while concave lenses spread them apart.",
                            "The chapter shows that lenses can make images that are real or virtual depending on where the object is placed.",
                        ],
                        "page_previews/page_0018.png",
                        "The lens section of the source chapter introduces image formation for convex and concave lenses.",
                        ["Convex lenses converge light.", "Concave lenses diverge light.", "Lens images can be real or virtual."],
                        ("note", "<strong>Picture it:</strong> a convex lens acts like a light helper that pulls rays together.")
                    ),
                ),
                (
                    "Lens Formula and Power",
                    slide(
                        [
                            "The chapter gives the lens formula 1/v - 1/u = 1/f and uses the same style of sign convention as mirrors, but measured from the optical centre.",
                            "It also defines power as the reciprocal of focal length. Power is useful because a lens with a short focal length bends light more strongly.",
                        ],
                        "page_previews/page_0025.png",
                        "The later pages summarize sign convention, the lens formula, and the power of a lens.",
                        ["Lens formula: 1/v - 1/u = 1/f", "Power P = 1/f", "Power is measured in dioptres (D)."],
                        ("tip", "<strong>Fast rule:</strong> shorter focal length means stronger lens power.")
                    ),
                ),
            ],
            [
                q("Which lens type converges light rays?", "Convex lens", "Concave lens", "Plane glass sheet", "Water puddle", "A convex lens brings rays together."),
                q("Which lens type diverges light rays?", "Concave lens", "Convex lens", "Mirror lens", "Pencil lens", "A concave lens spreads rays apart."),
                q("What is the lens formula given in the chapter?", "1/v - 1/u = 1/f", "1/u + 1/v = f", "u/v = f", "P = VI", "The chapter states the lens formula as 1/v - 1/u = 1/f."),
                q("What does lens power measure?", "How strongly the lens bends light", "How heavy the lens is", "How bright the room is", "How loud the lens is", "Power tells the converging or diverging strength of a lens."),
                q("What is the SI unit of lens power?", "Dioptre", "Newton", "Joule", "Metre per second", "Lens power is measured in dioptres."),
                q("What sign does a convex lens have for power?", "Positive", "Negative", "Zero always", "No sign is allowed", "A convex lens has positive power."),
                q("What sign does a concave lens have for power?", "Negative", "Positive", "Always zero", "No sign", "A concave lens has negative power."),
                q("Why is a lens with a short focal length considered strong?", "It bends light through larger angles", "It weighs more", "It is always thicker", "It makes shadows disappear", "Short focal length means stronger convergence or divergence."),
            ],
        ),
    ],
}


def attach_ids(modules: list[dict[str, object]]) -> None:
    for module_index, mod in enumerate(modules):
        for question_index, question in enumerate(mod["questions"], start=1):
            question["id"] = f"q{module_index}_{question_index}"


def main() -> None:
    modules = WORKSHOP["modules"]
    attach_ids(modules)

    base.TOPIC_SLUG = WORKSHOP["slug"]
    base.WORKSHOP_TITLE = WORKSHOP["title"]
    base.WORKSHOP_SUBTITLE = WORKSHOP["subtitle"]
    base.MODULES = modules

    slides = base.build_slides()
    quiz = base.build_quiz_data()
    html = base.build_html(slides, quiz)

    out = Path("output") / WORKSHOP["slug"]
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{WORKSHOP['slug']}_workshop.html").write_text(html, encoding="utf-8")
    (out / f"{WORKSHOP['slug']}_quiz.json").write_text(json.dumps(quiz, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
