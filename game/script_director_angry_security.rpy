# Part 4: angry boss and security

label security:
    hide secretary
    with dissolve

    "Oh no..."
    show guard
    "Someone who doesn't look happy appears."

    g "You're being disruptive. Please exit."

    jump worst_ending

label secretary_angry_boss:

    "Oh no... Someone who looks angry appears."

    show ad angry at truecenter

    b "What are you doing? Don't you know there are people working hard here."

    hide secretary
    with dissolve

label secretary_angry_boss_explain:
    while count_secretary_angry_boss < 3:
        $ count_secretary_angry_boss+= 1

        $ reply = renpy.input(["","Explain yourself to the angry man."], screen="viewport_llm")
        $ reply = reply.strip() or "stammer for way too long"
        $ mm.add_history(kind="adv", who=narrator.name, what=reply)

        $ prompt = """
        Context: the main character is at the lobby of Grizley, an entertainment company.
        There is a central desk, some office doors, a lift, and the doors to the street.
        The character is here for a job interview at 10 am, with the art director.
        The character was with the secretary, a woman, but couldn't find a proper way to mention the interview.
        After some time, the art director, a man who saw the previous interaction, arrives, visibly angry.
        Here are the possible actions:
        1) say nothing or a confusing blurb
        2) mention the interview at 10 am
        3) leave the building
        4) act in a very suspicious or rude manner
        5) something else

        Here is a description of what the character did:

        %s

        Evaluate what the answer may be among the previous options as a choice c.
        Be strict on the fact that for option 2), the answer must take decisive action to get this result; if the main character does not, the result should be 5.
        If the character takes no action, then the result should be 5).
        If the character says "", nothing, then the result should be 5).
        Moreover, describe what happens as a result of this action as a sentence s.
        Describe only the direct result of the action.
        Give your answer as a json of the form {"choice": c, "result": s}.
        """ % reply

        $ schema = {"choice":  "integer:1<=i<=5", "result":  "string"}

        $ answer = askllm("secretary_angry_boss_explain", prompt, schema)
        $ choice = answer["choice"]
        $ result = answer["result"]
        $ jump_state = ["secretary_boss_nervous", "boss_angry", "bad_ending", "security", "secretary_boss_nervous"][choice - 1]

        $ renpy.say(narrator, result, what_style="say_transcript")
        $ renpy.jump(jump_state)

    jump security

label secretary_boss_nervous:
    "It's a stressful situation... Say what seems the best for you."

    jump secretary_angry_boss_explain
