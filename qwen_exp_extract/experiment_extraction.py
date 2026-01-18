import pdfplumber
import dashscope
from dashscope import Generation

# === 配置你的 DashScope API Key ===
dashscope.api_key = "sk-27d337202fe14f388cef591a07794f8d"  # 替换为你的实际 API Key

def extract_text_from_pdf(pdf_path, max_pages=10):
    """从 PDF 中提取前 max_pages 页的文本（避免过长）"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages[:max_pages]):
            text += page.extract_text() or ""
            if len(text) > 8000:  # 限制输入长度（Qwen-turbo 最大上下文约 32768 tokens，但保守起见）
                break
    return text[:8000]

def analyze_experiment_with_qwen(text):
    """调用 Qwen API 提取实验名称和步骤"""
    prompt = f"""
你是一位专业的生物医学科研助理。请从以下论文/实验手册片段中提取两项信息：

1. **实验名称**：识别文中描述的核心实验技术名称（如“Western Blot”、“CRISPR-Cas9 基因编辑”、“单细胞 RNA 测序”等）。
2. **实验步骤**：以编号列表形式列出所有具体的实验操作步骤（仅包含可执行的操作，如“加入 1 mL PBS”、“37°C 孵育 2 小时”等），不要包含背景、原理或结果。

要求：
- 实验名称最多列出 3 个，按重要性排序。
- 实验步骤必须来自原文描述，不要编造。
- 输出格式严格如下（不要任何额外说明）：

实验名称：
- [名称1]
- [名称2]
- [名称3]

实验步骤：
1. [步骤1]
2. [步骤2]
...

---
文本开始：
{text}
---
文本结束。
"""

    # try:
    # response = Generation.call(
    #     model="qwen_exp_extract-turbo",  # 或 qwen_exp_extract-plus（更准但稍贵）
    #     prompt="我现在在用什么模型，参数量是多少",
    #     temperature=0.1,     # 降低随机性，提高稳定性
    #     max_tokens=1000
    # )
    return prompt
    # except Exception as e:
    #     return f"API 调用失败: {e}"

def main(pdf_path):
    print("正在提取 PDF 文本...")
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        print("PDF 中未提取到有效文本。")
        return

    print("正在调用 Qwen API 分析实验内容...")
    result = analyze_experiment_with_qwen(text)
    print("\n=== 提取结果 ===\n")
    print(result)

# === 使用示例 ===
if __name__ == "__main__":
    pdf_file = "exp.pdf"  # 替换为你的 PDF 文件路径
    main(pdf_file)