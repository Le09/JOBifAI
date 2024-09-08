# Part 5: Art director office.
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

label boss_angry_interview:
    jump ending

label interview:
    # $ im_portfolio_0 = im.Image(portfolio_0)
    # show expression im_portfolio_0

label sad_boss:
    show ad at truecenter

    b "I think it's better if we stop here."
    m "I see. I'm sorry I couldn't do my best today. I'll leave immediately."
    b "Wwait!!! I..."
    b "I have some change in my pocket. Buy yourself a good sandwich with that. Good luck."

    jump worst_ending