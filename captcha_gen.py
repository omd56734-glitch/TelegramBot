import random
import string
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def generate_captcha():
    # শুধুমাত্র ৪ ডিজিটের সংখ্যা
    captcha_text = ''.join(random.choices(string.digits, k=4))
    width, height = 200, 70
    image = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(image)
    
    for _ in range(80):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
    for _ in range(4):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([start, end], fill=(150, 150, 150), width=2)

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    draw.text((60, 20), captcha_text, fill=(20, 20, 20), font=font)
    
    bio = BytesIO()
    image.save(bio, 'PNG')
    bio.seek(0)
    
    return captcha_text, bio
