default persistent.img_account = "demo_cloudflare_account"
default persistent.img_api_key = "demo_key_value_1_a45ohopps7z"
default persistent.groq_api_key = "demo_key_value_2_yuzegfa8ert"


screen config_menu():
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
            label "Basic Configuration":
                xalign 0.5
                bottom_margin 20
            text _("These 3 fields NEED to be correctly set to be able to play.")
            null height 30
            default iac_value = VariableInputValue("persistent.img_account", returnable=True)
            default pak_value = VariableInputValue("persistent.img_api_key", returnable=True)
            default ck2_value = VariableInputValue("persistent.groq_api_key", returnable=True)
            text "CloudFlare AI account:"
            button:
                action iac_value.Toggle()
                input:
                    length 40
                    value iac_value
                    copypaste True
            text "CloudFlare AI token:"
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
            text _("To play, you will need to access the API to process the AI calls the game needs to work. These free accounts will give you enough to play as much as you want.")
            text _("{a=https://console.groq.com/keys}https://console.groq.com/keys{/a}")
            text _("{a=https://developers.cloudflare.com/workers-ai/get-started/rest-api/}https://developers.cloudflare.com/workers-ai/get-started/rest-api/{/a}")
            text _("(we are not affiliated to these services, they just seemed the most convenient)")
            text _("If you don't want to make this setup, you can play it directly on Steam:")
            text _("{a=https://store.steampowered.com/app/3248650/JOBifAI/}https://store.steampowered.com/app/3248650/JOBifAI/{/a}")
            null height 30
            textbutton "Advanced Configuration" action ShowMenu("advanced_config_menu")
            textbutton "Privacy" action ShowMenu("privacy")
            if not on_top:
                textbutton "Return" action Return()

screen advanced_config_menu():
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
            label "Advanced Configuration":
                xalign 0.5
                bottom_margin 20
            text _("This game use the standard OpenAI REST API.")
            text _("Any service compatible with it should work provided you give the right url and model.")
            text _("""For instance, local Ollama would work, with url "http://localhost:11434/v1/chat/completions" and model "llama2-uncensored".""")
            default url_value = VariableInputValue("persistent.llm_url", returnable=True)
            default model_value = VariableInputValue("persistent.llm_model", returnable=True)
            null height 30
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
            text _("If you're not sure what this means, please use the basic configuration.")
            text _("You can just erase the values to go back to standard configuration.")
            null height 30
            text _("There is no local option for image generation; it is considerably harder to setup SDXL with ComfyUI, and by design there is basically no privacy leak nor safety concerns with the images. We might consider it in the future if there is enough demand.")
            null height 30
            textbutton "Back to basic AI Configuration" action ShowMenu("config_menu")
            if not on_top:
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
                text _("Please refer to the services you use for their respective privacy terms.")
                text _("This version of JOBifAI directly calls the services, without any proxy or logging.")
                text _("If you want the best privacy, you can use a local LLM. See advanced configuration.")
                text _("Since you don't control the image generation prompt, there isn't much privacy leak from using an external provider.")
            null height 30
            textbutton "Back to basic AI Configuration" action ShowMenu("config_menu")
            textbutton "Return" action Return()

screen first_time():
    tag menu
    frame:
        xmargin 200
        ymargin 140
        xpadding 40
        vbox:
            label "Welcome":
                xalign 0.5
            vbox:
                text _("We hope you'll enjoy your time with JOBifAI!")
                text _("The AI calls use external services to run.")
                text _("Too inappropriate content might be rejected by the safety filters, in which case you can retry, or change your input.")
                text _("Please see basic configuration to use your own free keys, or use advanced options.")
                text _("If you don't want to make this setup, you can play it directly on Steam:")
                text _("{a=https://store.steampowered.com/app/3248650/JOBifAI/}https://store.steampowered.com/app/3248650/JOBifAI/{/a}")
            null height 30
            textbutton "Back to basic AI Configuration" action ShowMenu("config_menu")
            textbutton "Return" action Return()
