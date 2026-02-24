import os
import random
import shutil
from pathlib import Path

def split_wildlife_dataset(
    dataset_root, 
    train_ratio=0.8, 
    random_seed=42,
    image_format=['.jpg', '.jpeg', '.png'],
    annotation_format='.xml'
):
    """
    将野生动物检测数据集按比例拆分为训练集和测试集
    :param dataset_root: 数据集根目录（需包含JPEGImages和Annotations文件夹）
    :param train_ratio: 训练集比例（默认0.8）
    :param random_seed: 随机种子（保证拆分结果可复现）
    :param image_format: 支持的图片格式
    :param annotation_format: 标注文件格式（VOC为.xml）
    :return: 拆分完成，生成ImageSets/Main/train.txt和test.txt
    """
    # 1. 设置随机种子，保证结果可复现
    random.seed(random_seed)
    
    # 2. 定义路径
    image_dir = os.path.join(dataset_root, "Images")
    anno_dir = os.path.join(dataset_root, "xml")
    output_dir = os.path.join(dataset_root, "ImageSets", "Main")
    os.makedirs(output_dir, exist_ok=True)  # 创建输出目录
    
    # 3. 获取所有图片文件，并过滤出有对应标注的文件
    image_files = []
    for file in os.listdir(image_dir):
        # 过滤图片格式
        if Path(file).suffix.lower() in image_format:
            # 获取无后缀的文件名
            file_name = os.path.splitext(file)[0]
            # 检查是否有对应的标注文件
            anno_file = os.path.join(anno_dir, file_name + annotation_format)
            if os.path.exists(anno_file):
                image_files.append(file_name)
            else:
                print(f"警告：{file} 缺少对应的标注文件，已跳过")
    
    # 4. 数据校验
    if len(image_files) == 0:
        raise ValueError("未找到有效数据！请检查图片和标注文件路径是否正确")
    
    print(f"共找到 {len(image_files)} 个有效数据样本")
    
    # 5. 随机打乱数据
    random.shuffle(image_files)
    
    # 6. 按比例拆分
    split_idx = int(len(image_files) * train_ratio)
    train_files = image_files[:split_idx]
    test_files = image_files[split_idx:]
    
    print(f"拆分完成：训练集 {len(train_files)} 个样本，测试集 {len(test_files)} 个样本")
    
    # 7. 生成train.txt和test.txt文件
    # 训练集
    with open(os.path.join(output_dir, "train.txt"), 'w', encoding='utf-8') as f:
        f.write('\n'.join(train_files))
    
    # 测试集
    with open(os.path.join(output_dir, "test.txt"), 'w', encoding='utf-8') as f:
        f.write('\n'.join(test_files))
    
    # 可选：生成val.txt（和test.txt共用，新手可直接复用）
    with open(os.path.join(output_dir, "val.txt"), 'w', encoding='utf-8') as f:
        f.write('\n'.join(test_files))
    
    print(f"文件生成完成！路径：{output_dir}")
    print("生成的文件：train.txt, test.txt, val.txt")
    
    return {
        "训练集数量": len(train_files),
        "测试集数量": len(test_files),
        "文件路径": output_dir
    }

# ====================== 示例使用 ======================
if __name__ == "__main__":
    # 配置你的数据集路径
    DATASET_ROOT = r"C:\Users\ZLSHLT2601004\try dlam\__pycache__\wildanimals_ppmatch\animals\data"  # 替换为你的数据集根目录
    
    # 执行拆分
    try:
        result = split_wildlife_dataset(
            dataset_root=DATASET_ROOT,
            train_ratio=0.8,  # 80%训练集，20%测试集
            random_seed=42    # 固定随机种子，保证每次拆分结果一致
        )
        print("\n拆分结果汇总：")
        print(f"- 训练集：{result['训练集数量']} 个样本")
        print(f"- 测试集：{result['测试集数量']} 个样本")
        print(f"- 生成文件路径：{result['文件路径']}")
        
    except Exception as e:
        print(f"拆分失败：{e}")