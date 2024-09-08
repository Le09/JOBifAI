# Part 1: The game begins here.
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

    jump street
