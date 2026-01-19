from pdf2image import convert_from_path
import cv2
import numpy as np

pdf_path = "hire.pdf"
images = convert_from_path(pdf_path, dpi=200)

img = images[17]              # PIL Image (RGB)
img.save("origin.png")

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
cv2.imwrite("after.png", result_bgr)