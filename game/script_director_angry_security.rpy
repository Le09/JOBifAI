# Part 4: angry boss and security

label security:
    hide secretary
    with dissolve

    "Oh no... The nice lady is gone."
    show guard
    "Someone who looks less nice appears."

    g "You're being disruptive. Please exit."

    jump worst_ending

label angry_boss:

    "Oh no... Someone who looks angry appears."

    show ad angry at truecenter

    b "What are you doing? Don't you know there are people working hard here."

    hide secretary
    with dissolve

label angry_boss_explain:
    python:
        reply = renpy.input("Explain yourself to the angry man.")
        reply = reply.strip()

    while count_angry_boss < 3:
        $ count_angry_boss+= 1
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
        Be strict on the fact that for option 1), the answer must take decisive action to get this result; if the main character does not, the result should be 5.
        If the character takes no action, then the result should be 5).
        If the character says "", nothing, then the result should be 5).
        Moreover, describe what happens as a result of this action as a sentence s.
        Describe only the direct result of the action.
        Give your answer as a json of the form {"choice": c, "result": s}.
        """ % reply

        $ schema = {"choice":  "integer:1<=i<=5", "result":  "string"}

        #python:
        $ a = persistent.groq_api_key
        $ answer = retry("lobby_first", ask_llm, {"prompt": prompt, "schema":schema, "api_key": a})
        $ choice = answer["choice"]
        $ result = answer["result"]
        $ jump_state = ["boss_nervous", "boss_angry_interview", "bad_ending", "security", "boss_nervous"][choice - 1]

        # describe result  # maybe not depending on the transition?
        $ renpy.say(narrator, result)
        $ renpy.jump(jump_state)

    jump security

    # first question
    # confidence between 0 and 1
    # <.33 : suspicious -> security, or maybe 1 warning if > .25 then security
    # < .66: nothing
    # > exhalted, almost weird

    # 4 turns (questions?) to accept candidate
    # very bad: blackliste
    # ok: we may call you

label boss_nervous:
    "It's a stressful situation... Maybe next time tell him about the interview."

    jump angry_boss_explain
