from PIL import Image, ImageDraw, ImageFont
import os

# 创建一个简单的图标
icon_size = (64, 64)
image = Image.new('RGBA', icon_size, (255, 255, 255, 255))
draw = ImageDraw.Draw(image)

# 绘制背景渐变
for y in range(icon_size[1]):
    r = int(200 - (y / icon_size[1]) * 50)
    g = int(220 - (y / icon_size[1]) * 30)
    b = int(255 - (y / icon_size[1]) * 50)
    draw.line([(0, y), (icon_size[0], y)], fill=(r, g, b, 255))

# 绘制提示词相关的图标元素
# 绘制一个对话气泡
bubble_points = [(10, 20), (50, 20), (50, 40), (35, 40), (30, 45), (25, 40), (10, 40)]
draw.polygon(bubble_points, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)

# 绘制文本"提示"
try:
    # 尝试使用系统字体
    font = ImageFont.truetype("arial.ttf", 12)
    draw.text((15, 25), "提示", fill=(0, 0, 0, 255), font=font)
except:
    # 如果没有arial字体，使用默认字体
    draw.text((15, 25), "提示", fill=(0, 0, 0, 255))

# 绘制一个播放按钮（三角形）
triangle_points = [(40, 30), (50, 35), (40, 40)]
draw.polygon(triangle_points, fill=(0, 128, 255, 255), outline=(0, 0, 0, 255), width=1)

# 保存为ico文件
icon_path = "icon.ico"
image.save(icon_path, format='ICO')

print(f"图标已生成: {os.path.abspath(icon_path)}")