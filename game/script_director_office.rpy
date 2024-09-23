# Part 5: Art director office.
label boss_neutral:

    $ ad_mood = "neutral"
    play music "intro_boss.mp3"
    scene bg office
    with dissolve

    "What a cool office."

    show ad at truecenter
    with dissolve

    jump start_series_portfolio

label boss_angry:
    stop music
    play music "intro_boss_angry.mp3"
    $ ad_mood = "angry"
    scene bg office

    b "Look, I have a lot of meetings today so you'd better be quick."

    show ad angry
    with dissolve

    play music "meow-bossinterviewtension.mp3"
    queue music "meow-lagrangianfull.mp3"
    jump start_series_portfolio

label boss_happy:

    $ ad_mood = "happy"

    play music "intro_boss_happy.mp3"
    scene bg office
    with dissolve
    "What a cool office."

    show ad happy at truecenter
    b "So... This morning I got a call from our CCO."
    b "{i}My dearest art director, you took Grizley to new heights with your vision.{/i}"
    b "{i}With your latest submission... You might have been too high.{/i}"
    b "Pretty insulting, am I correct? Well, I needed to relax, so I asked the secretary for coffee."
    b "But what I got instead, was some tonka bean-infused cream melting into the velvety and delicate liquid, a concentrate of the most precious beans."
    menu:
        "Do you want some?"

        "No thank you, I'm trying to quit caffeine.":
            "You look at the art director slowly appreciating his coffee."

        "Thank you very much! I'd love that.":
            $ achievement_coffee.grant()
            "You wait for the coffee, listening to the director's extended rant about the CCO. Coffee arrives, served in a custom ceramic cup. It has a chocolatey rich color, and a delicious nutty scent. Forget the interview, the coffee alone was worth the trip."

    jump start_series_portfolio


label boss_nervous_interview:
    b "I'm not sure I understood everything, could you take a deep breath, and explain it to me again?"
    "It's a stressful situation... Say what seems the best for you."
    $ ad_mood = "angry"

    jump portfolio_presentation

label boss_ok_ending:

    $ ad_mood = "neutral"

    show ad
    stop music fadeout 1.0
    b "You're an interesting candidate, you know."
    play music "randoman-full.mp3"
    b "I must admit, if I could hire any interesting person, this company would be the size of a country."
    b "You see what I mean? Well, I have your contact info on your CV, so I'll call you back."

    jump ok_ending

label boss_happy_ending:
    show ad happy
    stop music fadeout 1.0
    b "I must say I'm really surprised."
    play music "randoman-full.mp3"
    b "In a good way. We can give you a trial."

    jump ending

label sad_boss:
    show ad at truecenter
    stop music fadeout 1.0

    b "I think it's better if we stop here."
    play music "meow-endingtension.mp3"
    m "I see. I'm sorry I couldn't do my best today. I'll leave immediately."
    b "Wwait!!! I..."
    b "I have some change in my pocket. Buy yourself a good sandwich with that. Good luck."

    jump worst_ending