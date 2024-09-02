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

# The game starts here.
label start:

    # play music "illurock.opus"

    if persistent.game_first_time:
        call screen config_menu
        # $ game_first_time = False

    scene bg bedroom
    with fade

    init python:
        # create venv called llenaige in 3.9, in game folder
        import os
        import sys
        path_venv = "~/.virtualenvs/llenaige/lib/python3.9/site-packages/"
        sys.path.append(os.path.expanduser(path_venv))
        from chatgpt_n.llm import ask_llm
        # config = {"groq_api_key": settings_api_key}

    m "Gin...ious... I'm a gin...ious..."
    show f green normal
    with dissolve
    f "Ahem... If you're so... rhum...markeable... Hohoho... Why aren't you working for Giggle?"
    m "Giggle... When I apply, I'll be there in no time. Watch me!"
    f "Watching... With my Eyes... Wide...  OZzzzZZZzzzzz"
    hide f green normal
    with dissolve
    m "Finn, you never handled alcohol too well."

    show j black normal
    with fade
    m "JOBifAI, how do I become concept designer for Giggle?"
    j "Complete these 4 steps to become concept designer for Giggle:"
    j "Step 1: Send this CV I made for you. It says you have a degree in Industrial Design from RISD."
    j "Add the link of your SinkedIN page I just made. I connected you to some notable concept designers."
    m "What is RISD? And who are these SinkedIN \'friends\' you connected me to? Their faces are weird."
    j "Step 2: Attach this portfolio I just generated for you, with the following description."
    j "I grew up in Videville, a small town known for its vertical lake..."
    j "At 10, while helping my grandfather build the town's cycle superhighway, a cyclist stopped by." 
    j "It was no other than Syd Meat. Listening to his encouraging words, my vocation became clear."
    m "You know what, if I don't apply, I have a 100\% chance of being rejected. So I'll apply."
    j " Step 3: Read this 587 page document detailing the work environment at Giggle."
    j "With these three steps, you're guaranteed to get hired!"
    j "Remember, this version of JOBifAI is experimental. It is not advised to use it in a real-life setting."
    m "Awesome. Now I just need to submit the CV and portfolio, and hope for the best."

    hide j black normal
    with fade

    m "Finn! Wake up!!! I got an interview with Giggle!"
    show f green normal
    with dissolve
    f "Wait... Wwwhat?"
    m "Don't tell me... You forgot our conversation last night?"
    f "I'm afraid I only remember not having a headache like now..."
    m "I got an interview! Tomorrow 10am, I'm meeting the CEO of Giggle!"
    f "That's awesome, I'll be rooting for you!"

    scene bg buildinghall
    with fade

    "Am I late? No one's there."

    "Galactic walls, ice-cream statues, pink electric barbed wires, just what I'd expect from the job of my dreams."

    "I see someone coming!"

    show s green normal
    with dissolve

    "A woman. She's smiling. Should I go and talk to her?"

    $ count = 0

    # reply = INPUT

    python:
        reply = renpy.input("Describe what you do.")
        reply = reply.strip()
    
    $ prompt = """
    Context: you are...
    Here are the possible actions:
    1) ask the secretary for instructions
    2) inspect the building
    3) act in a very suspicious or rude manner
    Here is a description of what the character did:
    
    %s

    Evaluate what the answer may be among the previous options as a choice c.
    Moreover, describe what happens as a result of this action as a sentence s.
    Give your answer of the form {"choice": c, "result": s}.
    """ % reply    
    
    $ schema = {"choice":  "integer:0<=i<=4", "result":  "string"}
    # answer = ask_llm_validate_input(prompt, schema=schema, config=config)
    
    # $ is for changing variables, uses python
    python:
        # answer = chatgpt.compl(prompt, schema=schema, config=config)
         
        answer = ask_llm(prompt, schema=schema, config=persistent.config)
    $ choice = answer["choice"]
    $ result = answer["result"]
    $ jump_state = {"1": "state", "2": state, "3": state}[choice]

    # describe result  # maybe not depending on the transition?
    # jump jump_state 

    label welcomesecretary:
    menu:

        "As soon as she catches my eye, I decide..."

        "To talk to her.":

            $ count += 1
            jump talksecretary

        "To pretend to look around.":
            while count < 3:     
                    $ count += 1
                    jump lookbuilding

            jump angryboss

    label lookbuilding:

        "What beautiful architecture."
        "Next time I'll definitely ask the lady for help."
        jump welcomesecretary

    label talksecretary:
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

        jump badending

    label angryboss:

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

        # jump angryboss
        # jump happyboss

        b "I see. Come with me."

        jump ending

    label badending:
        "{b}Bad Ending{/b}"

        return

    label ending:
        "{b}Good Ending{/b}."

        return
