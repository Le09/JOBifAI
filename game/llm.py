import json
import re
import requests
import jsonschema

# https://github.com/cheahjs/free-llm-api-resources
# GROQ

# https://llmpricecheck.com/
# https://novita.ai/model-api/pricing
# https://goose.ai/docs/api

# https://www.together.ai/pricing
# free tier: https://www.arliai.com/pricing

def send_to_llm(prompt):
    # TODO: get config from renpy.config
    url = configuration["url"]
    payload = {
        "prompt": prompt,
        "model": "gemma2",
        "stream": False,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def parse_json_answer(response, schema=None):
    markdown_text = response["response"]
    json_block_pattern = re.compile(r"```json(.*?)```", re.DOTALL)
    json_block_match = json_block_pattern.search(markdown_text)

    if not json_block_match:
        raise ValueError("No JSON block found in the Markdown text")
    json_block = json_block_match.group(1).strip()
    d = json.loads(json_block)
    e = (
        markdown_text[: json_block_match.start()]
        + markdown_text[json_block_match.end() :]
    )
    if schema:
        validate_json(d, schema)
    return d, e


def validate_json(json_data, schema):
    # raises if invalid
    jsonschema.validate(instance=json_data, schema=schema)
