from PIL import Image
from pathlib import Path
import os

def convert_images_to_webp():
    """将images目录中的所有图片转换为WebP格式，保存到webpimages目录"""
    images_dir = Path('images')
    webp_dir = Path('webpimages')

    # 确保webpimages目录存在
    webp_dir.mkdir(exist_ok=True)

    # 支持的源图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

    total_converted = 0

    # 遍历images目录中的所有文件夹
    for folder in images_dir.iterdir():
        if folder.is_dir() and not folder.name.startswith('.'):
            # 创建对应的webp文件夹
            webp_folder = webp_dir / folder.name
            webp_folder.mkdir(exist_ok=True)

            # 遍历文件夹中的图片
            for file in folder.iterdir():
                if file.is_file() and file.suffix.lower() in image_extensions:
                    webp_file = webp_folder / (file.stem + '.webp')

                    # 如果webp文件不存在，或者源文件比webp文件新，则转换
                    if not webp_file.exists() or file.stat().st_mtime > webp_file.stat().st_mtime:
                        try:
                            # 打开图片并转换为WebP
                            with Image.open(file) as img:
                                # 转换为RGB模式（如果图片是RGBA或P模式）
                                if img.mode in ('RGBA', 'P'):
                                    img = img.convert('RGB')

                                # 保存为WebP格式，质量设置为85
                                img.save(webp_file, 'WEBP', quality=85, method=6)

                                # 保留原始文件的修改时间
                                import os
                                original_mtime = file.stat().st_mtime
                                os.utime(webp_file, (original_mtime, original_mtime))

                                total_converted += 1
                                print(f"转换: {file} -> {webp_file}")
                        except Exception as e:
                            print(f"转换失败 {file}: {e}")

    print(f"\n总共转换了 {total_converted} 张图片为WebP格式")

if __name__ == '__main__':
    convert_images_to_webp()