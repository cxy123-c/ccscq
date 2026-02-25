# pip install openai
from openai import OpenAI

client = OpenAI(
    api_key="f6983782ce03f1372d7aea699a26a3e9f668ed14",
    base_url="https://api-fdk9ibp3l0meo7k9.aistudio-app.com/v1"
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