import os
from PIL import Image, ImageEnhance, ImageFilter
import colorsys
import base64
import io

def process_wanted_photo():
    im = Image.open("source-photo.jpg")
    w, h = im.size
    
    # 1. Precise crop on head & shoulders (320:265 ratio = 1.2075)
    target_aspect = 320 / 265
    crop_w = 2800
    crop_h = int(crop_w / target_aspect)
    crop_x = (w - crop_w) // 2
    crop_y = int(h * 0.18)
    
    cropped = im.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
    
    # Resize to high-res target 640x530
    resized = cropped.resize((640, 530), Image.Resampling.LANCZOS)
    
    # 2. Warm parchment background replacement & color grading
    # Convert to RGB
    rgb_im = resized.convert("RGB")
    pixels = rgb_im.load()
    pw, ph = rgb_im.size
    
    # Parchment tone: base #E5CEB1 -> (229, 206, 177)
    for y in range(ph):
        # Vertical parchment gradient
        parch_r = int(232 - (y / ph) * 16)
        parch_g = int(210 - (y / ph) * 20)
        parch_b = int(182 - (y / ph) * 25)
        
        for x in range(pw):
            r, g, b = pixels[x, y]
            h_val, s_val, v_val = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            
            # Studio grey background: saturation is very low (< 0.14) and brightness > 150
            if s_val < 0.14 and v_val > 0.58:
                # Blend with parchment texture
                blend = min(1.0, max(0.0, (v_val - 0.58) / 0.25))
                # Soft transition
                nr = int(r * (1 - blend) + parch_r * blend)
                ng = int(g * (1 - blend) + parch_g * blend)
                nb = int(b * (1 - blend) + parch_b * blend)
                pixels[x, y] = (nr, ng, nb)
                
    # 3. Enhance contrast & warm tone
    enhancer = ImageEnhance.Contrast(rgb_im)
    contrasted = enhancer.enhance(1.15)
    
    color_enhancer = ImageEnhance.Color(contrasted)
    colored = color_enhancer.enhance(1.05)
    
    # Save test image
    colored.save("assets/wanted_portrait.jpg", quality=90)
    print("Saved assets/wanted_portrait.jpg")
    
    # Encode to base64
    buf = io.BytesIO()
    colored.save(buf, format="JPEG", quality=88)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    with open("data/wanted_photo_b64.txt", "w", encoding="utf-8") as f:
        f.write(b64)
    print("Saved data/wanted_photo_b64.txt, len:", len(b64))

if __name__ == "__main__":
    process_wanted_photo()
