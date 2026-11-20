"""Xuất trang xem trên Claude (Artifact) từ cùng file JSON dùng cho xuat-excel.py.

Cách chạy (từ thư mục của agent):
    python cong-cu/xuat-trang.py <file.json> <thư mục trang>

Kết quả trong <thư mục trang>: index.html, các file video và ảnh bìa được chép vào,
và danh-sach-file.json (danh sách {"as", "path"} để đưa thẳng vào publish_files).
Ngoài các khối của xuat-excel.py còn có khối video:
    {"loai": "video", "tieu_de": "...", "muc": [{"file", "anh_bia", "ten", "ngay", "caption", "hashtag"}]}
Bản sao giống hệt nằm ở cả hai agent, sửa thì sửa cả hai.
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

TONES = {"do": "critical", "vang": "warning", "xanh": "good", "xam": "muted"}
NUMERIC = ("tien", "so", "phan_tram")


def esc(v):
    return html.escape(str(v))


def show(v, kind):
    if not isinstance(v, (int, float)) or kind not in NUMERIC:
        return v
    if kind == "phan_tram":
        return f"{v * 100:.0f}%"
    text = f"{v:,.0f}".replace(",", ".")
    return text + "đ" if kind == "tien" else text


def anchor(name):
    table = str.maketrans("àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ",
                          "aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd")
    return re.sub(r"[^a-z0-9]+", "-", name.lower().translate(table)).strip("-") or "phan"


def kpis(block):
    tiles = []
    for it in block["muc"]:
        note = str(it.get("ghi_chu", ""))
        tone = "critical" if "Giảm" in note else "good" if note else "muted"
        tiles.append(f'<div class="tile"><div class="tile-label">{esc(it["nhan"])}</div>'
                     f'<div class="tile-value">{esc(show(it["gia_tri"], it.get("dang")))}</div>'
                     f'<div class="tile-note {tone}">{esc(note)}</div></div>')
    return f'<div class="tiles">{"".join(tiles)}</div>'


def bullets(block):
    return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in block["dong"]) + "</ul>"


def table(block):
    cols, kinds = block["cot"], block.get("dang") or ["text"] * len(block["cot"])
    color = block.get("to_mau", {})
    ci = cols.index(color["cot"]) if color.get("cot") in cols else None
    head = "".join(f"<th>{esc(c)}</th>" for c in cols)
    rows = []
    for values in block["dong"]:
        tone = TONES.get(color.get(str(values[ci]))) if ci is not None else None
        cells = []
        for j, v in enumerate(values):
            kind = kinds[j] if j < len(kinds) else "text"
            num = kind in NUMERIC and isinstance(v, (int, float))
            text = esc(show(v, kind))
            if j == ci and tone:
                text = f'<span class="pill {tone}">{text}</span>'
            cells.append(f'<td class="{"num" if num else ""}">{text}</td>')
        rows.append(f'<tr class="{tone or ""}">{"".join(cells)}</tr>')
    note = f'<p class="note">{esc(block["ghi_chu"])}</p>' if block.get("ghi_chu") else ""
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>{note}'


def videos(block, out_dir, files):
    cards = []
    for i, it in enumerate(block["muc"]):
        src = Path(it["file"])
        shutil.copy2(src, out_dir / src.name)
        files.append(src.name)
        poster = ""
        if it.get("anh_bia") and Path(it["anh_bia"]).is_file():
            p = Path(it["anh_bia"])
            shutil.copy2(p, out_dir / p.name)
            files.append(p.name)
            poster = f' poster="{esc(p.name)}"'
        caption = " ".join(x for x in (it.get("caption", ""), it.get("hashtag", "")) if x)
        cards.append(
            f'<article class="video-card"><video controls playsinline preload="metadata" src="{esc(src.name)}"{poster}></video>'
            f'<div class="video-body"><h3>{esc(it.get("ten", src.stem))}</h3>'
            f'<p class="meta">{esc(it.get("ngay", ""))}</p>'
            f'<p class="caption" id="cap-{i}">{esc(caption)}</p>'
            f'<button type="button" class="copy" data-target="cap-{i}">Sao chép caption</button></div></article>')
    return f'<div class="videos">{"".join(cards)}</div>'


CSS = """
:root{--bg:#f6f7f9;--surface:#ffffff;--ink:#141a2b;--muted:#5d6475;--line:#dde1e8;--accent:#1f2a44;--hl:#e8364f;
--good:#166534;--good-bg:#dcfce7;--warn:#92400e;--warn-bg:#fef3c7;--crit:#9b1c1c;--crit-bg:#fde2e4;--mute-bg:#eef0f3;
--display:'Be Vietnam Pro',Arial,sans-serif;--body:'Be Vietnam Pro',Arial,sans-serif;color-scheme:light}
/* bố cục: đầu trang đậm, nav theo phần, các phần xếp dọc, bảng cuộn ngang trên điện thoại */
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f131c;--surface:#171c28;--ink:#e8ebf2;--muted:#9aa2b4;--line:#2a3142;--accent:#2b3a5e;--hl:#ff5a70;
--good:#86efac;--good-bg:#12301f;--warn:#fcd34d;--warn-bg:#3a2a0d;--crit:#fca5a5;--crit-bg:#3d1519;--mute-bg:#222838;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0f131c;--surface:#171c28;--ink:#e8ebf2;--muted:#9aa2b4;--line:#2a3142;--accent:#2b3a5e;--hl:#ff5a70;
--good:#86efac;--good-bg:#12301f;--warn:#fcd34d;--warn-bg:#3a2a0d;--crit:#fca5a5;--crit-bg:#3d1519;--mute-bg:#222838;color-scheme:dark}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.55}
header{background:var(--accent);color:#fff;padding:28px max(16px,calc((100% - 1080px)/2)) 22px}
header h1{font-family:var(--display);font-size:clamp(22px,4vw,32px);margin:0 0 8px;text-wrap:balance;letter-spacing:-.01em}
header p{margin:2px 0;opacity:.85;font-size:14px}
nav{display:flex;gap:8px;flex-wrap:wrap;padding:12px max(16px,calc((100% - 1080px)/2));background:var(--surface);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:2}
nav a{color:var(--ink);text-decoration:none;font-size:14px;padding:6px 12px;border-radius:999px;border:1px solid var(--line)}
nav a:hover,nav a:focus-visible{border-color:var(--hl);outline:none}
main{max-width:1080px;margin:0 auto;padding:8px 16px 48px;display:grid;gap:8px}
section{padding-top:20px}
h2{font-family:var(--display);font-size:22px;margin:0 0 4px;text-wrap:balance}
h3.block{font-size:16px;margin:22px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--hl);color:var(--ink)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-top:14px}
.tile{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.tile-label{font-size:13px;color:var(--muted);font-weight:600}
.tile-value{font-size:28px;font-weight:700;font-variant-numeric:tabular-nums;margin:2px 0}
.tile-note{font-size:13px}.tile-note.critical{color:var(--crit)}.tile-note.good{color:var(--good)}.tile-note.muted{color:var(--muted)}
ul{margin:0;padding-left:20px;display:grid;gap:4px;max-width:80ch}
.table-wrap{overflow-x:auto;background:var(--surface);border:1px solid var(--line);border-radius:12px}
table{border-collapse:collapse;width:100%;font-size:14px}
th{background:var(--accent);color:#fff;text-align:left;font-weight:600;padding:10px 12px;white-space:nowrap}
td{padding:9px 12px;border-top:1px solid var(--line);vertical-align:top}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.critical td{background:var(--crit-bg)}tr.warning td{background:var(--warn-bg)}tr.good td{background:var(--good-bg)}
.pill{display:inline-block;padding:2px 10px;border-radius:999px;font-weight:600;font-size:13px;white-space:nowrap}
.pill.critical{color:var(--crit);border:1px solid currentColor}.pill.warning{color:var(--warn);border:1px solid currentColor}
.pill.good{color:var(--good);border:1px solid currentColor}.pill.muted{color:var(--muted);background:var(--mute-bg)}
.note{color:var(--muted);font-size:13px;font-style:italic;margin:8px 2px 0}
.videos{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.video-card{background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden;display:flex;flex-direction:column}
.video-card video{width:100%;aspect-ratio:9/16;background:#000;display:block}
.video-body{padding:12px 14px;display:grid;gap:6px}
.video-body h3{margin:0;font-size:16px}.meta{margin:0;color:var(--hl);font-weight:600;font-size:14px}
.caption{margin:0;font-size:14px;color:var(--muted)}
button.copy{justify-self:start;font:inherit;font-size:13px;font-weight:600;padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--ink);cursor:pointer}
button.copy:hover,button.copy:focus-visible{border-color:var(--hl);outline:none}
footer{max-width:1080px;margin:0 auto;padding:0 16px 32px;color:var(--muted);font-size:12px}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
"""

SCRIPT = """
document.querySelectorAll('button.copy').forEach(function(b){b.addEventListener('click',function(){
var t=document.getElementById(b.dataset.target).textContent;
navigator.clipboard.writeText(t).then(function(){b.textContent='Đã sao chép';setTimeout(function(){b.textContent='Sao chép caption'},1500)},
function(){b.textContent='Bôi đen để sao chép'});});});
"""


def build(spec_path, out_dir):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    out = Path(out_dir)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    files, sections, links = [], [], []
    for page in spec["trang"]:
        aid = anchor(page["ten"])
        links.append(f'<a href="#{aid}">{esc(page["ten"])}</a>')
        parts = [f'<section id="{aid}"><h2>{esc(page["ten"])}</h2>']
        for block in page["khoi"]:
            if block.get("tieu_de"):
                parts.append(f'<h3 class="block">{esc(block["tieu_de"])}</h3>')
            kind = block["loai"]
            if kind == "chi_so":
                parts.append(kpis(block))
            elif kind == "doan":
                parts.append(bullets(block))
            elif kind == "bang":
                parts.append(table(block))
            elif kind == "video":
                parts.append(videos(block, out, files))
        parts.append("</section>")
        sections.append("".join(parts))
    info = "".join(f"<p>{esc(x)}</p>" for x in spec.get("thong_tin", []))
    doc = f"""<!DOCTYPE html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(spec.get("ten_trang", spec["tieu_de"]))}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header><h1>{esc(spec["tieu_de"])}</h1>{info}</header>
<nav aria-label="Các phần">{"".join(links)}</nav>
<main>{"".join(sections)}</main>
<footer>Trang do agent TIVO Smart tự cập nhật. Số liệu lấy từ file dữ liệu của shop.</footer>
<script>{SCRIPT}</script></body></html>"""
    (out / "index.html").write_text(doc, encoding="utf-8")
    listing = [{"as": "index.html", "path": str((out / "index.html").resolve())}]
    listing += [{"as": f, "path": str((out / f).resolve())} for f in dict.fromkeys(files)]
    (out / "danh-sach-file.json").write_text(json.dumps(listing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã tạo trang {out / 'index.html'} ({len(listing)} file). Danh sách để đăng: {out / 'danh-sach-file.json'}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        sys.exit("Cách dùng: python cong-cu/xuat-trang.py <file.json> <thư mục trang>")
    build(sys.argv[1], sys.argv[2])
