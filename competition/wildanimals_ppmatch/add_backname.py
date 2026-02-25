"""给train.txt/val.txt每行添加图片后缀（.jpg/.png）"""
import os

def add_img_suffix(file_path, suffix=".jpg"):
    # 备份原文件
    backup_path = file_path + ".suffix.bak"
    os.rename(file_path, backup_path)
    print(f"已备份原文件到：{backup_path}")
    
    # 读取并修改
    with open(backup_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 拆分原行（图片名 类别名）
        parts = line.split()
        if len(parts) == 2:
            img_name, cls_name = parts
            # 给图片名加后缀
            img_name += suffix
            new_line = f"{img_name} {cls_name}\n"
        else:
            new_line = line + "\n"
        new_lines.append(new_line)
    
    # 写入新文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"处理完成！{file_path} 已添加{suffix}后缀")

# 配置你的文件路径
if __name__ == "__main__":
    file_paths = [
        r"C:\Users\ZLSHLT2601004\try_dlam\competition\wildanimals_ppmatch\animals\data\ImageSets\Main\train.txt",
        # r"C:\Users\ZLSHLT2601004\try_dlam\competition\wildanimals_ppmatch\animals\data\ImageSets\Main\val.txt"
    ]
    # 如果你的图片是.png，改成suffix=".png"
    for path in file_paths:
        add_img_suffix(path, suffix=".jpg")