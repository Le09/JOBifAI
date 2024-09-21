
init python:
    import os
    import sys
    import uuid
    import datetime
    from ai_lib.llm import ask_llm
    from ai_lib.images import download_job_image, generate_job
    from ai_lib.exceptions import Unauthorized

    # disable moving through history with the scroll wheel
    # https://www.renpy.org/doc/html/keymap.html
    config.keymap['rollback'].remove('mousedown_4')
    config.keymap['rollforward'].remove('mousedown_5')

    def stringify_h(h):
        prefix = "_   " if h.what_args["style"] == "say_transcript" else "    "
        result = "%s%s" % (prefix, h.what)
        return "%s:\n%s" % (h.who, result) if h.who else result

    def stringify_history(full=True):
        if full:
            s_list = [stringify_h(h) for h in _history_list]
        else:
            s_list = [stringify_h(h) for h in _history_list if h.what_args["style"] == "say_transcript"]
        return "\n\n".join(s_list)

    def save_transcript():
        # I don't see a way to open a file dialog for the user to choose the path...
        # So let's default to the desktop. Hopefully it works on all platforms.
        # will it work with steam?
        transcript = stringify_history()
        path_home = os.path.expanduser("~")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename =  "%s_transcript_%s.txt" % (persistent.user_id, timestamp)
        file_path = os.path.join(path_home, "Desktop", filename)
        try:
            with open(file_path, "w") as f:
                f.write(transcript)
            renpy.notify("Transcript saved successfully on your Desktop!")
        except Exception as e:
            renpy.notify("Transcript save failed. Error: %s" % e)

    def path_join(*args):
        return "/".join(args)

    def debug_log(msg):
        if config.developer:
            renpy.say("DEBUG", msg)

    def askllm(state, prompt, schema):
        api_key = persistent.groq_api_key
        if not persistent.llm_url.strip():
            persistent.llm_url = "https://api.groq.com/openai/v1/chat/completions"
        if not persistent.llm_model.strip():
            persistent.llm_model = "llama3-8b-8192"
        url = persistent.llm_url.strip()
        model = persistent.llm_model.strip()
        if "demo" in api_key:
            api_key = persistent.groq_api_key_demo
        return retry(state, ask_llm, {"api_key": api_key, "prompt": prompt, "schema": schema, "user_id": persistent.user_id, "url": url, "model": model})

    def generate_image(state, prompt):
        api_key = persistent.prodia_api_key
        if "demo" in api_key:
            api_key = persistent.prodia_api_key_demo
        return retry(state, generate_job, {"prompt": prompt, "api_key": api_key})

    def download_image(job_id, file_path):
        api_key = persistent.prodia_api_key
        if "demo" in api_key:
            api_key = persistent.prodia_api_key_demo
        renpy.invoke_in_thread(download_job_image, job_id, file_path, api_key)

    def escape_text(text):
        return text.replace("{", "{{").replace("[", "[[").replace("}", "}}").replace("]", "]]")

    def retry(fallback, function, kwargs):
        try:
            return function(**kwargs)
        except Unauthorized as u:
            s = "The API key for the %s service was refused. You should configure it in the AI settings before retrying." % u.service_name
            renpy.say("SYSTEM", s)  # TODO: alert screen, and or give direct button to settings
            renpy.jump(fallback)
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
        if ".png" not in name:
            name += ".png"
        file_path = path_join(dir_base, name)
        return file_path
