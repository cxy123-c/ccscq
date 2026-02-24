

import json
d = {
    "name":"周杰伦",
    "age":11,
    "gender":"男",
}

#json.dumps(字典或列表，ensure_ascil=False); 
# ensure_ascii确保中文能正常显示，返回值：json字符串
s = json.dumps(d,ensure_ascii=False)
print(s)

l = [
    {
    "name":"周杰",
    "age":21,
    "gender":"男",
},
{
    "name":"杰伦",
    "age":31,
    "gender":"男",
},
{
    "name":"杰",
    "age":1,
    "gender":"男",
}
]

print(json.dumps(l,ensure_ascii=False))


json_str='{"name": "周杰伦", "age": 11, "gender": "男"}'
json_array_str='[{"name": "周杰", "age": 21, "gender": "男"}, {"name": "杰伦", "age": 31, "gender": "男"}, {"name": "杰", "age": 1, "gender": "男"}]'


#json.loads（json字符串），返回值：python字典 或 python列表
res_dict = json.loads(json_str)
print(res_dict, type(res_dict))

res_list = json.loads(json_array_str)

print(res_list, type(res_list))