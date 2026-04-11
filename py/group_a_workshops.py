from __future__ import annotations

import html
import json
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "output"


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def block(text: str) -> str:
    return dedent(text).strip()


def p(text: str) -> str:
    return f"<p>{esc(text)}</p>"


def hp(text: str) -> str:
    return f"<p>{text}</p>"


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def callout(kind: str, text_html: str) -> str:
    return f'<div class="{kind}">{text_html}</div>'


def preview_block(path: str, caption: str) -> str:
    safe = esc(caption)
    return block(
        f"""
        <figure class="preview">
          <img src="{path}" alt="{safe}">
          <figcaption>{safe}</figcaption>
        </figure>
        """
    )


def slide(title: str, preview: str, caption: str, parts: list[str]) -> dict[str, str]:
    return {"title": title, "body": "\n".join(parts + [preview_block(preview, caption)])}


def q(question_id: str, prompt: str, correct: str, wrong_1: str, wrong_2: str, wrong_3: str, explanation: str) -> dict[str, object]:
    return {
        "id": question_id,
        "question": prompt,
        "options": [correct, wrong_1, wrong_2, wrong_3],
        "answer": 0,
        "explanation": explanation,
    }


def module(name: str, slides: list[dict[str, str]], questions: list[dict[str, object]]) -> dict[str, object]:
    return {"name": name, "slides": slides, "questions": questions}


CHAPTERS: list[dict[str, object]] = []

CHAPTERS.extend([
    {
        "slug": "jesc106",
        "title": "Control and Coordination Workshop",
        "subtitle": "Kid-friendly science workshop with quick slides and short quizzes",
        "source_pdf": "jesc106.pdf",
        "modules": [
            module(
                "M0: Why the Body Needs Control",
                [
                    slide(
                        "Life Responds to Change",
                        "page_previews/page_0001.png",
                        "Opening page showing how living things respond to the world around them.",
                        [
                            p("Living things do not just move for no reason. They notice what is happening and then react."),
                            p("The chapter starts with familiar examples like a cat chasing a mouse, a child pulling away from heat, and a plant turning toward sunlight."),
                            bullets(["Movement can be a response to the environment.", "The response is controlled, not random.", "Different situations need different actions."]),
                            callout("note", "<strong>Big idea:</strong> control and coordination help an organism choose the right response at the right time."),
                        ],
                    ),
                    slide(
                        "How a Nerve Message Travels",
                        "page_previews/page_0002.png",
                        "Neuron diagram and the first look at sense organs and synapses.",
                        [
                            p("Nerve cells carry information as electrical impulses. The message starts at the dendrite, moves through the cell body, goes along the axon, and crosses the synapse to the next cell."),
                            p("Receptors in sense organs notice the change first. Gustatory receptors sense taste, and olfactory receptors sense smell."),
                            bullets(["Receptors detect the stimulus.", "A neuron carries the impulse.", "The synapse passes the message on."]),
                        ],
                    ),
                ],
                [
                    q("j106_q1", "What do receptors do in the nervous system?", "They detect changes in the environment", "They make food for the body", "They pump blood through the body", "They store bones in the brain", "Receptors are the body's first detectors."),
                    q("j106_q2", "Which part of a neuron receives information first?", "Dendrite", "Axon", "Cell wall", "Nucleus of a leaf cell", "The dendrite is where information is first acquired."),
                    q("j106_q3", "What is the gap between two neurons called?", "Synapse", "Pupil", "Valve", "Capillary", "The chapter names the tiny gap between neurons as a synapse."),
                    q("j106_q4", "Which receptors help you notice taste?", "Gustatory receptors", "Olfactory receptors", "Reproductive receptors", "Joint receptors", "Gustatory receptors detect taste."),
                    q("j106_q5", "How does the nervous system send a fast message?", "By electrical impulses", "By growing new leaves", "By melting proteins", "By turning water into metal", "The nervous system uses electrical impulses to carry information."),
                ],
            ),
            module(
                "M1: Reflexes and the Brain",
                [
                    slide(
                        "Reflex Actions Are Super Fast",
                        "page_previews/page_0003.png",
                        "The chapter moves into reflex actions and the reflex arc.",
                        [
                            p("A reflex action is a quick, automatic response to something that could hurt you. Touching a hot pan is the classic example."),
                            p("The signal uses a reflex arc, and the spinal cord helps the body react quickly."),
                            bullets(["Reflex actions are automatic.", "They protect the body from danger.", "The spinal cord helps make the response fast."]),
                        ],
                    ),
                    slide(
                        "The Brain Keeps the Plan Together",
                        "page_previews/page_0005.png",
                        "Brain structure pages with the main regions and their jobs.",
                        [
                            p("The brain helps control thinking, balance, memory, and many other actions. The cerebrum helps with thinking, the cerebellum helps with balance, and the medulla handles life-support jobs."),
                            p("It is protected by the skull, meninges, and a fluid cushion around it."),
                            bullets(["Cerebrum: thinking and learning", "Cerebellum: balance and movement", "Medulla: breathing and heartbeat control"]),
                        ],
                    ),
                ],
                [
                    q("j106_q6", "What is a reflex action?", "A quick automatic response", "A slow writing exercise", "A kind of plant seed", "A stomach juice", "The textbook defines reflex action as a quick, automatic response."),
                    q("j106_q7", "Which part of the body helps make reflex responses fast?", "Spinal cord", "Tooth enamel", "Ear lobe", "Rib cage only", "The spinal cord handles the shortcut response in a reflex arc."),
                    q("j106_q8", "Which brain part helps with balance?", "Cerebellum", "Retina", "Alveolus", "Stigma", "The cerebellum helps coordinate body balance and movement."),
                    q("j106_q9", "Which is an involuntary action?", "Heartbeat", "Drawing a picture", "Clapping on purpose", "Walking to a friend", "The chapter lists heartbeat as one of the actions the body controls on its own."),
                    q("j106_q10", "Why is the brain protected by the skull and meninges?", "Because it is delicate and important", "Because it needs sunlight", "Because it is a bone", "Because it can swim", "The brain needs strong protection because it controls many body functions."),
                ],
            ),
            module(
                "M2: Plants Respond Too",
                [
                    slide(
                        "The Sensitive Plant Responds Right Away",
                        "page_previews/page_0007.png",
                        "The plant example shows an immediate response to touch.",
                        [
                            p("Plants also respond to the world around them. The sensitive plant folds its leaves when touched."),
                            p("This is an immediate response, but it is not the same as growth."),
                            bullets(["Touch can trigger a quick plant response.", "Some plant movements are not growth based.", "Plants still need coordination."]),
                        ],
                    ),
                    slide(
                        "Growth Movements Are Directional",
                        "page_previews/page_0010.png",
                        "Pages on tropisms show how roots and shoots bend because of growth.",
                        [
                            p("Some plant movements happen because of growth. A shoot bends toward light, and roots grow downward into the soil. These are called tropisms."),
                            p("Plants may look still, but they are constantly adjusting their growth to match the environment."),
                            bullets(["Phototropism: growth in response to light", "Geotropism: growth in response to gravity", "Growth movements are slow but important"]),
                        ],
                    ),
                ],
                [
                    q("j106_q11", "What does the sensitive plant show when touched?", "Its leaves fold quickly", "Its roots become wings", "Its flowers turn into fruit", "Its stem becomes metal", "The chapter uses the sensitive plant as an example of a quick response to touch."),
                    q("j106_q12", "What is a movement caused by growth in a plant called?", "Tropism", "Synapse", "Reflex arc", "Hormone rush", "Growth-based directional movement in plants is called tropism."),
                    q("j106_q13", "What is phototropism?", "Growth in response to light", "Growth in response to sound", "Growth in response to hunger", "Growth in response to metal", "Phototropism means the plant grows toward light."),
                    q("j106_q14", "What is geotropism?", "Growth in response to gravity", "Growth in response to colour", "Growth in response to taste", "Growth in response to wind only", "Geotropism is the growth response to gravity."),
                    q("j106_q15", "Which plant part usually grows downward because of gravity?", "Root", "Petal", "Leaf blade", "Pollen grain", "Roots commonly show positive geotropism and grow downward."),
                ],
            ),
            module(
                "M3: Hormones Do the Long-Range Work",
                [
                    slide(
                        "Hormones in Animals",
                        "page_previews/page_0011.png",
                        "Endocrine glands and their hormone jobs are shown on this page.",
                        [
                            p("Hormones are chemical messengers. They move through the blood and tell another part of the body what to do."),
                            p("Growth hormone helps the body grow, insulin helps control blood sugar, and adrenaline helps you react in an emergency."),
                            bullets(["Growth hormone supports growth.", "Insulin controls blood sugar.", "Adrenaline prepares the body for danger."]),
                        ],
                    ),
                    slide(
                        "Feedback Keeps Hormones Balanced",
                        "page_previews/page_0013.png",
                        "The end of the chapter summarizes the big ideas for revision.",
                        [
                            p("The nervous system and hormone system work together. The nervous system is fast and precise. Hormones are slower but useful for long-range control."),
                            p("Plants also use chemical signals to coordinate growth and response."),
                            callout("note", "<strong>Final memory line:</strong> nerves send quick messages, hormones send long-range messages, and both help the body stay organized."),
                        ],
                    ),
                ],
                [
                    q("j106_q16", "What is the main job of hormones?", "To carry chemical messages", "To make bones turn into water", "To cut paper in the brain", "To paint the skin blue", "Hormones are chemical messengers used for coordination."),
                    q("j106_q17", "Which hormone helps control blood sugar?", "Insulin", "Adrenaline", "Growth hormone", "Olfactory hormone", "Insulin helps regulate the sugar level in blood."),
                    q("j106_q18", "Which hormone helps the body react in an emergency?", "Adrenaline", "Insulin", "Digestive juice", "Meninges", "Adrenaline prepares the body for quick action in danger."),
                    q("j106_q19", "What does feedback help the body do?", "Keep hormone action balanced", "Make all hormones stop forever", "Turn nerves into bones", "Erase all blood", "Feedback keeps hormone levels from going too high or too low."),
                    q("j106_q20", "Which system is fast and uses electrical impulses?", "Nervous system", "Respiratory system", "Digestive system", "Skeleton system", "The nervous system sends quick messages as electrical impulses."),
                ],
            ),
        ],
    }
])

CHAPTERS.extend([
    {
        "slug": "jesc108",
        "title": "Heredity Workshop",
        "subtitle": "Short chapter, clear summaries, and compact quiz practice",
        "source_pdf": "jesc108.pdf",
        "modules": [
            module(
                "M0: Variation and Inheritance",
                [
                    slide(
                        "Why Variation Matters",
                        "page_previews/page_0001.png",
                        "The opening pages show that offspring are similar but not identical.",
                        [
                            p("The chapter starts with a simple picture: children look like their parents, but not exactly. That small difference is called variation."),
                            p("Variation can be useful because it gives a species a better chance of surviving changes in the environment."),
                            bullets(["Offspring are similar, not identical.", "Variation appears during reproduction.", "Variation can help survival."]),
                        ],
                    ),
                    slide(
                        "Heredity Passes Traits On",
                        "page_previews/page_0002.png",
                        "The early chapter pages connect inherited traits to the next generation.",
                        [
                            p("Heredity means passing traits from parents to offspring. The chapter uses examples such as earlobes and eye colour to show this."),
                            p("At the same time, the chapter reminds us that traits can vary in a population."),
                            callout("note", "<strong>Big picture:</strong> heredity keeps the family likeness, while variation adds the differences."),
                        ],
                    ),
                ],
                [
                    q("j108_q1", "What is variation?", "Small differences among individuals", "A type of hormone", "A bone in the ear", "A gas from plants", "Variation means the small differences we see among individuals."),
                    q("j108_q2", "Why can variation help a species survive?", "Some members may fit new conditions better", "It always stops growth", "It makes all organisms identical", "It removes DNA", "Variation gives at least some individuals a better survival chance when conditions change."),
                    q("j108_q3", "What does heredity do?", "Passes traits from parents to offspring", "Turns plants into animals", "Creates only water", "Removes chromosomes", "Heredity is the passing of traits from one generation to the next."),
                    q("j108_q4", "Are offspring usually exact copies of their parents?", "No, they are similar but not identical", "Yes, always exact copies", "Only in flowering plants", "Only in reptiles", "The chapter keeps stressing that offspring are similar, but not exact copies."),
                    q("j108_q5", "Which trait is an example often used in the chapter?", "Earlobes", "Clouds", "Rivers", "Sand grains", "The chapter uses earlobe type as one example of inherited variation."),
                ],
            ),
            module(
                "M1: Mendel's Pea Experiments",
                [
                    slide(
                        "A Tall Plant Can Hide a Short Trait",
                        "page_previews/page_0003.png",
                        "The pages explain how Mendel studied tall and short pea plants.",
                        [
                            p("Mendel crossed pea plants with contrasting traits, such as tall and short. In the first generation, all the plants were tall."),
                            p("When the first generation self-pollinated, the second generation showed both tall and short plants."),
                        ],
                    ),
                    slide(
                        "Two Traits Can Be Inherited Independently",
                        "page_previews/page_0004.png",
                        "The next page shows the famous pea experiment with seed shape and seed colour.",
                        [
                            p("Mendel also studied more than one trait at a time. He found that shape and colour of seeds could be inherited independently."),
                            p("The chapter also gives the idea of dominant and recessive traits. If a trait appears with one copy, it is dominant. If it shows only when both copies are the same, it is recessive."),
                            bullets(["Dominant trait: shows with one copy", "Recessive trait: shows only with two matching copies", "Independent inheritance can create new combinations"]),
                        ],
                    ),
                ],
                [
                    q("j108_q6", "What did Mendel study?", "Contrasting traits in pea plants", "Only rainfall patterns", "Only bird songs", "Only rock colours", "Mendel used pea plants with different visible traits."),
                    q("j108_q7", "What did the first generation of Mendel's tall and short cross show?", "All the plants were tall", "All the plants were short", "All the plants were blue", "No plants grew", "The first generation showed only the tall trait."),
                    q("j108_q8", "What is a dominant trait?", "A trait that shows with one copy", "A trait that never appears", "A trait made only of water", "A trait found only in plants", "A dominant trait appears when a single copy is present."),
                    q("j108_q9", "What is a recessive trait?", "A trait that appears only when both copies match", "A trait that always wins instantly", "A trait made by sunlight", "A trait with no genes", "A recessive trait shows only when both copies are the same."),
                    q("j108_q10", "What kind of new offspring can independent inheritance produce?", "New combinations of traits", "Only exact copies", "Only metals", "Only clouds", "Independent inheritance mixes traits into new combinations."),
                ],
            ),
            module(
                "M2: Genes, Chromosomes, and Sex Determination",
                [
                    slide(
                        "Genes Help Make Proteins",
                        "page_previews/page_0005.png",
                        "The chapter explains how genes, chromosomes, and traits fit together.",
                        [
                            p("A gene is a section of DNA that gives instructions for making a protein. Proteins help create the traits we see."),
                            p("The chapter also explains that chromosomes carry genes. Each parent gives one copy, so sexually reproducing organisms usually have two copies of each gene."),
                        ],
                    ),
                    slide(
                        "XX, XY, and the Father's Role",
                        "page_previews/page_0006.png",
                        "The final page shows how sex is determined in human beings.",
                        [
                            p("In humans, sex is usually determined by chromosomes. Females have XX and males have XY. The mother gives an X chromosome to every child. The father gives either X or Y."),
                            p("If the father gives X, the child is a girl. If the father gives Y, the child is a boy."),
                            callout("note", "<strong>Short summary:</strong> genes guide traits, chromosomes carry genes, and X or Y helps decide sex in humans."),
                        ],
                    ),
                ],
                [
                    q("j108_q11", "What is a gene?", "A section of DNA that gives instructions for a protein", "A type of flower petal", "A body bone", "A kind of sugar cube", "The chapter defines a gene as a DNA section that provides information for one protein."),
                    q("j108_q12", "What do chromosomes carry?", "Genes", "Only water", "Only sound", "Only leaves", "Chromosomes are the structures that carry genes."),
                    q("j108_q13", "How many copies of each gene do sexually reproducing organisms usually have?", "Two", "One", "Five", "None", "The chapter says sexually reproducing organisms have two copies of genes for the same trait."),
                    q("j108_q14", "What sex chromosome pair do females have in humans?", "XX", "XY", "YY", "XZ", "Females in humans have XX sex chromosomes."),
                    q("j108_q15", "What sex chromosome pair do males have in humans?", "XY", "XX", "XO", "ZZ", "Males in humans have XY sex chromosomes."),
                ],
            ),
        ],
    }
])

CHAPTERS.extend([
    {
        "slug": "jesc107",
        "title": "How Do Organisms Reproduce? Workshop",
        "subtitle": "Kid-friendly science workshop with short lessons and practice questions",
        "source_pdf": "jesc107.pdf",
        "modules": [
            module(
                "M0: Why Reproduction Matters",
                [
                    slide(
                        "Why Organisms Reproduce",
                        "page_previews/page_0001.png",
                        "The chapter opens by asking why living things reproduce at all.",
                        [
                            p("Reproduction is not needed for one individual to stay alive, but it is needed for a species to continue."),
                            p("New individuals look like their parents, so the species keeps its body design from one generation to the next."),
                            bullets(["Reproduction keeps a species going.", "New individuals look like their parents.", "A species is easier to notice when many members exist."]),
                        ],
                    ),
                    slide(
                        "DNA Copying Creates Variation",
                        "page_previews/page_0002.png",
                        "Pages explain how DNA copying and variation happen during reproduction.",
                        [
                            p("Reproduction begins with copying DNA. That copy is usually close to the original, but not always perfect."),
                            p("Small changes create variation, and variation can help some members survive when the world changes."),
                            bullets(["DNA copying starts reproduction.", "Small copy errors create variation.", "Variation can help survival."]),
                        ],
                    ),
                ],
                [
                    q("j107_q1", "Why do organisms reproduce?", "To keep their species going", "To stop all growth", "To turn into rocks", "To erase DNA", "Reproduction is needed for the species, even though one individual can stay alive without it."),
                    q("j107_q2", "What is the first basic event in reproduction?", "DNA copying", "Melting of bones", "Colour change in leaves", "Loss of water from air", "The chapter says reproduction starts with a copy of DNA."),
                    q("j107_q3", "What are small differences in copied DNA called?", "Variations", "Synapses", "Reflexes", "Roots", "Small changes during DNA copying are called variations."),
                    q("j107_q4", "Why can variation be useful for a species?", "It may help some members survive change", "It always destroys the species", "It removes the need for DNA", "It makes all organisms identical", "Variation can help a species survive when conditions change."),
                    q("j107_q5", "Do all reproducing organisms make perfect copies?", "No, small changes can happen", "Yes, every copy is perfect", "Only plants make copies", "Only animals make copies", "The chapter explains that DNA copying is never absolutely perfect."),
                ],
            ),
            module(
                "M1: Asexual Reproduction",
                [
                    slide(
                        "One Parent, Many Ways",
                        "page_previews/page_0003.png",
                        "The source pages show several asexual methods in simple organisms and plants.",
                        [
                            p("Asexual reproduction uses one parent. The new individual comes from a single organism, so the process is often simple and fast."),
                            p("The chapter covers fission, fragmentation, regeneration, budding, vegetative propagation, and spore formation."),
                            bullets(["Fission splits one cell into two or more cells.", "Budding forms a small outgrowth.", "Vegetative propagation uses roots, stems, or leaves."]),
                        ],
                    ),
                    slide(
                        "Fragments, Buds, and Spores",
                        "page_previews/page_0006.png",
                        "Later pages focus on regeneration, budding, and spore formation.",
                        [
                            p("Hydra can grow a bud that becomes a new individual. Some organisms can regenerate lost parts. Fungi and some plants use spores, which are tiny units that can spread easily."),
                            p("Vegetative propagation is useful in plants because a root, stem, or leaf can grow into a new plant that keeps the same useful traits."),
                            bullets(["Hydra shows budding.", "Planaria shows regeneration.", "Spores help organisms spread widely."]),
                        ],
                    ),
                ],
                [
                    q("j107_q6", "Which kind of reproduction uses only one parent?", "Asexual reproduction", "Sexual reproduction", "Leaf colouring", "Blood circulation", "Asexual reproduction needs only one parent."),
                    q("j107_q7", "What happens in fission?", "One organism divides into two or more parts", "Two adults merge into one", "Seeds turn into metal", "Leaves become water", "Fission is simple splitting, common in bacteria and protozoa."),
                    q("j107_q8", "Which organism is famous for budding?", "Hydra", "Amoeba", "Mango tree", "Human being", "Hydra is the classic budding example in the chapter."),
                    q("j107_q9", "What is regeneration?", "Growing a whole body from a piece", "Stopping all growth", "Mixing pollen with water", "Turning light into heat", "Regeneration means a body part or piece can grow into a complete organism."),
                    q("j107_q10", "Which plant method uses roots, stems, or leaves to make new plants?", "Vegetative propagation", "Reflex action", "Synapse jumping", "Sex determination", "Vegetative propagation is asexual reproduction in plants using plant parts."),
                ],
            ),
            module(
                "M2: Sexual Reproduction in Flowering Plants",
                [
                    slide(
                        "Pollination Comes First",
                        "page_previews/page_0009.png",
                        "The source pages show flower parts and the movement of pollen grains.",
                        [
                            p("Sexual reproduction in flowering plants begins with pollination, which is the transfer of pollen grains from the anther to the stigma."),
                            p("The chapter uses the flower diagram to help you see where pollen starts, where it lands, and how the next steps create seeds and fruits."),
                            bullets(["Anther makes pollen grains.", "Stigma receives pollen.", "Fertilisation happens after pollination."]),
                        ],
                    ),
                    slide(
                        "Fertilisation Makes a New Beginning",
                        "page_previews/page_0010.png",
                        "Later pages connect pollen, ovule, seed, and fruit in a simple sequence.",
                        [
                            p("After fertilisation, the ovule develops into a seed and the ovary develops into a fruit."),
                            p("Because sexual reproduction mixes genetic material from two parents, the offspring can show more variation than asexual offspring."),
                            bullets(["Pollination moves pollen.", "Fertilisation joins the gametes.", "Seeds carry the embryo of the next plant."]),
                        ],
                    ),
                ],
                [
                    q("j107_q11", "What is pollination?", "Transfer of pollen from anther to stigma", "Transfer of water from root to leaf", "Breaking a stem into pieces", "Turning a seed into a fruit", "Pollination is the movement of pollen grains from anther to stigma."),
                    q("j107_q12", "What happens after pollination in flowering plants?", "Fertilisation", "Digestion", "Reflex action", "Spore release only", "The next main step after pollination is fertilisation."),
                    q("j107_q13", "Which flower part receives pollen?", "Stigma", "Root hair", "Petiole", "Stamen only", "The stigma is the pollen-receiving part of the flower."),
                    q("j107_q14", "What does the ovule become after fertilisation?", "Seed", "Leaf", "Stem", "Petal", "The chapter explains that the ovule develops into a seed."),
                    q("j107_q15", "Why does sexual reproduction usually create more variation?", "It combines genetic material from two parents", "It never uses DNA", "It always makes identical copies", "It only happens in one cell", "Mixing material from two parents creates more variety in offspring."),
                ],
            ),
            module(
                "M3: Human Reproduction and Health",
                [
                    slide(
                        "Puberty Means the Body Is Maturing",
                        "page_previews/page_0011.png",
                        "The chapter uses body changes at puberty as a sign of sexual maturation.",
                        [
                            p("Puberty is the time when the body becomes able to reproduce. Girls and boys both go through changes."),
                            p("The male reproductive system includes testes, vas deferens, seminal vesicles, prostate gland, urethra, and penis. The female reproductive system includes ovaries, fallopian tubes, uterus, and vagina."),
                        ],
                    ),
                    slide(
                        "Fertilisation, Embryo, and Health",
                        "page_previews/page_0014.png",
                        "The later pages explain fertilisation, the embryo, and ways to avoid pregnancy.",
                        [
                            p("In human beings, fertilisation usually happens in the fallopian tube. The embryo gets nourishment from the mother through the placenta."),
                            p("The chapter also talks about reproductive health and contraception. Condoms, oral pills, and copper-T are examples of methods used to avoid pregnancy."),
                            bullets(["Sperm is introduced into the vagina.", "Fertilisation happens in the fallopian tube.", "Reproductive health includes safe choices and protection."]),
                        ],
                    ),
                ],
                [
                    q("j107_q16", "What is puberty?", "The stage when the body becomes sexually mature", "A type of spore", "A reflex in plants", "A chemical equation", "Puberty is the stage when the body matures for reproduction."),
                    q("j107_q17", "Where does fertilisation usually happen in human beings?", "Fallopian tube", "Mouth", "Skin", "Stomach", "The chapter says fertilisation in humans usually happens in the fallopian tube."),
                    q("j107_q18", "Which organ produces sperms in males?", "Testes", "Ovary", "Uterus", "Pancreas", "The testes are the male reproductive organs that produce sperm."),
                    q("j107_q19", "Which organ produces eggs in females?", "Ovaries", "Testes", "Vas deferens", "Spinal cord", "The ovaries are the female reproductive organs that produce eggs."),
                    q("j107_q20", "What does a copper-T help with?", "Preventing pregnancy", "Making bones grow", "Turning pollen to fruit", "Speeding up reflexes", "The chapter lists copper-T as one of the methods used to avoid pregnancy."),
                ],
            ),
        ],
    }
])


def render_slide_html(slide_data: dict[str, str], slide_index: int) -> str:
    return block(
        f"""
        <article class="slide" data-slide-index="{slide_index}">
          <h3>{esc(slide_data["title"])}</h3>
          {slide_data["body"]}
        </article>
        """
    )


def render_question_html(question: dict[str, object]) -> str:
    buttons = []
    for index, option in enumerate(question["options"]):
        buttons.append(
            f'<button class="choice" type="button" onclick="answerQuestion(\'{question["id"]}\',{index})">{esc(str(option))}</button>'
        )
    return block(
        f"""
        <section class="question-card" data-qid="{question["id"]}">
          <p class="question-text">{esc(str(question["question"]))}</p>
          <div class="choices">{"".join(buttons)}</div>
          <div class="question-feedback"></div>
          <div class="question-explanation">{esc(str(question["explanation"]))}</div>
        </section>
        """
    )


def render_module(module_data: dict[str, object], module_index: int) -> str:
    slides_html = "\n".join(
        render_slide_html(slide_data, slide_index)
        for slide_index, slide_data in enumerate(module_data["slides"])
    )
    questions_html = "\n".join(render_question_html(question) for question in module_data["questions"])
    return block(
        f"""
        <section class="module" data-module-index="{module_index}">
          <div class="module-header">
            <h2>{esc(str(module_data["name"]))}</h2>
            <p class="module-summary">Read, look, then check yourself.</p>
          </div>
          <div class="slides">{slides_html}</div>
          <section class="quiz-panel">
            <div class="quiz-panel-head">
              <h3>Quick Check</h3>
              <p class="quiz-meta">Your answers are saved in this browser.</p>
              <div class="quiz-actions">
                <button type="button" onclick="retryMissed()">Retry missed</button>
                <button type="button" class="primary" onclick="startNextModule()">Next module</button>
              </div>
              <div class="quiz-score"></div>
            </div>
            <div class="questions">{questions_html}</div>
          </section>
        </section>
        """
    )


def build_quiz_json(chapter: dict[str, object]) -> dict[str, object]:
    modules = []
    for module_index, module_data in enumerate(chapter["modules"]):
        modules.append(
            {
                "id": module_index,
                "name": module_data["name"],
                "questions": [
                    {
                        "id": question["id"],
                        "question": question["question"],
                        "options": question["options"],
                        "answer": question["answer"],
                        "explanation": question["explanation"],
                    }
                    for question in module_data["questions"]
                ],
            }
        )
    return {
        "title": f'{chapter["title"]} - Interactive study deck generated from {chapter["source_pdf"]}',
        "version": "1.0",
        "totalQuestions": sum(len(module_data["questions"]) for module_data in chapter["modules"]),
        "modules": modules,
    }


def build_index_data(chapter: dict[str, object]) -> dict[str, object]:
    answers: dict[str, int] = {}
    modules = []
    for module_index, module_data in enumerate(chapter["modules"]):
        modules.append(
            {
                "id": module_index,
                "name": module_data["name"],
                "slides": len(module_data["slides"]),
                "questions": len(module_data["questions"]),
            }
        )
        for question in module_data["questions"]:
            answers[question["id"]] = question["answer"]
    return {"modules": modules, "answers": answers}


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg:#f4f7fb;--surface:#fff;--text:#172033;--muted:#5c6a82;--line:#d7e0ea;
      --accent:#1d4ed8;--accent2:#ea580c;--good:#15803d;--bad:#dc2626;
    }}
    *{{box-sizing:border-box}} body{{margin:0;font-family:Segoe UI,system-ui,sans-serif;color:var(--text);background:
      radial-gradient(circle at top left,rgba(29,78,216,.08),transparent 28%),
      radial-gradient(circle at top right,rgba(234,88,12,.10),transparent 26%),var(--bg)}}
    button{{border:1px solid var(--line);border-radius:12px;padding:10px 14px;background:#fff;color:var(--text);font-weight:700;cursor:pointer}}
    button.primary{{background:var(--accent);color:#fff;border-color:var(--accent)}}
    #progress{{position:fixed;inset:0 auto auto 0;height:4px;width:0;background:linear-gradient(90deg,var(--accent),var(--accent2));z-index:200}}
    #app{{max-width:1200px;margin:0 auto;padding:16px}}
    #header{{position:sticky;top:10px;z-index:120;display:flex;gap:12px;align-items:center;justify-content:space-between;padding:14px 16px;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);border:1px solid rgba(215,224,234,.95);border-radius:18px;box-shadow:0 10px 28px rgba(15,23,42,.08)}}
    #header .meta{{min-width:180px}} #header .meta strong{{display:block}} #header .center{{flex:1;text-align:center;color:var(--muted);font-weight:700}}
    #header .actions{{display:flex;gap:8px;flex-wrap:wrap}}
    #layout{{display:grid;grid-template-columns:280px minmax(0,1fr);gap:16px;margin-top:16px}}
    #toc{{position:sticky;top:92px;align-self:start;background:rgba(255,255,255,.94);border:1px solid var(--line);border-radius:18px;box-shadow:0 8px 24px rgba(15,23,42,.06);padding:14px;max-height:calc(100vh - 120px);overflow:auto}}
    #toc h2{{margin:0 0 10px;font-size:1rem}}
    .toc-module{{margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid var(--line)}} .toc-module:last-child{{border-bottom:0;padding-bottom:0;margin-bottom:0}}
    .toc-module h3{{margin:0 0 8px;font-size:.97rem}} .toc-list{{display:grid;gap:8px}}
    .toc-list button{{width:100%;text-align:left;background:#f8fbff;border-color:#e4edf7}} .toc-list button.current{{background:#e0ecff;border-color:#a7c5ff}}
    main{{min-width:0}}
    .module{{display:none;background:rgba(255,255,255,.95);border:1px solid var(--line);border-radius:22px;box-shadow:0 14px 36px rgba(15,23,42,.07);overflow:hidden}}
    .module.active{{display:block}} .module-header{{padding:20px 20px 0}} .module-header h2{{margin:0;font-size:clamp(1.4rem,2.1vw,2rem)}} .module-summary{{margin:6px 0 0;color:var(--muted)}}
    .slides{{padding:8px 20px 20px}} .slide{{display:none;padding-top:14px}} .slide.active{{display:block}} .slide h3{{margin:0 0 12px;color:var(--accent);font-size:1.35rem}} .slide p,.slide li{{line-height:1.7;font-size:1rem}} .slide ul{{margin:12px 0 16px 20px}}
    .preview{{margin:18px 0 0;border:1px solid var(--line);border-radius:18px;overflow:hidden;background:#f8fbff}} .preview img{{display:block;width:100%;max-height:380px;object-fit:contain;background:#f8fbff}} .preview figcaption{{padding:10px 12px;color:var(--muted);font-size:.95rem}}
    .note,.tip,.warn,.real{{border-left:5px solid;border-radius:14px;padding:14px 16px;margin:16px 0}} .note{{border-color:var(--accent);background:#eff6ff}} .tip{{border-color:#16a34a;background:#f0fdf4}} .warn{{border-color:#eab308;background:#fefce8}} .real{{border-color:var(--accent2);background:#fff7ed}}
    .quiz-panel{{display:none;padding:10px 20px 22px;border-top:1px solid var(--line);background:linear-gradient(180deg,#fff,#f8fbff)}} .quiz-panel.active{{display:block}}
    .quiz-panel-head{{display:grid;gap:8px;margin-bottom:16px}} .quiz-panel-head h3{{margin:0;font-size:1.25rem}} .quiz-meta,.quiz-score{{margin:0;color:var(--muted)}} .quiz-actions{{display:flex;gap:10px;flex-wrap:wrap}}
    .questions{{display:grid;gap:14px}} .question-card{{border:1px solid var(--line);border-radius:18px;padding:16px;background:#fff}} .question-text{{margin-top:0;font-weight:800}} .choices{{display:grid;gap:10px}}
    .choice{{width:100%;text-align:left;border-width:2px;background:#f8fbff}} .choice.correct{{border-color:var(--good);background:#f0fdf4}} .choice.wrong{{border-color:var(--bad);background:#fef2f2}} .choice.locked{{pointer-events:none;opacity:.82}}
    .question-feedback{{display:none;margin-top:10px;padding:10px 12px;border-radius:12px;font-weight:700}} .question-feedback.show{{display:block}} .question-feedback.pass{{background:#dcfce7;color:#166534}} .question-feedback.fail{{background:#fee2e2;color:#991b1b}}
    .question-explanation{{display:none;margin-top:10px;color:var(--muted)}} .question-explanation.show{{display:block}}
    #overlay{{display:none;position:fixed;inset:0;background:rgba(15,23,42,.34);z-index:110}}
    @media(max-width:920px){{#layout{{grid-template-columns:1fr}}#toc{{position:fixed;left:-320px;top:10px;width:min(320px,calc(100vw - 20px));height:calc(100vh - 20px);max-height:none;z-index:130;transition:left .2s ease}}#toc.open{{left:10px}}}}
    @media(max-width:700px){{#header{{flex-direction:column;align-items:stretch}}#header .center{{text-align:left}}#header .actions button{{flex:1 1 45%}}.slides,.quiz-panel,.module-header{{padding-left:14px;padding-right:14px}}}}
  </style>
</head>
<body>
  <div id="progress"></div>
  <div id="overlay" onclick="toggleToc(false)"></div>
  <div id="app">
    <header id="header">
      <div class="meta"><strong id="module-label"></strong><span id="mode-label"></span></div>
      <div class="center" id="counter"></div>
      <div class="actions">
        <button type="button" onclick="toggleToc()">TOC</button>
        <button type="button" onclick="step(-1)">Prev</button>
        <button type="button" class="primary" id="next-btn" onclick="step(1)">Next</button>
      </div>
    </header>
    <div id="layout">
      <aside id="toc"><h2>Contents</h2>{toc_html}</aside>
      <main id="main">{modules_html}</main>
    </div>
  </div>
  <script>
    window.WORKSHOP_INDEX = {index_json};
    const STORAGE_KEY = {storage_key_json};
    const modules = Array.from(document.querySelectorAll('.module'));
    const tocButtons = Array.from(document.querySelectorAll('[data-jump]'));
    const overlay = document.getElementById('overlay');
    const moduleLabel = document.getElementById('module-label');
    const modeLabel = document.getElementById('mode-label');
    const counter = document.getElementById('counter');
    const progress = document.getElementById('progress');
    const nextButton = document.getElementById('next-btn');
    const defaultState = {{module:0, slide:0, mode:'slides', answers:{{}}}};
    let state = loadState();

    function loadState() {{
      try {{
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? Object.assign({{}}, defaultState, JSON.parse(raw)) : structuredClone(defaultState);
      }} catch (err) {{ return structuredClone(defaultState); }}
    }}
    function saveState() {{ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }}
    function currentModuleData() {{ return window.WORKSHOP_INDEX.modules[state.module]; }}
    function currentSlideCount() {{ return currentModuleData().slides; }}
    function clampState() {{
      state.module = Math.max(0, Math.min(state.module, modules.length - 1));
      state.slide = Math.max(0, Math.min(state.slide, currentSlideCount() - 1));
      if (!['slides', 'quiz'].includes(state.mode)) state.mode = 'slides';
    }}
    function jump(moduleIndex, slideIndex = 0, mode = 'slides') {{ state.module = moduleIndex; state.slide = slideIndex; state.mode = mode; saveState(); render(); toggleToc(false); }}
    function startNextModule() {{ if (state.module < modules.length - 1) jump(state.module + 1, 0, 'slides'); }}
    function currentModuleQuestions(moduleIndex) {{ return Array.from(modules[moduleIndex].querySelectorAll('.question-card')).map(card => card.dataset.qid); }}
    function retryMissed() {{
      for (const qid of currentModuleQuestions(state.module)) {{
        const correct = window.WORKSHOP_INDEX.answers[qid];
        if (state.answers[qid] !== undefined && state.answers[qid] !== correct) delete state.answers[qid];
      }}
      state.mode = 'quiz'; saveState(); render();
    }}
    function answerQuestion(qid, choiceIndex) {{ state.answers[qid] = choiceIndex; saveState(); renderQuizPanel(state.module); }}
    function renderSlide(moduleIndex, slideIndex) {{
      const moduleEl = modules[moduleIndex];
      Array.from(moduleEl.querySelectorAll('.slide')).forEach((slide, index) => slide.classList.toggle('active', index === slideIndex));
      moduleEl.querySelector('.quiz-panel').classList.toggle('active', state.mode === 'quiz');
    }}
    function renderQuizPanel(moduleIndex) {{
      const moduleEl = modules[moduleIndex];
      const questions = Array.from(moduleEl.querySelectorAll('.question-card'));
      let correct = 0, answered = 0, missed = [];
      questions.forEach(card => {{
        const qid = card.dataset.qid;
        const correctIndex = window.WORKSHOP_INDEX.answers[qid];
        const chosen = state.answers[qid];
        const feedback = card.querySelector('.question-feedback');
        const explanation = card.querySelector('.question-explanation');
        const buttons = Array.from(card.querySelectorAll('.choice'));
        buttons.forEach((button, choiceIndex) => {{
          button.classList.remove('correct', 'wrong', 'locked');
          button.disabled = false;
          if (chosen !== undefined) {{
            button.classList.add('locked');
            button.disabled = true;
            if (choiceIndex === correctIndex) button.classList.add('correct');
            if (choiceIndex === chosen && chosen !== correctIndex) button.classList.add('wrong');
          }}
        }});
        if (chosen !== undefined) {{
          answered++;
          if (chosen === correctIndex) {{
            correct++;
            feedback.textContent = 'Correct';
            feedback.className = 'question-feedback show pass';
          }} else {{
            missed.push(qid);
            feedback.textContent = 'Try again';
            feedback.className = 'question-feedback show fail';
          }}
          explanation.classList.add('show');
        }} else {{
          feedback.className = 'question-feedback';
          feedback.textContent = '';
          explanation.classList.remove('show');
        }}
      }});
      moduleEl.querySelector('.quiz-score').textContent = 'Score: ' + correct + '/' + questions.length + ' correct. ' + answered + '/' + questions.length + ' answered.';
      const retryButton = moduleEl.querySelector('.quiz-actions button');
      retryButton.disabled = missed.length === 0;
      retryButton.textContent = missed.length ? 'Retry missed (' + missed.length + ')' : 'Retry missed';
      nextButton.textContent = state.module < modules.length - 1 ? 'Next' : 'Finish';
    }}
    function updateToc() {{
      tocButtons.forEach(button => {{
        const moduleIndex = Number(button.dataset.module);
        const slideIndex = button.dataset.slide !== undefined ? Number(button.dataset.slide) : 0;
        const isQuiz = button.dataset.mode === 'quiz';
        button.classList.toggle('current', moduleIndex === state.module && ((isQuiz && state.mode === 'quiz') || (!isQuiz && state.mode !== 'quiz' && slideIndex === state.slide)));
      }});
    }}
    function render() {{
      clampState();
      modules.forEach((moduleEl, index) => {{
        const active = index === state.module;
        moduleEl.classList.toggle('active', active);
        if (active) {{
          renderSlide(state.module, state.slide);
          renderQuizPanel(state.module);
        }} else {{
          moduleEl.querySelector('.quiz-panel').classList.remove('active');
        }}
      }});
      const data = currentModuleData();
      moduleLabel.textContent = data.name;
      modeLabel.textContent = state.mode === 'quiz' ? 'Quiz mode' : 'Slide mode';
      const totalSteps = currentSlideCount() + 1;
      const currentStep = state.mode === 'quiz' ? totalSteps : state.slide + 1;
      counter.textContent = 'Module ' + (state.module + 1) + ' of ' + modules.length + ' - Step ' + currentStep + ' of ' + totalSteps;
      progress.style.width = Math.round((currentStep / totalSteps) * 100) + '%';
      nextButton.textContent = state.mode === 'quiz' ? (state.module < modules.length - 1 ? 'Next' : 'Finish') : (state.slide < currentSlideCount() - 1 ? 'Next' : 'Quiz');
      updateToc();
    }}
    function step(delta) {{
      if (state.mode === 'quiz') {{
        if (delta < 0) {{
          state.mode = 'slides';
          state.slide = Math.max(0, currentSlideCount() - 1);
          saveState();
          render();
        }} else if (state.module < modules.length - 1) {{
          jump(state.module + 1, 0, 'slides');
        }}
        return;
      }}
      if (delta > 0) {{
        if (state.slide < currentSlideCount() - 1) state.slide++;
        else state.mode = 'quiz';
      }} else if (delta < 0) {{
        if (state.slide > 0) state.slide--;
        else if (state.module > 0) {{
          state.module--;
          state.slide = window.WORKSHOP_INDEX.modules[state.module].slides - 1;
        }}
      }}
      saveState();
      render();
    }}
    function toggleToc(force) {{
      if (!window.matchMedia('(max-width: 920px)').matches) return;
      const toc = document.getElementById('toc');
      const shouldOpen = typeof force === 'boolean' ? force : !toc.classList.contains('open');
      toc.classList.toggle('open', shouldOpen);
      overlay.style.display = shouldOpen ? 'block' : 'none';
    }}
    function handleKeydown(event) {{
      if (event.key === 't' || event.key === 'T') return toggleToc();
      if (event.key === 'ArrowRight' || event.key === ' ') {{ if (!(event.key === ' ' && event.shiftKey)) step(1); else step(-1); event.preventDefault(); return; }}
      if (event.key === 'ArrowLeft') return step(-1);
      if (event.key === 'Home') return jump(0, 0, 'slides');
      if (event.key === 'End') {{ const last = modules.length - 1; return jump(last, window.WORKSHOP_INDEX.modules[last].slides - 1, 'quiz'); }}
    }}
    document.addEventListener('keydown', handleKeydown);
    saveState();
    render();
  </script>
</body>
</html>
"""


def build_toc_html(chapter: dict[str, object]) -> str:
    parts = []
    for module_index, module_data in enumerate(chapter["modules"]):
        buttons = []
        for slide_index, slide_data in enumerate(module_data["slides"]):
            buttons.append(
                f'<button type="button" data-jump="1" data-module="{module_index}" data-slide="{slide_index}" onclick="jump({module_index},{slide_index},\'slides\')">{esc(slide_data["title"])}</button>'
            )
        buttons.append(
            f'<button type="button" data-jump="1" data-module="{module_index}" data-mode="quiz" onclick="jump({module_index},0,\'quiz\')">Quiz</button>'
        )
        parts.append(
            block(
                f"""
                <div class="toc-module">
                  <h3>{esc(str(module_data["name"]))}</h3>
                  <div class="toc-list">{"".join(buttons)}</div>
                </div>
                """
            )
        )
    return "\n".join(parts)


def build_modules_html(chapter: dict[str, object]) -> str:
    return "\n".join(render_module(module_data, module_index) for module_index, module_data in enumerate(chapter["modules"]))


def build_html(chapter: dict[str, object]) -> str:
    return HTML_TEMPLATE.format(
        title=chapter["title"],
        toc_html=build_toc_html(chapter),
        modules_html=build_modules_html(chapter),
        index_json=json.dumps(build_index_data(chapter), ensure_ascii=True),
        storage_key_json=json.dumps(f"{chapter['slug']}_workshop_state", ensure_ascii=True),
    )


def write_chapter(chapter: dict[str, object]) -> tuple[Path, Path]:
    doc_root = OUTPUT_ROOT / str(chapter["slug"])
    doc_root.mkdir(parents=True, exist_ok=True)
    html_path = doc_root / f"{chapter['slug']}_workshop.html"
    quiz_path = doc_root / f"{chapter['slug']}_quiz.json"
    html_path.write_text(build_html(chapter), encoding="utf-8")
    quiz_path.write_text(json.dumps(build_quiz_json(chapter), indent=2), encoding="utf-8")
    return html_path, quiz_path


def main() -> None:
    for chapter in CHAPTERS:
        write_chapter(chapter)


if __name__ == "__main__":
    main()
