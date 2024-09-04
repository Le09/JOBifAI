import os
import requests
from prodiapy import Prodia
import uuid


def get_random_object_name(base_name):
    name, ext = os.path.splitext(base_name)
    new_name = name + str(uuid.uuid4()).replace("-", "_")
    return new_name + ext  # ext would be "" or ".ext"


def generate_images_data_job(prompt, name, api_key=None, renpy=None):
    # ideally, we split this in two functions,
    # one for generating the job and another for downloading the image
    # so when we start the game, we launch all jobs
    # and then we download all images at chapter end
    # we might need to store the intermediary data though
    prodia = Prodia(api_key=api_key)
    job = prodia.sdxl.generate(prompt=prompt)
    # job is a dict with the keys 'job' and 'status'
    # job == {'job': 'a3d249df-4351-48df-ba54-ff9b0672785e', 'status': 'queued'}
    result = prodia.wait(job)
    # result, however, is an object...
    image_url = result.image_url
    response = requests.get(image_url)
    dir_base = renpy.config.basedir
    dir_images = os.path.join(dir_base, "game", "images")
    if ".png" not in name:
        name += ".png"
    file_path = os.path.join(dir_images, name)
    with open(file_path, 'wb') as file:
        file.write(response.content)

