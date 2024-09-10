# Part 5: Art director office.
label boss:

    scene bg office
    with dissolve

    show ad at truecenter
    "What a cool office."

    b "I'm not going to go over all of the new series concept, you had all this information in the job posting that you read so diligently."
    b "So I'll just let you see the very private image that our main artist drew to showcase it."
    # $ im_series_cover = im.Image(series_cover)

    $ im_series_cover_full = im.Scale(series_cover, 1080, 1080)
    $ im_series_cover_right = im.Scale(series_cover, 540, 540)

    window hide
    # show expression im_series_cover at truecenter
    show expression im_series_cover_full at truecenter
    with dissolve
    pause

    window show
    b "I'll let it magically hover above the desk so that you can keep it as reference during our discussion."

    hide expression im_series_cover_full
    show expression im_series_cover_right:
        xalign 0.65
        yalign 0.3
    with dissolve

    b "Now, your main portfolio submission for the project was quite striking, so that's why you're here today."


    $ im_portfolio_0 = im.Image(portfolio_0)
    $ im_portfolio_0_full = im.Scale(portfolio_0, 1080, 1080)
    $ scaled_dim = int(renpy.image_size(portfolio_0)[1] / 3)
    #$ im_portfolio_0_scaled = im.Scale(portfolio_0, 256, 256)  # also possible to do it like this
    window hide
    show expression im_portfolio_0_full at truecenter
    with dissolve
    pause


    window show
    b "I'll put it on the right for reference."
    hide expression im_portfolio_0_full

    show expression im_portfolio_0 at truecenter:
        xalign 0.95
        yalign 0.3
        xsize scaled_dim
        ysize scaled_dim
    with dissolve 

    m "What the hell is this? How am I going to explain?"

    jump boss_portfolio_presentation

label boss_portfolio_presentation:
    python:
        reply = renpy.input("Can you give a little presentation of your portfolio? Based on this picture?")
        reply = reply.strip()

    while count_interview_boss < 3:
        $ count_interview_boss+= 1
        $ prompt = """
        Context: the main character is having an interview at 10 am for Grizley, an entertainment company.
        There is a central desk, a door, a plant, some paintings.
        The art director is in a normal mood.
        The character submitted an image, the description d is as follows: %s
        Here are the possible actions for the character:
        1) say nothing or a confusing blurb
        2) give a description close to d
        3) leave the building
        4) act in a very suspicious or rude manner
        5) give a description quite original/interesting, but far from d
        6) give a very plain presentation or something else

        Here is a description of what the character did:

        %s

        Evaluate what the answer may be among the previous options as a choice c.
        Be strict on the fact that for option 2), the answer must take decisive action to get this result; if the main character does not, the result should be 6.
        If the character takes no action, then the result should be 6).
        If the character says "", nothing, then the result should be 6).
        Moreover, describe what happens as a result of this action as a sentence s.
        Describe only the direct result of the action.
        Give your answer as a json of the form {"choice": c, "result": s}.
        """ % (portfolio_prompt, reply)

        $ schema = {"choice":  "integer:1<=i<=6", "result":  "string"}

        #python:
        $ a = persistent.groq_api_key
        $ answer = retry("boss_portfolio_presentation", ask_llm, {"prompt": prompt, "schema":schema, "api_key": a})
        $ choice = answer["choice"]
        $ result = answer["result"]
        $ jump_state = ["boss_nervous_interview", "boss_happy", "bad_ending", "security", "boss_happy", "boss_nervous_interview"][choice - 1]

        # describe result  # maybe not depending on the transition?
        $ renpy.say(narrator, result)
        $ renpy.jump(jump_state)

    jump sad_boss


label boss_angry_interview:
    scene bg office
    show ad angry

    b "Look, I have a lot of meetings today so you'd better be quick."

    $ im_portfolio_0 = im.Image(portfolio_0)
    show expression im_portfolio_0
    with dissolve 

    m "What the hell is this? How am I going to explain?"

label angry_boss_portfolio_presentation:

    m "The director looks angry... What am I gonna do?"

    python:
        reply = renpy.input("Can you give a little presentation of your portfolio? Based on this picture?")
        reply = reply.strip()

    while count_angry_boss_interview < 3:
        $ count_angry_boss_interview+= 1
        $ prompt = """
        Context: the main character is having an interview at 10 am for Grizley, an entertainment company.
        There is a central desk, a door, a plant, some paintings.
        The art director is visibly angry, because the character was weird with the secretary.
        The character submitted an image, the description d is as follows: %s
        Here are the possible actions for the character:
        1) say nothing or a confusing blurb
        2) give a description close to d
        3) leave the building
        4) act in a very suspicious or rude manner
        5) give a description quite original/interesting, but far from d
        6) give a very plain presentation or something else

        Here is a description of what the character did:

        %s

        Evaluate what the answer may be among the previous options as a choice c.
        Be strict on the fact that for option 2), the answer must take decisive action to get this result; if the main character does not, the result should be 6.
        If the character takes no action, then the result should be 6).
        If the character says "", nothing, then the result should be 6).
        Moreover, describe what happens as a result of this action as a sentence s.
        Describe only the direct result of the action.
        Give your answer as a json of the form {"choice": c, "result": s}.
        """ % (portfolio_prompt, reply)

        $ schema = {"choice":  "integer:1<=i<=6", "result":  "string"}

        #python:
        $ a = persistent.groq_api_key
        $ answer = retry("angry_boss_portfolio_presentation", ask_llm, {"prompt": prompt, "schema":schema, "api_key": a})
        $ choice = answer["choice"]
        $ result = answer["result"]
        $ jump_state = ["boss_nervous_interview", "boss_happy", "bad_ending", "security", "boss_happy", "boss_nervous_interview"][choice - 1]

        # describe result  # maybe not depending on the transition?
        $ renpy.say(narrator, result)
        $ renpy.jump(jump_state)

    jump sad_boss


label boss_nervous_interview:
    "It's a stressful situation... Say what seems the best for you."

    jump angry_boss_portfolio_presentation

label interview:
    # $ im_portfolio_0 = im.Image(portfolio_0)
    # show expression im_portfolio_0

label boss_happy:
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