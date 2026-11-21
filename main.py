import os
from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()
api_key = os.getenv("OPEN_ROUTER_KEY")
if not api_key:
    raise ValueError("You don t have an API KEY")
client = OpenAI(api_key=api_key,base_url = "https://openrouter.ai/api/v1")
usage = {"prompt_tokens":0,"completion_token":0,"total_token":0,"model":None}
# response = client.chat.completions.create(
#     model = "openrouter/free",
#     messages=[
#         {
#             "role":"user",
#             "content":"How can i be a better person"
#         }
#     ]
# )
def load_memory(file_path):
    if os.path.exists(file_path):
        with open(file_path,"r") as f:
            return json.load(f)
    return []
def save_memory(file_path,memory):
    with open(file_path,"w") as f:
        json.dump(memory,f)
history = load_memory("memory.json")
while True:
    message = input(">> ")
    if message.startswith("/exit"):
        save_memory("memory.json",history)
        break
    history.append({
        "role":"user",
        "content":message
    })
    stream = client.chat.completions.create(
        model = "openrouter/free",
        messages=history,
        stream=True
    )
    response = []
    for chunk in stream:
        if chunk.choices:
            if chunk.usage:
                usage["completion_token"]+=chunk.usage.completion_tokens
                usage["prompt_tokens"]+=chunk.usage.prompt_tokens
                usage["total_token"]+=chunk.usage.total_tokens
                usage["model"] = chunk.model
            content = chunk.choices[0].delta.content
            if content:
                print(content,end ="")
                response.append(content)
    full_response = "".join(response)
    history.append({
        "role":"assistant",
        "content":full_response
    })
    print()


