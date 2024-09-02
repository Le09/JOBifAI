default persistent.prodia_api_key = "default_value_1"
default persistent.groq_api_key = "default_value_2"

screen config_menu():
    # Todo: 
    # input both keys /
    # save both keys
    # make it pretty
    # make it work with AI api
    tag menu

    frame:
        label "Configuration Menu":
            xalign 0.5
        default pak_value = VariableInputValue("persistent.prodia_api_key", returnable=True)
        default ck2_value = VariableInputValue("persistent.groq_api_key", returnable=True)
        vbox:
            xalign 0.5
            yalign 0.2
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
