# Part 6: Portfolio presentation.

label series_portfolio:
    b "I'm not going to go over all of the new series concept, you had all this information in the job posting that you read so diligently."
    b "So I'll just let you see the very private image that our main artist drew to showcase it."

    $ im_series_cover_full = im.Scale(series_cover, 1080, 1080)
    $ im_series_cover_right = im.Scale(series_cover, 540, 540)

    window hide
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

    jump portfolio_presentation

label portfolio_presentation:

    $ ad_mood_string_prompts = {
            "angry": "Because the applicant was late, the art director is in a bad mood already.",
            "neutral": "The art director wants to be very professional.",
            "happy": "The day has been good, so the art director is in a cheerful mood.",
    }
    $ ad_mood_string = ad_mood_string_prompts[ad_mood]

    $ ad_intro = """
    Your portfolio is absolutely stunning.
    It has this human touch and sensibility that we are really looking for here at Grizley.
    However, I can't help but be perplexed by the choices you made in expressing this subject.
    Can you explain to me why you made these choices? How can the viewer understand?
    """

    while count_boss_presentation < 3 and count_warning < 2 :
        $ count_boss_presentation+=1
        python:
            reply = renpy.input("Can you give a little presentation of your portfolio? Based on this picture?")
            reply = reply.strip()

        $ prompt = """

        Context: the initial subject was: %s
        The applicant submitted a portfolio that showed the following idea: %s
        The art director is evaluating the potential new designer for the show. Here is what the art director asked: %s

        %s

        Here is the applicant answer:

        %s

        Given this answer, evaluate how convinced the art director might be?
        Give your answer as json, with a number r between 0 and 1, and the direct answer a of the director to the applicant in the form {"confidence": r, "ad_answer": a}

        """%(series_idea, portfolio_idea, ad_intro, ad_mood_string, reply)

        $ schema = {"confidence":  "number:0<=i<=1", "ad_answer":  "string"}
        #python:
        $ a = persistent.groq_api_key
        $ answer = retry("portfolio_presentation", ask_llm, {"prompt": prompt, "schema":schema, "api_key": a})
        $ confidence = answer["confidence"]
        $ ad_answer = answer["ad_answer"]

        # TODO
        # first question
        # confidence between 0 and 1
        # <.33 : suspicious -> security, or maybe 1 warning if > .25 then security
        # < .66: nothing
        # > exhalted, almost weird

        # 4 turns (questions?) to accept candidate
        # very bad: blackliste
        # ok: we may call you

        if confidence < 0.10:
            $ jump_state = "security"
        elif confidence < 0.33:
            $ count_warning+=1
            $ jump_state = "portfolio_presentation"
        elif confidence < 0.67:
            $ jump_state = "boss_ok_ending"
        else:
            $ jump_state = "boss_happy_ending"

        # describe result  # maybe not depending on the transition?
        $ renpy.say(narrator, ad_answer)
        $ renpy.jump(jump_state)

    jump sad_boss