from paddleocr import PPStructureV3
from pdf2image import convert_from_path
import os
import cv2
import numpy as np

def remove_red(img, output_file_path):
    img.save("page_17.png")
    img_rgb = np.array(img)       # numpy, RGB, uint8

    # RGB -> HSV（注意：不是 BGR）
    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

    # 红色两个区间
    lower_red_1 = np.array([0, 70, 50])
    upper_red_1 = np.array([10, 255, 255])
    lower_red_2 = np.array([170, 70, 50])
    upper_red_2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    kernel = np.ones((5, 5), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    # 用 numpy 数组来做赋值
    result_rgb = img_rgb.copy()
    result_rgb[red_mask > 0] = (255, 255, 255)

    # cv2.imwrite 需要 BGR，先转一下
    result_bgr = cv2.cvtColor(result_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_file_path, result_bgr)

# ===== 1. 初始化 layout 模型（核心只有这一行）=====
layout_engine = PPStructureV3()

# ===== 2. PDF → 图片 =====
save_path = "hire_output_nored_17"
pdf_path = "hire.pdf"
images = convert_from_path(pdf_path, dpi=200)

os.makedirs("output", exist_ok=True)

# ===== 3. 对每一页做 layout =====
#for page_id, image in enumerate(images):
page_id = 17
image = images[17]
img_path = f"output/page_{page_id}.png"

remove_red(image, img_path)

result = layout_engine.predict(img_path)

print(f"\n===== Page {page_id} =====")
for block in result:
    block.print()
    block.save_to_json(save_path=save_path)
    block.save_to_markdown(save_path=save_path)