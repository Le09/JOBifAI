# The game begins here.
label start:

    if persistent.game_first_time:
        call screen config_menu
        $ persistent.game_first_time = False

    scene bg room
    with fade


    m "Gin...ious... I'm a gin...ious..."
    show henk
    with dissolve
    h "Ahem... If you're so... rhum...markeable... Hohoho... Why aren't you working for Grizley?"
    m "Grizley... When I apply, I'll be there in no time. Watch me!"
    h "Watching... With my Eyes... Wide...  OZzzzZZZzzzzz"
    hide henk
    with dissolve
    m "Henk, you never handled alcohol too well."

    scene bg cyber

    m "JOBifAI, how do I become concept designer for Grizley?"

    show j intro
    with dissolve

    j "Complete these 4 steps to become concept designer for Grizley:"
    j "Step 1: Send this CV I made for you. It says you have a degree in Industrial Design from RISD."


    j "Add the link of your SinkedIN page I just made. I connected you to some notable concept designers."
    m "What is RISD? And who are these SinkedIN \'friends\' you connected me to? Their faces are weird."
    j "Step 2: Attach this portfolio I am generating for you, with the following description:"

    show j cv

    j "I grew up in Videville, a small town known for its vertical lake..."
    j "At 10, while helping my grandfather build the town's cycle superhighway, a cyclist stopped by." 
    j "It was no other than Syd Meat. Listening to his encouraging words, my vocation became clear."
    m "You know what, if I don't apply, I have a 100\% chance of being rejected. So I'll apply."
    j " Step 3: Read this 587 page document detailing the work environment at Grizley."
    j "With these three steps, you're guaranteed to get hired!"
    j "Remember, this version of JOBifAI is experimental. It is not advised to use it in a real-life setting."
    m "Awesome. Now I just need to submit the CV and portfolio, and hope for the best. Let's wait a bit..."


label init_series:
    $ renpy.checkpoint(hard=False)
    $ prompt = """
    Generate a prompt p for Stable Diffusion.
    That prompt should describe a main illustration for a new interesting anime series targeting a teen audience created by a big entertainment company.
    Give a short description of that prompt s that a marketing department might use.
    Give your answer in a json of the form {'prompt': p, 'sentence': s}.
    """
    $ schema = {"prompt":  "string", "sentence": "string"}
    $ a = persistent.groq_api_key
    $ result = retry("start", ask_llm, {"prompt": prompt, "schema":schema, "api_key": a})

label init_series_job:
    $ renpy.checkpoint(hard=False)
    python:
        series_idea = result["sentence"]
        series_prompt = result["prompt"]
        if not series_cover_job:
            series_cover = get_random_object_name("portfolio/series.png")
            series_cover_job = retry("init_series_job", generate_job, {"prompt": series_prompt, "api_key": persistent.prodia_api_key})

label wake_up:
    scene bg room

    m "Henk! Wake up!!! I got an interview with Grizley!"
    show henk
    with dissolve
    h "Wait... Wwwhat?"
    m "Don't tell me... You forgot our conversation last night?"
    h "I'm afraid I only remember not having a headache, whereas now..."
    m "I got an interview! Tomorrow 10am, I'm meeting the CEO of Grizley!"
    h "Tomorrow! Too late to Escape! I'll be rooting for you!"

label street:
    scene bg street
    "Hope they won't ask any hard questions, I didn't have time to check out my CV and portfolio... The road is longer than I expected."

label finish_series_job:
    $ renpy.checkpoint(hard=False)
    python:
        if not exists_img(series_cover):
            series_cover = get_random_object_name("portfolio/series.png")
            retry("finish_series_job", download_job_image, {"job_id": series_cover_job, "file_path": img_full_path(series_cover), "api_key": persistent.prodia_api_key})

label company_lobby:

    scene bg lobby

    "Am I late? No one's there."
    # "Galactic walls, ice-cream statues, pink electric barbed wires, just what I'd expect from the job of my dreams."
    "I see someone coming, very slowly though... Guess I'll just wait."


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
        #   portfolio_0 = get_random_object_name("portfolio/img_0.png")
            portfolio_0_job = retry("before_portfolio_0", generate_job, {"prompt": portfolio_prompt, "api_key": persistent.prodia_api_key})

label finish_portfolio_0:
    $ renpy.checkpoint(hard=False)
    python:
        if not exists_img(portfolio_0):
            retry("finish_portfolio_0", download_job_image, {"job_id": portfolio_0_job, "file_path": img_full_path(portfolio_0), "api_key": persistent.prodia_api_key})
    
label dont_reload_image_here:
    $ renpy.checkpoint(hard=False)

    show secretary
    with dissolve

    "Looks like it's the secretary approaching. Should I say something?"
    # $ im_portfolio_0 = im.Image(portfolio_0)
    # show expression im_portfolio_0

    $ count = 0

label lobby_first:

    # reply = INPUT

    while count < 3 :
        $ count +=1

        python:
            reply = renpy.input("Describe what you do in front of the secretary.")
            reply = reply.strip()

        $ prompt = """
        Context: the main character is in the lobby of Grizley, an entertainment company.
        There is a central desk with a secretary, some office doors, a lift, and the doors to the street.
        Here are the possible actions:
        1) ask the secretary for instructions
        2) inspect the building
        3) leave the building
        4) act in a very suspicious or rude manner
        5) something else

        Here is a description of what the character did:

        %s

        Evaluate what the answer may be among the previous options as a choice c.
        Be strict on the fact that for option 1), the answer must take decisive action to get this result; if the main character does not, the result should be 5.
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
        $ jump_state = ["talk_secretary", "look_building", "bad_ending", "security", "look_building"][choice - 1]

        # describe result  # maybe not depending on the transition?
        $ renpy.say(narrator, result)
        $ renpy.jump(jump_state)

    jump angry_boss

label look_building:

    "What beautiful architecture."
    "Next time I'll definitely ask for help."
    jump lobby_first

label talk_secretary:
    show secretary at truecenter

    # s "Hi there! Welcome to Grizley, my name is Glora."

    python:
        answer = renpy.input("Is there any way I can help?")
        answer = answer.strip()

        if not answer:
            answer = "Errr..."

    # options: rude/suspicious (security)
    s "Sure! I'll take you to the art director's office."

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

label boss:

    scene bg office
    with dissolve

    show ad at truecenter
    "What a cool office."

    python:
        answer = renpy.input("So, what brings you here?")
        answer = answer.strip()

        if not answer:
            answer = "Errr..."

    # jump angry_boss
    # jump happy_boss

    b "I see. Come with me."

    jump ending

label interview:
    # $ im_portfolio_0 = im.Image(portfolio_0)
    # show expression im_portfolio_0