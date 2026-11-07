import os
from PIL import Image, ImageSequence

def make_transparent(input_path, output_path, bg_color_check, tolerance=40):
    im = Image.open(input_path)
    frames = []
    durations = []
    disposals = []
    
    for frame in ImageSequence.Iterator(im):
        durations.append(frame.info.get('duration', 100))
        disposals.append(2)  # clear to background
        
        rgba = frame.convert('RGBA')
        datas = rgba.getdata()
        
        new_data = []
        for item in datas:
            # item is (r, g, b, a)
            if bg_color_check(item):
                new_data.append((0, 0, 0, 0))
            else:
                new_data.append(item)
                
        rgba.putdata(new_data)
        frames.append(rgba)
        
    if frames:
        # Save as animated transparent GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            optimize=False,
            duration=durations,
            loop=0,
            disposal=2,
            transparency=0
        )
        print(f"Saved transparent GIF: {output_path} ({len(frames)} frames)")

# 1. Chopper happy: background is pale yellow/green (R > 200, G > 200, B > 180, and R close to G)
def is_chopper_bg(pixel):
    r, g, b, a = pixel
    return r > 210 and g > 230 and b > 180

# 2. Luffy chibi: background is pure white / off-white (R > 240, G > 240, B > 240)
def is_white_bg(pixel):
    r, g, b, a = pixel
    return r > 240 and g > 240 and b > 240

make_transparent("assets/chopper-happy.gif", "assets/chopper-transparent.gif", is_chopper_bg)
make_transparent("assets/luffy-chibi.gif", "assets/luffy-transparent.gif", is_white_bg)
