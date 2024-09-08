# Part 3: talking with Grizley secretary.
label talk_secretary:
    show secretary at truecenter

    # s "Hi there! Welcome to Grizley, my name is Glora."
    python:
        reply = renpy.input("Is there any way I can help?")
        reply = reply.strip()

    while count_ask_interview < 3:
        $ count_ask_interview+= 1
        $ prompt = """
        Context: the main character is in front of the secretary, a woman, of Grizley, an entertainment company.
        The character is here for a job interview at 10 am, with the art director.
        There is a central desk, some office doors, a lift, and the doors to the street.
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
        $ jump_state = ["look_building", "ready_interview", "bad_ending", "security", "look_building"][choice - 1]

        # describe result  # maybe not depending on the transition?
        $ renpy.say(narrator, result)
        $ renpy.jump(jump_state)

    jump angry_boss


    # python:
    #     answer = renpy.input("Is there any way I can help?")
    #     answer = answer.strip()

    #     if not answer:
    #         answer = "Errr..."

    # options: rude/suspicious (security)

label ready_interview:
    s "The art director's office is this way."

    jump boss

label security:
    hide s green normal
    with dissolve

    "Oh no... The nice lady is gone."
    "Someone who looks less nice appears."

    show guard
    g "You're being disruptive. Please exit"

    jump bad_ending

label angry_boss:

    "Oh no... Someone who looks angry appears."

    show ad angry at truecenter

    b "What is it?"

    python:
        answer = renpy.input("Why are you staring at my hard working secretary?")
        answer = answer.strip()

        if not answer:
            answer = "Errr..."

    hide secretary
    with dissolve

    # first question
    # confidence between 0 and 1
    # <.33 : suspicious -> security, or maybe 1 warning if > .25 then security
    # < .66: nothing
    # > exhalted, almost weird

    # 4 turns (questions?) to accept candidate
    # very bad: blackliste
    # ok: we may call you


    b "I see. Come with me."

    jump ending