import os
import requests
from prodiapy import Prodia


def generate_job(prompt, api_key):
    prodia = Prodia(api_key=api_key)
    job = prodia.sdxl.generate(prompt=prompt)
    return job["job"]


def download_job_image(job_id, file_path, api_key):
    job = {'job': job_id, 'status': 'queued'}
    prodia = Prodia(api_key=api_key)
    result = prodia.wait(job)
    image_url = result.image_url
    response = requests.get(image_url)
    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_job_image_url(job_id, api_key):
    job = {'job': job_id, 'status': 'queued'}
    prodia = Prodia(api_key=api_key)
    result = prodia.wait(job)
    return result.image_url
