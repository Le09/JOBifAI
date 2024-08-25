
init python:
    # create venv called llenaige in 3.9, in game folder
    import os
    import sys
    import uuid
    path_venv = "~/.virtualenvs/llenaige/lib/python3.9/site-packages/"
    sys.path.append(os.path.expanduser(path_venv))
    from ai_lib.llm import ask_llm
    from ai_lib.images import download_job_image, generate_job
    # config = {"groq_api_key": settings_api_key}
    def retry(fallback, function, kwargs):
        try:
            return function(**kwargs)
        except Exception as e:
            # TODO: more robust error handling
            if "body" in dir(e) and "error" in e.body:
                se = "Error: %s\n" % e.body["error"]["message"]
                se += "Justification: %s\n" % e.body["error"]["failed_generation"]
            else:
                se = e.message if "message" in dir(e) else str(e)
            s = "%s\n\n The operation failed. Do you want to retry?" % se
            again = renpy.confirm(s)
            if again:
                return retry(fallback, function, kwargs)
            else:
                renpy.jump(fallback)

    def exists_img(image_name):
        return renpy.exists(os.path.join("images", image_name))

    def get_random_object_name(base_name):
        name, ext = os.path.splitext(base_name)
        new_name = name + str(uuid.uuid4()).replace("-", "_")
        return new_name + ext  # ext would be "" or ".ext"

    def img_full_path(name):
        dir_base = renpy.config.basedir
        dir_images = os.path.join(dir_base, "game", "images")
        if ".png" not in name:
            name += ".png"
        file_path = os.path.join(dir_images, name)
        return file_path
