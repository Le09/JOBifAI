
init python:
    import os
    import sys
    import uuid
    from ai_lib.llm import ask_llm
    from ai_lib.images import download_job_image, generate_job

    # disable moving through history with the scroll wheel
    # https://www.renpy.org/doc/html/keymap.html
    config.keymap['rollback'].remove('mousedown_4')
    config.keymap['rollforward'].remove('mousedown_5')

    def askllm(state, prompt, schema):
        return retry(state, ask_llm, {"api_key":persistent.groq_api_key, "prompt": prompt, "schema": schema})

    def download_image(job_id, file_path, api_key):
        renpy.invoke_in_thread(download_job_image, job_id, file_path, api_key)

    def escape_text(text):
        return text.replace("{", "{{").replace("[", "[[").replace("}", "}}").replace("]", "]]")

    def retry(fallback, function, kwargs):
        try:
            return function(**kwargs)
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
        return renpy.exists(os.path.join("images", image_name))

    def create_folder(*args):
        dir_base = renpy.config.basedir
        full_path = os.path.join(dir_base, "game", *args)
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
            new_name = os.path.join(*folders, new_name)
        return new_name

    def img_full_path(name, images=True):
        dir_base = os.path.join(renpy.config.basedir, "game")
        if not images:
            dir_base = os.path.join(dir_base, "images")
        if ".png" not in name:
            name += ".png"
        file_path = os.path.join(dir_base, name)
        return file_path
