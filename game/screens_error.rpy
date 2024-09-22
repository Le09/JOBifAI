screen error_prodia_menu():
    tag menu
    $ on_top = touch_variant()
    frame:
        xmargin 200
        xpadding 40
        if on_top:
            ymargin 10
        else:
            ymargin 140

        vbox:
            if on_top:
                textbutton "Return" action Return()
            label "Prodia Error":
                xalign 0.5
                bottom_margin 20
            vbox:
                text _("This API key is invalid. Please correct it and try again.")
                text _("Follow the following link to create a new one if you need to.")
                text _("{a=https://docs.prodia.com/reference/getting-started-guide}https://docs.prodia.com/reference/getting-started-guide{/a}")
                null height 30
            default pak_value = VariableInputValue("persistent.prodia_api_key", returnable=True)
            vbox:
                text "Prodia API Key:"
                button:
                    action pak_value.Toggle()
                    input:
                        length 40
                        value pak_value
                        copypaste True
                null height 30
            vbox:
                xalign .1
                textbutton "Basic Configuration" action ShowMenu("config_menu")
                textbutton "Advanced Configuration" action ShowMenu("advanced_config_menu")
            if not on_top:
                textbutton "Return" action Return()

screen error_llm_menu():
    tag menu
    $ on_top = touch_variant()
    frame:
        xmargin 200
        xpadding 40
        if on_top:
            ymargin 10
        else:
            ymargin 140

        vbox:
            if on_top:
                textbutton "Return" action Return()
            label "LLM Error":
                xalign 0.5
                bottom_margin 20
            text _("This API key is invalid. Please correct it and try again.")
            text _("Follow the following link to create a new one if you need to.")
            text _("{a=https://console.groq.com/keys}https://console.groq.com/keys{/a}")
            null height 30
            default pak_value = VariableInputValue("persistent.groq_api_key", returnable=True)
            text "Groq API Key:"
            button:
                action pak_value.Toggle()
                input:
                    length 60
                    value pak_value
                    copypaste True
            null height 30
            textbutton "Basic Configuration" action ShowMenu("config_menu")
            textbutton "Advanced Configuration" action ShowMenu("advanced_config_menu")
            if not on_top:
                textbutton "Return" action Return()
