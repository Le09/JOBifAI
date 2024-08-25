# Declare characters used by this game.
define s = Character(_("Secretary"), color="#c8ffc8")
define m = Character(_("Me"), color="#c8c8ff")
define b = Character(_("Boss"), color="#ffc8ff")

# This is a variable that is True if you've compared a VN to a book, and False
# otherwise.
default book = False

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

    label secretary:
    menu:

        "As soon as she catches my eye, I decide..."

        "To talk to her.":

            $ count += 1
            jump talks

        "To pretend to look around.":
            while count < 3:     
                    $ count += 1
                    jump lookbuilding

            jump angryboss

    label lookbuilding:

        "What beautiful architecture."
        "Next time I'll definitely ask the lady for help."
        jump secretary

    label talks:
        scene bg buildinghall
        show s green normal at truecenter

        s "Hi there!"

        python:
            answer = renpy.input("Is there any way I can help?")
            answer = answer.strip()

            if not answer:
                answer = "Errr..."

        s "Sure! I'll take you to the chef's office."

        jump boss


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

        b "I see. Come with me."

        jump ending

    label ending:
        "{b}Good Ending{/b}."

        return
