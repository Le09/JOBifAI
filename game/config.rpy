default persistent.prodia_api_key = "default_value_1"
default persistent.groq_api_key = "default_value_2"

screen config_menu():
    tag menu

    frame:
        label "Configuration Menu":
            xalign 0.5

        vbox:
            xalign 0.5
            yalign 0.2
            text _("To play, you will need two API keys to process the AI calls needed to make this game work. These accounts are free and will give you enough free call to play the game as much as you want.")
            text _("{a=https://console.groq.com/keys}https://console.groq.com/keys{/a}")
            text _("{a=https://docs.prodia.com/reference/getting-started-guide}https://docs.prodia.com/reference/getting-started-guide{/a}")
            text _("(we are not affiliated to these services, they just seemed the most convenient)")
        default pak_value = VariableInputValue("persistent.prodia_api_key", returnable=True)
        default ck2_value = VariableInputValue("persistent.groq_api_key", returnable=True)
        vbox:
            xalign 0.5
            yalign 0.5
            text "Prodia API Key:":
                textalign 0.5
            button:
                action pak_value.Toggle()
                input:
                    value pak_value
                    copypaste True
            text "Groq Key:"
            button:
                action ck2_value.Toggle()
                input:
                    value ck2_value
                    copypaste True

        textbutton "Return" action Return()
# python:
#    import chatgpt
    # apikey = renpy.input("What is your OPENAI API Key?", length=64)
