# Company wants to hire concept designer.
# Drunk, you sent SO generated images in a portfolio.
# The AD did not catch up on this as they have strict non AI poligcy.
# IDEA: you need to BS your way through portfolio & serie concepts are random

# Declare characters used by this game.
define s = Character(_("Secretary"), color="#c8ffc8")
define m = Character(_("Me"), color="#c8c8ff")
define b = Character(_("Boss"), color="#ffc8ff")
define g = Character(_("Guard"), color="#ffffff")


# The game starts here.
label start:

    # play music "illurock.opus"

    scene bg buildinghall
    with fade

    "Am I late? No one's there."

    "Galactic walls, ice-cream statues, pink electric barbed wires, just what I'd expect from the job of my dreams."

    "I see someone coming!"

    show s green normal
    with dissolve

    "A woman. She's smiling. Should I go and talk to her?"

    $ count = 0

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
