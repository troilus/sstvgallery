import os
import json
from datetime import datetime
from pathlib import Path

def generate_gallery_data():
    base_dir = Path('images')
    webp_base_dir = Path('webpimages')
    gallery_data = {}
    
    # 遍历所有文件夹
    for folder in base_dir.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            images = []
            webp_folder = webp_base_dir / folder.name
            
            # 支持的图片格式（不包括webp，webp作为替代格式）
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
            
            # 读取文件夹中的图片
            for file in folder.iterdir():
                if file.is_file() and file.suffix.lower() in image_extensions:
                    # 获取文件修改时间
                    stat = file.stat()
                    date_str = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')
                    
                    # 检查是否存在对应的webp版本
                    webp_file = webp_folder / (file.stem + '.webp')
                    if webp_file.exists():
                        image_url = f'webpimages/{folder.name}/{webp_file.name}'
                        image_size = webp_file.stat().st_size
                    else:
                        image_url = f'images/{folder.name}/{file.name}'
                        image_size = stat.st_size
                    
                    images.append({
                        'name': file.name,
                        'date': date_str,
                        'url': image_url,
                        'size': image_size
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