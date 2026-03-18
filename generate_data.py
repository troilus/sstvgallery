import os
import json
import re
from datetime import datetime
from pathlib import Path

def extract_date_from_filename(filename):
    """从文件名中提取日期"""
    # 匹配格式：YYYY-MM-DD 或 YYYY.MM.DD
    match = re.search(r'(\d{4})[-./](\d{2})[-./](\d{2})', filename)
    if match:
        year, month, day = match.groups()
        return f'{year}-{month}-{day}'
    return None

def generate_gallery_data():
    base_dir = Path('webpimages')
    gallery_data = {}

    # 如果webpimages目录不存在，则创建它
    if not base_dir.exists():
        base_dir.mkdir(parents=True, exist_ok=True)

    # 遍历所有文件夹
    for folder in base_dir.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            images = []

            # 支持的图片格式
            image_extensions = {'.webp'}

            # 读取文件夹中的图片
            for file in folder.iterdir():
                if file.is_file() and file.suffix.lower() in image_extensions:
                    # 从文件名中提取日期
                    date_str = extract_date_from_filename(file.name)

                    # 如果文件名中没有日期，使用文件的修改时间
                    if not date_str:
                        stat = file.stat()
                        date_str = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')

                    images.append({
                        'name': file.stem,  # 使用文件名（不带扩展名）
                        'date': date_str,
                        'url': f'webpimages/{folder.name}/{file.name}',
                        'size': file.stat().st_size
                    })

            # 按日期从新到旧排序
            images.sort(key=lambda x: x['date'], reverse=True)

            if images:
                gallery_data[folder.name] = images
    
    # 确保data目录存在
    Path('data').mkdir(exist_ok=True)
    
    # 保存数据
    with open('data/gallery-data.json', 'w', encoding='utf-8') as f:
        json.dump(gallery_data, f, ensure_ascii=False, indent=2)
    
    print("Gallery data generated successfully!")

if __name__ == '__main__':
    generate_gallery_data()