# Part 3: talking with Grizley secretary.
label talk_secretary:
    scene bg desk
    show secretary at truecenter

    # TODO prompt does not work

    # python:
        # reply = renpy.input("Is there any way I can help?")
        # reply = reply.strip()
    $ reply = renpy.input(["Secretary","Is there any way I can help?"], screen="viewport_llm")
    # hack that doesn't look nice in the history.
    # "Me: [reply]"

    $ narrator.add_history(kind="adv", who=narrator.name, what=reply)

    while count_ask_interview < 3:
        $ count_ask_interview+= 1
        $ prompt = """
        Context: the main character is in front of the secretary, a woman, of Grizley, an entertainment company.
        There is a central desk, some office doors, a lift, and the doors to the street.
        Here are the possible actions:
        1) say nothing or a confusing blurb
        2) explicitly mention being there for a job interview (at 10 am), with the art director.
        3) leave the building
        4) act in a very suspicious or rude manner
        5) something else

        Here is a description of what the character did:

        %s

        Evaluate what the answer may be among the previous options as a choice c.
        Be strict on the following:
        - If the character is polite but doesn't mention the interview, then the result should be 5.
        - If the character takes no action, then the result should be 5.
        - If the character says "", nothing, then the result should be 5.
        - If the character is annoying, confusing, too shy, then the result should be 5.
        - It should only be 2 when the character says something about the interview.
        Moreover, describe what happens as a result of this action as a sentence s.
        Describe only the direct result of the action.
        Give your answer as a json of the form {"choice": c, "result": s}.
        """ % reply

        $ schema = {"choice":  "integer:1<=i<=5", "result":  "string"}

        #python:
        $ a = persistent.groq_api_key
        $ answer = askllm("talk_secretary", prompt, schema)
        $ choice = answer["choice"]
        $ result = answer["result"]
        $ jump_state = ["secretary_nervous", "ready_interview", "bad_ending", "security", "secretary_nervous"][choice - 1]

        # describe result  # maybe not depending on the transition?
        $ renpy.say(narrator, result)
        $ renpy.jump(jump_state)

        # show screen say_scroll("", result)
        # pause
        # hide screen say_scroll

    jump secretary_angry_boss

label secretary_nervous:

    "It's a stressful situation... Maybe next time tell her about the interview."

    jump talk_secretary

label ready_interview:
    s "The art director's office is this way."

    jump boss_happy
