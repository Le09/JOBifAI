﻿init offset = -90

screen say_scroll(who, what):
    style_prefix "say"
    zorder 99
    $ on_top = touch_variant()

    frame:
        xmargin 200
        ysize 320
        xpadding 20
        if on_top:
            yoffset 50
        else:
            yoffset 720

        vbox:
            spacing 20
            text who id "who":
                justify True
            viewport:
                draggable True
                scrollbars "vertical"
                id "namebox"
                text what id "what":
                    justify True

screen viewport_llm(prompt):
    style_prefix "input"
    zorder 99
    $ on_top = touch_variant()
    frame:
        if on_top:
            yoffset 50
        else:
            yoffset 720
        ysize 320
        xmargin 200
        xpadding 20

        vbox:
            spacing 20
            text prompt[1] style "input_prompt":
                justify True
            viewport:
                draggable True
                scrollbars "vertical"
                input id "input":
                    xalign 0
                    xmaximum 2000
                    multiline True
                    copypaste True
                    justify False
