import os
import json
from datetime import datetime
from pathlib import Path

def generate_gallery_data():
    base_dir = Path('images')
    gallery_data = {}
    
    # 遍历所有文件夹
    for folder in base_dir.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            images = []
            
            # 支持的图片格式
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
            
            # 读取文件夹中的图片
            for file in folder.iterdir():
                if file.is_file() and file.suffix.lower() in image_extensions:
                    # 获取git提交时间作为"创建时间"
                    stat = file.stat()
                    images.append({
                        'name': file.name,
                        'date': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d'),
                        'url': f'images/{folder.name}/{file.name}',
                        'size': stat.st_size
                    })
            
            # 按日期排序
            images.sort(key=lambda x: x['date'])
            
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