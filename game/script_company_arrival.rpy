# Part 2: arriving at company Grizley.
label street:
    scene bg street
    "Hope they won't ask any hard questions, I didn't have time to check out my CV and portfolio... The road is longer than I expected."

label finish_series_job:
    $ renpy.checkpoint(hard=False)
    python:
        if not exists_img(series_cover):
            retry("finish_series_job", download_image, {"job_id": series_cover_job, "file_path": img_full_path(series_cover), "api_key": persistent.prodia_api_key})

label company_lobby:

    scene bg lobby

    "Am I late? No one's there."
    # "Galactic walls, ice-cream statues, pink electric barbed wires, just what I'd expect from the job of my dreams."
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
            portfolio_0_job = retry("before_portfolio_0", generate_job, {"prompt": portfolio_prompt, "api_key": persistent.prodia_api_key})

label finish_portfolio_0:
    $ renpy.checkpoint(hard=False)
    python:
        if not exists_img(portfolio_0):
            retry("finish_portfolio_0", download_image, {"job_id": portfolio_0_job, "file_path": img_full_path(portfolio_0), "api_key": persistent.prodia_api_key})
    
label dont_reload_image_here:
    $ renpy.checkpoint(hard=False)

label lobby_first:

    while count_first_move < 3 :
        $ count_first_move +=1

        $ reply = renpy.input(["","Describe what you do."], screen="viewport_llm")
        # hack that doesn't look nice in the history.
        "Me: [reply]"

        $ prompt = """
        Context: the main character is in the lobby of Grizley, an entertainment company.
        There is a central desk with a secretary, some office doors, a lift, and the doors to the street.
        Here are the possible actions:
        1) inspect the building
        2) go towards the secretary
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

        #python:
        $ a = persistent.groq_api_key
        $ answer = askllm("lobby_first", prompt, schema)
        $ choice = answer["choice"]
        $ result = answer["result"]
        $ jump_state = ["look_building", "talk_secretary", "bad_ending", "security", "look_building"][choice - 1]

        # describe result  # maybe not depending on the transition?
        $ renpy.say(narrator, result)
        $ renpy.jump(jump_state)

    jump secretary_angry_boss

label look_building:
    "What beautiful architecture."
    "Next time I'll definitely do something."
    jump lobby_first