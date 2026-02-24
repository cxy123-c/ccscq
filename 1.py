# pip install openai
from openai import OpenAI

client = OpenAI(
    api_key="",
    base_url=""
)

completion = client.chat.completions.create(
    model="default",
    temperature=0.6,
    messages=[
        {"role": "user", "content": "你好，请你扮演大雄"}
    ],
    stream=True
)

for chunk in completion:
    if hasattr(chunk.choices[0].delta, "reasoning_content") and chunk.choices[0].delta.reasoning_content:
        print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
    else:
        print(chunk.choices[0].delta.content, end="", flush=True)
       