# Part 6: Portfolio presentation.

label start_series_portfolio:
    if not exists_img(series_cover) or not exists_img(portfolio_0):
        $ count_waiting_time+=1
        if count_waiting_time > 4:
            b "I'm sorry, I'm called urgently. We'll reschedule our meeting."
            b "We've had a lot of submissions lately. We'll do a reference check before calling you back."
            b "The secretary told me we cannot find your portfolio. Did you configure everything correctly?"
            jump bad_ending

        b "I'm sorry, I've got an urgent call. Let me answer it, and we can start the interview."
        b "......"
        m "They talk so fast, I'm not sure I understand most of it... that's a professional studio for you."
        $ renpy.pause(count_waiting_time * 10, hard=True)

        jump start_series_portfolio

label series_portfolio:
    play music "meow-bossenter.mp3" loop
    b "I'm not going to go over all of the new series concept, you had all this information in the job posting that you read so diligently."
    b "So I'll just let you see the very private image that our main artist drew to showcase it."

    $ im_series_cover_full = im.Scale(series_cover, 1000, 1000)
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
    $ im_portfolio_0_full = im.Scale(portfolio_0, 1000, 1000)
    $ scaled_dim = 420
    #$ im_portfolio_0_scaled = im.Scale(portfolio_0, 256, 256)  # also possible to do it like this
    window hide
    show expression im_portfolio_0_full at truecenter
    with dissolve
    pause


    window show
    b "I'll put it on the right for reference."
    hide expression im_portfolio_0_full

    stop music fadeout 1.0

    show expression im_portfolio_0 at truecenter:
        xalign 0.98
        yalign 0.3
        xsize scaled_dim
        ysize scaled_dim
    with dissolve

    pause

    m "What the hell is this? How am I going to explain?"

    play music "meow-bossinterviewbass.mp3"

    b "Can you give a little presentation of your portfolio? Based on the concept, why did you make this choice?"

    jump portfolio_presentation

label portfolio_presentation:

    $ ad_mood_string_prompts = {
            "angry": "Because the applicant was late, the art director is in a bad mood already.",
            "neutral": "The art director wants to be very professional.",
            "happy": "The day has been good, so the art director is in a cheerful mood.",
    }
    $ ad_mood_string = ad_mood_string_prompts[ad_mood]

    $ ad_answer = """
    Your portfolio is absolutely stunning.
    It has this human touch and sensibility that we are really looking for here at Grizley.
    However, I can't help but be perplexed by the choices you made in expressing this subject.
    Can you explain to me why you made these choices? How can the viewer understand?
    """

    while count_boss_presentation < 5 and count_warning < 3 :
        $ count_boss_presentation+=1

        $ reply = renpy.input(["Boss","Time to convince the Art Director!"], screen="viewport_llm")
        $ reply = reply.strip() or "huuuuuh..."

        $ narrator.add_history(kind="adv", who=narrator.name, what=reply)

        $ prompt_add = count_boss_presentation == 2
        $ prompt_direct = "The director should describe a bit what the original subject was about to get the applicant to explain the link with the portfolio" if prompt_add else ""
        $ prompt = """
        Context: the initial subject was: %s
        The applicant submitted a portfolio that showed the following idea: %s
        The art director is evaluating the potential new designer for the show. Here is what the art director said last: %s

        %s
        The current confidence level of the art director is at %s

        Here is the applicant answer:

        %s

        Given this answer, evaluate how convinced the art director might be?
        Give your answer as json, with a number r between 0 and 1, and the direct answer a of the director to the applicant in the form {"confidence": r, "ad_answer": a}
        If r is above 0.67, the director is convinced and will give a positive answer otherwise, he should press the candidate.
        %s

        """%(series_idea, portfolio_idea, ad_answer, ad_mood_string, str(confidence), reply, prompt_direct)

        $ schema = {"confidence":  "number:0<=i<=1", "ad_answer":  "string"}

        $ answer = askllm("portfolio_presentation", prompt, schema)
        $ confidence = answer["confidence"]
        $ ad_answer = answer["ad_answer"]

        $ debug_log("Confidence: %s" % str(confidence))

        if confidence < 0.10:  # must be a really bad answer
            show ad angry
            # $ ad_mood = "angry"
            $ jump_state = "security"
        elif confidence >= 0.85:
            show ad happy
            # $ ad_mood = "happy"
            $ jump_state = "boss_happy_ending"
        else:
            if confidence < 0.33:
                show ad angry
                # $ ad_mood = "angry"
                stop music
                $ count_warning+=1
                play music "meow-bossinterviewtension.mp3"
            $ jump_state = "portfolio_presentation"

        $ b.add_history(kind="adv", who=b.name, what=ad_answer)

        if count_boss_presentation < 5:
            show screen say_scroll("Boss: ", ad_answer)
        else:
            show screen say_scroll("Boss: ", "This conversation has been interesting, to say the least. But time is running out.")
        pause
        hide screen say_scroll

        $ renpy.jump(jump_state)

    if confidence < 0.5:
        jump sad_boss
    elif confidence >= 0.8:
        jump boss_happy_ending
    else:
        jump boss_ok_ending
