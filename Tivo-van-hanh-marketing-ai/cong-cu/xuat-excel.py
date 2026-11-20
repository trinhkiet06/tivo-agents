"""Xuất file Excel đã định dạng sẵn cho người đọc từ một file JSON.

Cách chạy (từ thư mục của agent):
    python cong-cu/xuat-excel.py <file.json>

Mẫu JSON: cong-cu/mau-excel.json. Bản sao giống hệt nằm ở cả hai agent, sửa thì sửa cả hai.

Cấu trúc JSON:
    out, tieu_de, thong_tin (danh sách dòng nhỏ dưới tiêu đề), trang (danh sách sheet).
    Mỗi trang: ten, khoi (danh sách khối, xếp từ trên xuống). Các loại khối:
      chi_so : muc = [{nhan, gia_tri, dang, ghi_chu}]  -> các ô số liệu lớn
      doan   : tieu_de, dong = [chuỗi]                -> gạch đầu dòng
      bang   : tieu_de, cot, dang (theo cột), dong, to_mau, ghi_chu
    dang: text | tien | so | phan_tram (0.25 = 25%) | ngay (chuỗi dd/mm/yyyy giữ nguyên)
    to_mau: {"cot": <tên cột>, "<giá trị>": "do" | "vang" | "xanh" | "xam"} -> tô cả dòng
"""
import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

NAVY, ACCENT, GREY = "1F2A44", "E8364F", "6B7280"
FILLS = {
    "do": ("FDE2E4", "9B1C1C"),
    "vang": ("FEF3C7", "92400E"),
    "xanh": ("DCFCE7", "166534"),
    "xam": ("F3F4F6", "374151"),
}
NUMERIC = ("tien", "so", "phan_tram")


def show(v, kind):
    """Đổi số sang chữ kiểu Việt Nam: 4.850.000đ, 25%. Excel máy tiếng Anh sẽ hiện dấu phẩy nếu để dạng số."""
    if not isinstance(v, (int, float)) or kind not in NUMERIC:
        return v
    if kind == "phan_tram":
        return f"{v * 100:.0f}%"
    text = f"{v:,.0f}".replace(",", ".")
    return text + "đ" if kind == "tien" else text
THIN = Side(style="thin", color="D1D5DB")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
FONT = "Arial"
MIN_COLS = 6
MIN_WIDTH = 120


def fill(color):
    return PatternFill("solid", start_color=color, end_color=color)


def text_len(v):
    return max((len(line) for line in str(v).split("\n")), default=0)


class Sheet:
    def __init__(self, ws, ncols):
        self.ws, self.ncols, self.row, self.widths, self.pending = ws, ncols, 1, [10] * ncols, []
        self.cells = []  # (dòng, cột, chữ) của các ô bảng, để tính chiều cao khi đã biết độ rộng cột

    def merged(self, text, font, fill_color=None, height=None, align="left"):
        ws, r = self.ws, self.row
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=self.ncols)
        c = ws.cell(r, 1, text)
        c.font = font
        c.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True, indent=1)
        if fill_color:
            for col in range(1, self.ncols + 1):
                ws.cell(r, col).fill = fill(fill_color)
        if height:
            ws.row_dimensions[r].height = height
        self.row += 1

    def section(self, title):
        self.row += 1
        self.merged(title, Font(name=FONT, size=13, bold=True, color=NAVY), height=24)
        for col in range(1, self.ncols + 1):
            self.ws.cell(self.row - 1, col).border = Border(bottom=Side(style="medium", color=ACCENT))

    def header(self, title, info):
        self.merged(title, Font(name=FONT, size=18, bold=True, color="FFFFFF"), NAVY, 40)
        for line in info:
            self.merged(line, Font(name=FONT, size=10, italic=True, color=GREY), height=18)

    def kpis(self, items):
        self.pending.append((self.row + 1, items))
        self.row += 4

    def place_kpis(self, r, items):
        ws, total, groups, start, acc = self.ws, sum(self.widths), [], 1, 0
        for col in range(1, self.ncols + 1):
            acc += self.widths[col - 1]
            if acc >= total * (len(groups) + 1) / len(items) - 1e-6 and len(groups) < len(items) - 1:
                groups.append((start, col))
                start = col + 1
        groups.append((start, self.ncols))
        for it, (c0, c1) in zip(items, groups):
            for rr, val, font in (
                (r, it["nhan"], Font(name=FONT, size=10, bold=True, color=GREY)),
                (r + 1, it["gia_tri"], Font(name=FONT, size=20, bold=True, color=NAVY)),
                (r + 2, it.get("ghi_chu", ""), Font(name=FONT, size=10, color=ACCENT if "Giảm" in str(it.get("ghi_chu", "")) else "166534")),
            ):
                ws.merge_cells(start_row=rr, start_column=c0, end_row=rr, end_column=c1)
                cell = ws.cell(rr, c0, show(val, it.get("dang")) if rr == r + 1 else val)
                cell.font = font
                cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                for col in range(c0, c1 + 1):
                    ws.cell(rr, col).fill = fill("F8FAFC")
            ws.row_dimensions[r + 1].height = 34
            ws.row_dimensions[r + 2].height = 30

    def bullets(self, lines):
        for line in lines:
            self.merged(f"•  {line}", Font(name=FONT, size=11), height=max(18, 16 * (1 + len(line) // 120)))

    def table(self, block):
        ws, cols = self.ws, block["cot"]
        kinds = block.get("dang") or ["text"] * len(cols)
        color = block.get("to_mau", {})
        color_col = cols.index(color["cot"]) if color.get("cot") in cols else None
        r = self.row
        for j, name in enumerate(cols):
            c = ws.cell(r, j + 1, name)
            c.font = Font(name=FONT, size=11, bold=True, color="FFFFFF")
            c.fill = fill(NAVY)
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            c.border = BOX
            self.widths[j] = max(self.widths[j], min(text_len(name) + 4, 40))
        ws.row_dimensions[r].height = 30
        for i, values in enumerate(block["dong"]):
            rr = r + 1 + i
            tone = FILLS.get(color.get(str(values[color_col]))) if color_col is not None else None
            base = tone[0] if tone else ("FFFFFF" if i % 2 == 0 else "F8FAFC")
            for j, v in enumerate(values):
                kind = kinds[j] if j < len(kinds) else "text"
                numeric = kind in NUMERIC and isinstance(v, (int, float))
                c = ws.cell(rr, j + 1, show(v, kind))
                c.font = Font(name=FONT, size=11, color=tone[1] if tone else "111827",
                              bold=bool(tone) and j == color_col)
                c.fill = fill(base)
                c.border = BOX
                c.alignment = Alignment(horizontal="right" if numeric else "left", vertical="center",
                                        wrap_text=True, indent=0 if numeric else 1)
                self.widths[j] = max(self.widths[j], min(text_len(show(v, kind)) + 3, 55))
                self.cells.append((rr, j, str(show(v, kind))))
        self.row = r + 1 + len(block["dong"])
        if block.get("ghi_chu"):
            self.merged(block["ghi_chu"], Font(name=FONT, size=10, italic=True, color=GREY),
                        height=max(18, 15 * (1 + len(block["ghi_chu"]) // 130)))

    def finish(self, used_cols):
        short = MIN_WIDTH - sum(self.widths)
        if short > 0:
            spare = list(range(used_cols, self.ncols)) or [self.ncols - 1]
            for j in spare:
                self.widths[j] += short / len(spare)
        for r, items in self.pending:
            self.place_kpis(r, items)
        lines = {}
        for r, j, text in self.cells:
            per_line = max(int(self.widths[j] * 0.8) - 1, 6)
            n = sum(max(1, -(-len(part) // per_line)) for part in text.split(chr(10)))
            lines[r] = max(lines.get(r, 1), n)
        for r, n in lines.items():
            self.ws.row_dimensions[r].height = max(20, 15 * n + 6)
        for j, w in enumerate(self.widths):
            self.ws.column_dimensions[get_column_letter(j + 1)].width = w
        ps = self.ws.page_setup
        ps.orientation, ps.paperSize = "landscape", self.ws.PAPERSIZE_A4
        ps.fitToWidth, ps.fitToHeight = 1, (1 if self.row <= 60 else 0)
        self.ws.sheet_properties.pageSetUpPr.fitToPage = True
        self.ws.print_options.horizontalCentered = True
        self.ws.page_margins.left = self.ws.page_margins.right = 0.4
        self.ws.sheet_view.showGridLines = False


def build(spec_path):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    wb = Workbook()
    wb.remove(wb.active)
    for page in spec["trang"]:
        used = max([1] + [len(b["cot"]) for b in page["khoi"] if b["loai"] == "bang"])
        ncols = max(MIN_COLS, used)
        sh = Sheet(wb.create_sheet(page["ten"][:31]), ncols)
        sh.header(spec["tieu_de"] if page is spec["trang"][0] else f'{spec["tieu_de"]}: {page["ten"]}',
                  spec.get("thong_tin", []) if page is spec["trang"][0] else [])
        for block in page["khoi"]:
            if block["loai"] == "video":  # chỉ có trên trang Claude, Excel không phát được video
                continue
            if block.get("tieu_de"):
                sh.section(block["tieu_de"])
            if block["loai"] == "chi_so":
                sh.kpis(block["muc"])
            elif block["loai"] == "doan":
                sh.bullets(block["dong"])
            elif block["loai"] == "bang":
                sh.table(block)
        sh.finish(used)
    out = Path(spec["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f"Đã tạo {out}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        sys.exit("Cách dùng: python cong-cu/xuat-excel.py <file.json>")
    build(sys.argv[1])
