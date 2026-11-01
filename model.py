import json
import os
import urllib.request

KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = "claude-haiku-5-5"

def ask(question):
    body = {
        "model": MODEL,
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": question}],
    }
    request = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(body).encode(),
        headers={
            "x-api-key": KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )

    with urllib.request.urlopen(request) as response:
        answer = json.loads(response.read())

    text = ""
    for block in answer["content"]:
        if block["type"] == "text":
            text = text + block["text"]
    return text.strip()
