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
        m "I'm waiting for so long... and I can't leave now. Hopefully just a few more seconds..."
        $ retry("start_series_portfolio", download_image, {"job_id": series_cover_job, "file_path": img_full_path(series_cover), "force": True})
        b "Sorry for the wait, you know how it is, there's always a multi-million dollar project cooking."

label start_check_portfolio:
    if not exists_img(portfolio_0):
        b "Oh, I'm sorry, your portfolio isn't in your file."
        b "We've had a lot of submissions lately, so we got an assistant who does a reference check."
        b "I'll call in the secretary to bring your submissions back, please wait a minute..."
        m "Are these people supposed to be professional? Unbelievable."
        $ retry("finish_portfolio_0", download_image, {"job_id": portfolio_0_job, "file_path": img_full_path(portfolio_0), "force": True})
        b "Alright, thank you for your patience. It's one of the most important virtues."

label series_portfolio:
    play music "meow-bossenter.mp3" loop
    b "I don't need introductions, so we can begin the interview."
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
    show expression im_portfolio_0 at truecenter:
        xalign 0.98
        yalign 0.3
        xsize scaled_dim
        ysize scaled_dim
    with dissolve


    m "..."
    m "What the hell is this? How am I going to explain?"

    stop music fadeout 1.0
    play music "meow-bossinterviewbass.mp3"
    queue music "meow-lagrangianfull.mp3"
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
        play sound "validate.mp3"
        $ reply = reply.strip() or "huuuuuh..."

        $ mm.add_history(kind="adv", who=narrator.name, what=reply)

        $ prompt_add = count_boss_presentation == 2
        $ prompt_direct = "The director should describe a bit what the original subject was about to get the applicant to explain the link with the portfolio" if prompt_add else ""
        if count_boss_presentation == 5:
            $ prompt_direct = "There is no time left for the interview, so the director should simply conclude, giving a very vague description of his general feeling on the interview, unless confidence is above .8, and he can be really positive."
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
            play sound "bad_cancel.mp3"
            # $ ad_mood = "angry"
            $ jump_state = "security"
        elif confidence >= 0.85:
            show ad happy
            play sound "good.mp3"
            # $ ad_mood = "happy"
            $ jump_state = "boss_happy_ending"
        else:
            if confidence < 0.33:
                show ad angry
                play sound "weird.mp3"
                # $ ad_mood = "angry"
                stop music
                $ count_warning+=1
                play music "meow-bossinterviewtension.mp3"
                queue music "meow-lagrangianfull.mp3"
            elif confidence < 0.6:
                show ad
            else:
                show ad happy
                play sound "ok.mp3"
            $ jump_state = "portfolio_presentation"

        $ bb.add_history(kind="adv", who=b.name, what=ad_answer)

        $ renpy.invoke_in_thread(voice_text, ad_answer[:120], "normal")
        show screen say_scroll("Boss: ", ad_answer)
        pause  # otherwise the screen instantly disappears!
        hide screen say_scroll

        $ renpy.jump(jump_state)
    if count_boss_presentation >= 5:
        play sound "weird.mp3"
        b "Oh, but I didn't see the time... we have to move on."
        b "This conversation has been interesting, to say the least."

    if confidence < 0.5:
        play sound "weird.mp3"
        jump sad_boss
    elif confidence >= 0.8:
        play sound "good.mp3"
        jump boss_happy_ending
    else:
        play sound "ok.mp3"
        jump boss_ok_ending
