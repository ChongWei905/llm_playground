from unstructured.partition.pdf import partition_pdf
import json


def extract_with_unstructured(pdf_path):
    # partition_pdf 会自动识别文档结构
    # strategy="hi_res" 会使用布局模型识别标题、正文等（需要安装 detectron2）
    # 如果环境简单，可以使用 strategy="fast" 或 "auto"
    elements = partition_pdf(
        filename=pdf_path,
        strategy="auto",  # 高分辨率策略，识别标题效果最好
        infer_table_structure=False,
        chunking_strategy="by_title"  # 这是一个大招：它能自动按标题把正文分组
    )
    print(elements)

    result_dict = {}
    current_title = None

    for element in elements:
        # 检查元素类型
        element_type = element.category
        text = element.text.strip()

        # Unstructured 识别出的 'Title' 通常对应你的小标题（如 2.1. 工作環境）
        if element_type == "Title":
            current_title = text
            if current_title not in result_dict:
                result_dict[current_title] = []

        # 'NarrativeText' 或 'ListItem' 对应你的实验步骤
        elif element_type in ["NarrativeText", "ListItem", "UncategorizedText"]:
            if current_title:
                result_dict[current_title].append(text)

    return result_dict


if __name__ == "__main__":
    pdf_file = "95A16F99BECC44A7AB6D2600A5064020.pdf"
    try:
        data = extract_with_unstructured(pdf_file)
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"提取失败，请确保已安装相关依赖: {e}")