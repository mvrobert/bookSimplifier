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
    "slug": "jesc111",
    "title": "Electricity",
    "subtitle": "Kid-friendly science workshop with tiny lessons and quick quizzes",
    "modules": [
        module(
            "M0: Current and Circuits",
            [
                (
                    "A Circuit Needs a Closed Path",
                    slide(
                        [
                            "Electric current is the flow of charge through a conductor. The chapter begins by showing that a battery, wire, bulb, and switch must make a closed loop before current can flow.",
                            "If the circuit is broken, the current stops. So the switch simply opens or closes the path that charges can travel through.",
                        ],
                        "page_previews/page_0001.png",
                        "The opening pages introduce current as flowing charge and explain why a circuit must be closed.",
                        ["Current is flow of charge.", "A circuit must be closed for current to flow.", "A switch opens or closes the path."],
                        ("note", "<strong>Simple picture:</strong> no path, no current.")
                    ),
                ),
                (
                    "Potential Difference Pushes Charges",
                    slide(
                        [
                            "Charges do not move on their own in a wire. A cell or battery creates a potential difference, which is like an electric push that keeps charges moving.",
                            "The chapter also introduces the ammeter and voltmeter. An ammeter measures current and is connected in series. A voltmeter measures potential difference and is connected in parallel.",
                        ],
                        "page_previews/page_0002.png",
                        "The source pages define current, charge, and potential difference, then show the basic circuit symbols.",
                        ["Potential difference is measured in volts.", "Current is measured in amperes.", "Ammeter is in series; voltmeter is in parallel."],
                        ("tip", "<strong>Kid analogy:</strong> voltage is the push, current is the flow.")
                    ),
                ),
            ],
            [
                q("What is electric current?", "Flow of electric charge", "A type of light bulb", "A kind of magnet", "A sound signal", "Current is the rate of flow of charge."),
                q("What is needed for current to flow in a simple circuit?", "A closed path", "An open gap", "A painted wire", "A warm desk", "Current flows only when the circuit is complete."),
                q("Which device measures current?", "Ammeter", "Voltmeter", "Thermometer", "Barometer", "An ammeter measures electric current."),
                q("How is an ammeter connected?", "In series", "In parallel only", "Not connected at all", "Inside the battery", "The ammeter must be in series with the circuit."),
                q("Which device measures potential difference?", "Voltmeter", "Ammeter", "Ruler", "Compass", "A voltmeter measures potential difference."),
                q("How is a voltmeter connected?", "In parallel", "In series only", "Not connected at all", "Across the sky", "A voltmeter is connected in parallel across the points."),
                q("What does a cell or battery provide in a circuit?", "Potential difference", "Only colour", "Only resistance", "Only sound", "The battery provides the push that moves charges."),
                q("What happens when the circuit is broken?", "Current stops flowing", "Current gets faster", "Voltage becomes sound", "The wire turns into glass", "A broken circuit cannot carry current."),
            ],
        ),
        module(
            "M1: Ohm's Law and Resistance",
            [
                (
                    "V and I Move Together",
                    slide(
                        [
                            "The chapter studies how potential difference and current are related using a nichrome wire. When the graph of V against I is a straight line through the origin, it shows that V is directly proportional to I.",
                            "That is Ohm's law: V = IR. Here R is resistance, the property that opposes current flow.",
                        ],
                        "page_previews/page_0004.png",
                        "The Ohm's law section shows a straight-line V-I graph for a nichrome wire.",
                        ["Ohm's law says V is proportional to I.", "The equation is V = IR.", "Resistance controls how much current flows."],
                        ("real", "<strong>Graph clue:</strong> a straight line through the origin means the ratio V/I stays constant.")
                    ),
                ),
                (
                    "What Changes Resistance",
                    slide(
                        [
                            "Resistance depends on the length, thickness, and material of a wire. A longer wire offers more resistance. A thicker wire offers less.",
                            "The chapter also introduces resistivity, which is a material property. It helps compare materials fairly, not just wires of different shapes.",
                        ],
                        "page_previews/page_0005.png",
                        "The source pages discuss resistance, resistivity, and the factors that affect current flow.",
                        ["Longer wire -> more resistance.", "Thicker wire -> less resistance.", "Resistivity helps compare materials themselves."],
                        ("tip", "<strong>Easy memory:</strong> long path, hard trip. Wide path, easier trip.")
                    ),
                ),
            ],
            [
                q("What does Ohm's law say?", "Voltage is directly proportional to current at constant temperature", "Current is always zero", "Resistance equals voltage squared", "Power is the same as charge", "The chapter states V is directly proportional to I when temperature stays the same."),
                q("What is the formula for Ohm's law?", "V = IR", "V = I/R", "R = VI", "P = I/t", "Ohm's law is written V = IR."),
                q("What is resistance?", "Opposition to the flow of current", "A kind of battery", "A type of wire color", "A form of light", "Resistance resists the flow of charges."),
                q("Which wire usually has greater resistance?", "A longer wire", "A shorter wire", "A thicker wire only", "A wet paper strip", "Resistance increases with length."),
                q("Which wire usually has less resistance?", "A thicker wire", "A thinner wire", "A longer wire", "A broken wire", "Greater area of cross-section lowers resistance."),
                q("What is resistivity?", "A material property related to resistance", "The voltage of a battery", "The speed of electrons in a bulb", "The colour of a wire", "Resistivity helps compare materials."),
                q("Why is a V-I graph useful?", "It shows whether V and I are proportional", "It tells the weather", "It removes resistance", "It makes a circuit open", "A straight V-I line is evidence of Ohm's law."),
                q("If resistance increases and voltage stays fixed, current usually", "Decreases", "Increases", "Becomes light", "Stops being measured", "From V = IR, larger R gives smaller I for fixed V."),
            ],
        ),
        module(
            "M2: Series and Parallel Resistors",
            [
                (
                    "Resistors in Series",
                    slide(
                        [
                            "In a series connection, resistors are joined end to end. The same current flows through each one, and the total resistance is the sum of the individual resistances.",
                            "The chapter points out a practical issue too: if one part of a series circuit breaks, the whole circuit stops.",
                        ],
                        "page_previews/page_0007.png",
                        "The series-resistor section shows that resistances add and the same current passes through each resistor.",
                        ["Series connection means one path.", "Equivalent resistance adds up.", "A break anywhere can stop the whole circuit."],
                        ("note", "<strong>Remember:</strong> series is like a single-file line.")
                    ),
                ),
                (
                    "Resistors in Parallel",
                    slide(
                        [
                            "In a parallel connection, each branch gets the same potential difference. The current splits between the branches, and the equivalent resistance becomes smaller than any one branch resistance.",
                            "That is why homes use parallel wiring. One appliance can be switched off without shutting down every other appliance in the house.",
                        ],
                        "page_previews/page_0008.png",
                        "The parallel-resistor section explains how current splits and why home wiring is done in parallel.",
                        ["Parallel connection gives multiple paths.", "Equivalent resistance becomes smaller.", "Devices can work independently in parallel."],
                        ("real", "<strong>Household clue:</strong> parallel wiring lets your fan and lamp work separately.")
                    ),
                ),
            ],
            [
                q("What happens to resistances in series?", "They add up", "They cancel out", "They become zero", "They turn into voltage", "In series, equivalent resistance is the sum of all resistances."),
                q("In a series circuit, the current through each resistor is", "The same", "Always different", "Always zero", "Not measurable", "The same current flows through the whole series path."),
                q("What happens to current in a parallel circuit?", "It splits among branches", "It disappears", "It becomes negative", "It always stays in one wire", "Parallel paths divide the current."),
                q("Why is home wiring done in parallel?", "Each appliance can work independently", "Because parallel circuits have no current", "Because resistors become infinite", "Because switches are removed", "Parallel wiring gives separate control to each device."),
                q("What is the equivalent resistance of resistors in series?", "Sum of the individual resistances", "Product of the resistances", "Always the smallest resistance", "Always zero", "Series resistance adds directly."),
                q("How does equivalent resistance in parallel compare with the smallest branch resistance?", "It is smaller", "It is always larger", "It is equal to the largest", "It becomes infinite", "Parallel combinations reduce total resistance."),
                q("What happens if one device fails in a series circuit?", "The whole circuit can stop", "All other devices get brighter", "Resistance disappears", "The battery vanishes", "A break in a series path stops current everywhere."),
                q("Which connection gives multiple paths for current?", "Parallel", "Series", "No connection", "Open switch only", "Parallel circuits provide more than one path."),
            ],
        ),
        module(
            "M3: Heating Effect and Power",
            [
                (
                    "Current Can Turn Into Heat",
                    slide(
                        [
                            "When current flows through a resistor, some electrical energy turns into heat. This is the heating effect of electric current. Devices like heaters, irons, and kettles use that effect on purpose.",
                            "The chapter gives Joule's law of heating: H = I2Rt. That means more current, more resistance, or more time can all increase the heat produced.",
                        ],
                        "page_previews/page_0010.png",
                        "The heating-effect pages show how electrical energy turns into heat in a resistor.",
                        ["Heating effect means electrical energy becomes heat.", "Joule's law: H = I2Rt.", "Heaters and irons use this effect."],
                        ("tip", "<strong>Think it through:</strong> a wire can do work or become warm, depending on the circuit.")
                    ),
                ),
                (
                    "Power and Energy Use",
                    slide(
                        [
                            "Electric power tells how fast electrical energy is used. The chapter writes power as P = VI, and also as P = I2R or P = V2/R. The unit is watt, and commercial energy is counted in kilowatt-hour.",
                            "That is why appliance labels matter. A 1000 W heater uses energy faster than a 100 W bulb, even though both use the same idea of current and voltage.",
                        ],
                        "page_previews/page_0011.png",
                        "The final pages of the chapter define electric power and the kilowatt-hour unit of energy.",
                        ["Power = rate of energy use.", "P = VI = I2R = V2/R.", "1 kWh is the commercial unit of electrical energy."],
                        ("real", "<strong>Money clue:</strong> the electricity bill is really a bill for energy used over time.")
                    ),
                ),
            ],
            [
                q("What is the heating effect of electric current?", "Electrical energy changing into heat", "Heat turning into light only", "A battery making water", "A magnet becoming charged", "Current through a resistor can dissipate energy as heat."),
                q("What is Joule's law of heating?", "H = I2Rt", "H = V/I", "H = R/I", "H = P/t", "The chapter states heat produced is proportional to I2, R, and t."),
                q("What does electric power tell us?", "How fast electrical energy is used", "How long a wire is", "How heavy a bulb is", "How red the current looks", "Power is the rate of energy consumption."),
                q("What is the formula for electric power?", "P = VI", "P = I/R", "P = V + I", "P = Rt", "The chapter gives P = VI."),
                q("Which unit is used for power?", "Watt", "Volt", "Ohm", "Coulomb", "Power is measured in watts."),
                q("What is 1 kWh?", "Energy used by 1 kW for 1 hour", "Current in one wire", "Voltage in one cell", "Resistance of one bulb", "Kilowatt-hour is the commercial unit of energy."),
                q("Which appliance is a good example of the heating effect?", "Electric iron", "Paper clip", "Pencil eraser", "Glass marble", "An iron uses heating effect on purpose."),
                q("If current increases in a resistor, the heat produced usually", "Increases", "Decreases to zero", "Cannot be measured", "Changes into sound only", "From H = I2Rt, more current means more heat."),
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
