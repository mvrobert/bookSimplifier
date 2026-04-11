from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


TOPIC_SLUG = "chemical_reactions_and_equations"
WORKSHOP_TITLE = "Chemical Reactions and Equations Workshop"
WORKSHOP_SUBTITLE = "Interactive study deck generated from jesc101.pdf"


def clean_html(text: str) -> str:
    return dedent(text).strip()


def q(question_id: str, prompt: str, correct: str, wrong_1: str, wrong_2: str, wrong_3: str, explanation: str) -> dict[str, object]:
    return {
        "id": question_id,
        "question": prompt,
        "options": [correct, wrong_1, wrong_2, wrong_3],
        "answer": 0,
        "explanation": explanation,
    }


MODULES = [
    {
        "name": "M0: Detecting Chemical Change",
        "slides": [
            {
                "title": "Welcome and Navigation",
                "content": clean_html(
                    """
                    <h2>Chapter Scope</h2>
                    <p>This workshop is built from <code>jesc101.pdf</code>, the Class 10 chapter on Chemical Reactions and Equations. The source chapter opens with familiar situations such as souring milk, rusting iron, fermentation, cooking, digestion, and respiration to make one point clear: a chemical reaction is identified when the original substance changes into something with a new identity. The deck below keeps that same progression, moving from observation, to symbolic equations, to reaction types, and finally to oxidation in daily life.</p>
                    <table>
                      <tr><th>Key</th><th>Action</th></tr>
                      <tr><td>Space / Right Arrow</td><td>Next slide</td></tr>
                      <tr><td>Shift+Space / Left Arrow</td><td>Previous slide</td></tr>
                      <tr><td>Home / End</td><td>Jump to first or last slide</td></tr>
                      <tr><td>T</td><td>Open the table of contents</td></tr>
                      <tr><td>R</td><td>Retry failed quiz questions</td></tr>
                    </table>
                    <div class="note"><strong>Source note:</strong> This deck follows the progression on pages 1-16 of <code>jesc101.pdf</code> and turns the chapter into workshop-style modules with review quizzes.</div>
                    """
                ),
            },
            {
                "title": "How We Know a Chemical Reaction Happened",
                "content": clean_html(
                    """
                    <h2>Everyday Indicators</h2>
                    <p>The chapter begins by asking learners to observe everyday events rather than memorise definitions. Milk left out in summer turns sour, food is cooked, grapes ferment, and food is digested in the body. In each case, the starting material does not merely change shape or size; it becomes chemically different. The text then turns these observations into practical indicators used in the lab and in exam questions: change in state, change in colour, evolution of a gas, and change in temperature.</p>
                    <div class="diagram">
                    Daily observation -> visible clue -> inference
                    sour milk       -> smell/taste shift -> new substances formed
                    rusting iron    -> reddish coating   -> oxidation occurred
                    acid + metal    -> bubbles           -> gas evolved
                    burning metal   -> heat/light/ash    -> product formed
                    </div>
                    <div class="tip"><strong>Exam habit:</strong> when a question gives observations such as bubbling, colour fade, precipitate formation, or heat release, it is usually prompting you to identify the reaction evidence before naming the reaction type.</div>
                    """
                ),
            },
            {
                "title": "Activities That Establish the Evidence",
                "content": clean_html(
                    """
                    <h2>Three Foundational Activities</h2>
                    <p>The source chapter uses simple demonstrations to anchor the topic. Burning a cleaned magnesium ribbon in air produces a bright flame and white magnesium oxide ash. Adding dilute hydrochloric or sulphuric acid to zinc granules releases hydrogen gas and changes the temperature of the vessel. Mixing lead nitrate and potassium iodide solutions forms a yellow precipitate of lead iodide. These are not random lab tricks; together they cover the most common reaction signals: energy release, gas evolution, and precipitate formation.</p>
                    <table>
                      <tr><th>Activity</th><th>Observation</th><th>Concept reinforced</th></tr>
                      <tr><td>Magnesium + oxygen</td><td>Bright light, white ash</td><td>New product formed</td></tr>
                      <tr><td>Zinc + dilute acid</td><td>Bubbles, warmer flask</td><td>Gas evolution and temperature change</td></tr>
                      <tr><td>Lead nitrate + potassium iodide</td><td>Yellow solid appears</td><td>Precipitation</td></tr>
                    </table>
                    <div class="warn"><strong>Lab note:</strong> the textbook explicitly warns that magnesium burning should be handled with teacher assistance and with eye protection because the flame is intense.</div>
                    """
                ),
            },
            {
                "title": "From Description to Word Equation",
                "content": clean_html(
                    """
                    <h2>Why We Write Reactions Symbolically</h2>
                    <p>A sentence such as "when magnesium ribbon is burnt in oxygen, it forms magnesium oxide" is scientifically correct, but it is too long to compare, classify, or balance efficiently. The chapter therefore introduces the word equation as the first compact representation: <code>magnesium + oxygen -> magnesium oxide</code>. This step matters because it separates reactants from products and prepares the learner to replace names with chemical formulae. Once that shift is made, reaction analysis becomes systematic instead of verbal.</p>
                    <div class="real"><strong>Real classroom value:</strong> many balancing mistakes happen because students rush directly to formulae. If the reactants and products are wrong at the word-equation stage, balancing will only preserve the wrong chemistry more neatly.</div>
                    <p>Think of the flow as: observe the event, describe it in words, identify the substances, and only then move into symbols and coefficients.</p>
                    """
                ),
            },
        ],
        "questions": [
            q("q0_1", "Which observation from the chapter is a clear sign that a chemical reaction has taken place?", "Evolution of a gas", "A change in the shape of a beaker", "A substance being cut into pieces", "A solid being ground into powder", "Page 2 lists gas evolution, colour change, state change, and temperature change as reaction indicators."),
            q("q0_2", "Why is a magnesium ribbon cleaned before it is burned in air?", "To remove the oxide layer so magnesium can react properly", "To make it dissolve in water faster", "To increase its mass before burning", "To cool the ribbon down", "The chapter asks students to rub the ribbon with sandpaper so the surface oxide layer does not interfere."),
            q("q0_3", "What is formed when magnesium burns in oxygen?", "Magnesium oxide", "Magnesium hydroxide", "Magnesium sulphate", "Magnesium chloride", "The opening activity states that burning magnesium in oxygen produces magnesium oxide."),
            q("q0_4", "In the zinc and dilute acid activity, the bubbles indicate the release of which gas?", "Hydrogen", "Oxygen", "Nitrogen", "Carbon dioxide", "On pages 1-2, zinc reacting with dilute acid is used to show gas evolution; the gas formed is hydrogen."),
            q("q0_5", "What visible result is observed when lead nitrate solution is mixed with potassium iodide solution?", "A yellow precipitate forms", "A blue gas forms", "The liquid freezes instantly", "No visible change occurs", "The lead nitrate and potassium iodide activity is used to show the formation of a yellow precipitate."),
            q("q0_6", "Which daily-life example in the chapter is used to illustrate chemical change?", "Fermentation of grapes", "Melting of ice", "Breaking a glass", "Sharpening a pencil", "Page 1 lists grape fermentation among the familiar chemical changes."),
            q("q0_7", "Which statement best distinguishes a chemical change from a physical change in this chapter?", "The identity of the original substance changes", "Only the size of the substance changes", "The material can always be restored by cooling", "The mass disappears completely", "The introduction emphasises that the nature and identity of the initial substance change in a chemical reaction."),
            q("q0_8", "In a word equation, substances written before the arrow are called", "reactants", "products", "catalysts", "precipitates", "The chapter uses the word-equation format to separate reactants from products."),
            q("q0_9", "What is the main purpose of converting a reaction description into a word equation first?", "To make the reaction shorter and easier to analyse", "To avoid naming the products", "To remove the need for formulae later", "To prove that balancing is unnecessary", "Page 2 explains that sentence descriptions are long, and word equations provide a shorter, clearer representation."),
            q("q0_10", "Which of the following is NOT listed as evidence of a chemical reaction on page 2?", "Change in shape", "Change in colour", "Change in temperature", "Evolution of a gas", "The text explicitly lists colour, state, gas evolution, and temperature change, not shape change."),
            q("q0_11", "Respiration is included in the chapter introduction because it is", "a chemical reaction occurring inside the body", "a purely physical change", "an example of only volume expansion", "a way to separate mixtures", "The first page uses respiration as an everyday example of chemical change."),
            q("q0_12", "Digestion is treated as a chemical process in the chapter because", "food is transformed into different substances in the body", "food only changes shape mechanically", "the body cools down during digestion", "digestion is only a filtration process", "The introduction groups digestion with other processes where the original substance changes identity."),
            q("q0_13", "When a reaction vessel becomes warmer during a reaction, the observation mainly indicates", "a temperature change associated with reaction", "that the vessel has broken", "that the reaction must be physical", "that no new substance is formed", "The zinc and acid activity asks students to touch the flask and notice the temperature change."),
            q("q0_14", "Which pair from the chapter is mixed to demonstrate precipitate formation?", "Lead nitrate and potassium iodide", "Hydrogen and oxygen", "Sodium and water", "Copper and oxygen", "The early activities use lead nitrate solution plus potassium iodide solution to show precipitate formation."),
            q("q0_15", "Which sequence best matches the textbook's learning flow?", "Observation -> verbal description -> word equation -> symbolic equation", "Balancing -> precipitation -> corrosion -> observation", "Formula memorisation -> guessing products -> observation", "Redox definition -> gas test -> word equation", "The chapter starts from observed changes, then describes them in words, and only after that moves toward symbolic equations."),
        ],
    },
    {
        "name": "M1: Writing and Balancing Equations",
        "slides": [
            {
                "title": "Symbolic Equations and State Symbols",
                "content": clean_html(
                    """
                    <h2>From Names to Formulae</h2>
                    <p>After introducing word equations, the chapter replaces substance names with chemical formulae. That gives a compact symbolic equation such as <code>Mg + O2 -> MgO</code>, which can then be refined into a balanced equation. The text also stresses complete notation: if the physical state is known, it should be written using <code>(s)</code>, <code>(l)</code>, <code>(g)</code>, and <code>(aq)</code>. This turns a reaction line into a much richer scientific statement because it reveals whether a reactant is a solid, liquid, gas, or dissolved in water.</p>
                    <table>
                      <tr><th>Symbol</th><th>Meaning</th></tr>
                      <tr><td>(s)</td><td>Solid</td></tr>
                      <tr><td>(l)</td><td>Liquid</td></tr>
                      <tr><td>(g)</td><td>Gas</td></tr>
                      <tr><td>(aq)</td><td>Aqueous solution</td></tr>
                    </table>
                    <div class="note">A complete equation records both the chemistry and the state of each substance. That matters in later topics such as precipitation and gas evolution.</div>
                    """
                ),
            },
            {
                "title": "Balancing by Counting Atoms",
                "content": clean_html(
                    """
                    <h2>Method Used in the Chapter</h2>
                    <p>The chapter demonstrates balancing through a structured atom-count method. In the example <code>Fe + H2O -> Fe3O4 + H2</code>, boxes are mentally placed around the formulae so the student remembers not to alter subscripts. The next step is to count atoms of iron, hydrogen, and oxygen on both sides, then adjust coefficients until the counts match. The worked solution arrives at <code>3Fe + 4H2O -> Fe3O4 + 4H2</code>. This example is important because it shows balancing as a logical correction of counts, not a guessing game.</p>
                    <div class="diagram">
                    Start:   Fe + H2O -> Fe3O4 + H2
                    Count:   Fe 1|3, H 2|2, O 1|4
                    Adjust:  3Fe + 4H2O -> Fe3O4 + 4H2
                    Check:   Fe 3|3, H 8|8, O 4|4
                    </div>
                    <div class="tip"><strong>Rule:</strong> change coefficients in front of formulae, never the subscripts inside a chemical formula. Changing a subscript changes the substance itself.</div>
                    """
                ),
            },
            {
                "title": "Why Balanced Equations Matter",
                "content": clean_html(
                    """
                    <h2>Conservation of Mass in Practice</h2>
                    <p>A skeletal equation only tells you which substances react and which substances form. A balanced equation goes further and respects the law of conservation of mass by ensuring that the number of atoms of each element is the same on both sides. The chapter makes this explicit: atoms do not disappear, and atoms of one element do not change into atoms of another. Balancing therefore is not cosmetic. It is the way a written equation is made physically consistent with what actually happens during the reaction.</p>
                    <div class="warn"><strong>Common mistake:</strong> students often see <code>H2</code> or <code>O2</code> and try to "balance" by editing the subscript. That is not balancing. It is inventing a different substance.</div>
                    <p>Once an equation is balanced, it can support stoichiometric reasoning, classification of reaction type, and more advanced analysis later in chemistry.</p>
                    """
                ),
            },
            {
                "title": "Worked Examples You Should Recognise",
                "content": clean_html(
                    """
                    <h2>Pattern Recognition</h2>
                    <p>The chapter repeatedly moves between observation and correct symbolic form. Burning magnesium is finally written as <code>2Mg(s) + O2(g) -> 2MgO(s)</code>. Zinc reacting with acid can be expressed using a balanced equation that produces a salt and hydrogen gas. Precipitation examples include aqueous reactants and a solid product. These patterns are worth memorising not as isolated facts but as templates: combination reactions often reduce many inputs to one product, precipitation reactions often show <code>(aq)</code> reactants producing an insoluble <code>(s)</code> product, and balancing always comes after the right formulae are established.</p>
                    <div class="real"><strong>Fast test strategy:</strong> when you are given a word equation in an exam, first write correct formulae, then add state symbols if known, then balance, and only then classify the reaction.</div>
                    """
                ),
            },
        ],
        "questions": [
            q("q1_1", "What does the state symbol (aq) represent in a chemical equation?", "A substance dissolved in water", "A substance in gaseous form", "A substance in solid crystalline form", "A substance exposed to air", "The chapter uses (aq) for aqueous solution, meaning dissolved in water."),
            q("q1_2", "Which state symbol stands for a gas?", "(g)", "(s)", "(l)", "(aq)", "Pages 3-5 list the standard state symbols used in complete chemical equations."),
            q("q1_3", "What is the main difference between a skeletal equation and a balanced equation?", "A balanced equation has equal numbers of each type of atom on both sides", "A skeletal equation always includes heat terms", "A balanced equation never uses formulae", "A skeletal equation contains only products", "The chapter explains that balancing makes the atom counts equal on both sides."),
            q("q1_4", "In balancing equations, what are you allowed to change?", "Only the coefficients in front of formulae", "Only the subscripts inside formulae", "Only the product names", "Only the state symbols", "The balancing method explicitly says not to change anything inside the formula boxes."),
            q("q1_5", "What is the balanced form of Fe + H2O -> Fe3O4 + H2 shown in the chapter?", "3Fe + 4H2O -> Fe3O4 + 4H2", "Fe + H2O -> Fe3O4 + H2", "2Fe + 2H2O -> Fe2O3 + 2H2", "4Fe + H2O -> Fe3O4 + H2", "Pages 4-5 work this example through and end with 3Fe + 4H2O -> Fe3O4 + 4H2."),
            q("q1_6", "Why must chemical equations be balanced?", "Because atoms are conserved during a chemical reaction", "Because products must always outnumber reactants", "Because only balanced equations can include solids", "Because balancing changes the reaction type", "The text ties balancing directly to the conservation of mass and unchanged atom counts."),
            q("q1_7", "Which representation is the first shortened step after a sentence description of a reaction?", "A word equation", "An ionic equation", "A periodic table entry", "A structural formula diagram", "Page 2 introduces the word equation before the symbolic equation."),
            q("q1_8", "What does the symbol (s) mean in a complete chemical equation?", "Solid", "Solution", "Suspension", "Steam", "The state-symbol table in the chapter uses (s) for solid."),
            q("q1_9", "If a student changes O2 to O3 while balancing, what has gone wrong?", "They changed the substance instead of the coefficient", "They correctly balanced oxygen atoms", "They converted a product into a reactant", "They only changed the physical state", "The chapter's box method exists to prevent altering subscripts and therefore changing the identity of the substance."),
            q("q1_10", "Which part of a balanced equation shows how many units of a substance participate?", "The coefficient written before the formula", "The subscript inside the formula", "The chapter number", "The state symbol in brackets", "Balancing uses coefficients outside formulae to adjust atom counts."),
            q("q1_11", "Which symbol shows a liquid state?", "(l)", "(g)", "(aq)", "(s)", "The chapter lists (l) as the notation for liquid."),
            q("q1_12", "What should you do immediately after writing formulae for reactants and products in an exam?", "Balance the equation by checking atom counts", "Rename all products in words again", "Remove the arrow and use an equals sign", "Delete all state symbols", "The chapter's method is formulae first, then balancing by counting atoms."),
            q("q1_13", "Why are state symbols especially useful in precipitation reactions?", "They show which product is an insoluble solid", "They remove the need to balance the equation", "They prove a reaction is exothermic", "They indicate the mass of each substance", "Later in the chapter, precipitation reactions are identified partly by the solid product written with (s)."),
            q("q1_14", "Which statement about a complete chemical equation is correct?", "It can show reactants, products, and physical states symbolically", "It only lists the names of products", "It must avoid formulae", "It cannot include gases", "The chapter summary on page 14 states this directly."),
            q("q1_15", "What is the balanced equation for burning magnesium in oxygen?", "2Mg + O2 -> 2MgO", "Mg + O -> MgO", "Mg + O2 -> MgO2", "2Mg + O -> 2MgO", "The magnesium reaction becomes balanced by placing coefficient 2 before Mg and MgO."),
        ],
    },
    {
        "name": "M2: Classifying Reaction Types",
        "slides": [
            {
                "title": "Combination Reactions and Heat Release",
                "content": clean_html(
                    """
                    <h2>Many Reactants, One Product</h2>
                    <p>In a combination reaction, two or more substances combine to form a single product. The chapter uses calcium oxide plus water as the anchor example: <code>CaO(s) + H2O(l) -> Ca(OH)2(aq) + Heat</code>. Because the beaker becomes hot, the example also introduces the idea of exothermic reactions. That pairing is useful. Students often memorise reaction types and heat flow separately, but the textbook shows that a single reaction can be both a combination reaction and exothermic.</p>
                    <div class="diagram">
                    Calcium oxide + water
                              |
                              v
                       calcium hydroxide + heat
                    </div>
                    <div class="tip">Burning coal and formation of water from hydrogen and oxygen are included as additional combination reactions on page 7.</div>
                    """
                ),
            },
            {
                "title": "Decomposition Reactions Need Energy Input",
                "content": clean_html(
                    """
                    <h2>One Reactant Breaking Apart</h2>
                    <p>Decomposition reactions are described as the opposite of combination reactions. Instead of several reactants joining, one compound splits into simpler substances. The chapter presents three triggers: heat, electricity, and light. Thermal decomposition is shown through ferrous sulphate and lead nitrate, electrolytic decomposition through water, and photochemical decomposition through silver chloride and silver bromide in sunlight. This section also introduces endothermic reactions because decomposition often requires energy input to break chemical bonds.</p>
                    <table>
                      <tr><th>Trigger</th><th>Example in chapter</th><th>Product clue</th></tr>
                      <tr><td>Heat</td><td>Lead nitrate</td><td>Brown fumes of nitrogen dioxide</td></tr>
                      <tr><td>Electricity</td><td>Water</td><td>Hydrogen and oxygen gases</td></tr>
                      <tr><td>Light</td><td>Silver chloride / silver bromide</td><td>Used in photography</td></tr>
                    </table>
                    """
                ),
            },
            {
                "title": "Displacement Reactions Depend on Reactivity",
                "content": clean_html(
                    """
                    <h2>One Element Replaces Another</h2>
                    <p>When iron nails are placed in copper sulphate solution, the blue colour fades and the nails become coated with deposited copper. The equation <code>Fe + CuSO4 -> FeSO4 + Cu</code> shows that iron displaces copper from its compound. The chapter then adds zinc and lead examples to reinforce the reactivity idea: more reactive elements displace less reactive ones from their compounds. This section is especially useful for classification questions because the defining clue is not colour or gas but substitution of one element by another.</p>
                    <div class="real"><strong>Interpretation shortcut:</strong> if the reaction looks like element + compound -> new compound + displaced element, first test whether it is a displacement reaction before considering other labels.</div>
                    """
                ),
            },
            {
                "title": "Double Displacement and Precipitation",
                "content": clean_html(
                    """
                    <h2>Exchange of Ions</h2>
                    <p>Double displacement reactions involve an exchange of ions between two compounds. The chapter's main example is <code>Na2SO4(aq) + BaCl2(aq) -> BaSO4(s) + 2NaCl(aq)</code>. The key observation is the formation of insoluble white barium sulphate, which is why this is also called a precipitation reaction. Unlike single displacement, no free element appears. Instead, two ionic partners swap places and one newly formed compound falls out of solution as a solid.</p>
                    <div class="diagram">
                    Na2SO4(aq) + BaCl2(aq)
                        ion exchange
                              |
                              v
                    BaSO4(s) + 2NaCl(aq)
                    </div>
                    <div class="note">The chapter later asks learners to revisit the yellow lead iodide example and notice that it also fits the double displacement pattern.</div>
                    """
                ),
            },
        ],
        "questions": [
            q("q2_1", "What is the defining feature of a combination reaction?", "Two or more reactants form a single product", "One compound splits into simpler substances", "A metal loses shine in air", "An insoluble solid dissolves in water", "Page 6 defines combination reactions as reactions in which a single product forms from two or more reactants."),
            q("q2_2", "Which textbook reaction is used to show a combination reaction with heat release?", "CaO + H2O -> Ca(OH)2 + Heat", "Fe + CuSO4 -> FeSO4 + Cu", "Na2SO4 + BaCl2 -> BaSO4 + 2NaCl", "CuO + H2 -> Cu + H2O", "The calcium oxide and water example on page 6 is both a combination and an exothermic reaction."),
            q("q2_3", "A reaction in which heat is given out along with the products is called", "exothermic", "endothermic", "displacement", "photolytic", "The chapter summary on page 14 defines exothermic reactions this way."),
            q("q2_4", "Decomposition reactions are described as", "the opposite of combination reactions", "always displacement reactions", "reactions with no products", "reactions involving only metals", "The chapter explicitly calls decomposition the opposite of combination."),
            q("q2_5", "Which type of energy causes decomposition of silver chloride in the chapter?", "Light", "Sound", "Magnetism", "Pressure", "The silver chloride and silver bromide examples are photochemical decompositions caused by sunlight."),
            q("q2_6", "What is the volume ratio of gases obtained when water is decomposed by electricity?", "Hydrogen is collected in double the amount of oxygen", "Oxygen is collected in double the amount of hydrogen", "Equal amounts of nitrogen and oxygen are formed", "Only hydrogen is formed", "The chapter asks why one test tube collects double the gas and identifies it as hydrogen."),
            q("q2_7", "Which reaction type best describes Fe + CuSO4 -> FeSO4 + Cu?", "Displacement reaction", "Combination reaction", "Neutralisation reaction", "Combustion reaction", "Iron displaces copper from copper sulphate, so page 11 identifies it as a displacement reaction."),
            q("q2_8", "Why can zinc displace copper from copper sulphate solution?", "Zinc is more reactive than copper", "Copper is more reactive than zinc", "Copper is a gas", "Zinc is always aqueous", "The chapter states that zinc and lead are more reactive than copper and can therefore displace it."),
            q("q2_9", "In a double displacement reaction, what is exchanged between the reactants?", "Ions or groups of atoms", "Only electrons from one atom", "Only heat energy", "Only state symbols", "Page 12 explains that double displacement reactions involve exchange of ions between reactants."),
            q("q2_10", "Why is Na2SO4 + BaCl2 -> BaSO4 + 2NaCl also called a precipitation reaction?", "Because insoluble barium sulphate is formed", "Because water evaporates completely", "Because both reactants are metals", "Because light is required", "The white insoluble BaSO4 formed in the reaction is a precipitate."),
            q("q2_11", "Which of the following is a decomposition reaction from the chapter?", "Heating lead nitrate", "Burning coal in oxygen", "Iron placed in copper sulphate", "Mixing sodium sulphate with barium chloride", "Lead nitrate breaks down on heating, so it is a decomposition reaction."),
            q("q2_12", "Reactions that absorb energy are known as", "endothermic", "exothermic", "corrosive", "substitution", "The chapter notes that decomposition often requires energy and calls such reactions endothermic."),
            q("q2_13", "Which description matches a displacement reaction pattern?", "Element + compound -> new compound + new element", "Compound + compound -> single product", "Element + element -> single product only", "Compound -> compound without any change", "This is the structural pattern of the iron-copper sulphate example."),
            q("q2_14", "What is the colour of the precipitate formed in the sodium sulphate and barium chloride activity?", "White", "Blue", "Green", "Black", "Page 11 says the insoluble precipitate formed is white barium sulphate."),
            q("q2_15", "What kind of reaction is represented by lead nitrate plus potassium iodide forming lead iodide and potassium nitrate?", "Double displacement reaction", "Combination reaction", "Only a physical change", "Displacement by a free metal", "The chapter revisits this yellow precipitate example and points out that it also fits double displacement."),
        ],
    },
    {
        "name": "M3: Redox, Corrosion, and Rancidity",
        "slides": [
            {
                "title": "Oxidation and Reduction Through Oxygen Transfer",
                "content": clean_html(
                    """
                    <h2>Using Copper and Copper Oxide</h2>
                    <p>The redox section starts with copper powder being heated in air to form black copper(II) oxide. That step is oxidation because copper gains oxygen. The reverse idea is then shown by passing hydrogen over hot copper(II) oxide, which removes oxygen and leaves brown copper behind. The chapter uses this pair to define the terms clearly: gain of oxygen means oxidation, loss of oxygen means reduction. It also points out that the same reaction can oxidise one reactant while reducing another.</p>
                    <div class="diagram">
                    2Cu + O2 -> 2CuO      (copper gains oxygen)
                    CuO + H2 -> Cu + H2O  (CuO loses oxygen)
                    </div>
                    <div class="tip">If you can identify which substance gains oxygen and which one loses oxygen, most basic redox questions in this chapter become straightforward.</div>
                    """
                ),
            },
            {
                "title": "A Broader Redox Rule",
                "content": clean_html(
                    """
                    <h2>Oxygen and Hydrogen Both Matter</h2>
                    <p>The chapter extends the redox definition beyond oxygen alone. A substance is oxidised if it gains oxygen or loses hydrogen. A substance is reduced if it loses oxygen or gains hydrogen. This broader rule helps interpret reactions such as <code>ZnO + C -> Zn + CO</code> and <code>MnO2 + 4HCl -> MnCl2 + 2H2O + Cl2</code>. In both cases, one reactant is oxidised while another is reduced. That paired change is exactly why these are called oxidation-reduction or redox reactions.</p>
                    <div class="note">Redox analysis is often easier if you ask two questions in order: who gains oxygen, and who loses oxygen? If oxygen is not obvious, check who gains or loses hydrogen.</div>
                    """
                ),
            },
            {
                "title": "Oxidation in Everyday Life",
                "content": clean_html(
                    """
                    <h2>Corrosion and Rancidity</h2>
                    <p>After the equation-heavy sections, the chapter returns to everyday life. Corrosion is defined as the attack of a metal by moisture, acids, or other substances in the surroundings. Rusting of iron is the most familiar example, but silver developing a black coating and copper developing a green coating are also cited. Rancidity is the oxidation of fats and oils in food, which changes smell and taste. To slow rancidity, foods are kept in airtight containers, antioxidants are added, and chip packets are flushed with nitrogen.</p>
                    <table>
                      <tr><th>Process</th><th>Visible effect</th><th>Prevention idea</th></tr>
                      <tr><td>Corrosion of iron</td><td>Reddish-brown rust</td><td>Reduce contact with moisture and air</td></tr>
                      <tr><td>Rancidity of food oils</td><td>Bad smell and taste</td><td>Airtight storage, antioxidants, nitrogen flushing</td></tr>
                    </table>
                    """
                ),
            },
            {
                "title": "Chapter Recap and Classification Checklist",
                "content": clean_html(
                    """
                    <h2>How to Solve Most Questions in This Chapter</h2>
                    <p>A practical problem-solving order emerges from the chapter summary. First, identify the reactants and products correctly. Second, write a complete equation with state symbols where relevant. Third, balance the equation so atom counts match. Fourth, classify the reaction by looking for structural clues: many reactants to one product, one reactant breaking apart, one element replacing another, ion exchange with precipitate, or oxygen/hydrogen transfer. Finally, connect the reaction to real-life meaning when appropriate, especially for corrosion, respiration, digestion, and rancidity.</p>
                    <div class="real"><strong>Fast checklist:</strong> observe the clue, write the equation, balance it, classify it, and explain the observation. That sequence matches the teaching style of the original chapter and prevents most avoidable mistakes.</div>
                    """
                ),
            },
        ],
        "questions": [
            q("q3_1", "If a substance gains oxygen during a reaction, it is said to be", "oxidised", "neutralised", "precipitated", "distilled", "Page 12 defines oxidation as gain of oxygen."),
            q("q3_2", "If a substance loses oxygen during a reaction, it is said to be", "reduced", "combined", "vaporised", "dissolved", "The chapter defines reduction as loss of oxygen."),
            q("q3_3", "When copper powder is heated in air, what black substance forms?", "Copper(II) oxide", "Copper sulphate", "Copper chloride", "Copper carbonate", "The oxidation activity shows copper becoming coated with black copper oxide."),
            q("q3_4", "In the reaction CuO + H2 -> Cu + H2O, which substance is reduced?", "CuO", "H2", "H2O", "Both are only oxidised", "Copper(II) oxide loses oxygen and is therefore reduced."),
            q("q3_5", "In the reaction CuO + H2 -> Cu + H2O, hydrogen is", "oxidised", "reduced", "precipitated", "unchanged", "Hydrogen gains oxygen to form water, so it is oxidised."),
            q("q3_6", "Why are reactions involving both oxidation and reduction called redox reactions?", "Because one reactant is oxidised while another is reduced", "Because they always involve red-coloured products", "Because they are restricted to rusting only", "Because they cannot be balanced", "Page 12 explicitly states that one reactant is oxidised while the other is reduced."),
            q("q3_7", "Which statement about ZnO + C -> Zn + CO is correct according to the chapter?", "Carbon is oxidised and zinc oxide is reduced", "Carbon is reduced and zinc is oxidised", "Both carbon and zinc oxide are oxidised", "No redox change occurs", "Page 13 explains that in reaction (1.31), carbon is oxidised to CO and ZnO is reduced to Zn."),
            q("q3_8", "Corrosion is the process in which", "a metal is attacked by substances like moisture or acids in its surroundings", "a salt dissolves in water", "a gas forms from every reaction", "food is always heated", "Page 13 defines corrosion using attack by moisture, acids, and surrounding substances."),
            q("q3_9", "What is the common visible sign of rusting iron mentioned in the chapter?", "A reddish-brown coating", "A white crystalline crust", "A blue solution", "A yellow gas", "The text describes rusting as a reddish-brown powdery coating on iron."),
            q("q3_10", "What kind of coating is mentioned for silver during corrosion?", "Black", "Green", "Red", "White", "The chapter gives black coating on silver as an example of corrosion/tarnishing."),
            q("q3_11", "What kind of coating is mentioned for copper during corrosion?", "Green", "Black", "Yellow", "Brown", "Page 13 mentions the green coating formed on copper."),
            q("q3_12", "Rancidity happens when", "fats and oils get oxidised", "water freezes in food", "food is filtered", "salt precipitates from food", "The chapter defines rancidity as oxidation of fats and oils, changing smell and taste."),
            q("q3_13", "Why do chips manufacturers flush packets with nitrogen according to the chapter?", "To prevent oxidation of the chips", "To make the chips heavier", "To heat the chips during packing", "To add extra smell", "Page 13 says nitrogen is used to reduce oxidation and prevent rancidity."),
            q("q3_14", "Which storage method helps slow down rancidity?", "Keeping food in airtight containers", "Leaving food exposed to humid air", "Adding more oxygen to the packet", "Storing oil in open trays", "The chapter notes airtight storage as a way to slow oxidation of oils and fats."),
            q("q3_15", "In the reaction 2PbO + C -> 2Pb + CO2, which statement is correct?", "Carbon is oxidised and lead oxide is reduced", "Carbon is reduced and lead is oxidised", "Only lead is oxidised", "No oxidation or reduction takes place", "The summary exercise on page 14 tests this exact redox interpretation."),
        ],
    },
]


def build_slides() -> list[dict[str, object]]:
    slides: list[dict[str, object]] = []
    for module_index, module in enumerate(MODULES):
        for slide in module["slides"]:
            slides.append({"m": module_index, "t": slide["title"], "c": slide["content"]})
        slides.append({"m": module_index, "t": f"Quiz: {module['name']}", "q": True})
    return slides


def build_quiz_data() -> dict[str, object]:
    modules = []
    for module_index, module in enumerate(MODULES):
        modules.append({"id": module_index, "name": module["name"], "questions": module["questions"]})
    return {
        "title": f"{WORKSHOP_TITLE} - {WORKSHOP_SUBTITLE}",
        "version": "1.0",
        "totalQuestions": sum(len(module["questions"]) for module in MODULES),
        "modules": modules,
    }


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>__TITLE__</title>
  <style>
    :root {
      --bg: #f8f9fa;
      --text: #1a1a2e;
      --muted: #64748b;
      --surface: #ffffff;
      --border: #e2e8f0;
      --primary: #2563eb;
      --secondary: #7c3aed;
      --good: #16a34a;
      --bad: #dc2626;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background:
        radial-gradient(circle at top left, rgba(37, 99, 235, 0.08), transparent 32%),
        radial-gradient(circle at top right, rgba(124, 58, 237, 0.10), transparent 30%),
        var(--bg);
      color: var(--text);
      font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
    }
    code, pre, .diagram {
      font-family: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace;
    }
    #progress-bar {
      position: fixed;
      top: 0;
      left: 0;
      height: 4px;
      width: 0;
      background: linear-gradient(90deg, #2563eb, #7c3aed);
      z-index: 1000;
    }
    #app {
      max-width: 1100px;
      margin: 0 auto;
      padding: 18px 16px 36px;
    }
    #header {
      position: sticky;
      top: 6px;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(226, 232, 240, 0.9);
      border-radius: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 12px 16px;
      margin-bottom: 18px;
      z-index: 100;
      box-shadow: 0 6px 16px rgba(15, 23, 42, 0.08);
    }
    #header .left,
    #header .center,
    #header .right {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    #header .center {
      justify-content: center;
      flex: 1;
    }
    #header .left {
      min-width: 220px;
      font-weight: 600;
    }
    #pct {
      min-width: 46px;
      text-align: right;
      font-weight: 700;
      color: var(--primary);
    }
    button {
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 14px;
      background: #fff;
      color: var(--text);
      cursor: pointer;
      font-weight: 600;
    }
    button:hover {
      border-color: var(--primary);
    }
    #slide {
      background: var(--surface);
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
      padding: 40px 48px;
      min-height: 520px;
      border: 1px solid rgba(226, 232, 240, 0.85);
    }
    #slide h1 {
      margin-top: 0;
      margin-bottom: 24px;
      font-size: 2rem;
      line-height: 1.2;
    }
    #slide h2 {
      margin-top: 0;
      color: var(--primary);
    }
    #slide p,
    #slide li,
    #slide td,
    #slide th {
      line-height: 1.7;
      font-size: 1.03rem;
    }
    #slide pre {
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
      white-space: pre;
      overflow-x: auto;
    }
    #slide table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    #slide th,
    #slide td {
      border: 1px solid var(--border);
      padding: 10px 12px;
      text-align: left;
      vertical-align: top;
    }
    #slide tr:hover td {
      background: #f8fafc;
    }
    .diagram {
      border: 2px dashed #cbd5e1;
      background: #f8fafc;
      border-radius: 10px;
      padding: 16px;
      white-space: pre;
      overflow-x: auto;
      margin: 18px 0;
    }
    .note,
    .tip,
    .warn,
    .real {
      border-left: 5px solid;
      padding: 14px 16px;
      border-radius: 10px;
      margin: 18px 0;
    }
    .note { border-color: #2563eb; background: #eff6ff; }
    .tip { border-color: #22c55e; background: #f0fdf4; }
    .warn { border-color: #eab308; background: #fefce8; }
    .real { border-color: #7c3aed; background: #faf5ff; }
    .quiz-container {
      max-width: 700px;
      margin: 0 auto;
    }
    .quiz-opt {
      width: 100%;
      text-align: left;
      margin-bottom: 12px;
      border: 2px solid var(--border);
      transition: border-color 0.15s ease, background 0.15s ease;
    }
    .quiz-opt.correct {
      border-color: var(--good);
      background: #f0fdf4;
    }
    .quiz-opt.wrong {
      border-color: var(--bad);
      background: #fef2f2;
    }
    .quiz-opt.disabled {
      pointer-events: none;
      opacity: 0.78;
    }
    .quiz-feedback {
      display: none;
      border-radius: 10px;
      padding: 14px 16px;
      margin-top: 16px;
    }
    .quiz-feedback.show { display: block; }
    .quiz-feedback.pass {
      background: #dcfce7;
      color: #166534;
    }
    .quiz-feedback.fail {
      background: #fee2e2;
      color: #991b1b;
    }
    #nav {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      margin-top: 18px;
    }
    #nav .prev {
      background: #e2e8f0;
    }
    #nav .next {
      background: var(--primary);
      color: #fff;
      border-color: var(--primary);
    }
    #toc {
      position: fixed;
      top: 0;
      left: -360px;
      width: 350px;
      height: 100vh;
      background: #ffffff;
      border-right: 1px solid var(--border);
      z-index: 201;
      transition: left 0.2s ease;
      padding: 24px 18px;
      overflow-y: auto;
      box-shadow: 8px 0 24px rgba(15, 23, 42, 0.1);
    }
    #toc.open {
      left: 0;
    }
    #toc-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.32);
      z-index: 200;
    }
    #toc-overlay.open {
      display: block;
    }
    .toc-module {
      margin-bottom: 18px;
      padding-bottom: 14px;
      border-bottom: 1px solid #eef2f7;
    }
    .toc-module h3 {
      margin: 0 0 10px 0;
      color: var(--secondary);
    }
    .toc-link {
      display: block;
      width: 100%;
      text-align: left;
      margin-bottom: 6px;
      background: #fff;
    }
    .toc-link.current {
      border-color: var(--primary);
      background: #eff6ff;
    }
    .quiz-meta {
      color: var(--muted);
      margin-bottom: 14px;
    }
    @media (max-width: 768px) {
      #slide { padding: 20px 24px; }
      #header {
        flex-direction: column;
        align-items: stretch;
      }
      #header .left,
      #header .center,
      #header .right {
        justify-content: space-between;
        min-width: 0;
      }
    }
    @media print {
      #header, #nav, #progress-bar, #toc, #toc-overlay { display: none !important; }
      #slide { box-shadow: none; border: none; }
      body { background: #fff; }
    }
  </style>
</head>
<body>
  <div id="progress-bar"></div>
  <div id="app">
    <div id="header">
      <div class="left" id="module-label">Module 0</div>
      <div class="center" id="slide-counter">1 / 1</div>
      <div class="right">
        <button onclick="toggleTOC()" title="Table of Contents (T)">TOC</button>
        <button onclick="retryFailed()" title="Retry failed quiz questions (R)">Retry</button>
        <span id="pct">0%</span>
      </div>
    </div>
    <div id="slide"></div>
    <div id="nav">
      <button class="prev" onclick="go(-1)">Prev</button>
      <button class="next" onclick="go(1)">Next</button>
    </div>
  </div>
  <div id="toc-overlay" onclick="toggleTOC(false)"></div>
  <div id="toc">
    <h2>Table of Contents</h2>
    <div id="toc-body"></div>
  </div>

  <script>
    const QUIZ_DATA = __QUIZ_JSON__;
    const SLIDES = __SLIDES_JSON__;
    const MODULE_NAMES = __MODULE_NAMES_JSON__;
    const STORE_KEY = '__STORE_KEY__';

    let cur = 0;
    let quizState = {};
    let failedQs = [];
"""

HTML_TEMPLATE += """
    function save() {
      const data = { cur, quizState, failedQs, ts: Date.now() };
      try { localStorage.setItem(STORE_KEY, JSON.stringify(data)); } catch (e) {}
      try { document.cookie = STORE_KEY + '=' + cur + ';max-age=31536000;path=/'; } catch (e) {}
    }

    function load() {
      try {
        const data = JSON.parse(localStorage.getItem(STORE_KEY));
        if (data) {
          cur = data.cur || 0;
          quizState = data.quizState || {};
          failedQs = data.failedQs || [];
        }
      } catch (e) {}
    }

    function esc(value) {
      return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    }

    function hashSeed(seed) {
      let h = 2166136261;
      for (let i = 0; i < seed.length; i += 1) {
        h ^= seed.charCodeAt(i);
        h = Math.imul(h, 16777619);
      }
      return h >>> 0;
    }

    function shuffleOpts(opts, seed) {
      const items = opts.map((text, index) => ({ text, correct: index === 0 }));
      let state = hashSeed(seed) || 1;
      for (let i = items.length - 1; i > 0; i -= 1) {
        state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
        const j = state % (i + 1);
        const tmp = items[i];
        items[i] = items[j];
        items[j] = tmp;
      }
      return items;
    }

    function getModule(moduleId) {
      return QUIZ_DATA.modules.find((module) => module.id === moduleId);
    }

    function ensureQuizState(moduleId) {
      const module = getModule(moduleId);
      if (!quizState[moduleId]) {
        quizState[moduleId] = { answers: {}, score: 0, total: module.questions.length, done: false };
      }
      return quizState[moduleId];
    }

    function renderQuiz(moduleId) {
      const module = getModule(moduleId);
      const state = ensureQuizState(moduleId);
      state.total = module.questions.length;
      state.score = Object.values(state.answers).filter((answer) => answer.correct).length;

      const nextQuestion = module.questions.find((question) => !state.answers[question.id]);
      if (!nextQuestion) {
        state.done = true;
        const pct = Math.round((state.score / state.total) * 100);
        return `
          <div class="quiz-container">
            <h1>${esc(module.name)} Quiz</h1>
            <p class="quiz-meta">You completed ${state.total} questions for this module.</p>
            <div class="${pct >= 70 ? 'quiz-feedback pass show' : 'quiz-feedback fail show'}">
              Score: ${state.score} / ${state.total} (${pct}%).
              Use Retry to revisit questions answered incorrectly.
            </div>
          </div>
        `;
      }

      const questionIndex = module.questions.findIndex((question) => question.id === nextQuestion.id);
      const options = shuffleOpts(nextQuestion.options, nextQuestion.id);

      return `
        <div class="quiz-container">
          <h1>${esc(module.name)} Quiz</h1>
          <p class="quiz-meta">Question ${questionIndex + 1} of ${module.questions.length}</p>
          <h2>${esc(nextQuestion.question)}</h2>
          ${options.map((option, index) => `
            <button class="quiz-opt" id="opt-${index}" onclick="answerQuiz(${moduleId}, '${nextQuestion.id}', ${index})">${esc(option.text)}</button>
          `).join('')}
          <div class="quiz-feedback" id="quiz-feedback"></div>
        </div>
      `;
    }

    function answerQuiz(moduleId, questionId, chosenIndex) {
      const module = getModule(moduleId);
      const state = ensureQuizState(moduleId);
      if (state.answers[questionId]) {
        return;
      }

      const question = module.questions.find((item) => item.id === questionId);
      const options = shuffleOpts(question.options, question.id);
      const chosen = options[chosenIndex];
      const isCorrect = !!chosen.correct;

      state.answers[questionId] = { chosen: chosen.text, correct: isCorrect };
      state.score = Object.values(state.answers).filter((answer) => answer.correct).length;

      if (!isCorrect && !failedQs.some((item) => item.moduleId === moduleId && item.qId === questionId)) {
        failedQs.push({ moduleId, qId: questionId });
      }
      if (Object.keys(state.answers).length === module.questions.length) {
        state.done = true;
      }

      options.forEach((option, index) => {
        const button = document.getElementById(`opt-${index}`);
        if (!button) return;
        button.classList.add('disabled');
        if (option.correct) {
          button.classList.add('correct');
        } else if (index === chosenIndex) {
          button.classList.add('wrong');
        }
      });

      const feedback = document.getElementById('quiz-feedback');
      if (feedback) {
        feedback.className = `quiz-feedback show ${isCorrect ? 'pass' : 'fail'}`;
        feedback.innerHTML = `<strong>${isCorrect ? 'Correct.' : 'Not quite.'}</strong> ${esc(question.explanation)}`;
      }

      save();
      setTimeout(render, isCorrect ? 1200 : 3000);
    }

    function retryFailed() {
      if (!failedQs.length) {
        alert('No failed quiz questions are currently tracked.');
        return;
      }

      const retryItems = failedQs.slice();
      retryItems.forEach((item) => {
        const state = ensureQuizState(item.moduleId);
        delete state.answers[item.qId];
        state.score = Object.values(state.answers).filter((answer) => answer.correct).length;
        state.done = false;
      });

      const first = retryItems[0];
      failedQs = [];
      cur = SLIDES.findIndex((slide) => slide.q && slide.m === first.moduleId);
      render();
    }
"""

HTML_TEMPLATE += """
    function go(dir) {
      cur = Math.max(0, Math.min(SLIDES.length - 1, cur + dir));
      render();
    }

    function jump(index) {
      cur = index;
      render();
      toggleTOC(false);
    }

    function toggleTOC(force) {
      const toc = document.getElementById('toc');
      const overlay = document.getElementById('toc-overlay');
      const shouldOpen = typeof force === 'boolean' ? force : !toc.classList.contains('open');
      toc.classList.toggle('open', shouldOpen);
      overlay.classList.toggle('open', shouldOpen);
    }

    function buildTOC() {
      const tocBody = document.getElementById('toc-body');
      const html = MODULE_NAMES.map((moduleName, moduleIndex) => {
        const links = SLIDES.map((slide, slideIndex) => ({ slide, slideIndex }))
          .filter((entry) => entry.slide.m === moduleIndex)
          .map((entry) => `
            <button class="toc-link ${entry.slideIndex === cur ? 'current' : ''}" onclick="jump(${entry.slideIndex})">
              ${entry.slide.q ? 'Quiz' : esc(entry.slide.t)}
            </button>
          `)
          .join('');
        return `<div class="toc-module"><h3>${esc(moduleName)}</h3>${links}</div>`;
      }).join('');
      tocBody.innerHTML = html;
    }

    function render() {
      const slide = SLIDES[cur];
      const progress = Math.round(((cur + 1) / SLIDES.length) * 100);
      document.getElementById('progress-bar').style.width = progress + '%';
      document.getElementById('pct').textContent = progress + '%';
      document.getElementById('slide-counter').textContent = `${cur + 1} / ${SLIDES.length}`;
      document.getElementById('module-label').textContent = MODULE_NAMES[slide.m];
      document.getElementById('slide').innerHTML = slide.q ? renderQuiz(slide.m) : `<h1>${esc(slide.t)}</h1>${slide.c}`;
      save();
      buildTOC();
    }

    document.addEventListener('keydown', (event) => {
      const tag = (event.target && event.target.tagName) || '';
      if (tag === 'INPUT' || tag === 'TEXTAREA') {
        return;
      }
      if (event.key === ' ' && !event.shiftKey) {
        event.preventDefault();
        go(1);
      } else if ((event.key === ' ' && event.shiftKey) || event.key === 'ArrowLeft') {
        event.preventDefault();
        go(-1);
      } else if (event.key === 'ArrowRight') {
        event.preventDefault();
        go(1);
      } else if (event.key === 'Home') {
        event.preventDefault();
        cur = 0;
        render();
      } else if (event.key === 'End') {
        event.preventDefault();
        cur = SLIDES.length - 1;
        render();
      } else if (event.key === 't' || event.key === 'T') {
        event.preventDefault();
        toggleTOC();
      } else if (event.key === 'r' || event.key === 'R') {
        event.preventDefault();
        retryFailed();
      }
    });

    load();
    render();
  </script>
</body>
</html>
"""


def build_html(slides: list[dict[str, object]], quiz_data: dict[str, object]) -> str:
    return (
        HTML_TEMPLATE.replace("__TITLE__", WORKSHOP_TITLE)
        .replace("__QUIZ_JSON__", json.dumps(quiz_data, ensure_ascii=False))
        .replace("__SLIDES_JSON__", json.dumps(slides, ensure_ascii=False))
        .replace("__MODULE_NAMES_JSON__", json.dumps([module["name"] for module in MODULES], ensure_ascii=False))
        .replace("__STORE_KEY__", f"{TOPIC_SLUG}_workshop")
    )


def main() -> None:
    output_dir = Path("output") / "workshop"
    output_dir.mkdir(parents=True, exist_ok=True)

    slides = build_slides()
    quiz_data = build_quiz_data()

    html_output = output_dir / f"{TOPIC_SLUG}_workshop.html"
    quiz_output = output_dir / f"{TOPIC_SLUG}_quiz.json"

    html_output.write_text(build_html(slides, quiz_data), encoding="utf-8")
    quiz_output.write_text(json.dumps(quiz_data, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
