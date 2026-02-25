import os
import config_data as config
import hashlib

def check_md5(md5_str: str):
    # 检查传入的md5字符串是否被处理过了
    # return False(md5未处理过) True （已经处理过，已经有记录了）
    if not os.path.exists(config.md5_path):
        # if进入表示文件不存在
        open(config.md5_path,'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
    pass 

def save_md5(md5_str: str):
    # 将传入的md5字符串记录到文件内保存
    with open(config.md5_path,'a',encoding='utf-8') as f:
        f.write(md5_str + '\n')



def get_string_md5(input_str: str,encoding='utf-8'):
    # 将传入的字符串转换成md5字符串
    #将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)
    # 创建md5对象
    md5_obj  = hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()

    return md5_hex

class KnowledgeBaseService(object):

    def __init__(self):
        self.chroma = None
        self.spliter = None

    def upload_by_str(self,data,filename):
        pass

if __name__ =='__main__':
    save_md5('7a8941058aaf4df5147042ce104568da')
    print(check_md5("7a8941058aaf4df5147042ce104568da"))
    # r1 = get_string_md5("周杰伦")
    # r2 = get_string_md5("周杰伦1")
    # r3 = get_string_md5("周杰伦2")

    # print(r1)
    # print(r2)
    # print(r3)
