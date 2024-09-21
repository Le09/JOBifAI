default persistent.prodia_api_key = "demo_key_value_1_a45ohopps7z"
default persistent.groq_api_key = "demo_key_value_2_yuzegfa8ert"

default persistent.prodia_api_key_demo = "PRODIA_DEMO_KEY"
default persistent.groq_api_key_demo = "LLM_DEMO_KEY"

screen config_menu():
    tag menu

    frame:
        xmargin 200
        ymargin 140
        xpadding 40

        vbox:
            label "Basic Configuration":
                xalign 0.5
                bottom_margin 20
            vbox:
                xalign 0.5
                yalign 0.2
                text _("Leave demo in these fields to use our demo keys.")
                text _("To play, you will need two API keys to process the AI calls needed to make this game work. These accounts are free and will give you enough free call to play the game as much as you want.")
                text _("{a=https://console.groq.com/keys}https://console.groq.com/keys{/a}")
                text _("{a=https://docs.prodia.com/reference/getting-started-guide}https://docs.prodia.com/reference/getting-started-guide{/a}")
                text _("(we are not affiliated to these services, they just seemed the most convenient)")
                null height 30
            default pak_value = VariableInputValue("persistent.prodia_api_key", returnable=True)
            default ck2_value = VariableInputValue("persistent.groq_api_key", returnable=True)
            vbox:
                xalign 0.2
                yalign 0.5
                text "Prodia API Key:":
                    textalign 0.5
                button:
                    action pak_value.Toggle()
                    input:
                        length 40
                        value pak_value
                        copypaste True
                text "Groq Key:"
                button:
                    action ck2_value.Toggle()
                    input:
                        length 60
                        value ck2_value
                        copypaste True
                null height 30
            vbox:
                xalign .1
                textbutton "Advanced Configuration" action ShowMenu("advanced_config_menu")
                textbutton "Privacy" action ShowMenu("privacy")
                textbutton "Demo Disclaimer" action ShowMenu("demo_disclaimer")
            vbox:
                textbutton "Return" action Return()

screen advanced_config_menu():
    tag menu

    frame:
        xmargin 200
        ymargin 140
        xpadding 40
        vbox:
            label "Advanced Configuration":
                xalign 0.5
                bottom_margin 20
            vbox:
                text _("This game use the standard OpenAI REST API.")
                text _("Any service compatible with it should work provided you give the right url and model.")
                text _("""For instance, local Ollama would work, with url "http://localhost:11434/v1/chat/completions" and model "llama2-uncensored".""")
                text _("If you're not sure what this means, please use the basic configuration.")
                text _("You can just erase the values to go back to standard configuration.")
            default url_value = VariableInputValue("persistent.llm_url", returnable=True)
            default model_value = VariableInputValue("persistent.llm_model", returnable=True)
            null height 30
            vbox:
                xalign 0.2
                text "LLM url:"
                button:
                    action url_value.Toggle()
                    input:
                        length 66
                        value url_value
                        copypaste True
                text "LLM model:"
                button:
                    action model_value.Toggle()
                    input:
                        length 36
                        value model_value
                        copypaste True
            null height 30
            text _("There is no local option for image generation; it is considerably harder to setup SDXL with ComfyUI, and by design there is basically no privacy leak nor safety concerns with the images. We might consider it in the future if there is enough demand.")

            null height 30
            textbutton "Back to basic AI Configuration" action ShowMenu("config_menu")
            textbutton "Return" action Return()

screen privacy():
    tag menu
    frame:
        xmargin 200
        ymargin 140
        xpadding 40
        vbox:
            label "Privacy":
                xalign 0.5
            vbox:
                text _("We do not proxy or log any data.")
                text _("Your queries are identified by a random ID that is not tied in any way to your account.")
                text _("If you want the best privacy, you can use a local LLM. See advanced configuration.")
            null height 30
            textbutton "Back to basic AI Configuration" action ShowMenu("config_menu")
            textbutton "Return" action Return()

screen demo_disclaimer():
    tag menu
    frame:
        xmargin 200
        ymargin 140
        xpadding 40
        vbox:
            label "Disclaimer":
                xalign 0.5
            vbox:
                text _("The AI calls use an external service with our demo keys.")
                text _("Too inappropriate content might be rejected by the safety filters, in which case you can retry, or change your input.")
                text _("If the demo keys that are packaged by default are abused by users, they might stop working.")
                text _("In that case, please see basic configuration to use your own free keys, or use advanced options.")
            null height 30
            textbutton "Back to basic AI Configuration" action ShowMenu("config_menu")
            textbutton "Return" action Return()
