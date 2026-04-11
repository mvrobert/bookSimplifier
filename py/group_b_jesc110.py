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
    "slug": "jesc110",
    "title": "The Human Eye and the Colourful World",
    "subtitle": "Kid-friendly science workshop with tiny lessons and quick quizzes",
    "modules": [
        module(
            "M0: Meet the Human Eye",
            [
                (
                    "A Living Camera",
                    slide(
                        [
                            "The human eye helps us see the world by focusing light on the retina. The cornea does the first bending, the lens makes fine adjustments, and the brain reads the signals.",
                            "The chapter compares the eye with a camera because both form an image on a light-sensitive surface. In the eye, that surface is the retina.",
                        ],
                        "page_previews/page_0001.png",
                        "The opening pages introduce the human eye as a light-focusing system that forms images on the retina.",
                        ["Cornea and lens bend light.", "The pupil controls how much light enters.", "The retina receives the image and sends signals onward."],
                        ("note", "<strong>Big idea:</strong> seeing is a teamwork job between the eye and the brain.")
                    ),
                ),
                (
                    "How the Eye Adjusts Focus",
                    slide(
                        [
                            "The eye can focus on both near and far objects because the lens changes shape. This ability is called accommodation.",
                            "A normal young eye can see clearly from about 25 cm to far away. That nearest clear distance is called the near point or least distance of distinct vision.",
                        ],
                        "page_previews/page_0002.png",
                        "The next source pages explain accommodation and the near point of a normal eye.",
                        ["Accommodation means changing focal length.", "The near point is about 25 cm for a normal young eye.", "Ciliary muscles help the lens change shape."],
                        ("tip", "<strong>Memory shortcut:</strong> near objects need a stronger bend, far objects need a gentler bend.")
                    ),
                ),
            ],
            [
                q("Which part of the eye receives the image?", "Retina", "Iris", "Pupil", "Eyelid", "The retina is the light-sensitive surface of the eye."),
                q("What is the cornea's main job in vision?", "It bends light entering the eye", "It stores food", "It makes the pupil", "It turns light into sound", "The cornea does much of the refraction at the front of the eye."),
                q("What does the pupil control?", "How much light enters the eye", "How tall a person is", "The size of the retina", "The colour of the iris only", "The pupil regulates light entering the eye."),
                q("What is accommodation?", "The eye lens changing its focal length", "The eye closing forever", "The retina moving away", "The iris becoming a mirror", "Accommodation is the eye's ability to adjust focus."),
                q("Which muscle helps change the lens shape?", "Ciliary muscles", "Biceps", "Heart muscles", "Toe muscles", "Ciliary muscles control the lens curvature."),
                q("For a normal young eye, the near point is about", "25 cm", "25 m", "2.5 cm", "2.5 m", "The source chapter gives about 25 cm."),
                q("Why is the human eye compared to a camera?", "Both form images on a light-sensitive surface", "Both use fuel", "Both can fly", "Both always magnify", "The retina acts like a camera screen."),
                q("What happens to signals from the retina?", "They go to the brain through optic nerves", "They stay in the pupil", "They turn into bones", "They leave as steam", "The optic nerves carry signals from eye to brain."),
            ],
        ),
        module(
            "M1: Vision Problems and Fixes",
            [
                (
                    "Myopia and Hypermetropia",
                    slide(
                        [
                            "Myopia, or near-sightedness, means distant objects look blurry while nearby ones look clear. Hypermetropia, or far-sightedness, means nearby objects look blurry while distant ones look clear.",
                            "The chapter shows that myopia is corrected with a concave lens, and hypermetropia is corrected with a convex lens.",
                        ],
                        "page_previews/page_0003.png",
                        "The defect-of-vision pages compare myopia and hypermetropia and show how spectacles correct them.",
                        ["Myopia affects distant vision.", "Hypermetropia affects near vision.", "Concave and convex lenses can correct these defects."],
                        ("real", "<strong>Kid clue:</strong> if the blackboard looks fuzzy from the back row, the eye may need a different lens shape.")
                    ),
                ),
                (
                    "Presbyopia and Cataract",
                    slide(
                        [
                            "As people age, the eye can lose some of its accommodation power. That age-related problem is called presbyopia. Another condition mentioned in the chapter is cataract, where the lens becomes cloudy and vision becomes impaired.",
                            "The important lesson is that good vision depends on healthy focusing parts. When one part changes, a suitable lens or surgery may be needed to help again.",
                        ],
                        "page_previews/page_0004.png",
                        "The source pages continue with presbyopia, near point changes, and cataract.",
                        ["Presbyopia is age-related loss of accommodation.", "Cataract makes the lens cloudy.", "Eye care can include lenses or surgery depending on the problem."],
                        ("tip", "<strong>Friendly reminder:</strong> normal vision is not the same as perfect vision forever. Eyes can change with age.")
                    ),
                ),
            ],
            [
                q("Myopia is also called", "Near-sightedness", "Far-sightedness", "Colour blindness", "Night blindness", "Myopia means nearby objects are seen more clearly than distant ones."),
                q("Which lens corrects myopia?", "Concave lens", "Convex lens", "Plane mirror", "Prism", "A concave lens helps the myopic eye focus distant objects on the retina."),
                q("Hypermetropia is also called", "Far-sightedness", "Near-sightedness", "Twinkling", "Dispersion", "Hypermetropia means nearby objects are hard to see clearly."),
                q("Which lens corrects hypermetropia?", "Convex lens", "Concave lens", "Flat glass", "Magnet", "A convex lens adds the needed convergence."),
                q("What is presbyopia?", "Loss of accommodation with age", "A type of mirror", "A colour in the rainbow", "A kind of battery", "Presbyopia is age-related weakening of focusing ability."),
                q("What is cataract?", "Clouding of the eye lens", "A bent pencil in water", "A bright star", "A glass slab", "Cataract makes the lens cloudy."),
                q("If a student cannot read the blackboard from the last row, which defect may be present?", "Myopia", "Hypermetropia always", "A prism effect", "A heating effect", "Difficulty seeing distant objects points to myopia."),
                q("Which part of the eye changes lens curvature?", "Ciliary muscles", "The pupil", "The retina", "The cornea", "Ciliary muscles help adjust focus."),
            ],
        ),
        module(
            "M2: Prism Colors and Rainbows",
            [
                (
                    "White Light Has Many Colours",
                    slide(
                        [
                            "A prism can spread white light into a band of colours. The chapter calls this dispersion.",
                            "It also explains that the angle of deviation is the amount by which the emergent ray turns away from the original direction.",
                        ],
                        "page_previews/page_0005.png",
                        "The prism activity shows how white light can split into a colourful band.",
                        ["Dispersion means splitting white light into colours.", "A prism bends different colours by different amounts.", "The angle of deviation measures the turn in the ray."],
                        ("note", "<strong>Picture to keep:</strong> a prism is like a colour sorter for light.")
                    ),
                ),
                (
                    "Rainbows and Colour in Nature",
                    slide(
                        [
                            "The chapter uses the same physics to explain rainbows and other colour effects. Sunlight can split into colours, and the atmosphere can also bend or scatter light so that the sky looks different at different times of day.",
                            "The important habit is to link the colourful scene back to light behaviour: refraction, dispersion, and scattering all play a part.",
                        ],
                        "page_previews/page_0006.png",
                        "Later pages connect dispersion with rainbow formation and colour effects in nature.",
                        ["Rainbows are linked with dispersion and refraction.", "The atmosphere can also change the look of light.", "Colour patterns in nature have physical reasons."],
                        ("real", "<strong>Nature clue:</strong> a rainbow is not paint in the sky. It is sunlight being split and bent.")
                    ),
                ),
            ],
            [
                q("What is dispersion of light?", "Splitting white light into colours", "Making light louder", "Turning light into heat", "Stopping the sun", "Dispersion is the separation of white light into its component colours."),
                q("What device in the chapter is used to show dispersion?", "Prism", "Lens", "Mirror", "Thermometer", "A prism separates white light into a colour band."),
                q("What is the angle of deviation?", "The angle between the original and emergent ray directions", "The colour of the sky", "The size of the prism", "The speed of sound", "It measures how much the ray is turned by the prism."),
                q("Which effect helps explain a rainbow?", "Dispersion", "Freezing", "Filtration", "Magnetism", "A rainbow is tied to dispersion and refraction."),
                q("Why do different colours separate in a prism?", "They bend by different amounts", "They all have the same speed", "They are different metals", "They are heavier", "Different colours refract differently in the prism."),
                q("What happens to white light in dispersion?", "It splits into a band of colours", "It becomes invisible", "It turns into sound", "It freezes into ice", "White light separates into its colours."),
                q("Which natural scene is often used as a rainbow example?", "A rainbow in the sky", "A cracked wall", "A metal spoon", "A chalk board", "Rainbows are the classic dispersion example."),
                q("Which three ideas are linked to colourful sky and rainbow scenes?", "Refraction, dispersion, and scattering", "Melting, freezing, and boiling", "Force, mass, and speed", "Charging, discharging, and fusing", "The chapter connects these light phenomena."),
            ],
        ),
        module(
            "M3: Twinkling and Blue Sky",
            [
                (
                    "Atmospheric Refraction in Real Life",
                    slide(
                        [
                            "The Earth's atmosphere bends light because it is not perfectly uniform. That is why stars twinkle and the Sun can seem to rise a little early and set a little late.",
                            "The chapter explains this as atmospheric refraction. The air changes density, light bends repeatedly, and the apparent position of objects can shift a little.",
                        ],
                        "page_previews/page_0008.png",
                        "The atmosphere pages explain twinkling, advanced sunrise, and delayed sunset.",
                        ["Twinkling of stars is due to atmospheric refraction.", "Sunrise appears a bit early and sunset a bit late.", "The air is not perfectly steady, so the bending changes slightly."],
                        ("tip", "<strong>Friendly image:</strong> the atmosphere is like a moving lens around Earth.")
                    ),
                ),
                (
                    "Scattering Makes the Sky Blue",
                    slide(
                        [
                            "Tiny particles in air scatter shorter wavelengths of light more strongly, so blue light reaches our eyes from many directions. That is why the clear sky looks blue.",
                            "The same scattering idea explains the Tyndall effect, the red colour of warning signals in fog, and the glowing path of a beam of light in a smoky room.",
                        ],
                        "page_previews/page_0009.png",
                        "The final source pages explain scattering, the blue sky, and why red signals stay visible.",
                        ["Scattering is the spreading of light by tiny particles.", "Blue light is scattered more strongly than red light.", "Red warning lights are useful because red is scattered less."],
                        ("note", "<strong>Big idea:</strong> the sky's colour is not paint. It is scattered sunlight.")
                    ),
                ),
            ],
            [
                q("Why do stars twinkle?", "Atmospheric refraction changes their apparent brightness and position", "Because stars blink on purpose", "Because the Moon pushes them", "Because they are underwater", "Twinkling comes from changing refraction in the atmosphere."),
                q("Why do we see the Sun a little before actual sunrise?", "Atmospheric refraction bends sunlight", "The Earth stops rotating", "The Sun moves faster", "The clouds turn into mirrors", "Refraction makes the Sun appear slightly higher than it really is."),
                q("Why is the clear sky blue?", "Blue light is scattered more strongly by air", "Blue paint is in the clouds", "The ocean reflects the sky", "The Sun is blue", "Shorter wavelengths are scattered more strongly."),
                q("What is the Tyndall effect?", "Visibility of a light beam due to scattering", "A lens formula", "A mirror law", "A sound wave", "Tyndall effect is seen when scattered light makes the beam path visible."),
                q("Why are danger signals often red?", "Red light is scattered less and stays visible farther away", "Red light is the brightest color in all weather", "Red light has no wavelength", "Red light makes fog disappear", "Red is least scattered by fog or smoke."),
                q("Which phenomenon explains the wavering of hot air above a fire?", "Atmospheric refraction", "Fusion", "Condensation", "Magnetism", "Hot air changes density and bends light differently."),
                q("Why do planets not twinkle much?", "They appear as extended sources, so variations average out", "They make no light at all", "They are closer to the Sun only", "They are made of glass", "Planets are not point-like, so twinkling averages away."),
                q("If Earth had no atmosphere, the sky would look", "Dark", "Always green", "Perfectly red", "Exactly white", "Without scattering in air, the sky would not appear blue."),
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
