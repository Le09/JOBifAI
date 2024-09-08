# Part 3: Art director office.
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