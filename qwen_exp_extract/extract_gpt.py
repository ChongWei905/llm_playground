# import miner
# import json
# from pathlib import Path
#
# def pdf_to_json(pdf_path: str, output_json: str):
#     miner = MinerU(
#         layout=True,      # 启用版面分析（非常重要）
#         ocr=True,         # 支持扫描版
#         language="auto"   # 中英文自动
#     )
#
#     result = miner.parse(pdf_path)
#
#     with open(output_json, "w", encoding="utf-8") as f:
#         json.dump(result, f, ensure_ascii=False, indent=2)
#
#     return result
#
# if __name__ == "__main__":
#     pdf_path = "paper.pdf"
#     output_json = "paper_mineru.json"
#     pdf_to_json(pdf_path, output_json)
