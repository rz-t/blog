import re
import string
import random
from PIL import Image, ImageFont, ImageDraw, ImageFilter

def gen_vcode():
    optional = string.digits + string.ascii_letters
    # 去掉0oil
    optional = re.sub(r'[0oil]', '', optional, flags=re.RegexFlag.I)

    # 图片大小130x50
    width = 120
    height = 60

    image = Image.new('RGB', (width, height), 'white')

    # 设置字体
    font = ImageFont.truetype('FreeSans', 40)
    # 创建draw对象
    draw = ImageDraw.Draw(image)
    text = ''
    for item in range(4):
        _ = random.choice(optional)
        text += _
        draw.text((4 + random.randint(4, 7) + 20*item, 5 + random.randint(3, 7)), text=_, fill='black', font=font)

    # 干扰线
    for num in range(8):
        x1 = random.randint(0, width/2)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height/2)
        y2 = random.randint(height/2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)
    
    return image.filter(ImageFilter.FIND_EDGES), text
