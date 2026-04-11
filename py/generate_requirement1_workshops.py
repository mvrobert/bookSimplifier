from __future__ import annotations

import json
from pathlib import Path

import generate_workshop as base


def image_block(path: str, caption: str) -> str:
    return (
        f'<div style="margin:18px 0 10px;">'
        f'<img src="{path}" alt="{caption}" '
        f'style="width:100%;max-height:420px;object-fit:contain;border:1px solid #e2e8f0;'
        f'border-radius:12px;background:#f8fafc;">'
        f'<p style="font-size:0.95rem;color:#475569;margin-top:8px;">{caption}</p>'
        f"</div>"
    )


def callout(kind: str, text: str) -> str:
    return f'<div class="{kind}">{text}</div>'


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def slide(paragraphs: list[str], image: str | None = None, caption: str | None = None, points: list[str] | None = None, box: tuple[str, str] | None = None) -> str:
    parts = [f"<p>{text}</p>" for text in paragraphs]
    if points:
        parts.append(bullets(points))
    if image and caption:
        parts.append(image_block(image, caption))
    if box:
        parts.append(callout(box[0], box[1]))
    return base.clean_html("\n".join(parts))


def q(prompt: str, correct: str, wrong_1: str, wrong_2: str, wrong_3: str, explanation: str) -> dict[str, object]:
    return {
        "question": prompt,
        "options": [correct, wrong_1, wrong_2, wrong_3],
        "answer": 0,
        "explanation": explanation,
    }


def module(name: str, slide_defs: list[tuple[str, str]], questions: list[dict[str, object]]) -> dict[str, object]:
    slides = [{"title": title, "content": content} for title, content in slide_defs]
    return {"name": name, "slides": slides, "questions": questions}


WORKSHOPS = [
    {
        "slug": "jesc102",
        "title": "Acids, Bases and Salts",
        "subtitle": "Kid-friendly science workshop with tiny lessons and quick quizzes",
        "modules": [
            module(
                "M0: Colour Clues and Safe Clues",
                [
                    (
                        "Meet Acids and Bases",
                        slide(
                            [
                                "Some everyday materials give us strong clues about their nature. Lemon juice and tamarind taste sour because they contain acids. Soap solution feels slippery because it is basic. In science, we do not taste unknown substances, so we learn to look for safer clues instead.",
                                "Indicators are the heroes here. They change colour when they meet acidic or basic solutions. That lets you identify what a liquid is doing without putting yourself at risk.",
                            ],
                            image="page_previews/page_0001.png",
                            caption="The opening source page introduces acids, bases, and colour indicators.",
                            points=[
                                "Acids are often linked with sour substances.",
                                "Bases are often linked with bitter or slippery materials.",
                                "Unknown chemicals should be tested with indicators, not by tasting.",
                            ],
                            box=("tip", "<strong>Try this thought game:</strong> If you had lemon juice, soap water, and plain water, which one would you expect to turn blue litmus red?")
                        ),
                    ),
                    (
                        "How Indicators Talk in Colours",
                        slide(
                            [
                                "Litmus, turmeric, methyl orange, phenolphthalein, and universal indicator all help us read a solution. Each one gives a different colour signal, so scientists choose the tool that matches the job.",
                                "Turmeric is especially fun because it links science with the kitchen. A yellow turmeric stain can become reddish-brown in a basic solution and then turn yellow again when washed well with water.",
                            ],
                            points=[
                                "Blue litmus turns red in an acid.",
                                "Red litmus turns blue in a base.",
                                "Universal indicator helps compare how strong or weak a solution is.",
                            ],
                            box=("note", "<strong>Remember:</strong> an indicator does not create acidity or basicity. It only reveals what is already there.")
                        ),
                    ),
                ],
                [
                    q("Which kind of substance is usually linked with a sour taste?", "Acid", "Base", "Salt", "Metal", "Sour taste is one common everyday clue for acids."),
                    q("Which safe tool helps you identify acids and bases without tasting them?", "Indicator", "Magnet", "Thermometer", "Pulley", "Indicators change colour to reveal acidic or basic nature."),
                    q("What happens to blue litmus paper in an acidic solution?", "It turns red", "It turns green", "It turns blue again", "It becomes colourless", "Blue litmus turning red is a classic acid test."),
                    q("What happens to red litmus paper in a basic solution?", "It turns blue", "It turns yellow", "It stays permanently red", "It melts", "Bases turn red litmus blue."),
                    q("Which kitchen material can act as a natural indicator?", "Turmeric", "Sand", "Salt crystals", "Charcoal", "Turmeric is a natural indicator mentioned in the source material."),
                    q("Why should you not taste an unknown laboratory liquid?", "Because it may be harmful", "Because it always tastes sweet", "Because tasting changes its pH", "Because it becomes a gas", "Safety comes first. Unknown chemicals should never be tasted."),
                    q("Which indicator is especially helpful for comparing the strength of acids and bases?", "Universal indicator", "Iron filings", "Copper wire", "Filter paper", "Universal indicator gives a colour range linked with pH."),
                    q("A soap solution is most likely to be", "basic", "acidic", "neutral gas", "metallic", "Soap solution is commonly basic."),
                ],
            ),
            module(
                "M1: Reactions and Neutralisation",
                [
                    (
                        "What Acids and Bases Do",
                        slide(
                            [
                                "Acids and bases do much more than change indicator colours. Acids can react with metals to produce a salt and hydrogen gas. Acids can also react with carbonates to release carbon dioxide. Those reactions give bubbles, which is a useful clue for learners.",
                                "Bases react with acids in a special way called neutralisation. When that happens, the sharp effect of the acid and the slippery effect of the base can cancel out, making salt and water.",
                            ],
                            image="page_previews/page_0006.png",
                            caption="A later source page shows reaction patterns and equations for acids, bases, and oxides.",
                            points=[
                                "Acid + metal -> salt + hydrogen",
                                "Acid + carbonate -> salt + water + carbon dioxide",
                                "Acid + base -> salt + water",
                            ],
                            box=("real", "<strong>Everyday link:</strong> Antacids help calm extra stomach acid because they contain mild basic substances.")
                        ),
                    ),
                    (
                        "Why Oxides Matter",
                        slide(
                            [
                                "Metal oxides usually behave like bases, while many non-metal oxides behave like acids. That is why metallic oxides often react with acids the way bases do. This idea helps you classify substances instead of memorising every example one by one.",
                                "When you think in reaction patterns, science becomes easier. Instead of seeing separate equations, you start spotting families of behaviour.",
                            ],
                            points=[
                                "Metal oxides often show basic character.",
                                "Non-metal oxides often show acidic character.",
                                "Neutralisation is one of the most useful reaction patterns in daily life.",
                            ],
                            box=("tip", "<strong>Quick check:</strong> If bubbles of carbon dioxide appear after adding acid to a chalk-like substance, a carbonate may be present.")
                        ),
                    ),
                ],
                [
                    q("When an acid reacts with a metal, which gas is usually released?", "Hydrogen", "Nitrogen", "Helium", "Chlorine", "Acid-metal reactions commonly produce hydrogen gas."),
                    q("When an acid reacts with a carbonate, which gas is released?", "Carbon dioxide", "Oxygen", "Hydrogen", "Argon", "Acids reacting with carbonates release carbon dioxide."),
                    q("What are the products of a neutralisation reaction?", "Salt and water", "Metal and oxygen", "Only gas", "Only water", "Neutralisation is the reaction between an acid and a base to form salt and water."),
                    q("Which kind of oxide usually behaves like a base?", "Metal oxide", "Non-metal oxide", "Noble gas oxide", "Water only", "Metal oxides generally show basic behaviour."),
                    q("Which kind of oxide often behaves like an acid?", "Non-metal oxide", "Metal oxide", "Plastic oxide", "Glass oxide", "Non-metal oxides often show acidic behaviour."),
                    q("Why do antacids help a person with too much stomach acid?", "They contain basic substances that neutralise acid", "They increase the acid quickly", "They freeze the stomach", "They remove all water from the stomach", "Antacids work through neutralisation."),
                    q("Which observation may suggest that a carbonate is reacting with an acid?", "Fizzing or bubbling", "The liquid becomes magnetic", "The beaker disappears", "The solution always turns black", "Carbon dioxide gas causes fizzing in acid-carbonate reactions."),
                    q("Which word best describes a reaction in which acid and base cancel each other's effect?", "Neutralisation", "Rusting", "Distillation", "Filtration", "Neutralisation is the correct scientific term."),
                ],
            ),
            module(
                "M2: The pH Scale",
                [
                    (
                        "Reading the pH Number Line",
                        slide(
                            [
                                "The pH scale is a handy number line from 0 to 14. Numbers below 7 show acidity, 7 shows neutrality, and numbers above 7 show basicity. The farther a value is from 7, the stronger the acidic or basic effect tends to be.",
                                "This is useful because science becomes more precise. Instead of only saying a liquid is acidic, you can compare whether it is weakly acidic like rainwater or strongly acidic like concentrated acid.",
                            ],
                            image="page_previews/page_0010.png",
                            caption="The pH activity pages turn colour changes into a number scale from 0 to 14.",
                            points=[
                                "pH less than 7 -> acidic",
                                "pH equal to 7 -> neutral",
                                "pH greater than 7 -> basic",
                            ],
                            box=("note", "<strong>Important idea:</strong> lower pH means stronger acidity, while higher pH means stronger basicity.")
                        ),
                    ),
                    (
                        "Why pH Matters in Real Life",
                        slide(
                            [
                                "Your body and your surroundings care about pH. Tooth enamel can start getting damaged when the mouth becomes too acidic for too long. Farmers check soil conditions because crops do better within a suitable pH range. Even our digestive system depends on acids and bases being controlled carefully.",
                                "That makes pH more than a lab topic. It is a tool for health, farming, cleaning, and environmental care.",
                            ],
                            points=[
                                "Very acidic food leftovers can affect teeth.",
                                "Soil pH can influence plant growth.",
                                "Digestive comfort can depend on acid-base balance.",
                            ],
                            box=("tip", "<strong>Kid memory trick:</strong> Think of 7 as the middle seat. Acid sits on one side, base sits on the other.")
                        ),
                    ),
                ],
                [
                    q("What pH value is considered neutral?", "7", "0", "3", "14", "A neutral solution has pH 7."),
                    q("A solution with pH 3 is", "acidic", "basic", "metallic", "neutral gas", "Any pH below 7 is acidic."),
                    q("A solution with pH 11 is", "basic", "acidic", "neutral", "salt only", "Any pH above 7 is basic."),
                    q("Which direction on the pH scale shows stronger acidity?", "Toward 0", "Toward 14", "Toward 7 from both sides equally", "There is no pattern", "Lower pH values mean stronger acidity."),
                    q("Which direction on the pH scale shows stronger basicity?", "Toward 14", "Toward 0", "Toward 7 only", "Toward 1", "Higher pH values mean stronger basicity."),
                    q("Why is pH useful in farming?", "Because soil pH affects plant growth", "Because it turns plants into metals", "Because it removes sunlight", "Because it measures wind speed", "The right soil pH helps crops grow well."),
                    q("Why is very low pH harmful to tooth enamel?", "Strong acidity can damage it", "It makes teeth magnetic", "It turns teeth into salt", "It increases chlorophyll", "Acidic conditions can erode tooth enamel."),
                    q("Which tool is commonly used to estimate pH through colour change?", "Universal indicator", "Compass", "Ruler", "Spring balance", "Universal indicator links colour shades to pH values."),
                ],
            ),
            module(
                "M3: Helpful Salts in Daily Life",
                [
                    (
                        "Common Salt Does More Than Season Food",
                        slide(
                            [
                                "Common salt is not just something sprinkled on food. It is an important raw material for making many useful substances. From one familiar starting material, chemists can prepare sodium hydroxide, baking soda, bleaching powder, and more.",
                                "This is a powerful science lesson: ordinary-looking substances can become the starting point for many useful products when we understand reactions properly.",
                            ],
                            image="page_previews/page_0014.png",
                            caption="The source pages connect common salt with several useful products of daily life.",
                            points=[
                                "Common salt is a useful chemical raw material.",
                                "It helps in making several products used at home and in industry.",
                                "Salts can have very different uses from the substances that formed them.",
                            ],
                            box=("real", "<strong>Look around:</strong> baking soda in kitchens, bleaching powder in sanitation, and plaster materials in classrooms all connect with salt chemistry.")
                        ),
                    ),
                    (
                        "Baking Soda, Washing Soda and POP",
                        slide(
                            [
                                "Baking soda helps in baking and is also used in some antacids. Washing soda is useful for cleaning and softening hard water. Plaster of Paris, often called POP, is valuable for casts, moulds, and decorative shapes because it sets into a hard solid after mixing.",
                                "These examples show why science is exciting for kids: the chemistry in your classroom, kitchen, and health kit is full of hidden stories.",
                            ],
                            points=[
                                "Baking soda can release carbon dioxide while heating or reacting.",
                                "Washing soda helps in cleaning work.",
                                "Plaster of Paris is made from gypsum and sets after mixing.",
                            ],
                            box=("tip", "<strong>Mini challenge:</strong> Next time you see a chalky white powder, ask yourself whether it is food-related, cleaning-related, or building-related chemistry.")
                        ),
                    ),
                ],
                [
                    q("Which familiar substance is an important raw material for making many useful chemicals?", "Common salt", "Sand only", "Coal only", "Plastic only", "Common salt is a major raw material in this topic."),
                    q("Which substance is commonly used in baking and some antacids?", "Baking soda", "Copper sulphate", "Iron rust", "Graphite", "Baking soda has both kitchen and health-related uses."),
                    q("Which substance is useful for cleaning and softening hard water?", "Washing soda", "Lime water", "Hydrogen gas", "Nitrogen gas", "Washing soda is used in cleaning and water treatment."),
                    q("What does POP stand for?", "Plaster of Paris", "Power of Pressure", "Point of pH", "Part of Plastic", "POP is the short form of Plaster of Paris."),
                    q("Plaster of Paris is useful for making", "casts and moulds", "electric current", "rainbows", "oxygen cylinders", "POP is widely used for casts, moulds, and decorative items."),
                    q("Which product is often used for sanitation and disinfection?", "Bleaching powder", "Sugar", "Iron nails", "Chalk dust", "Bleaching powder is used in sanitation-related work."),
                    q("What is one reason salts are interesting in science?", "They can have very different uses in daily life", "They never react", "They only exist in gases", "They always taste sweet", "Different salts have very different properties and uses."),
                    q("Which gas can be released from baking soda in some reactions?", "Carbon dioxide", "Hydrogen", "Neon", "Helium", "Baking soda can release carbon dioxide in suitable reactions."),
                ],
            ),
        ],
    },
    {
        "slug": "jesc103",
        "title": "Metals and Non-metals",
        "subtitle": "Kid-friendly science workshop with tiny lessons and quick quizzes",
        "modules": [
            module(
                "M0: Spotting Metals",
                [
                    (
                        "Shiny, Strong and Shapeable",
                        slide(
                            [
                                "Metals often stand out because they are lustrous, which means they have a shiny surface when freshly cleaned. Many metals can be hammered into sheets or stretched into wires, so they are useful for tools, utensils, and electrical work.",
                                "Non-metals are usually different. They are often dull, brittle, and poor conductors, though science always keeps a few exceptions to make things interesting.",
                            ],
                            image="page_previews/page_0001.png",
                            caption="The opening source page begins by comparing the physical properties of metals and non-metals.",
                            points=[
                                "Lustre means shine.",
                                "Malleability means a metal can be hammered into sheets.",
                                "Ductility means a metal can be drawn into wires.",
                            ],
                            box=("tip", "<strong>Picture this:</strong> Wires need ductility, foil needs malleability, and bells need sonority.")
                        ),
                    ),
                    (
                        "Useful Clues and Surprising Exceptions",
                        slide(
                            [
                                "Most metals conduct heat and electricity well, which is why copper and aluminium are so useful. Many are sonorous too, so they produce a ringing sound when struck.",
                                "But not every metal acts exactly the same. Sodium is soft enough to cut with a knife, and mercury is liquid at room temperature. Learning science means noticing patterns without forgetting exceptions.",
                            ],
                            points=[
                                "Metals are usually hard, but sodium is soft.",
                                "Mercury is a liquid metal.",
                                "Most non-metals are poor conductors, but graphite is a useful exception.",
                            ],
                            box=("note", "<strong>Smart habit:</strong> A good science learner says “usually” when talking about properties, because exceptions matter.")
                        ),
                    ),
                ],
                [
                    q("What does metallic lustre mean?", "A shiny surface", "A rough surface", "A sour taste", "A gas bubble", "Lustre means shine."),
                    q("Which property allows a metal to be hammered into sheets?", "Malleability", "Brittleness", "Acidity", "Neutrality", "Malleability is the ability to form sheets."),
                    q("Which property allows a metal to be drawn into wires?", "Ductility", "Rusting", "Softness", "Transparency", "Ductility is needed for making wires."),
                    q("Why is copper widely used in electrical wiring?", "It conducts electricity well", "It is a gas", "It is always colourless", "It is softer than wax", "Copper is an excellent conductor."),
                    q("Which metal is liquid at room temperature?", "Mercury", "Iron", "Copper", "Magnesium", "Mercury is the common liquid metal."),
                    q("Which metal is soft enough to cut with a knife?", "Sodium", "Gold", "Iron", "Zinc", "Sodium is unusually soft for a metal."),
                    q("What does sonorous mean?", "Makes a ringing sound when struck", "Turns litmus red", "Breaks into powder in water", "Always floats", "Metals such as bells are described as sonorous."),
                    q("Which non-metal is a well-known conductor exception?", "Graphite", "Sulphur", "Phosphorus", "Iodine", "Graphite conducts electricity even though it is a non-metal."),
                ],
            ),
            module(
                "M1: Reactions of Metals and Non-metals",
                [
                    (
                        "How Metals React",
                        slide(
                            [
                                "Metals react with oxygen to form metal oxides, and many of those oxides are basic in nature. Some metals react quickly, some slowly, and some need heating. That difference in speed helps us compare reactivity.",
                                "Metals can also react with water and acids. Very reactive metals like sodium and potassium react so strongly that they are stored carefully to stop unwanted contact with air or moisture.",
                            ],
                            image="page_previews/page_0006.png",
                            caption="The middle pages focus on how different metals react with oxygen, water, and acids.",
                            points=[
                                "More reactive metals react faster.",
                                "Metal + acid can give salt + hydrogen gas.",
                                "Sodium and potassium need very careful handling.",
                            ],
                            box=("warn", "<strong>Safety note:</strong> Highly reactive metals are never classroom toys. They must be handled with strict care.")
                        ),
                    ),
                    (
                        "Why Non-metals Behave Differently",
                        slide(
                            [
                                "Non-metals often form acidic oxides when they react with oxygen. They usually do not react with acids in the same dramatic way that many metals do. That makes them easy to compare with metals in reaction tables.",
                                "Some metal oxides, such as those of aluminium and zinc, can react with both acids and bases. These are called amphoteric oxides, a useful word that shows chemistry likes categories with edge cases.",
                            ],
                            points=[
                                "Metal oxides are often basic.",
                                "Many non-metal oxides are acidic.",
                                "Amphoteric oxides can react with both acids and bases.",
                            ],
                            box=("real", "<strong>Thinking like a scientist:</strong> Instead of memorising one example, ask what pattern the example belongs to.")
                        ),
                    ),
                ],
                [
                    q("When a metal reacts with oxygen, what is commonly formed?", "Metal oxide", "Metal chloride only", "Sugar", "Soap", "Metal + oxygen usually forms a metal oxide."),
                    q("What gas is often produced when a metal reacts with an acid?", "Hydrogen", "Neon", "Oxygen only", "Carbon monoxide", "Metal-acid reactions commonly release hydrogen."),
                    q("Which pair of metals is stored carefully because it reacts very strongly?", "Sodium and potassium", "Gold and silver", "Copper and iron", "Lead and tin", "Sodium and potassium are highly reactive."),
                    q("Many metal oxides are", "basic", "always neutral", "always acidic", "living", "Metal oxides often show basic character."),
                    q("Many non-metal oxides are", "acidic", "always metallic", "always neutral", "always liquid", "Non-metal oxides commonly show acidic character."),
                    q("An oxide that reacts with both acids and bases is called", "amphoteric", "neutral only", "inert", "radioactive", "Aluminium oxide and zinc oxide are common amphoteric examples."),
                    q("Why do metals show different speeds of reaction?", "Because they have different reactivities", "Because they all have the same reactivity", "Because oxygen changes into metal", "Because acids disappear", "Reactivity differences explain reaction speed."),
                    q("Which metal reaction clue may show that hydrogen is being produced?", "Bubbling or fizzing", "The metal becomes invisible", "The beaker becomes magnetic", "Everything freezes instantly", "Gas release is often seen as fizzing."),
                ],
            ),
            module(
                "M2: Reactivity and Ionic Compounds",
                [
                    (
                        "Why Reactivity Order Matters",
                        slide(
                            [
                                "Some metals are very reactive, some are moderately reactive, and some are much less reactive. This order matters because a more reactive metal can often displace a less reactive metal from its compound.",
                                "The same idea helps in extraction. Very reactive metals are harder to obtain from their ores, while less reactive metals can sometimes be found in a free state in nature.",
                            ],
                            image="page_previews/page_0014.png",
                            caption="Later pages connect reactivity with extraction and natural occurrence of metals.",
                            points=[
                                "A more reactive metal can replace a less reactive one.",
                                "Highly reactive metals are usually found as compounds.",
                                "Less reactive metals may be found free in nature.",
                            ],
                            box=("note", "<strong>Useful clue:</strong> Reactivity helps explain both lab reactions and mining processes.")
                        ),
                    ),
                    (
                        "What Makes Ionic Compounds Special",
                        slide(
                            [
                                "When metals react with non-metals, electrons can be transferred and ionic compounds can form. These compounds are often hard, have high melting points, and conduct electricity when molten or dissolved in water.",
                                "That combination of properties makes ionic compounds very different from many covalent substances you meet later in carbon chemistry.",
                            ],
                            points=[
                                "Ionic compounds are often hard solids.",
                                "They usually have high melting and boiling points.",
                                "They conduct electricity in molten state or in solution.",
                            ],
                            box=("tip", "<strong>Memory hook:</strong> solid ionic compounds hold ions tightly, but melted or dissolved ionic compounds let ions move around.")
                        ),
                    ),
                ],
                [
                    q("What can a more reactive metal do to a less reactive metal in a compound?", "Displace it", "Turn it into water", "Make it disappear completely", "Always freeze it", "Displacement depends on reactivity order."),
                    q("Highly reactive metals are usually found in nature as", "compounds", "free shining pieces", "gases only", "plants", "Highly reactive metals usually combine with other substances."),
                    q("Less reactive metals may sometimes be found", "in free state", "only in acids", "only in water", "inside indicators", "Gold and similar metals can occur free in nature."),
                    q("What type of compound often forms when metals react with non-metals?", "Ionic compound", "Only organic compound", "Protein", "Plastic", "Metal-non-metal reactions often produce ionic compounds."),
                    q("Ionic compounds usually have", "high melting points", "very low melting points like ice cream", "no solid form", "no charged particles", "Strong ionic attraction gives high melting points."),
                    q("When do ionic compounds conduct electricity well?", "When molten or dissolved in water", "Only as solid blocks", "Only when frozen", "Never", "Ions need freedom to move in order to conduct."),
                    q("Why do solid ionic compounds conduct poorly?", "Their ions cannot move freely", "They have no charges at all", "They become wood", "They lose all atoms", "In the solid state the ions are fixed in place."),
                    q("Which idea helps explain both metal extraction and displacement reactions?", "Reactivity", "Colour alone", "Taste alone", "Shape alone", "Reactivity is the connecting idea."),
                ],
            ),
            module(
                "M3: Corrosion, Alloys and Uses",
                [
                    (
                        "Why Rusting Is a Big Deal",
                        slide(
                            [
                                "Metals are useful, but they can slowly get damaged. Iron rusts when it reacts with oxygen and moisture. This is a kind of corrosion, and it costs money, time, and effort because bridges, tools, and machines need protection.",
                                "Science fights back with methods like painting, oiling, greasing, galvanising, and alloying. Each method tries to stop oxygen, water, or unwanted reactions from attacking the metal surface.",
                            ],
                            image="page_previews/page_0018.png",
                            caption="The closing source pages connect metal science with alloys, corrosion, and daily use.",
                            points=[
                                "Corrosion damages metal objects.",
                                "Rusting is corrosion of iron.",
                                "Protective coatings slow down corrosion.",
                            ],
                            box=("real", "<strong>Everyday engineering:</strong> bicycles, gates, and water tanks last longer when metal surfaces are protected.")
                        ),
                    ),
                    (
                        "Why We Make Alloys",
                        slide(
                            [
                                "Pure metals are not always the best choice. Gold is soft, iron can rust, and some metals need extra strength. An alloy is a mixture of metals, or a metal with a small amount of another element, made to improve useful properties.",
                                "Brass, bronze, and steel are famous examples. Alloys can be harder, stronger, or more resistant to corrosion than the pure metals they come from.",
                            ],
                            points=[
                                "An alloy is made to improve properties.",
                                "Steel is stronger than pure iron for many jobs.",
                                "Jewellery gold is often mixed with other metals for hardness.",
                            ],
                            box=("tip", "<strong>Design thinking:</strong> Scientists and engineers do not just ask “What is this metal?” They also ask “What job must this metal do?”")
                        ),
                    ),
                ],
                [
                    q("What is rusting?", "Corrosion of iron", "Melting of copper", "Freezing of mercury", "A neutralisation reaction", "Rusting is the corrosion of iron."),
                    q("Which two things are important for rusting iron?", "Oxygen and moisture", "Sunlight and sand", "Only nitrogen", "Only carbon dioxide", "Rusting needs both oxygen and moisture."),
                    q("Which method can help protect iron from rusting?", "Painting or galvanising", "Cutting it into smaller pieces", "Adding sugar", "Heating it every hour", "Protective coatings reduce contact with air and water."),
                    q("What is an alloy?", "A mixture made to improve metal properties", "A single pure metal only", "A type of gas", "A kind of acid", "Alloys are designed mixtures."),
                    q("Why is pure gold often mixed with other metals?", "To make it harder", "To turn it into a gas", "To make it sour", "To remove shine", "Pure gold is soft, so jewellery uses harder mixtures."),
                    q("Which material is an alloy widely used for strength?", "Steel", "Oxygen", "Graphite", "Chlorophyll", "Steel is a useful strong alloy."),
                    q("Why do engineers use alloys?", "To get better properties than pure metals", "To remove all atoms", "To stop metals from existing", "To make everything acidic", "Alloys can be stronger or more corrosion-resistant."),
                    q("Corrosion is a problem because it", "damages useful metal objects", "always improves strength", "creates food", "turns metal into plants", "Corrosion weakens and damages metal structures."),
                ],
            ),
        ],
    },
    {
        "slug": "jesc104",
        "title": "Carbon and its Compounds",
        "subtitle": "Kid-friendly science workshop with tiny lessons and quick quizzes",
        "modules": [
            module(
                "M0: Why Carbon Is Special",
                [
                    (
                        "The Tiny Builder Element",
                        slide(
                            [
                                "Carbon is special because it can form a huge variety of compounds. A big reason is tetravalency, which means one carbon atom can form four bonds. Another reason is catenation, which means carbon atoms can join to other carbon atoms to make chains, branches, and rings.",
                                "That is why carbon shows up everywhere: food, fuels, fibres, medicines, plastics, and living bodies all rely on carbon chemistry.",
                            ],
                            image="page_previews/page_0001.png",
                            caption="The opening source page introduces carbon as a versatile element used in many daily-life materials.",
                            points=[
                                "Carbon can form four bonds.",
                                "Carbon atoms can join with one another.",
                                "Huge numbers of compounds become possible.",
                            ],
                            box=("tip", "<strong>Think of carbon like a smart connector toy:</strong> four joining points and lots of ways to build.")
                        ),
                    ),
                    (
                        "Covalent Bonds and Their Style",
                        slide(
                            [
                                "In many carbon compounds, atoms share electrons instead of transferring them. That shared connection is called a covalent bond. Because of this bonding style, many carbon compounds have lower melting and boiling points than ionic compounds and usually do not conduct electricity.",
                                "That difference in bonding explains a big difference in behaviour. Structure and properties are linked.",
                            ],
                            points=[
                                "Covalent bonding involves sharing electrons.",
                                "Many carbon compounds are poor conductors.",
                                "Bonding helps explain properties.",
                            ],
                            box=("note", "<strong>Science shortcut:</strong> If you know the bonding style, you can often predict some properties.")
                        ),
                    ),
                ],
                [
                    q("What does tetravalency of carbon mean?", "Carbon forms four bonds", "Carbon has four colours", "Carbon is always a gas", "Carbon dissolves every metal", "Tetravalency means carbon has combining capacity of four."),
                    q("What does catenation mean?", "Carbon atoms link to each other", "Carbon turns into oxygen", "Carbon becomes an acid", "Carbon loses all bonds", "Catenation is the ability to form chains with itself."),
                    q("Why can carbon form so many compounds?", "Because of tetravalency and catenation", "Because it is always molten", "Because it never bonds", "Because it has only one valency", "Those two features together create huge variety."),
                    q("A covalent bond is formed by", "sharing electrons", "throwing away all electrons", "only transferring neutrons", "breaking the atom completely", "Covalent bonding involves sharing electrons."),
                    q("Many carbon compounds are poor conductors because they are mainly", "covalent", "metallic", "radio waves", "alloys", "Covalent compounds generally conduct poorly."),
                    q("Which element is central in food, fuels, and many living structures?", "Carbon", "Helium", "Neon", "Argon", "Carbon chemistry is everywhere in daily life."),
                    q("What kind of shapes can carbon skeletons form?", "Chains, branches, and rings", "Only squares", "Only triangles", "Only liquids", "Carbon can build many structural patterns."),
                    q("Which type of compounds often has lower melting points than ionic compounds?", "Many covalent carbon compounds", "All metal oxides", "Alloys only", "Salts only", "Covalent compounds often melt more easily than ionic ones."),
                ],
            ),
            module(
                "M1: Hydrocarbons and Families",
                [
                    (
                        "Saturated and Unsaturated Friends",
                        slide(
                            [
                                "Hydrocarbons are compounds made of only carbon and hydrogen. If all carbon-carbon bonds are single, the compound is saturated. If double or triple bonds appear, the compound is unsaturated.",
                                "That one change makes a big difference in reactivity. Unsaturated compounds can take part in addition reactions more easily.",
                            ],
                            image="page_previews/page_0010.png",
                            caption="The source pages group hydrocarbons into families and compare their formulas.",
                            points=[
                                "Single bonds only -> saturated",
                                "Double or triple bonds -> unsaturated",
                                "Structure affects reactivity",
                            ],
                            box=("tip", "<strong>Quick image:</strong> Saturated means “full” of single bonds. Unsaturated leaves room for extra joining.")
                        ),
                    ),
                    (
                        "Homologous Series Make Patterns Easy",
                        slide(
                            [
                                "Chemists love patterns, and homologous series are a great example. Members of a homologous series have similar structures and similar chemical behaviour. Each next member differs by a small repeating unit.",
                                "This means you do not need to memorise every compound separately. Once you understand the family pattern, many names and formulas make more sense.",
                            ],
                            points=[
                                "Members of a homologous series show a pattern.",
                                "Similar structure often means similar chemical properties.",
                                "A repeating unit helps organise the family.",
                            ],
                            box=("note", "<strong>Pattern power:</strong> Science gets easier when you spot families instead of isolated facts.")
                        ),
                    ),
                ],
                [
                    q("A hydrocarbon contains only", "carbon and hydrogen", "carbon and oxygen", "hydrogen and nitrogen", "carbon and iron", "Hydrocarbons are made only of carbon and hydrogen."),
                    q("A saturated hydrocarbon has", "only single bonds between carbon atoms", "only triple bonds", "only ionic bonds", "no hydrogen atoms", "Saturated hydrocarbons contain only single carbon-carbon bonds."),
                    q("An unsaturated hydrocarbon may contain", "double or triple bonds", "only sodium", "only oxygen gas", "only single bonds and no carbon", "Unsaturated hydrocarbons include multiple bonds."),
                    q("Which type of hydrocarbon usually undergoes addition reactions more easily?", "Unsaturated hydrocarbon", "Saturated hydrocarbon", "Noble gas", "Salt crystal", "Multiple bonds make addition easier."),
                    q("What is a homologous series?", "A family of compounds with similar structures and patterns", "A type of rust", "A pH scale colour", "A metal alloy", "Homologous series organise compounds into related families."),
                    q("Why are homologous series useful?", "They help you see patterns instead of memorising each compound separately", "They remove all carbon", "They stop reactions", "They make metals softer", "Pattern recognition is the key benefit."),
                    q("Which statement fits saturated compounds best?", "They are full of single carbon-carbon bonds", "They always contain chlorine", "They are metals", "They never burn", "Single bonds define saturation."),
                    q("Which statement fits unsaturated compounds best?", "They contain at least one multiple bond", "They contain no carbon", "They are always solids", "They always have pH 7", "Multiple bonds define unsaturation."),
                ],
            ),
            module(
                "M2: Useful Reactions of Carbon Compounds",
                [
                    (
                        "Burning, Oxidation and Clean Flames",
                        slide(
                            [
                                "Carbon compounds can burn to produce carbon dioxide, water, heat, and often light. A clean blue flame usually suggests more complete burning, while a yellow smoky flame suggests incomplete burning and soot formation.",
                                "Some substances can also add oxygen to carbon compounds. That process is oxidation, and it changes one substance into another with different properties.",
                            ],
                            image="page_previews/page_0014.png",
                            caption="The middle source pages discuss oxidation and other reactions of carbon compounds.",
                            points=[
                                "Combustion releases heat.",
                                "Oxidation adds oxygen or removes hydrogen in many cases.",
                                "Flame colour can hint at how complete the burning is.",
                            ],
                            box=("real", "<strong>Kitchen clue:</strong> A steady blue flame is usually a sign of better burning than a smoky yellow one.")
                        ),
                    ),
                    (
                        "Addition and Substitution",
                        slide(
                            [
                                "Unsaturated compounds can undergo addition reactions because their multiple bonds can open up and attach new atoms. Saturated compounds, especially under special conditions, often show substitution reactions instead, where one atom is replaced by another.",
                                "These reaction types help us compare families of carbon compounds and predict what kind of changes they can undergo.",
                            ],
                            points=[
                                "Addition is linked strongly with unsaturation.",
                                "Substitution is common in some saturated compounds.",
                                "Bond type influences reaction type.",
                            ],
                            box=("tip", "<strong>Memory trick:</strong> Addition fills an open spot. Substitution swaps one partner for another.")
                        ),
                    ),
                ],
                [
                    q("What is combustion?", "Burning of a substance in oxygen", "Freezing of a liquid", "Mixing salt with water", "Only dissolving sugar", "Combustion means burning."),
                    q("A clean blue flame usually suggests", "more complete burning", "no burning at all", "only water formation", "a magnetic reaction", "Blue flames usually indicate better combustion."),
                    q("A smoky yellow flame suggests", "incomplete combustion", "neutralisation", "electrolysis", "no carbon present", "Soot and smoke indicate incomplete combustion."),
                    q("What does oxidation often involve?", "Gain of oxygen or loss of hydrogen", "Gain of sand", "Loss of all atoms", "Only turning into a metal", "Oxidation changes substances through oxygen or hydrogen changes."),
                    q("Which type of compound often undergoes addition reactions?", "Unsaturated compound", "Noble gas", "Salt only", "Pure metal", "Multiple bonds support addition reactions."),
                    q("What happens in a substitution reaction?", "One atom or group is replaced by another", "All atoms vanish", "Only heat is removed", "The substance becomes a planet", "Substitution means replacement."),
                    q("Why does bond type matter in carbon chemistry?", "It affects how compounds react", "It changes gravity", "It removes carbon", "It stops all burning", "Structure controls reactivity."),
                    q("Which reaction type best matches “new atoms join across a multiple bond”?", "Addition", "Rusting", "Neutralisation", "Filtration", "That is the idea of an addition reaction."),
                ],
            ),
            module(
                "M3: Ethanol, Ethanoic Acid and Soap",
                [
                    (
                        "From Useful Liquids to Useful Acids",
                        slide(
                            [
                                "Ethanol is a familiar carbon compound with many uses, but it must be handled responsibly because it is flammable and can be harmful when misused. Ethanoic acid is another important compound and is linked with vinegar in dilute form.",
                                "These two examples help children see that carbon chemistry is not just about formulas. It is about real materials with real uses, real benefits, and real safety rules.",
                            ],
                            image="page_previews/page_0018.png",
                            caption="The later source pages connect carbon compounds with alcohols, acids, soap, and cleaning action.",
                            points=[
                                "Ethanol is flammable.",
                                "Ethanoic acid is related to vinegar.",
                                "Useful chemicals also need safe handling.",
                            ],
                            box=("warn", "<strong>Safety reminder:</strong> Useful does not mean harmless. Science always combines knowledge with care.")
                        ),
                    ),
                    (
                        "Why Soap Can Clean Oily Dirt",
                        slide(
                            [
                                "Water alone cannot remove oily dirt well, but soap molecules are clever. One end of a soap molecule is attracted to water, and the other end is attracted to oil. That helps break greasy dirt into tiny droplets that water can wash away.",
                                "Detergents are also cleaning agents, but soaps are a beautiful example of how molecular structure explains a common daily-life effect.",
                            ],
                            points=[
                                "Soap works because it can connect with both water and oil.",
                                "Grease gets trapped in tiny droplets called micelles.",
                                "Cleaning action is really a story about molecular design.",
                            ],
                            box=("note", "<strong>Big idea:</strong> Tiny molecules can create big changes that you can see with your eyes.")
                        ),
                    ),
                ],
                [
                    q("Which carbon compound is related to vinegar in dilute form?", "Ethanoic acid", "Methane", "Carbon dioxide", "Graphite", "Vinegar contains dilute ethanoic acid."),
                    q("Which statement about ethanol is correct?", "It is flammable", "It is a metal", "It cannot burn", "It is always solid", "Ethanol is flammable and must be handled carefully."),
                    q("Why is safe handling important even for useful chemicals?", "Because usefulness does not remove risk", "Because useful chemicals can never react", "Because all chemicals are sweet", "Because risk only exists in space", "Safety remains important for all chemicals."),
                    q("Why can soap remove oily dirt better than plain water?", "Soap interacts with both water and oil", "Soap turns oil into metal", "Soap removes all oxygen", "Soap freezes water instantly", "Soap molecules have two different helpful ends."),
                    q("What is a micelle?", "A tiny droplet structure that traps oily dirt", "A type of metal wire", "A pH paper", "A salt crystal", "Soap forms micelles around oily dirt."),
                    q("Which part of soap helps connect to oil?", "The oil-loving end of the soap molecule", "Only the water-loving end", "The QR code", "The indicator colour", "Soap has one end that is attracted to oil."),
                    q("What makes soap a great example in science?", "Its cleaning action is explained by molecular structure", "It never mixes with water", "It removes all atoms", "It behaves like a noble gas", "Soap links molecular design with visible effects."),
                    q("Ethanoic acid belongs to which broad class of substances in this workshop?", "Carbon compounds", "Metals", "Noble gases", "Salts only", "Ethanoic acid is an important carbon compound."),
                ],
            ),
        ],
    },
    {
        "slug": "jesc105",
        "title": "Life Processes",
        "subtitle": "Kid-friendly science workshop with tiny lessons and quick quizzes",
        "modules": [
            module(
                "M0: What Keeps Living Things Alive",
                [
                    (
                        "Life Means Constant Work",
                        slide(
                            [
                                "Living things are not alive only when they run, jump, or wave. Even when you are resting, your body is still busy. Cells keep repairing, moving materials, making energy available, and maintaining order inside the body.",
                                "That is why life processes matter. They are the quiet jobs that keep organisms alive all the time, even when no obvious movement can be seen.",
                            ],
                            image="page_previews/page_0001.png",
                            caption="The opening source page explains that life depends on invisible maintenance processes, not only visible movement.",
                            points=[
                                "Life needs continuous maintenance.",
                                "Molecular movement inside the body matters.",
                                "Visible movement alone is not enough to define life.",
                            ],
                            box=("tip", "<strong>Think deeper:</strong> A sleeping dog is alive because many hidden processes are still happening.")
                        ),
                    ),
                    (
                        "Nutrition Starts the Story",
                        slide(
                            [
                                "Organisms need materials to grow, repair, and release energy. Green plants make food through photosynthesis, while animals and humans depend on eating other organisms or their products.",
                                "Nutrition is therefore the first big survival system. Without food or a way to make food, the rest of the body's processes cannot keep going for long.",
                            ],
                            points=[
                                "Plants are autotrophs because they make food.",
                                "Animals are heterotrophs because they depend on ready-made food.",
                                "Food supports growth, repair, and energy release.",
                            ],
                            box=("note", "<strong>Word power:</strong> “auto” means self, so an autotroph makes its own food.")
                        ),
                    ),
                ],
                [
                    q("Why are life processes important?", "They maintain the body and keep it alive", "They only help in sleeping", "They are needed only for machines", "They remove all molecules", "Life processes are the maintenance jobs of living organisms."),
                    q("Why is visible movement not enough to define life?", "Because many important life activities are hidden inside the body", "Because all living things are always still", "Because plants are metals", "Because movement does not exist", "Internal molecular and cellular activity matters."),
                    q("Which organisms make their own food?", "Autotrophs", "Heterotrophs", "Only animals", "Only fungi in this lesson", "Autotrophs prepare their own food."),
                    q("Green plants make food mainly by", "photosynthesis", "rusting", "neutralisation", "distillation", "Photosynthesis is the food-making process in plants."),
                    q("Which organisms depend on ready-made food?", "Heterotrophs", "Autotrophs", "Only stones", "Only gases", "Heterotrophs depend on other organisms for food."),
                    q("What does food supply for the body?", "Energy, growth, and repair materials", "Only colour", "Only sound", "Only magnets", "Food supports multiple life needs."),
                    q("A sleeping person is still alive because", "life processes continue inside the body", "all cells stop working", "oxygen is no longer needed", "the heart becomes metal", "Hidden maintenance processes keep running."),
                    q("What does the word autotroph suggest?", "Self-feeding or self-nourishing", "Always moving fast", "Made of metal", "Having no cells", "“Auto” helps remember self-made food."),
                ],
            ),
            module(
                "M1: Respiration and Breathing",
                [
                    (
                        "Why Food Alone Is Not Enough",
                        slide(
                            [
                                "Food stores energy, but that energy must be released in a usable way. Respiration breaks down food to release energy that cells can use. This happens inside the body all the time.",
                                "Breathing and respiration are connected, but they are not exactly the same thing. Breathing moves air in and out, while respiration is the chemical process that releases energy from food.",
                            ],
                            image="page_previews/page_0010.png",
                            caption="Middle source pages explain how respiration releases energy from food and how gas exchange supports it.",
                            points=[
                                "Breathing is movement of air.",
                                "Respiration releases energy from food.",
                                "Oxygen helps complete aerobic respiration.",
                            ],
                            box=("tip", "<strong>Easy distinction:</strong> Breathing is the door. Respiration is what happens inside the room.")
                        ),
                    ),
                    (
                        "Different Paths of Respiration",
                        slide(
                            [
                                "When oxygen is available, cells can release more energy through aerobic respiration. When oxygen is limited, some organisms or body cells may use anaerobic pathways instead. That can lead to different end products.",
                                "This matters in real life. Muscles working very hard may not get oxygen fast enough for every cell all the time, which is one reason the body can feel tired or strained.",
                            ],
                            points=[
                                "Aerobic respiration uses oxygen.",
                                "Anaerobic respiration happens without enough oxygen.",
                                "Energy release and end products can differ.",
                            ],
                            box=("real", "<strong>Sports link:</strong> Heavy exercise reminds you that respiration is not just a textbook idea.")
                        ),
                    ),
                ],
                [
                    q("What is respiration mainly about?", "Releasing energy from food", "Only drinking water", "Only movement of legs", "Only sleeping", "Respiration makes food energy usable."),
                    q("What is breathing?", "Movement of air in and out of the body", "Breaking down food inside cells", "A kind of alloy", "A neutralisation reaction", "Breathing is physical movement of air."),
                    q("Which process directly releases usable energy inside cells?", "Respiration", "Breathing only", "Rusting", "Melting", "Respiration is the energy-releasing process."),
                    q("Aerobic respiration needs", "oxygen", "only salt", "graphite", "kerosene", "Aerobic respiration uses oxygen."),
                    q("Anaerobic respiration happens when", "oxygen is absent or insufficient", "oxygen is very abundant", "water is solid", "all cells stop", "Anaerobic pathways work without enough oxygen."),
                    q("Why can intense exercise make muscles feel strained?", "Oxygen supply may not keep up fully with demand", "Because muscles become wooden", "Because breathing stops forever", "Because all food disappears", "Hard-working muscles can face oxygen shortage."),
                    q("Which statement is correct?", "Breathing and respiration are related but not identical", "They are exactly the same word", "Breathing happens only in plants", "Respiration happens only outside the body", "One is movement of air, the other is cellular energy release."),
                    q("Why does the body need respiration?", "To make stored food energy usable", "To turn bones into gas", "To create litmus paper", "To stop the heart", "Respiration keeps energy available for life processes."),
                ],
            ),
            module(
                "M2: Transport in Bodies and Plants",
                [
                    (
                        "The Body Needs Delivery Systems",
                        slide(
                            [
                                "Cells are spread throughout the body, so oxygen, food, water, and wastes cannot stay in one place. Transport systems move these materials where they need to go. In humans, blood and the heart play the central role.",
                                "The heart works like a powerful pump. Blood carries oxygen, nutrients, hormones, and wastes through vessels so cells can keep functioning.",
                            ],
                            image="page_previews/page_0014.png",
                            caption="The transport pages focus on the heart, blood flow, and movement of materials inside the body.",
                            points=[
                                "The heart pumps blood.",
                                "Blood carries oxygen and nutrients.",
                                "Transport also helps remove wastes.",
                            ],
                            box=("note", "<strong>Big picture:</strong> A transport system is a delivery and cleanup network at the same time.")
                        ),
                    ),
                    (
                        "Plants Also Need Transport",
                        slide(
                            [
                                "Plants may not have a heart, but they still need transport. Water and minerals move upward from the roots through xylem, while prepared food can move through phloem to places that need it.",
                                "This shows one of the most beautiful ideas in biology: different organisms solve the same problem in different ways.",
                            ],
                            image="page_previews/page_0018.png",
                            caption="Later source pages describe xylem and phloem as transport tissues in plants.",
                            points=[
                                "Xylem mainly carries water and minerals.",
                                "Phloem carries prepared food.",
                                "Transport is essential in both plants and animals.",
                            ],
                            box=("tip", "<strong>Memory trick:</strong> Xylem lifts water up. Phloem shares food around.")
                        ),
                    ),
                ],
                [
                    q("Why does the body need a transport system?", "To move materials to and from cells", "To change metals into plants", "To stop respiration", "To remove all water", "Cells need a delivery system."),
                    q("Which organ pumps blood through the body?", "Heart", "Liver", "Kidney", "Stomach", "The heart is the main pump."),
                    q("What does blood carry?", "Oxygen, nutrients, and wastes", "Only bones", "Only sound", "Only acids", "Blood transports many important materials."),
                    q("Which plant tissue mainly carries water and minerals?", "Xylem", "Phloem", "Epidermis", "Petal", "Xylem is the water-carrying tissue."),
                    q("Which plant tissue carries prepared food?", "Phloem", "Xylem", "Bark only", "Root cap only", "Phloem transports food."),
                    q("Why is transport important even in plants?", "Because different parts need water, minerals, and food", "Because plants do not have cells", "Because roots can fly", "Because leaves are metals", "Plants also need internal distribution."),
                    q("Which statement is true?", "Transport helps with both supply and waste removal", "Transport only brings colour", "Transport happens only during sleep", "Transport is not needed in multicellular organisms", "Delivery and cleanup are both transport roles."),
                    q("What does the heart mainly act like?", "A pump", "A magnet", "A pH paper", "A beaker", "The heart drives circulation by pumping blood."),
                ],
            ),
            module(
                "M3: Excretion and Balance",
                [
                    (
                        "Cleaning Up the Body",
                        slide(
                            [
                                "Life processes create wastes as well as useful products. If those wastes stay inside too long, they can harm the body. Excretion removes these unwanted materials and helps keep internal conditions balanced.",
                                "In humans, kidneys filter the blood and form urine. Tiny units called nephrons do the filtering work, proving again that big body jobs depend on tiny structures.",
                            ],
                            image="page_previews/page_0020.png",
                            caption="The final pages cover excretion and how the body filters wastes.",
                            points=[
                                "Excretion removes harmful wastes.",
                                "Kidneys filter the blood.",
                                "Nephrons are the tiny filtering units.",
                            ],
                            box=("real", "<strong>Body wisdom:</strong> Survival is not only about taking things in. It is also about removing the right things.")
                        ),
                    ),
                    (
                        "Balance Matters in Plants Too",
                        slide(
                            [
                                "Plants also handle extra materials and water balance in their own ways. Stomata help in gas exchange and water loss, while transport tissues and surrounding cells help manage movement and pressure inside the plant.",
                                "Across humans and plants, one shared truth appears again and again: life survives by maintaining balance through many connected processes.",
                            ],
                            points=[
                                "Excretion and balance support life.",
                                "Plants also regulate water and gases.",
                                "Life processes work as a team, not as separate islands.",
                            ],
                            box=("tip", "<strong>Final thought:</strong> Nutrition, respiration, transport, and excretion are like teammates keeping the organism stable.")
                        ),
                    ),
                ],
                [
                    q("Why is excretion important?", "It removes harmful wastes from the body", "It creates all food", "It turns blood into bones", "It stops all movement", "Excretion protects the body by removing wastes."),
                    q("Which organs mainly filter blood to form urine?", "Kidneys", "Lungs", "Eyes", "Skin only", "Kidneys are the main excretory organs."),
                    q("What is a nephron?", "A tiny filtering unit in the kidney", "A type of blood vessel", "A food molecule", "A metal alloy", "Nephrons do the filtering work."),
                    q("What can happen if harmful wastes are not removed?", "They can damage the body", "They become food", "They increase photosynthesis", "They become magnets", "Waste buildup is harmful."),
                    q("Which plant structures help in gas exchange and water loss?", "Stomata", "Nephrons", "Ribosomes", "Bones", "Stomata are important openings in leaves."),
                    q("Which statement fits life processes best?", "They work together to maintain balance", "They are all unrelated", "Only nutrition matters", "Only excretion matters", "Life processes are connected systems."),
                    q("What is one major job of the urinary system?", "Removing dissolved wastes", "Making chlorophyll", "Producing metal sheets", "Raising pH paper", "Urine formation helps remove wastes."),
                    q("Why are nephrons important even though they are tiny?", "Small structures can perform essential body functions", "Tiny things are never useful", "They replace the heart", "They only store oxygen", "Nephrons show how microscopic units do vital work."),
                ],
            ),
        ],
    },
]


def attach_question_ids(modules: list[dict[str, object]]) -> None:
    for module_index, mod in enumerate(modules):
        questions = mod["questions"]
        for question_index, question in enumerate(questions, start=1):
            question["id"] = f"q{module_index}_{question_index}"


def write_workshop(workshop: dict[str, object]) -> None:
    modules = workshop["modules"]
    attach_question_ids(modules)

    base.TOPIC_SLUG = workshop["slug"]
    base.WORKSHOP_TITLE = workshop["title"]
    base.WORKSHOP_SUBTITLE = workshop["subtitle"]
    base.MODULES = modules

    slides = base.build_slides()
    quiz_data = base.build_quiz_data()
    html = base.build_html(slides, quiz_data)

    output_dir = Path("output") / workshop["slug"]
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / f"{workshop['slug']}_workshop.html").write_text(html, encoding="utf-8")
    (output_dir / f"{workshop['slug']}_quiz.json").write_text(
        json.dumps(quiz_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def main() -> None:
    for workshop in WORKSHOPS:
        write_workshop(workshop)


if __name__ == "__main__":
    main()
