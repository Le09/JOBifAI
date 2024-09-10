# Part 5: Art director office.
label boss_neutral:

    $ ad_mood = "neutral"

    scene bg office
    with dissolve

    "What a cool office."

    show ad at truecenter
    with dissolve

    jump series_portfolio

label boss_angry:

    $ ad_mood = "angry"

    scene bg office

    b "Look, I have a lot of meetings today so you'd better be quick."

    show ad angry
    with dissolve

    jump series_portfolio

label boss_happy:

    $ ad_mood = "happy"

    scene bg office
    with dissolve
    "What a cool office."

    b "Would you like some coffee?"
    show ad at truecenter
    m "Thank you, but I'm trying to quit caffeine."
    b "More for me then!"

    jump series_portfolio


label boss_nervous_interview:
    b "I'm not sure I understood everything, could you take a deep breath, and explain it to me again?"
    "It's a stressful situation... Say what seems the best for you."
    $ ad_mood = "angry"

    jump portfolio_presentation

label boss_ok_ending:

    $ ad_mood = "neutral" # useless for now

    show ad
    b "You're an interesting candidate, you know."
    b "I must admit, if I could hire any interesting person, this company would be the size of a country."
    b "You see what I mean? Well, I have your contact info on your CV, so I'll call you back."

    jump ok_ending

label boss_happy_ending:
    show ad happy
    b "I must say I'm really surprised."
    b "In a good way. We can give you a trial."

    jump ending

label sad_boss:
    show ad at truecenter

    b "I think it's better if we stop here."
    m "I see. I'm sorry I couldn't do my best today. I'll leave immediately."
    b "Wwait!!! I..."
    b "I have some change in my pocket. Buy yourself a good sandwich with that. Good luck."

    jump worst_ending