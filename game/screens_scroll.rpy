init offset = -90

screen say_scroll(who, what):
    style_prefix "say"
    zorder 99

    add "gui/viewport.png" xalign 0.5 yalign 1.0

    side "c":
        area (000, 800, 1920, 277)

        viewport id "vp2":
            draggable True
            mousewheel True
            # scrollbar thumb size
            child_size 1900, 1000
            scrollbars "vertical"

            if who is not None:

                vbox:
                    pos (0.01, 0.02)
                    text who id "who"

                vbox:
                    xfill True
                    pos (0.01, 0.08)
                    id "namebox"
                    style "namebox"
                    text what id "what"
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

screen viewport_llm(prompt):
    style_prefix "input"
    zorder 99
    add "gui/viewport.png" xalign 0.5 yalign 1.0
    side "c":
        area (000, 800, 1920, 277)

        viewport id "vp":
            child_size 1900, 1000
            draggable True
            mousewheel True
            scrollbars "vertical"

            vbox:
                xfill True
                pos (0.01, 0.02)

                text prompt[1] style "input_prompt"

            vbox:
                pos (0.01, 0.2)
                # this field with this specific id is necessary for the custom input screen
                input id "input"
