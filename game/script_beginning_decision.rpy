﻿label before_going:
    hide henk
    with dissolve

    stop music fadeout 1.0

    play music "eyeswideopen-walking.mp3"
    m "Reading the job posting, checking my own application, looking up the itinerary on the map..."
    m "So many things to do and so little time. Which one should I do before I go?"

    $ reply = renpy.input(["","Describe what you do."], screen="viewport_llm")
    play sound "validate.mp3"
    $ reply = reply.strip() or "Browse on 4chan for the latest memes."
    $ mm.add_history(kind="adv", who=narrator.name, what=reply)
    $ prompt = """
Context: the unnamed main character is preparing to leave for a job interview with only a limited time.
Here are the possible actions:
1) read the job posting
2) check their own application
3) look up the itinerary on the map
4) multiple things
5) something else
Here is a description of what the character did:

%s

Here is the series idea: %s

Here is the portfolio idea: %s

Instructions:
- Always check first if the character attempts to do more than one thing (e.g., both reading the series and checking the portfolio). In such cases, the result must always be 4. If the character tries to read both the job posting and the portfolio, the result must be 4.
- If the character performs only one action, match that action accordingly (1, 2, 3, 5).
- If the choice is 1, describe reading the series idea in the job posting.
- If the choice is 2, describe checking the portfolio.
- If the choice is 4 or 5, describe the character getting distracted by a browser tab, wasting time.

Evaluate what the answer may be among the previous options as a choice c.
Moreover, narrate what happens at the second person as a result of this action using the second-person point of view as a sentence s.
Describe only the direct result of the action.

Give your answer as a json of the form {"choice": c, "result": s}.
    """ % (reply, series_idea, portfolio_idea)
    $ result = askllm("before_going", prompt, {"choice": "integer:1<=i<=5", "result": "string"})
    $ choice = result["choice"]
    $ result = result["result"]
    $ jump_state = ["street", "street", "street_map", "street_lost", "street_lost"][choice - 1]
    $ renpy.say(narrator, result, what_style="say_transcript")

    $ renpy.jump(jump_state)
    with fade

label street_lost:
    scene bg street
    "Hope they won't ask any hard questions, I didn't have time to check out my CV and portfolio... The road was longer than I expected. How many buildings are even here?"

label random:
    stop music fadeout 1.0
    play music "randoman.mp3"
    "I see a man with a barely hanging fake moustache.
    Oh no, there he comes...
    I don't want to be late for my interview."

    show randle
    # with dissolve  # with voice, it's better without

    r "Let me introduce myself, my name is Ran Doman.
    I see you are walking towards Grizley building.
    I am conducting a small survey for my... ahem... PhD.
    Have you noticed any disappearances, suspicious lay-offs lately?"

    m "Random Man? PhD? You?"

    r "A secret agent! That's who I am!"

    m "I'm in a hurry, goodbye."

    r "Noooo, danger zone!"

    hide randle
    with dissolve

    "As you run towards the building, you wonder about this man.
    Did he work for Grizley before? Did something happen to him there?"

    stop music fadeout 1.0
    $ achievement_rambling.grant()

    jump at_the_door

label street_map:
    scene bg street
    "It was a good idea to check the itinerary. I'm a bit early and feel refreshed."
    jump at_the_door

label street:
    scene bg street
    "Hope they won't ask any hard questions, I didn't have the time to go over all documents... And the road was longer than I expected. I feel sweaty walking so much."
    jump at_the_door