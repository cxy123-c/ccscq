#1.获取client 对象
from openai import OpenAI
#2. 调用模型
client = OpenAI (
    api_key="sk-b76a9577ffb94f32899431f99679241e",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
response = client.chat.completions.create(
    model="qwen3-max",
    messages=[
        {"role":"system","content":"你是一个Python编程专家，并且话很多"},
        {"role":"assistant","content":"好的，我是编程专家，并且话不多，你还要问什么？"},
        {"role":"user","content":"输出1-10的数字，使用python代码"}
    ],
    stream=True     #开启流式输出的功能
)
#3.处理结果
for chunk in response:
    print(
        chunk.choices[0].delta.content,
        end=' ',        #每段之间以空格分隔
        flush=True          #立刻刷新缓冲区
    )