"""
功能：批量修改VOC数据集列表文件（train.txt/val.txt）
将单行格式（如wolf009）改为双行格式（wolf009 wolf）
自动识别文件名前缀作为类别名，也可自定义类别映射
"""
import os

def add_class_suffix(file_path, class_mapping=None):
    """
    处理单个列表文件
    :param file_path: 要修改的文件路径（如train.txt）
    :param class_mapping: 类别映射字典（可选），例：{'wf': 'wolf', 'dg': 'dog'}
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：文件 {file_path} 不存在！")
        return
    
    # 读取原文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 处理每一行
    new_lines = []
    for line in lines:
        line = line.strip()  # 去除换行符/空格
        if not line:  # 跳过空行
            continue
        
        # 步骤1：提取文件名前缀（字母部分）作为类别名
        class_name = ""
        for i, char in enumerate(line):
            if char.isdigit():  # 找到第一个数字的位置，前面的就是类别前缀
                class_name = line[:i]
                break
        # 如果没找到数字（全字母），用整个文件名作为类别
        if not class_name:
            class_name = line
        
        # 步骤2：如果有自定义类别映射，替换类别名
        if class_mapping and class_name in class_mapping:
            class_name = class_mapping[class_name]
        
        # 步骤3：拼接新行（原内容 + 空格 + 类别名）
        new_line = f"{line} {class_name}\n"
        new_lines.append(new_line)
    
    # 写入修改后的内容（覆盖原文件，会自动备份）
    # 先备份原文件
    backup_path = file_path + ".bak"
    os.rename(file_path, backup_path)
    print(f"已备份原文件到：{backup_path}")
    
    # 写入新内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"处理完成！文件 {file_path} 共修改 {len(new_lines)} 行")

# ====================== 自定义配置（根据你的数据集修改） ======================
if __name__ == "__main__":
    # 1. 配置要处理的文件路径（改成你的实际路径）
    file_paths = [
        r"C:\Users\ZLSHLT2601004\try_dlam\competition\wildanimals_ppmatch\animals\data\ImageSets\Main\train.txt",
        r"C:\Users\ZLSHLT2601004\try_dlam\competition\wildanimals_ppmatch\animals\data\ImageSets\Main\val.txt"
    ]
    
    # 2. 可选：自定义类别映射（如果前缀和类别名不一致时用）
    # 例：如果文件名是wf009，想映射为wolf，就写 {'wf': 'wolf'}
    custom_class_mapping = {
        # 'wf': 'wolf',
        # 'dg': 'dog',
        # 'br': 'bird'
    }
    
    # 3. 批量处理文件
    for file_path in file_paths:
        add_class_suffix(file_path, custom_class_mapping)
    
    print("\n所有文件处理完成！")