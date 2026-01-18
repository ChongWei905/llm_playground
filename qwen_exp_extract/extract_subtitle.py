import re

import pdfplumber


def extract_text_without_margins(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 获取页面高度和宽度
            width = page.width
            height = page.height

            # 定义裁剪区域 (x0, top, x1, bottom)
            # 这里的数值比例需要根据你的 PDF 实际情况调整，例如忽略顶部 5% 和底部 5%
            bbox = (0, height * 0.05, width, height * 0.95)
            cropped_page = page.within_bbox(bbox)

            text += cropped_page.extract_text() or ""
    return text

def extract_content_by_hierarchy(text):
    # 定义匹配二级标题（如 2.1.）和三级标题（如 2.2.1.）的正则
    # 这里的正则去掉了 ^ 行首限制的严格模式，改为判断每行开始的特征
    l2_pattern = re.compile(r'^(\d+\.\d+\.)\s*(.*)')
    l3_pattern = re.compile(r'^(\d+\.\d+\.\d+\.)\s*(.*)')

    result_dict = {}
    lines = text.split('\n')

    current_l2_key = None

    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue

        # 检查是否为三级标题
        l3_match = l3_pattern.match(clean_line)
        if l3_match:
            if current_l2_key is not None:
                # 开启一个新的三级标题内容块
                content = l3_match.group(2).strip()
                result_dict[current_l2_key].append(content)
            continue

        # 检查是否为二级标题
        l2_match = l2_pattern.match(clean_line)
        if l2_match:
            # 开启一个新的二级标题 Key
            full_l2_content = l2_match.group(2).strip()

            # 优化逻辑：如果长度 > 15 且包含冒号
            # 使用正则支持中英文冒号分词
            if len(full_l2_content) > 15 and (':' in full_l2_content or '：' in full_l2_content):
                # 找到第一个出现的冒号位置（无论是中文还是英文冒号）
                split_match = re.split(r'[:：]', full_l2_content, maxsplit=1)
                if len(split_match) == 2:
                    current_l2_key = split_match[0].strip()
                    l2_first_element = split_match[1].strip()

                    if current_l2_key not in result_dict:
                        result_dict[current_l2_key] = []
                    # 将冒号后的内容作为 list 的第一个元素
                    if l2_first_element:
                        result_dict[current_l2_key].append(l2_first_element)
                else:
                    current_l2_key = full_l2_content
            else:
                current_l2_key = full_l2_content

            if current_l2_key not in result_dict:
                result_dict[current_l2_key] = []
            continue

        # 如果既不是二级也不是三级标题，则是正文内容，需要追加到最近的一个三级标题内容中
        if current_l2_key and result_dict[current_l2_key]:
            # 获取当前二级标题下的最后一个三级标题内容，进行追加
            last_idx = len(result_dict[current_l2_key]) - 1
            result_dict[current_l2_key][last_idx] += " " + clean_line
        elif current_l2_key:
            # 如果二级标题下还没有三级标题，内容可以暂时记录在 Key 描述里或者根据需求处理
            # 这里示例：将其合并到 Key 的名称中
            pass

    return result_dict




if __name__ == "__main__":
    text = extract_text_without_margins("exp.pdf")
    extracted_data = extract_content_by_hierarchy(text)

    # 打印结果
    import json

    print(json.dumps(extracted_data, indent=4, ensure_ascii=False))
