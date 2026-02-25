import requests
import json
import base64
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from openai import OpenAI

def get_img_data(image_path):
    with open(image_path, "rb") as image_file:
        # 读取文件并转换为Base64
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    # 设置图像格式
    image_format = "png"  # 根据实际情况修改，比如jpg、bmp 等
    image_data = f"data:image/{image_format};base64,{base64_image}"
    return image_data

def multimodel_emb(key, input):
    url = "https://qianfan.baidubce.com/v2/embeddings"

    payload = json.dumps({
        "model": "gme-qwen2-vl-2b-instruct",
        "input":input
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response

def get_answer(image_path, key, label):
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    qianfan_url = "https://qianfan.baidubce.com/v2"

    client = OpenAI(api_key=key, base_url=qianfan_url)
    model_name = 'ernie-4.5-turbo-vl-preview'

    base64_image = encode_image(image_path)

    # 提交信息至GPT4o
    response = client.chat.completions.create(
        model=model_name,  # 选择模型
        messages=[
            {
                "role": "system",
                "content": "你是一位专业的内镜医生."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"这是医生给这张图片的描述：{label}，请你根据医生描述再描述这张图片"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ]
            }
        ],
        stream=True,
    )

    reply = ""
    for res in response:
        content = res.choices[0].delta.content
        if content:
            reply += content

    return reply


if __name__ == '__main__':
    key = "bce-v3/ALTAK-WH5U3w7bjJIFZHgZYGLH3/60a555f12897de78b018b2a956b804df198876ce"

    # 对第3张图片嵌入
    image_path = "3_胃体胆汁反流并灰白色隆起.png"
    image_data = get_img_data(image_path)
    my_input_3 = [
            {
                "text": "胃镜倒镜观察胃底，胃内见胆汁反流，灰白色黏膜范围扩大至胃体部",
                "image": image_data
            }
        ]
    response = multimodel_emb(key, my_input_3)
    emb_3 = json.loads(response.text)['data'][0]['embedding']

    # 对第4张图片嵌入
    image_path = "4_正常胃底.png"
    image_data = get_img_data(image_path)
    my_input_4 = [
            {
                "text": "胃镜倒镜观察胃底，这是一张正常的胃底图",
                "image": image_data
            }
        ]
    response = multimodel_emb(key, my_input_4)
    emb_4 = json.loads(response.text)['data'][0]['embedding']

    # 输入问题
    my_query = [
            {
                "text": "胃底胆汁反流的内镜下表现",
            }
        ]
    response = multimodel_emb(key, my_query)
    emb_query = json.loads(response.text)['data'][0]['embedding']

    # 进行向量匹配
    vectors = np.array([
        emb_query,
        emb_3,
        emb_4
    ])
    similarity_matrix = cosine_similarity(vectors)
    print(similarity_matrix)

    # 结果：emb_3和emb_query的相似度为0.8，所以 '3_胃体胆汁反流并灰白色隆起.png'这张图片就是检索到的图片
    # [[1.         0.80715132 0.61011071]
    #  [0.80715132 1.         0.7486741 ]
    #  [0.61011071 0.7486741  1.        ]]


    '''
    进行增强回答
    '''
    image_path = "data/pic/3_胃体胆汁反流并灰白色隆起.png"
    label = my_input_3[0]['text']
    result = get_answer(image_path, key, label)


    print(result)