# Part 1: The game begins here.
label start:
    $ dir_session = get_random_object_name("session", folders=["images"])
    $ create_folder(dir_session)
    if not persistent.user_id:
        $ persistent.user_id = get_random_object_name("user_id_")
    if persistent.game_first_time:
        call screen first_time
        $ persistent.game_first_time = False

    scene bg room
    with fade
    # play music "eyeswideopen-intro.mp3"

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
    j "......"

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
        portfolio_prompt = result["prompt"] + ", 2D Game Art style, painterly brushstrokes, vibrant colors, dramatic lighting, AI artifacts, Ankama vivid animation style"
        if not portfolio_0:
            portfolio_0 = get_random_object_name("p0.webp", [dir_session])

label jobifai_instructions:
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
    $ result = askllm("start", prompt, schema)

label init_series_job:
    $ renpy.checkpoint(hard=False)
    python:
        series_idea = result["sentence"]
        series_prompt = "Create an action-adventure scene inspired by classic JRPG in a vibrant anime-style, where: " + result["prompt"]
        if not series_cover:
            series_cover = get_random_object_name("series.webp", [dir_session])

label wake_up:
    scene bg room
    $ achievement_woke_up.grant()

    m "Henk! Wake up!!! I got an interview with Grizley!"
    show henk
    with dissolve
    h "Wait... Wwwhat?"
    m "Don't tell me... You forgot our conversation last night?"
    h "I'm afraid I only remember not having a headache, whereas now..."
    m "I got an interview! Tomorrow 10am, I'm meeting the CEO of Grizley!"
    h "Tomorrow! Too late to Escape! I'll be rooting for you!"

    jump before_going
