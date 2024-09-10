
label series_portfolio:
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

    # TODO
    $ jump boss_state
