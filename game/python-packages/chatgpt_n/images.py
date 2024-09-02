import requests
from prodiapy import Prodia


def generate_images_data_job(prompt, object_name):
    # ideally, we split this in two functions,
    # one for generating the job and another for downloading the image
    # so when we start the game, we launch all jobs
    # and then we download all images at chapter end
    # we might need to store the intermediary data though
    api_key = "YOUR_PRODIA_KEY"  # TODO: get from configuration
    prodia = Prodia(api_key=api_key)
    job = prodia.sdxl.generate(prompt=prompt)
    # job is a dict with the keys 'job' and 'status'
    # job == {'job': 'a3d249df-4351-48df-ba54-ff9b0672785e', 'status': 'queued'}
    result = prodia.wait(job)
    # result, however, is an object...
    image_url = result.image_url
    response = requests.get(image_url)
    file_name = object_name + ".png"
    with open(file_name, 'wb') as file:
        file.write(response.content)

