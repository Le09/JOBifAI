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
    $ result = retry("random_prompt_0", ask_llm, {"prompt": prompt, "schema":schema, "api_key": a})

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

    scene bg desk
    show secretary
    with dissolve

    "Looks like it's the secretary. Should I say something?"

label lobby_first:
    jump talk_secretary
