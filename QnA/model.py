import tiktoken
from .similarity_search import similarity_search
from .promt_template import info_context, system_prompt, user_prompt
from config import Config
import json
import os
import ssl
import requests
import sys
sys.path.append("..")
# import token size calculation function


def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


ROLE = "user" if Config.PHI3_LOCATION == "azure" else "system"
print(ROLE)

def format_message(message):

    # get the last 2 messages from the user and last 2 message of the assistant
    req_message = []
    req_message.append({
        "role": ROLE,
        "content": system_prompt.format(
            guardian_name=Config.GUARDIAN_NAME,
            children_name=Config.STUDENT_NAME,
            school_name=Config.SCHOOL_NAME
        )
    })

    max_conversation_to_feed = 1
    prev = -(max_conversation_to_feed * 2 + 1)
    context = message[prev:]
    for msg in context:
        req_message.append({
            "role": msg["role"],
            "content": msg["content"][0]["text"]
        })
    query = context[-1]["content"][0]["text"]
    # delete the last message from the req_message
    req_message.pop()
    context = similarity_search(query)
    req_message.append({
        "role": ROLE,
        "content": info_context.format(
            context=similarity_search(
                query) if context else "No context found"
        )
    })
    req_message.append({
        "role": "user",
        "content": user_prompt.format(
            query=query
        )
    })

    return req_message


def phi3(message, max_tokens=1024, temperature=0.7, top_p=1):
    allowSelfSignedHttps(True)
    print(Config.PHI3_LOCATION)

    messages = format_message(message)
    content_for_slm = ""

    if Config.PHI3_LOCATION == 'local' or Config.PHI3_LOCATION == 'port':
        url = "http://localhost:11434/api/chat/"
        data = {
            "model": "phi3",
            "messages": messages,
            "stream": False
        }
        with open("./queries/req_message_to_phi3.json", "w") as f:
            json.dump(data, f, indent=4)

        try:
            body = json.dumps(data)
            req = requests.post(url, data=body)
            response = req.json()
            with open("./queries/resp_from_phi3.json", "w") as f:
                json.dump(response, f, indent=4)

            for x in messages:
                content_for_slm += x["content"] + " "
            content_for_slm += response.get("message").get("content")

            token_size = len(content_for_slm)

            # make array in json and store token size for calculation of available tokens
            with open("./queries/token_size.json", "r") as f:
                # do not delete existing data in token_size.json
                try:
                    token_size_data = json.load(f)
                except:
                    token_size_data = []

            with open("./queries/token_size.json", "w") as f:
                token_size_data.append(token_size)
                json.dump(token_size_data, f, indent=4)

            return response.get("message").get("content")
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""

    if Config.PHI3_LOCATION == 'azure':
        data = {
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
        with open("./queries/req_message_to_phi3.json", "w") as f:
            json.dump(data, f, indent=4)
        url = "https://gpt-4-sahillede.openai.azure.com/openai/deployments/GPT/chat/completions?api-version=2023-03-15-preview"
        api_key = Config.AZURE_OPENAI_GPT4_API_KEY

        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        headers = {
            'Content-Type': 'application/json',
            'api-key': f'{api_key}'
        }

        try:
            body = json.dumps(data)
            req = requests.post(url, headers=headers, data=body)
            response = req.json()
            with open("./queries/resp_from_phi3.json", "w") as f:
                json.dump(response, f, indent=4)
            return response.get("choices")[0].get("message").get("content")
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""
