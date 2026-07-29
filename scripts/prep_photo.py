import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_photo(input_path, output_path="source-prepped.png"):
    # 1. Background removal
    with open(input_path, "rb") as f:
        img_bytes = f.read()
    no_bg_bytes = remove(img_bytes)

    nparr = np.frombuffer(no_bg_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    # Convert to grayscale
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
        gray = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)
        gray[alpha == 0] = 255
    else:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Boost local contrast via CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)

    cv2.imwrite(output_path, enhanced)
    print(f"Prepped image saved to {output_path}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(src)