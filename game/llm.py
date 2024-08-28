import json
import jsonschema
import re

from groq import Groq


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


def ask_llm(prompt, context=None, is_json=True, schema=None, model="llama3-8b-8192", full_schema=None):
    api_key = "GROQ_API_KEY"  # TODO: get from configuration
    client = Groq(api_key=api_key)
    messages = [{"role": "user", "content": prompt}]
    if context:
        messages = [{"role": "system", "content": context}] + messages
    args = {
        "messages": messages,
        "model": model,
        "stream": False,
    }
    if schema:
        full_schema = transform_json_schema(schema)
    if full_schema:
        args["response_format"] = full_schema
    chat_completion = client.chat.completions.create(**args)
    result = chat_completion.choices[0].message.content
    if is_json:
        result = parse_json_answer(result)
    if full_schema:
        full_schema["type"] = "object"  # yeah this is stupid
        # to check maximum and minimum constraints
        validate_json(result, full_schema)
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
    jsonschema.validate(instance=json_data, schema=schema)


if __name__ == "__main__":
    context = "You are a very rude and foul-mouthed employer. The day has been long and you're not on your best mood. You are about to reply to a message from an employee."
    prompt = "How rude is the following message? 'You do not seem to be the sharpest tool in the shed.' Give your answer as json with the key 'response' that is a sentence replying directly to the message, and the key 'score' be a number where 0 means completely harmless and 1 means extremely insulting."
    schema = {"response": "string", "score": "number:0<=min<=1"}
    response = ask_llm(prompt, context=context, schema=schema)
    print(response)
