default prodia_api_key = "default_value_1"
default config_key_2 = "default_value_2"

screen config_menu():
    tag menu

    frame:
        label "Configuration Menu"

        vbox:
            text "Prodia API Key"
            input value VariableInputValue("prodia_api_key")

            text "Key 2:"
            input value VariableInputValue("config_key_2")

        textbutton "Return" action Return()
