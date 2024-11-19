# Part 2: arriving at company Grizley.
label at_the_door:
    scene bg street
    play music "meow-bassline.mp3"
    "This is it. These big glass doors, the cute bear logo... I'm at the door of Grizley."

label finish_series_job:
    $ renpy.checkpoint(hard=False)
    python:
        if not exists_img(series_cover):
            download_image(series_prompt, img_full_path(series_cover))

label company_lobby:

    # stop music fadeout 1.0
    scene bg lobby

    "Am I late? No one's there."
    "I see someone at the desk. Maybe I should check. I'll take my time though."

    play music "meow-lobby.mp3" loop

label finish_portfolio_0:
    $ renpy.checkpoint(hard=False)
    python:
        if not exists_img(portfolio_0):
            download_image(portfolio_prompt, img_full_path(portfolio_0))

label dont_reload_image_here:
    $ renpy.checkpoint(hard=False)

label lobby_first:

    while count_first_move < 3 :
        $ count_first_move +=1
        $ couch = "comfy" if earring_got else "disorderly"
        $ couch_choice = "6) inspect couch" if not earring_got else ""

        $ reply = renpy.input(["","Describe what you do."], screen="viewport_llm")
        play sound "validate.mp3"
        $ reply = reply.strip() or "look around somewhat nervously"
        $ mm.add_history(kind="adv", who=narrator.name, what=reply)


        $ prompt = """
        Context: the main character is in the lobby of Grizley, an entertainment company.
        There is a central desk with a secretary, some office doors, a lift, and the doors to the street.
        There are also some plants and a %s couch.
        Here are the possible actions:
        1) inspect the building
        2) go towards the secretary
        3) leave the building
        4) act in a very suspicious or rude manner
        5) something else
        %s

        Here is a description of what the character did:

        %s

        Evaluate what the answer may be among the previous options as a choice c.
        Be strict on the fact that for option 2), the answer must take decisive action to get this result; if the main character does not, the result should be 5.
        If the character takes no action, then the result should be 5).
        If the character says "", nothing, then the result should be 5).
        Moreover, describe what happens as a result of this action as a sentence s.
        Describe only the direct result of the action.
        Give your answer as a json of the form {"choice": c, "result": s}.
        """ % (couch, couch_choice, reply)

        $ schema = {"choice":  "integer:1<=i<=5" if earring_got else "integer:1<=i<=6", "result":  "string"}

        #python:
        $ answer = askllm("lobby_first", prompt, schema)
        $ choice = answer["choice"]
        $ result = answer["result"]
        $ jump_state = ["look_building", "talk_secretary", "bad_ending", "security", "look_building", "earring_got"][choice - 1]

        # describe result  # maybe not depending on the transition?
        $ renpy.say(narrator, result, what_style="say_transcript")
        $ renpy.jump(jump_state)

    jump secretary_angry_boss

label look_building:
    "What beautiful architecture."
    "Next time I'll definitely do something."
    jump lobby_first

label earring_got:
    $ earring_got = True
    "The cushions are a mess. Reminds me of home."
    "What's this, a feather? Oh, it's an earring. I'll keep it."
    play sound "good.mp3"
    $ achievement_earring_found.grant()
    "Ok, I feel ready know. I should move on."
    jump lobby_first