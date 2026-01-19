import cv2
import numpy as np


def remove_red_seal(image_path, output_path):
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print("无法加载图片")
        return

    # 将图片拆分为通道 (OpenCV 顺序: B, G, R)
    blue_c, green_c, red_c = cv2.split(img)

    # --- 新增逻辑：区分偏灰和偏红并加黑文字 ---
    # 将通道转换为 int16 防止计算差值时溢出
    r = red_c.astype(np.int16)
    g = green_c.astype(np.int16)
    b = blue_c.astype(np.int16)

    # 定义“偏红”的判定阈值。R 比 G 和 B 高出 40 以上认为是红印章
    color_threshold = 40
    is_red = (r - g > color_threshold) & (r - b > color_threshold)
    
    # 定义“偏灰”的判定：R, G, B 非常接近
    # 这里我们简单取非红且不是全白的区域作为潜在文字区
    is_gray = ~is_red & (red_c < 200) 

    # 如果是偏灰色，就将该像素在红色通道中设为纯黑 (0)
    # 这样在后续的二值化中，这些字迹会变得非常清晰
    red_c[is_gray] = 0
    # ---------------------------------------

    # 使用处理后的红色通道进行二值化
    # 此时，原本偏灰的文字已经被我们强行抹黑了
    # 而红色印章在 red_c 中依然是高亮（接近白色）的，会被 threshold 过滤掉
    _, binary = cv2.threshold(red_c, 150, 255, cv2.THRESH_BINARY)

    # 保存结果
    cv2.imwrite(output_path, binary)
    print(f"增强处理完成，结果已保存至: {output_path}")


if __name__ == "__main__":
    # 示例调用
    # remove_red_seal('path_to_your_image.png', 'output_no_seal.png')
    pass