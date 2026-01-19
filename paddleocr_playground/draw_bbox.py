import cv2

img = cv2.imread("output/page_17.png")   # 原图
bbox = [
    121,
    647,
    995,
    685
]     # 你的 bbox

x1, y1, x2, y2 = bbox

# 画矩形
cv2.rectangle(
    img,
    (int(x1), int(y1)),
    (int(x2), int(y2)),
    color=(0, 255, 0),   # 绿色
    thickness=2
)

cv2.imwrite("page_with_bbox.png", img)