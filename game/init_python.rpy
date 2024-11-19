
init -11 python:
    import os
    import sys
    import uuid
    import datetime
    import base64
    import requests

    # disable moving through history with the scroll wheel
    # https://www.renpy.org/doc/html/keymap.html
    config.keymap['rollback'].remove('mousedown_4')
    config.keymap['rollforward'].remove('mousedown_5')

    class BannedException(Exception):
        pass

    def touch_variant():
        result = renpy.variant("touch") or renpy.variant("steam_deck")
        if persistent.touch == "yes":
            result = True
        elif persistent.touch == "no":
            result = False
        return result

    def stringify_h(h):
        prefix = "_   " if h.what_args["style"] == "say_transcript" else "    "
        result = "%s%s" % (prefix, h.what)
        return "%s:\n%s" % (h.who, result) if h.who else result

    def stringify_history():
        s_list = [stringify_h(h) for h in _history_list if h.what_args["style"] == "say_transcript"]
        return "\n\n".join(s_list)

    def save_transcript(ending_state):
        transcript = stringify_history()
        timestamp = datetime.datetime.now().strftime("t_%Y-%m-%d_%H-%M-%S")
        try:
            ask_server("transcript", {"transcript": transcript, "timestamp": timestamp, "state": ending_state})
        except Exception as e:
            pass

    def path_join(*args):
        return "/".join(args)

    def debug_log(msg):
        if config.developer:
            renpy.say("DEBUG", msg)

    def ask_server(function_name, args):
        url = "https://jobifai.woolion.art/api"
        #url = "http://localhost:3000/lambda"
        if not persistent.ticket:
            authentify()
        payload = {"ticket": persistent.ticket, "user_id": persistent.steam_id, "function_name": function_name,"args": args}
        response = requests.post(url, json=payload)
        if response.status_code == 403:
            raise BannedException()
        if response.status_code == 401:
            authentify()
            response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def authentify():
        if not persistent.steam_id:
            get_steam_id()
        get_ticket()
        ask_server("auth", {})

    def get_steam_id():
        try:
            uid = achievement.steam.get_csteam_id()  # account_id
            persistent.steam_id = uid
        except Exception as e:
            # TODO: call screen to say this version needs steam
            raise

    def get_ticket():
        if persistent.ticket:
            try:
                achievement.steam.cancel_ticket()
                persistent.ticket = None
            except Exception as e:
                print("Failed to cancel ticket: %s" % e)
        ticket = achievement.steam.get_session_ticket()
        print("Ticket: %s" % ticket)
        persistent.ticket = base64.b64encode(ticket).decode("utf-8")

    def askllm(state, prompt, schema):
        args = {"prompt": prompt, "schema": schema}
        return retry(state, ask_server, {"function_name": "ask_llm", "args": args})

    def download_flux_image(prompt, file_path):
        response = ask_server("download_image", {"prompt": prompt})
        image = response["image"]
        with open(file_path, 'wb') as file:
            file.write(base64.b64decode(image))

    def download_image(prompt, file_path, force=False):
        if force:
            return download_flux_image(prompt, file_path)
        else:
            renpy.invoke_in_thread(download_flux_image, prompt, file_path)

    def escape_text(text):
        return text.replace("{", "{{").replace("[", "[[").replace("}", "}}").replace("]", "]]")

    def retry_auth():
        try:
            return authentify()
        except Exception as e:
            s = "Steam authentication failed.\n\nYou need a valid Steam account and the Steam client running to play this game.\nConfirm retrial of authentication, or quit the game?"
            again = renpy.confirm(s)
            if again:
                return retry_auth()
            else:
                renpy.quit()

    def retry(fallback, function, kwargs):
        try:
            return function(**kwargs)
        except BannedException:
            s = "You have been banned from the game.\nIf you think this is unfair, please contact the developers.\nSelecting yes will quit the game, selecting no will cause the game running to stop."
            again = renpy.confirm(s)
            renpy.quit()
        except Exception as e:
            # TODO: more robust error handling
            if "body" in dir(e) and "error" in e.body:
                se = "Error: %s\n" % e.body["error"]["message"]
                if "failed_generation" in e.body["error"]:
                    se += "Justification: %s\n" % e.body["error"]["failed_generation"]
            else:
                se = e.message if "message" in dir(e) else str(e)
            s = "%s\n\n The operation failed. Do you want to retry?" % se
            s = escape_text(s)
            again = renpy.confirm(s)
            if again:
                return retry(fallback, function, kwargs)
            else:
                renpy.jump(fallback)

    def exists_img(image_name):
        return renpy.exists(image_name)

    def create_folder(*args):
        dir_base = renpy.config.basedir
        full_path = path_join(dir_base, "game", *args)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

    def get_random_object_name(base_name, folders=None, short=True):
        # it seems that renpy crashes while parsing the source if the filename is too long...
        # so normally I would put short to False, but it does not work
        name, ext = os.path.splitext(base_name)
        new_name = name + str(uuid.uuid4())[:8]
        salt = str(uuid.uuid4())
        salt = salt[:8] if short else salt.replace("-", "")
        new_name = name + salt
        new_name = new_name + ext  # ext would be "" or ".ext"
        if folders:
            new_name = path_join(*folders, new_name)
        return new_name

    def img_full_path(name, images=True):
        dir_base = path_join(renpy.config.basedir, "game")
        if not images:
            dir_base = path_join(dir_base, "images")
        file_path = path_join(dir_base, name)
        return file_path

    renpy.music.register_channel(name='beeps', mixer='voice')

    def voice_text(text, preset):
        build_sentence(text, preset)
        renpy.sound.play("audio/output.wav", channel="beeps", loop=False)

    def stop_voice():
        renpy.sound.stop(channel="beeps")

    def make_voice(preset):  # preset is the name of the audio folder
        def voice(event, **kwargs):
            if event == "show":
                voice_text(_last_say_what, preset)
            elif event == "slow_done" or event == "end":
                stop_voice()
        return voice
