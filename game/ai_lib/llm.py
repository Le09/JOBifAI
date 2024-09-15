import json
import re
import requests

str_to_types = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
}

class RetryableError(Exception):
    pass

def transform_json_schema(short_schema):
    """
    Transform a JSON schema written in short notation to the standard JSON schema
    accepted by response_format.

    :param short_schema: A dictionary representing the short JSON schema
    :return: A dictionary representing the standard JSON schema
    """
    standard_schema = {"type": "json_object", "properties": {}}
    for key, value in short_schema.items():
        if ":" in value:
            # Handle "type:min<=key<=max" notation
            type_, constraint = value.split(":")
            min_max = constraint.split("<=")
            min_val = float(min_max[0])
            max_val = float(min_max[2])
            standard_schema["properties"][key] = {
                "type": type_,
                "minimum": min_val,
                "maximum": max_val
            }
        else:
            standard_schema["properties"][key] = {"type": value}
    return standard_schema


def ask_llm(*args, retries=3, **kwargs):
    result = None
    while not result:
        try:
            result = ask_llm_once(*args, **kwargs)
        except RetryableError:
            if retries:
                retries -= 1
            else:
                raise
    return result


def ask_llm_once(prompt, context=None, is_json=True, schema=None, model="llama3-8b-8192", full_schema=None, api_key=None, user_id="user"):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = [{"role": "user", "content": prompt}]
    if context:
        messages = [{"role": "system", "content": context}] + messages
    args = {
        "messages": messages,
        "model": model,
        "stream": False,
        "user": user_id,
    }
    if schema:
        full_schema = transform_json_schema(schema)
    if full_schema:
        args["response_format"] = full_schema
    response = requests.post(url, headers=headers, data=json.dumps(args))
    status = response.status_code
    if status != 200:
        if response.status_code not in [401, 403, 404]:
            raise RetryableError()
        else:
            response.raise_for_status()  # Raise an exception for HTTP errors
    try:
        result = response.json()["choices"][0]["message"]["content"]
        if is_json:
            result = parse_json_answer(result)
        if full_schema:
            full_schema["type"] = "object"  # yeah this is stupid
            # to check maximum and minimum constraints
            validate_json(relax_json_schema(result, full_schema), full_schema)
    except Exception as e:
        raise RetryableError(str(e))
    return result


def parse_json_answer(markdown_text):
    # sometimes the llm might just answer with a valid json, and json.loads work.
    # more commonly it answers with a json block inside.
    # the model might be unreliable so avoid anything that schema with non-zero depth
    json_block_pattern = re.compile(r"\{(.*?)\}", re.DOTALL)
    json_block_match = json_block_pattern.search(markdown_text)

    if not json_block_match:
        raise ValueError("No JSON block found in the text")
    json_block = json_block_match.group(0)
    d = json.loads(json_block)
    e = markdown_text[json_block_match.end():]  # might be empty
    d["explanation"] = e
    return d


def validate_json(json_data, schema):
    # raises if invalid
    # normally we would to that...
    # jsonschema.validate(instance=json_data, schema=schema)
    # but that depends on pydantic so it's a no-go
    for key, type_str in schema["properties"].items():
        v = json_data[key]
        assert isinstance(v, str_to_types[type_str["type"]])

def relax_json_schema(json_dict, full_schema):
    props = full_schema["properties"]
    for key, value in json_dict.items():
        if key in props:
            expected_type = props[key]["type"]
            if expected_type == "number" and isinstance(value, str):
                json_dict[key] = float(value)
            elif expected_type == "integer" and isinstance(value, str):
                json_dict[key] = int(value)
            elif expected_type == "boolean" and isinstance(value, str):
                json_dict[key] = value.lower() not in ["false", "0"]
            else:
                json_dict[key] = value
    return json_dict

if __name__ == "__main__":
    context = "You are a very rude and foul-mouthed employer. The day has been long and you're not on your best mood. You are about to reply to a message from an employee."
    prompt = "How rude is the following message? 'You do not seem to be the sharpest tool in the shed.' Give your answer as json with the key 'response' that is a sentence replying directly to the message, and the key 'score' be a number where 0 means completely harmless and 1 means extremely insulting."
    schema = {"response": "string", "score": "number:0<=min<=1"}
    response = ask_llm(prompt, context=context, schema=schema)
    print(response)
