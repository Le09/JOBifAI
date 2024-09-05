# Company wants to hire concept designer.
# Drunk, you sent SO generated images in a portfolio.
# The AD did not catch up on this as they have strict non AI poligcy.
# IDEA: you need to BS your way through portfolio & serie concepts are random

# Declare characters used by this game.
define s = Character(_("Secretary"), color="#c8ffc8")
define m = Character(_("Me"), color="#c8c8ff")
define b = Character(_("Boss"), color="#ffc8ff")
define g = Character(_("Guard"), color="#ffffaa")
define f = Character(_("Friend"), color="#c8c8")
define j = Character(_("JOBifAI"), color="#ccc8c8")

default persistent.game_first_time = True
default persistent.config = {"groq_api_key": persistent.groq_api_key}

default portfolio_idea = None
default portfolio_prompt = None
default portfolio_0 = None
default portfolio_0_job = None

default series_idea = None
default series_prompt = None
default series_cover = None
default series_cover_job = None

default prompt = None
default schema = None
default result = None
default im_portfolio_0 = None
default answer = None
default choice = None
default jump_state = None

init python:
    # create venv called llenaige in 3.9, in game folder
    import os
    import sys
    import uuid
    path_venv = "~/.virtualenvs/llenaige/lib/python3.9/site-packages/"
    sys.path.append(os.path.expanduser(path_venv))
    from chatgpt_n.llm import ask_llm
    from chatgpt_n.images import download_job_image, generate_job
    # config = {"groq_api_key": settings_api_key}
    def retry(fallback, function, kwargs):
        try:
            return function(**kwargs)
        except Exception as e:
            # TODO: more robust error handling
            if "body" in dir(e) and "error" in e.body:
                se = "Error: %s\n" % e.body["error"]["message"]
                se += "Justification: %s\n" % e.body["error"]["failed_generation"]
            else:
                se = e.message if "message" in dir(e) else str(e)
            s = "%s\n\n The operation failed. Do you want to retry?" % se
            again = renpy.confirm(s)
            if again:
                return retry(fallback, function, kwargs)
            else:
                renpy.jump(fallback)

    def exists_img(image_name):
        return renpy.exists(os.path.join("images", image_name))

    def get_random_object_name(base_name):
        name, ext = os.path.splitext(base_name)
        new_name = name + str(uuid.uuid4()).replace("-", "_")
        return new_name + ext  # ext would be "" or ".ext"

    def img_full_path(name):
        dir_base = renpy.config.basedir
        dir_images = os.path.join(dir_base, "game", "images")
        if ".png" not in name:
            name += ".png"
        file_path = os.path.join(dir_images, name)
        return file_path


# The game starts here.
label start:

    # play music "illurock.opus"

    if persistent.game_first_time:
        call screen config_menu
        # $ game_first_time = False

    scene bg bedroom
    with fade


    m "Gin...ious... I'm a gin...ious..."
    show f green normal
    with dissolve
    f "Ahem... If you're so... rhum...markeable... Hohoho... Why aren't you working for Grizley?"
    m "Grizley... When I apply, I'll be there in no time. Watch me!"
    f "Watching... With my Eyes... Wide...  OZzzzZZZzzzzz"
    hide f green normal
    with dissolve
    m "Finn, you never handled alcohol too well."

    show j black normal
    with fade
    m "JOBifAI, how do I become concept designer for Grizley?"
    j "Complete these 4 steps to become concept designer for Grizley:"
    j "Step 1: Send this CV I made for you. It says you have a degree in Industrial Design from RISD."
    j "Add the link of your SinkedIN page I just made. I connected you to some notable concept designers."
    m "What is RISD? And who are these SinkedIN \'friends\' you connected me to? Their faces are weird."
    j "Step 2: Attach this portfolio I just generated for you, with the following description."
    j "I grew up in Videville, a small town known for its vertical lake..."
    j "At 10, while helping my grandfather build the town's cycle superhighway, a cyclist stopped by." 
    j "It was no other than Syd Meat. Listening to his encouraging words, my vocation became clear."
    m "You know what, if I don't apply, I have a 100\% chance of being rejected. So I'll apply."
    j " Step 3: Read this 587 page document detailing the work environment at Grizley."
    j "With these three steps, you're guaranteed to get hired!"
    j "Remember, this version of JOBifAI is experimental. It is not advised to use it in a real-life setting."
    m "Awesome. Now I just need to submit the CV and portfolio, and hope for the best."


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

    hide j black normal
    with fade

    m "Finn! Wake up!!! I got an interview with Grizley!"
    show f green normal
    with dissolve
    f "Wait... Wwwhat?"
    m "Don't tell me... You forgot our conversation last night?"
    f "I'm afraid I only remember not having a headache like now..."
    m "I got an interview! Tomorrow 10am, I'm meeting the CEO of Grizley!"
    f "That's awesome, I'll be rooting for you!"

    scene bg buildinghall
    with fade

    label finish_series_job:
        $ renpy.checkpoint(hard=False)
        python:
            if not exists_img(series_cover):
                series_cover = get_random_object_name("portfolio/series.png")
                retry("finish_series_job", download_job_image, {"job_id": series_cover_job, "file_path": img_full_path(series_cover), "api_key": persistent.prodia_api_key})

    "Am I late? No one's there."

    "Galactic walls, ice-cream statues, pink electric barbed wires, just what I'd expect from the job of my dreams."

    "I see someone coming!"

    show s green normal
    with dissolve

    # init game assets

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
                portfolio_0 = get_random_object_name("portfolio/img_0.png")
                portfolio_0_job = retry("before_portfolio_0", generate_job, {"prompt": portfolio_prompt, "api_key": persistent.prodia_api_key})
    
    label finish_portfolio_0:
        $ renpy.checkpoint(hard=False)
        python:
            if not exists_img(portfolio_0):
                retry("finish_portfolio_0", download_job_image, {"job_id": portfolio_0_job, "file_path": img_full_path(portfolio_0), "api_key": persistent.prodia_api_key})
        
    label dont_reload_image_here:
        $ renpy.checkpoint(hard=False)
        "A woman. She's smiling. Should I go and talk to her?"
        $ im_portfolio_0 = im.Image(portfolio_0)
        show expression im_portfolio_0 

    label lobby_first:
        $ count = 0

        # reply = INPUT

        python:
            reply = renpy.input("Describe what you do.")
            reply = reply.strip()

        $ prompt = """
        Context: you are in the lobby of Grizley, an entertainment company.
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
        Moreover, describe what happens as a result of this action as a sentence s.
        Describe only the direct result of the action.
        Give your answer as a json of the form {"choice": c, "result": s}.
        """ % reply    
        
        $ schema = {"choice":  "integer:1<=i<=4", "result":  "string"}
        
        #python:
        $ a = persistent.groq_api_key
        $ answer = retry("lobby_first", ask_llm, {"prompt": prompt, "schema":schema, "api_key": a})
        $ choice = answer["choice"]
        $ result = answer["result"]
        $ jump_state = ["talk_secretary", "look_building", "bad_ending", "security"][choice - 1]

        # describe result  # maybe not depending on the transition?
        $ renpy.say(narrator, result)
        $ renpy.jump(jump_state) 

    label welcome_secretary:
    menu:

        "As soon as she catches my eye, I decide..."

        "To talk to her.":

            $ count += 1
            jump talk_secretary

        "To pretend to look around.":
            while count < 3:     
                    $ count += 1
                    jump look_building

            jump angry_boss

    label look_building:

        "What beautiful architecture."
        "Next time I'll definitely ask the lady for help."
        jump welcome_secretary

    label talk_secretary:
        scene bg buildinghall
        show s green normal at truecenter

        s "Hi there!"

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

        show g blue normal
        g "You're being disruptive. Please exit"

        jump bad_ending

    label angry_boss:

        hide s green normal
        with dissolve
        "Oh no... Someone who looks angry appears."

        show b red angry at truecenter

        b "What is it?"

        python:
            answer = renpy.input("Why are you staring at my hard working secretary?")
            answer = answer.strip()

            if not answer:
                answer = "Errr..."

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

        show b red normal at truecenter
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

    label bad_ending:
        "{b}Bad Ending{/b}"

        return

    label ending:
        "{b}Good Ending{/b}."

        return
