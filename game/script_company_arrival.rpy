# Part 2: arriving at company Grizley.
label street:
    scene bg street
    "Hope they won't ask any hard questions, I didn't have time to check out my CV and portfolio... The road is longer than I expected."

label finish_series_job:
    $ renpy.checkpoint(hard=False)
    python:
        if not exists_img(series_cover):
            retry("finish_series_job", download_image, {"job_id": series_cover_job, "file_path": img_full_path(series_cover)})

label company_lobby:

    scene bg lobby

    "Am I late? No one's there."
    "I see someone at the desk. Maybe I should check. I'll take my time though."


label random_prompt_0:
    $ renpy.checkpoint(hard=False)
    $ prompt = """
    Generate a random prompt p for Stable Diffusion.
    Its subject should be appealing to people, yet mash different ideas in 
    a very unexpected way.
    Give a short human-readable description of that prompt s.
    Give your answer in a json of the form {'prompt': p, 'sentence': s}.
    """
    $ schema = {"prompt":  "string", "sentence": "string"}
    $ a = persistent.groq_api_key
    $ result = askllm("random_prompt_0", prompt, schema)

label before_portfolio_0:
    $ renpy.checkpoint(hard=False)
    python:
        portfolio_idea = result["sentence"]
        portfolio_prompt = result["prompt"]
        if not portfolio_0:
            portfolio_0 = get_random_object_name("p0.png", [dir_session])
            portfolio_0_job = generate_image("before_portfolio_0", portfolio_prompt)

label finish_portfolio_0:
    $ renpy.checkpoint(hard=False)
    python:
        if not exists_img(portfolio_0):
            retry("finish_portfolio_0", download_image, {"job_id": portfolio_0_job, "file_path": img_full_path(portfolio_0)})
    
label dont_reload_image_here:
    $ renpy.checkpoint(hard=False)

label lobby_first:

    while count_first_move < 3 :
        $ count_first_move +=1
        $ couch = "comfy" if earring_got else "disorderly"
        $ couch_choice = "6) inspect couch" if not earring_got else ""

        $ reply = renpy.input(["","Describe what you do."], screen="viewport_llm")
        # hack that doesn't look nice in the history.
        # Don't display reply again but add it to history.
        $ narrator.add_history(kind="adv", who=narrator.name, what=reply)

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
        $ renpy.say(narrator, result)
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
    "Ok, I feel ready know. I should move on."
    jump lobby_first