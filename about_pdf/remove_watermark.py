import re
import math
import argparse
from collections import Counter, defaultdict

import fitz  # PyMuPDF


# -----------------------------
# Color helpers
# -----------------------------
def int_to_rgb(c: int):
    return ((c >> 16) & 255, (c >> 8) & 255, c & 255)


def is_watermark_color(
    c: int,
    min_rgb: int = 160,
    max_rgb: int = 245,
    max_channel_diff: int = 18,
    min_luma: int = 170,
):
    """
    Decide if a color looks like a "typical watermark" light/low-contrast color.

    Conditions (all must pass):
    1) Each channel in [min_rgb, max_rgb]  (light color)
    2) max(r,g,b) - min(r,g,b) <= max_channel_diff (low saturation / near-gray)
    3) luma (perceived brightness) >= min_luma
    """
    r, g, b = int_to_rgb(int(c))

    if not (min_rgb <= r <= max_rgb and min_rgb <= g <= max_rgb and min_rgb <= b <= max_rgb):
        return False

    if (max(r, g, b) - min(r, g, b)) > max_channel_diff:
        return False

    # luma / luminance (0..255)
    luma = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    if luma < min_luma:
        return False

    return True


# -----------------------------
# Angle helpers
# -----------------------------
def angle_from_dir(d):
    """
    d is usually (dx, dy) from rawdict line["dir"].
    Return angle degrees normalized into (-90, 90].
    """
    dx, dy = float(d[0]), float(d[1])
    a = math.degrees(math.atan2(dy, dx))  # [-180, 180]
    while a <= -90:
        a += 180
    while a > 90:
        a -= 180
    return a


def quantize_angle(a_deg: float, step: float = 2.0) -> float:
    return round(a_deg / step) * step


def proj(x, y, ux, uy):
    return x * ux + y * uy


# -----------------------------
# Watermark tolerant detection
# -----------------------------
FULL_RE = re.compile(r"[A-Za-z]\d{8}\s+\d{4}/\d{1,2}/\d{1,2}")

# 全局变量或通过参数传递，用于存储探测到的完整水印文本
WATERMARK_PROTOTYPE = None

def find_watermark_prototype(doc):
    """
    扫描前几页，找到一个完整的符合格式的水印作为基准原型
    """
    for i in range(min(5, doc.page_count)):
        page = doc.load_page(i)
        text = page.get_text()
        match = FULL_RE.search(text)
        if match:
            return match.group(0).strip()
    return None


def looks_like_cut_watermark(text: str) -> bool:
    """
    如果已经确定了原型，只要当前文本是原型的子串，即判定为水印
    """
    global WATERMARK_PROTOTYPE
    t = " ".join(text.split()).strip()
    if not t:
        return False

    # 如果还没找到原型，先尝试用正则匹配完整的
    if WATERMARK_PROTOTYPE is None:
        match = FULL_RE.search(t)
        if match:
            WATERMARK_PROTOTYPE = match.group(0)
            return True
        # 在没找到原型前，退而求其次：如果有字母+4位以上数字，也可能是一个截断部分
        # 但为了稳妥，我们可以等第一步探测结果
        return False

    # 核心逻辑：被切割的水印一定是原型的子字符串
    if t in WATERMARK_PROTOTYPE:
        # 为了防止误伤极短的正常文本（如单个数字），增加长度校验
        if len(t) >= 4:
            return True

    return False


# -----------------------------
# Extraction & clustering
# -----------------------------
def collect_candidate_spans(
    page,
    min_size: float,
    min_rgb: int,
    max_rgb: int,
    max_channel_diff: int,
    min_luma: int,
):
    """
    Use rawdict to get line direction (rotation). Filter by watermark-like color range.
    Return list of span items with angle and bbox.
    """
    raw = page.get_text("rawdict")
    items = []

    for block in raw.get("blocks", []):
        if block.get("type") != 0:
            continue

        for line in block.get("lines", []):
            d = line.get("dir")
            if not d:
                continue

            ang = angle_from_dir(d)
            ang_q = quantize_angle(ang, step=2.0)

            for span in line.get("spans", []):
                color = span.get("color")
                if color is None:
                    continue

                if not is_watermark_color(
                    int(color),
                    min_rgb=min_rgb,
                    max_rgb=max_rgb,
                    max_channel_diff=max_channel_diff,
                    min_luma=min_luma,
                ):
                    continue

                size = float(span.get("size", 0.0))
                if size < min_size:
                    continue

                text = span.get("text", "")
                if not text or not text.strip():
                    continue

                bbox = fitz.Rect(span["bbox"])
                if bbox.is_empty or bbox.get_area() <= 0:
                    continue

                items.append(
                    {
                        "bbox": bbox,
                        "text": text,
                        "size": size,
                        "color": int(color),
                        "angle_q": ang_q,
                    }
                )
    return items


def dominant_diagonal_angle(items, min_abs_angle=10.0):
    c = Counter(it["angle_q"] for it in items if abs(it["angle_q"]) >= min_abs_angle)
    if not c:
        return None
    return c.most_common(1)[0][0]


def cluster_by_watermark_instances(items, angle_q, normal_tol=6.0, size_bucket=1.5):
    selected = [it for it in items if it["angle_q"] == angle_q]
    if not selected:
        return []

    theta = math.radians(angle_q)
    ux, uy = math.cos(theta), math.sin(theta)  # direction unit
    nx, ny = -uy, ux  # normal unit

    buckets = defaultdict(list)
    for it in selected:
        key = round(it["size"] / max(size_bucket, 0.1))
        buckets[key].append(it)

    clusters = []
    for _, spans in buckets.items():
        pts = []
        for it in spans:
            cx = (it["bbox"].x0 + it["bbox"].x1) / 2.0
            cy = (it["bbox"].y0 + it["bbox"].y1) / 2.0
            pn = proj(cx, cy, nx, ny)
            pa = proj(cx, cy, ux, uy)
            pts.append((pn, pa, it))

        pts.sort(key=lambda x: x[0])

        cur, cur_pn = [], None
        for pn, pa, it in pts:
            if cur_pn is None or abs(pn - cur_pn) <= normal_tol:
                cur.append((pn, pa, it))
                cur_pn = pn if cur_pn is None else (0.7 * cur_pn + 0.3 * pn)
            else:
                clusters.append(cur)
                cur = [(pn, pa, it)]
                cur_pn = pn
        if cur:
            clusters.append(cur)

    out = []
    for cl in clusters:
        cl.sort(key=lambda x: x[1])
        out.append([x[2] for x in cl])
    return out


def cluster_text(cluster):
    parts = [it["text"].strip() for it in cluster if it["text"].strip()]
    return " ".join(parts)


# -----------------------------
# Main redaction
# -----------------------------
def remove_small_diagonal_watermarks(
    input_pdf: str,
    output_pdf: str,
    min_span_size: float = 6.0,
    min_abs_angle: float = 10.0,
    normal_tol: float = 6.0,
    size_bucket: float = 1.5,
    min_hits_per_page: int = 3,
    fill_white: bool = True,
    # color-range params:
    min_rgb: int = 160,
    max_rgb: int = 245,
    max_channel_diff: int = 18,
    min_luma: int = 170,
):
    doc = fitz.open(input_pdf)
    global WATERMARK_PROTOTYPE
    WATERMARK_PROTOTYPE = find_watermark_prototype(doc)
    if WATERMARK_PROTOTYPE:
        print(f"Found watermark prototype: '{WATERMARK_PROTOTYPE}'")

    total_redacted_spans = 0
    total_pages_touched = 0

    fill = (1, 1, 1) if fill_white else None

    for i in range(doc.page_count):
        page = doc.load_page(i)

        items = collect_candidate_spans(
            page,
            min_size=min_span_size,
            min_rgb=min_rgb,
            max_rgb=max_rgb,
            max_channel_diff=max_channel_diff,
            min_luma=min_luma,
        )
        if not items:
            continue

        angle_q = dominant_diagonal_angle(items, min_abs_angle=min_abs_angle)
        if angle_q is None:
            continue

        clusters = cluster_by_watermark_instances(
            items, angle_q=angle_q, normal_tol=normal_tol, size_bucket=size_bucket
        )
        if not clusters:
            continue

        watermark_clusters = []
        for cl in clusters:
            text = cluster_text(cl)
            if looks_like_cut_watermark(text):
                watermark_clusters.append(cl)

        if len(watermark_clusters) < min_hits_per_page:
            continue

        rects = []
        for cl in watermark_clusters:
            for it in cl:
                rects.append(it["bbox"])

        for r in rects:
            page.add_redact_annot(r, fill=fill)

        if rects:
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
            total_redacted_spans += len(rects)
            total_pages_touched += 1

    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()
    return total_pages_touched, total_redacted_spans


def main():
    ap = argparse.ArgumentParser(
        description="Remove small repeated diagonal text watermarks by color-range + tolerant pattern (PyMuPDF)."
    )
    ap.add_argument("input_pdf", help="Input PDF path")
    ap.add_argument("output_pdf", help="Output PDF path")

    ap.add_argument("--min-size", type=float, default=6.0, help="Min span size to consider (default 6)")
    ap.add_argument("--min-abs-angle", type=float, default=10.0, help="Exclude near-horizontal (default 10 deg)")
    ap.add_argument("--normal-tol", type=float, default=6.0, help="Clustering tolerance in points (default 6)")
    ap.add_argument("--size-bucket", type=float, default=1.5, help="Size bucketing granularity (default 1.5)")
    ap.add_argument("--min-hits", type=int, default=3, help="Min watermark instances per page to apply (default 3)")
    ap.add_argument("--no-white-fill", action="store_true", help="Don't force white fill")

    # Color range controls
    ap.add_argument("--min-rgb", type=int, default=160, help="Min per-channel RGB (default 160)")
    ap.add_argument("--max-rgb", type=int, default=245, help="Max per-channel RGB (default 245)")
    ap.add_argument("--max-channel-diff", type=int, default=18, help="Max (maxRGB-minRGB) to keep it grayish (default 18)")
    ap.add_argument("--min-luma", type=int, default=170, help="Min brightness / luma (default 170)")

    args = ap.parse_args()

    pages, spans = remove_small_diagonal_watermarks(
        args.input_pdf,
        args.output_pdf,
        min_span_size=args.min_size,
        min_abs_angle=args.min_abs_angle,
        normal_tol=args.normal_tol,
        size_bucket=args.size_bucket,
        min_hits_per_page=args.min_hits,
        fill_white=(not args.no_white_fill),
        min_rgb=args.min_rgb,
        max_rgb=args.max_rgb,
        max_channel_diff=args.max_channel_diff,
        min_luma=args.min_luma,
    )

    print(f"Done. pages_touched={pages}, redacted_span_rects={spans}")


if __name__ == "__main__":
    main()