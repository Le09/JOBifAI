
init python:
    # create venv called llenaige in 3.9, in game folder
    import os
    import sys
    import uuid
    path_venv = "~/.virtualenvs/llenaige/lib/python3.9/site-packages/"
    sys.path.append(os.path.expanduser(path_venv))
    import asyncio
    import requests
    import aiohttp
    import ssl
    import certifi
    from ai_lib.llm import ask_llm
    from ai_lib.images import download_job_image, generate_job, get_job_image_url

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

    def download_image(job_id, file_path, api_key):
        if renpy.platform == "web":  # HTML5 does not support async
            download_job_image(job_id=job_id, file_path=file_path, api_key=api_key)
        else:
            url = get_job_image_url(job_id=job_id, api_key=api_key)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(download_image_async(url, file_path))
            #renpy.run(renpy.loader.run_async(download_image_async(url, save_as)))

    async def download_image_async(url, file_path):
        # https://docs.aiohttp.org/en/stable/client_advanced.html
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.get(url) as response:
                with open(file_path, 'wb') as file:
                    file.write(await response.read())
