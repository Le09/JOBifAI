import requests
import time


def generate_job(prompt, api_key):
    url = "https://api.prodia.com/v1/sdxl/generate"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": api_key,
    }
    payload = {"prompt": prompt}
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["job"]


def get_job_image_url(job_id, api_key):
    url = f"https://api.prodia.com/v1/job/{job_id}"
    headers = {
        "accept": "application/json",
        "X-Prodia-Key": api_key,
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    while result["status"] not in ['succeeded', 'failed']:
        time.sleep(1)  # wait 1 second
        response = requests.get(url, headers=headers)
        result = response.json()
    return result["imageUrl"]


def download_job_image(job_id, file_path, api_key):
    image_url = get_job_image_url(job_id, api_key)
    response = requests.get(image_url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
