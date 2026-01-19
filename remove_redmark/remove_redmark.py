
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import os


class ContractProcessor:
    """处理带有红色印章的PDF合同"""

    def __init__(self, output_dir="processed_output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def process_pdf_page(self, pdf_path, page_num, dpi):
        """
        处理PDF的指定页面

        Args:
            pdf_path: PDF文件路径
            page_num: 页码（从0开始）
            dpi: 转换分辨率，越高质量越好但内存占用越大
        """
        print(f"正在转换PDF第 {page_num + 1} 页...")
        images = convert_from_path(pdf_path, dpi=dpi, first_page=page_num+1, last_page=page_num+1)

        if not images:
            raise ValueError("无法读取PDF页面")

        # 转换为OpenCV格式
        img_array = np.array(images[0])
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # 保存原始图像
        original_path = os.path.join(self.output_dir, "01_original.png")
        cv2.imwrite(original_path, img_bgr)
        print(f"原始图像已保存: {original_path}")

        # 步骤1: 增强灰色文字
        enhanced_img = self.enhance_gray_text(img_bgr.copy())
        enhanced_path = os.path.join(self.output_dir, "02_enhanced.png")
        cv2.imwrite(enhanced_path, enhanced_img)
        print(f"文字增强完成: {enhanced_path}")

        # 步骤2: 检测红色印章区域
        red_mask = self.detect_red_seal(enhanced_img)
        mask_path = os.path.join(self.output_dir, "03_red_mask.png")
        cv2.imwrite(mask_path, red_mask)
        print(f"印章区域检测完成: {mask_path}")

        # 步骤3: 智能移除印章（使用图像修复）
        removed_img = self.remove_seal_with_inpainting(enhanced_img, red_mask)
        removed_path = os.path.join(self.output_dir, "04_seal_removed.png")
        cv2.imwrite(removed_path, removed_img)
        print(f"印章移除完成: {removed_path}")

        # 步骤4: 文字修复和优化
        final_img = self.restore_and_optimize(removed_img)
        final_path = os.path.join(self.output_dir, "05_final.png")
        cv2.imwrite(final_path, final_img)
        print(f"最终处理完成: {final_path}")

        # 步骤5: 转回PDF
        self.save_as_pdf(final_img, os.path.join(self.output_dir, "final_output.pdf"))
        print("已转换为PDF格式")

        return final_img

    def enhance_gray_text(self, img):
        """增强灰色文字的对比度"""
        print("正在增强灰色文字...")

        # 转换到LAB色彩空间，L通道是亮度
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # 使用CLAHE (对比度限制自适应直方图均衡化) 增强L通道
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l_enhanced = clahe.apply(l)

        # 合并回LAB
        lab_enhanced = cv2.merge([l_enhanced, a, b])
        enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

        # 额外的锐化处理
        kernel_sharpen = np.array([
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ])
        enhanced = cv2.filter2D(enhanced, -1, kernel_sharpen)

        return enhanced

    def detect_red_seal(self, img):
        """检测红色印章区域，返回mask"""
        print("正在检测红色印章...")

        # 转换到HSV色彩空间
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 定义红色的HSV范围（两个区间）
        # 红色在HSV中分布在0-10和170-180两个区间
        lower_red_1 = np.array([0, 100, 100])
        upper_red_1 = np.array([10, 255, 255])
        lower_red_2 = np.array([160, 100, 100])
        upper_red_2 = np.array([180, 255, 255])

        # 创建红色mask
        mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
        mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        # 形态学处理，连接断开的区域
        kernel = np.ones((5, 5), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel, iterations=1)

        # 膨胀mask，确保完全覆盖印章边缘
        kernel_dilate = np.ones((7, 7), np.uint8)
        red_mask = cv2.dilate(red_mask, kernel_dilate, iterations=2)

        return red_mask

    def remove_seal_with_inpainting(self, img, mask):
        """使用图像修复算法智能移除印章"""
        print("正在使用图像修复算法移除印章...")

        # 使用Telea算法进行修复（快速且效果好）
        # inpaintRadius: 修复半径，值越大修复范围越广
        inpainted = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

        # 也可以尝试NS (Navier-Stokes) 算法，效果可能更自然但速度较慢
        # inpainted = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_NS)

        return inpainted

    def restore_and_optimize(self, img):
        """修复和优化最终图像"""
        print("正在进行最终优化...")

        # 1. 轻微去噪，保留文字边缘
        denoised = cv2.fastNlMeansDenoisingColored(img, None, h=10, hColor=10,
                                                   templateWindowSize=7, searchWindowSize=21)

        # 2. 转换为灰度图
        gray = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)

        # 3. 自适应阈值二值化（对不均匀光照效果好）
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, blockSize=15, C=10
        )

        # 4. 轻微的形态学处理，修复断裂的笔画
        kernel = np.ones((2, 2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)

        # 5. 转回BGR格式（如果需要彩色输出，可以保留去噪后的彩色图）
        final = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

        return final

    def save_as_pdf(self, img, output_path):
        """将处理后的图像转换为PDF"""
        print(f"正在保存为PDF: {output_path}")

        # 如果是BGR格式，转换为RGB
        if len(img.shape) == 3:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img_rgb = img

        # 使用PIL保存为PDF
        pil_img = Image.fromarray(img_rgb)
        pil_img.save(output_path, "PDF", resolution=300.0, quality=95)


def main():
    """主函数示例"""
    # 初始化处理器
    processor = ContractProcessor(output_dir="contract_processed")

    # 处理PDF
    pdf_path = "我的合同.pdf"  # 替换为你的PDF路径
    page_num = 35  # 要处理的页码（从0开始）

    try:
        result = processor.process_pdf_page(
            pdf_path=pdf_path,
            page_num=page_num,
            dpi=300  # 可以根据内存情况调整，200-400之间
        )
        print("✅ 处理完成！")
        print(f"所有中间结果和最终PDF已保存到: contract_processed/")
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")


if __name__ == "__main__":
    main()