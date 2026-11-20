"""Tạo trang tổng quan TIVO (1 trang Claude gộp kế hoạch, video, lịch sale, sản phẩm).

Cách chạy (từ thư mục Tivo-van-hanh-marketing-ai):
    python cong-cu/xuat-tong-quan.py

Tự lấy dữ liệu mới nhất:
- Đợt sale đang làm: thư mục output/3-video/<tên-sale>/ có nguon/lich-dang-video.json mới nhất (bỏ qua thu-nghiem).
- Kế hoạch: output/1-ke-hoach/nguon/ke-hoach-<tên-sale>.json (không có thì lấy file mới nhất).
- Lịch sale: data/lich-sale-va-ngan-sach.xlsx. Sản phẩm: data/san-pham.xlsx, data/ton-kho.xlsx, ảnh data/anh-san-pham.
Kết quả: output/tong-quan/index.html, ảnh sản phẩm thu nhỏ trong output/tong-quan/sp/ và
output/tong-quan/danh-sach-file.json (danh sách file để publish_files, video lấy thẳng từ thư mục đợt sale).
Cần: pip install openpyxl pillow
"""
import datetime as dt
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

import openpyxl
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output" / "tong-quan"
THU = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


def esc(v):
    return html.escape("" if v is None else str(v))


def plain(s):
    s = unicodedata.normalize("NFD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def money(v):
    try:
        return f"{int(float(v)):,}".replace(",", ".") + "đ"
    except (TypeError, ValueError):
        return ""


def day_label(d):
    return f"{THU[d.weekday()]} {d:%d/%m}"


def blocks(doc):
    for t in doc.get("trang", []):
        for k in t.get("khoi", []):
            yield t.get("ten", ""), k


def find_table(doc, title_part):
    for _, k in blocks(doc):
        if k.get("loai") == "bang" and title_part.lower() in str(k.get("tieu_de", "")).lower():
            return k
    return None


def find_text(doc, title_part):
    for _, k in blocks(doc):
        if k.get("loai") == "doan" and title_part.lower() in str(k.get("tieu_de", "")).lower():
            return k.get("dong", [])
    return []


def tone(text):
    t = plain(text)
    if any(w in t for w in ("bo qua", "gap", "het hang", "loi")):
        return "bad"
    if any(w in t for w in ("cho", "trong tuan", "can")):
        return "warn"
    if any(w in t for w in ("da ", "xong", "nhap", "dat")):
        return "good"
    return "mute"


# ---------- đọc dữ liệu ----------

def active_sale():
    cands = [p for p in (ROOT / "output/3-video").glob("*/nguon/lich-dang-video.json")
             if p.parts[-3] != "thu-nghiem"]
    if not cands:
        sys.exit("Chưa có lịch đăng video nào trong output/3-video/<tên-sale>/nguon/")
    p = max(cands, key=lambda x: x.stat().st_mtime)
    return p.parts[-3], json.loads(p.read_text(encoding="utf-8"))


def plan_for(sale):
    folder = ROOT / "output/1-ke-hoach/nguon"
    p = folder / f"ke-hoach-{sale}.json"
    if not p.exists():
        cands = sorted(folder.glob("ke-hoach-*.json"), key=lambda x: x.stat().st_mtime)
        p = cands[-1] if cands else None
    return json.loads(p.read_text(encoding="utf-8")) if p else {}


def sale_calendar():
    wb = openpyxl.load_workbook(ROOT / "data/lich-sale-va-ngan-sach.xlsx", data_only=True)
    ws = wb["Lịch sale"]
    rows, header = [], None
    for r in ws.iter_rows(values_only=True):
        if header is None:
            if r and r[0] and "chương trình" in str(r[0]).lower():
                header = r
            continue
        if not r or not r[0] or not isinstance(r[2], dt.datetime):
            continue
        rows.append({"ten": str(r[0]).strip(), "bat_dau": r[1], "dinh": r[2], "ket_thuc": r[3],
                     "muc": r[6] or "", "gio": r[7] or "", "ghi_chu": r[8] or ""})
    return rows


def products():
    wb = openpyxl.load_workbook(ROOT / "data/san-pham.xlsx", data_only=True)
    ws = wb.worksheets[0]
    head, out = None, []
    for r in ws.iter_rows(values_only=True):
        if head is None:
            if r and "MÃ SP" in [str(x).strip() if x else "" for x in r]:
                head = [str(x).strip() if x else "" for x in r]
            continue
        row = dict(zip(head, r))
        if not row.get("MÃ SP"):
            continue
        out.append(row)
    stock = {}
    wb = openpyxl.load_workbook(ROOT / "data/ton-kho.xlsx", data_only=True)
    for r in wb.worksheets[0].iter_rows(min_row=2, values_only=True):
        if r and r[0]:
            stock[str(r[0]).strip()] = (r[2], r[3])
    return out, stock


def thumb(code):
    src = ROOT / f"data/anh-san-pham/{code}/{code}-1.png"
    if not src.exists():
        return None
    dst = OUT / "sp" / f"{code}.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGBA")
    box = im.getchannel("A").getbbox()
    if box:
        im = im.crop(box)
    im.thumbnail((360, 360), Image.LANCZOS)
    im.save(dst, optimize=True)
    return f"sp/{code}.png"


# ---------- dựng trang ----------

CSS = """
:root{
  /* Phòng điều hành bán hàng: dải đỏ thương hiệu ở trên, lưới thẻ thông tin bên dưới, đọc từ tổng quan tới chi tiết */
  --brand:#C62828; --brand-ink:#8E1414; --gold:#E9A82B;
  --ink:#1F1416; --muted:#6E5D60; --line:#EADFDF; --paper:#FFFFFF; --canvas:#F6F1F1;
  --good:#1E7F4F; --good-bg:#E5F4EC; --warn:#9A6200; --warn-bg:#FFF3D6; --bad:#B3261E; --bad-bg:#FDE7E5; --mute-bg:#EFEAEA;
  --display:"Lexend","Be Vietnam Pro",system-ui,sans-serif; --body:"Be Vietnam Pro",system-ui,-apple-system,"Segoe UI",sans-serif;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --brand:#E0473F; --brand-ink:#FF8A80; --gold:#F2BC52; --ink:#F4ECEC; --muted:#B9A9AB; --line:#3A2C2E; --paper:#211819; --canvas:#171112;
  --good:#6FD39F; --good-bg:#16352A; --warn:#F2BC52; --warn-bg:#3A2E12; --bad:#FF8A80; --bad-bg:#3E1A18; --mute-bg:#2C2223; color-scheme:dark;}}
:root[data-theme="dark"]{
  --brand:#E0473F; --brand-ink:#FF8A80; --gold:#F2BC52; --ink:#F4ECEC; --muted:#B9A9AB; --line:#3A2C2E; --paper:#211819; --canvas:#171112;
  --good:#6FD39F; --good-bg:#16352A; --warn:#F2BC52; --warn-bg:#3A2E12; --bad:#FF8A80; --bad-bg:#3E1A18; --mute-bg:#2C2223; color-scheme:dark;}
*{box-sizing:border-box}
html,body{margin:0}
body{background:var(--canvas);color:var(--ink);font:15px/1.55 var(--body)}
a{color:var(--brand-ink)}
a:focus-visible,button:focus-visible,video:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:var(--display);text-wrap:balance;margin:0}
.num{font-variant-numeric:tabular-nums}
header.top{background:var(--paper);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;gap:14px;flex-wrap:wrap;padding-top:14px;padding-bottom:14px}
.mark{width:38px;height:38px;border-radius:10px;background:var(--brand);display:grid;place-items:center;flex:none}
.brand-name{font-family:var(--display);font-weight:700;font-size:17px;letter-spacing:.02em}
.brand-sub{color:var(--muted);font-size:13px}
.top-links{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.top-links a{text-decoration:none;font-size:13px;font-weight:600;padding:7px 12px;border-radius:999px;border:1px solid var(--line);color:var(--ink);background:var(--paper)}
.top-links a:hover{border-color:var(--brand);color:var(--brand-ink)}
.hero{background:linear-gradient(120deg,#7F1717 0%,#B71C1C 48%,#E53935 100%);color:#fff}
.hero .wrap{display:grid;grid-template-columns:1.4fr 1fr;gap:28px;padding-top:30px;padding-bottom:30px;align-items:center}
.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.85;font-weight:600}
.hero h1{font-size:clamp(30px,5vw,52px);line-height:1.05;margin:6px 0 10px;font-weight:800}
.hero p{margin:0;max-width:60ch;opacity:.92}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:600;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25)}
.chip b{color:var(--gold)}
.count{justify-self:end;text-align:center;background:rgba(0,0,0,.18);border:1px solid rgba(255,255,255,.2);border-radius:20px;padding:18px 26px;min-width:220px}
.count .big{font-family:var(--display);font-size:76px;font-weight:800;line-height:1;color:#FFD27A}
.count .unit{font-size:14px;opacity:.9}
.count .when{margin-top:8px;font-size:13px;opacity:.85}
main .wrap{display:grid;gap:22px;padding-top:24px;padding-bottom:40px}
.grid2{display:grid;grid-template-columns:1.1fr .9fr;gap:22px}
.card{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:20px}
.card h2{font-size:18px;font-weight:700;display:flex;align-items:baseline;gap:10px;margin-bottom:14px}
.card h2 small{font-family:var(--body);font-weight:500;font-size:13px;color:var(--muted)}
.todo{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.todo li{display:grid;grid-template-columns:6px 1fr auto;gap:12px;align-items:start;padding:12px 14px 12px 0;border-radius:12px;background:var(--canvas)}
.todo .stripe{align-self:stretch;border-radius:6px 0 0 6px}
.todo .who{font-size:12.5px;color:var(--muted);margin-top:2px}
.pill{display:inline-block;white-space:nowrap;font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px}
.good{color:var(--good);background:var(--good-bg)} .warn{color:var(--warn);background:var(--warn-bg)}
.bad{color:var(--bad);background:var(--bad-bg)} .mute{color:var(--muted);background:var(--mute-bg)}
.stripe.good{background:var(--good)} .stripe.warn{background:var(--gold)} .stripe.bad{background:var(--bad)} .stripe.mute{background:var(--line)}
.summary{margin:0;padding-left:18px;display:grid;gap:6px}
.videos{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.vcard{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--canvas);display:flex;flex-direction:column}
.vmedia{aspect-ratio:9/16;background:#120b0c;display:grid;place-items:center;position:relative}
.vmedia video{width:100%;height:100%;object-fit:cover;display:block}
.vmedia .wait{color:#c9b8ba;text-align:center;padding:16px;font-size:13px}
.vmedia .wait strong{display:block;font-family:var(--display);font-size:34px;color:#fff;margin-bottom:6px}
.vbody{padding:12px 14px;display:grid;gap:6px}
.vbody h3{font-size:15px}
.vbody .meta{font-size:13px;color:var(--muted)}
details{font-size:13px}
details summary{cursor:pointer;color:var(--brand-ink);font-weight:600}
details p{margin:6px 0 0;white-space:pre-wrap}
.copy{margin-top:6px;font:600 12px var(--body);padding:6px 10px;border-radius:8px;border:1px solid var(--line);background:var(--paper);color:var(--ink);cursor:pointer}
.copy:hover{border-color:var(--brand)}
.sales{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.sales li{display:grid;grid-template-columns:64px 1fr auto;gap:12px;align-items:center;padding:10px 12px;border-radius:12px;border:1px solid var(--line)}
.sales li.now{border-color:var(--brand);box-shadow:inset 4px 0 0 var(--brand)}
.date{text-align:center;line-height:1.1}
.date .d{font-family:var(--display);font-size:24px;font-weight:800}
.date .m{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
.sales .t{font-weight:600}
.sales .s{font-size:12.5px;color:var(--muted)}
.left{font-size:13px;font-weight:700;color:var(--brand-ink);white-space:nowrap}
.prods{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.prod{border:1px solid var(--line);border-radius:14px;padding:12px;display:grid;gap:6px;background:var(--paper)}
.prod .img{aspect-ratio:1;background:radial-gradient(circle at 50% 45%,var(--canvas) 0 60%,transparent 61%);display:grid;place-items:center}
.prod img{max-width:78%;max-height:88%;object-fit:contain}
.prod h3{font-size:14px;font-family:var(--body);font-weight:700}
.price{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
.price .now{font-family:var(--display);font-weight:800;color:var(--brand-ink);font-size:16px}
.price .old{font-size:12px;color:var(--muted);text-decoration:line-through}
.bar{height:6px;border-radius:6px;background:var(--mute-bg);overflow:hidden}
.bar i{display:block;height:100%;border-radius:6px}
.stock{font-size:12px;color:var(--muted);display:flex;justify-content:space-between;gap:6px}
.tags{display:flex;gap:6px;flex-wrap:wrap}
.need{width:100%;border-collapse:collapse;font-size:14px}
.need th{text-align:left;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:600;padding:0 10px 8px 0;border-bottom:1px solid var(--line)}
.need td{padding:10px 10px 10px 0;border-bottom:1px solid var(--line);vertical-align:top}
.need td:last-child{font-weight:600}
.tablebox{overflow-x:auto}
footer{color:var(--muted);font-size:12.5px;padding:0 0 30px}
@media (max-width:980px){.prods{grid-template-columns:repeat(3,1fr)}.videos{grid-template-columns:repeat(2,1fr)}.grid2{grid-template-columns:1fr}}
@media (max-width:640px){.hero .wrap{grid-template-columns:1fr}.count{justify-self:start}.prods{grid-template-columns:repeat(2,1fr)}.videos{grid-template-columns:1fr 1fr}.top-links{margin-left:0}}
@media (max-width:400px){.videos{grid-template-columns:1fr}}
@media (prefers-reduced-motion:no-preference){.vcard,.prod{transition:transform .15s ease}.vcard:hover,.prod:hover{transform:translateY(-2px)}}
"""

JS = """
(function(){
  var el=document.getElementById('countdown'); if(!el) return;
  var peak=new Date(el.dataset.peak+'T00:00:00+07:00');
  function upd(){
    var now=new Date(); var vn=new Date(now.getTime()+ (now.getTimezoneOffset()+420)*60000);
    var today=new Date(vn.getFullYear(),vn.getMonth(),vn.getDate());
    var p=new Date(peak.getTime()+(now.getTimezoneOffset()+420)*60000); p=new Date(p.getFullYear(),p.getMonth(),p.getDate());
    var d=Math.round((p-today)/86400000);
    var big=document.getElementById('cd-big'), unit=document.getElementById('cd-unit');
    if(d>0){big.textContent=d; unit.textContent='ngày nữa';}
    else if(d===0){big.textContent='Hôm nay'; big.style.fontSize='44px'; unit.textContent='là ngày cao điểm';}
    else {big.textContent='Đã qua'; big.style.fontSize='44px'; unit.textContent='đợt sale đã kết thúc';}
  }
  upd();
  document.querySelectorAll('[data-left]').forEach(function(n){
    var t=new Date(n.dataset.left+'T00:00:00'); var now=new Date(); var today=new Date(now.getFullYear(),now.getMonth(),now.getDate());
    var d=Math.round((t-today)/86400000); n.textContent = d>0 ? 'còn '+d+' ngày' : (d===0?'hôm nay':'');
  });
  document.querySelectorAll('.copy').forEach(function(b){
    b.addEventListener('click',function(){
      var txt=document.getElementById(b.dataset.target).textContent;
      if(navigator.clipboard){navigator.clipboard.writeText(txt).then(function(){b.textContent='Đã chép';setTimeout(function(){b.textContent='Chép caption'},1600)},function(){b.textContent='Không chép được, hãy bôi đen để chép'})}
    });
  });
})();
"""


def build():
    sale, vdoc = active_sale()
    pdoc = plan_for(sale)
    today = dt.date.today()
    files = []

    # Đợt sale: lấy ngày cao điểm trong lịch sale nội bộ khớp tên thư mục
    cal = sale_calendar()
    key = plain(sale.replace("-", " "))
    match = next((r for r in cal if key and key in plain(r["ten"])), None)
    peak = match["dinh"].date() if match else None
    sale_name = match["ten"] if match else vdoc.get("tieu_de", sale)

    # Video
    lich = find_table(vdoc, "Lịch đăng video")
    cap = find_table(vdoc, "Caption")
    caps = {str(r[0]).strip(): (r[1], r[2]) for r in (cap or {}).get("dong", [])}
    vids = []
    for r in (lich or {}).get("dong", []):
        code = str(r[0]).split("–")[0].split("-")[0].strip()
        mp4 = ROOT / f"output/3-video/{sale}/{code}.mp4"
        cover = ROOT / f"output/3-video/{sale}/{code}-anh-bia.jpg"
        has = mp4.exists()
        if has:
            files.append({"as": f"video/{code}.mp4", "path": str(mp4)})
            if cover.exists():
                files.append({"as": f"video/{code}-anh-bia.jpg", "path": str(cover)})
        vids.append({"code": code, "ten": str(r[0]), "sp": r[1], "ngay": r[2], "tt": r[4], "ghi": r[5],
                     "has": has, "cover": cover.exists(), "cap": caps.get(code)})
    done = sum(v["has"] for v in vids)

    todo = (find_table(vdoc, "Việc cần làm") or {}).get("dong", [])
    order = {"Gấp": 0, "Trong tuần": 1, "Khi có thể": 2}
    todo = sorted(todo, key=lambda r: order.get(str(r[3]), 3))
    need = (find_table(vdoc, "chỗ đang dùng mặc định") or {}).get("dong", [])
    summary = find_text(vdoc, "Tóm tắt nhanh")
    plan_status = next((s.split("Trạng thái:")[1].strip() for s in pdoc.get("thong_tin", [])
                        if isinstance(s, str) and "Trạng thái:" in s), "Chưa có kế hoạch")
    plan_main = find_text(pdoc, "Tóm tắt nhanh")

    # Lịch sale sắp tới
    upcoming = [r for r in cal if r["ket_thuc"] and r["ket_thuc"].date() >= today][:6]

    # Sản phẩm
    prods, stock = products()
    cards = []
    for p in prods:
        code = str(p["MÃ SP"]).strip()
        img = thumb(code)
        if img:
            files.append({"as": img, "path": str(OUT / img)})
        s = stock.get(code)
        cards.append((p, code, img, s))

    # ---------- HTML ----------
    h = []
    a = h.append
    links = json.loads((ROOT / "cong-cu/trang-claude.json").read_text(encoding="utf-8"))
    a("<!DOCTYPE html><html lang=\"vi\"><head><meta charset=\"utf-8\">")
    a("<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">")
    a("<title>TIVO Tổng quan TikTok</title>")
    a("<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\"><link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>")
    a("<link href=\"https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Lexend:wght@600;700;800&display=swap\" rel=\"stylesheet\">")
    a(f"<style>{CSS}</style></head><body>")

    a("<header class=\"top\"><div class=\"wrap\">")
    a("<div class=\"mark\" aria-hidden=\"true\"><svg width=\"22\" height=\"22\" viewBox=\"0 0 24 24\"><path d=\"M4 5h16v4h-6v11h-4V9H4z\" fill=\"#fff\"/></svg></div>")
    a(f"<div><div class=\"brand-name\">TIVO SMART</div><div class=\"brand-sub\">Bảng điều hành TikTok · cập nhật {esc(day_label(today))}/{today.year}</div></div>")
    a("<nav class=\"top-links\" aria-label=\"Trang chi tiết\">")
    if "ke-hoach" in links:
        a(f"<a href=\"{esc(links['ke-hoach']['url'])}\">Kế hoạch chi tiết</a>")
    if "video" in links:
        a(f"<a href=\"{esc(links['video']['url'])}\">Lịch đăng video chi tiết</a>")
    a("</nav></div></header>")

    # Hero
    a("<section class=\"hero\"><div class=\"wrap\"><div>")
    a("<div class=\"eyebrow\">Đợt sale đang chuẩn bị</div>")
    a(f"<h1>{esc(sale_name)}</h1>")
    if match:
        run = f"Chạy {day_label(match['bat_dau'].date())} – {day_label(match['ket_thuc'].date())}"
        a(f"<p>{esc(run)} · ngày cao điểm <strong>{esc(day_label(peak))}</strong>"
          + (f" · khung giờ chính {esc(match['gio'])}" if match["gio"] else "") + "</p>")
    a("<div class=\"chips\">")
    a(f"<span class=\"chip\">Kế hoạch: <b>{esc(plan_status)}</b></span>")
    a(f"<span class=\"chip\">Video: <b class=\"num\">{done}/{len(vids)}</b> đã xong</span>")
    if match and match["muc"]:
        a(f"<span class=\"chip\">Mức độ: <b>{esc(match['muc'])}</b></span>")
    a("</div></div>")
    if peak:
        d = (peak - today).days
        big, unit = (str(d), "ngày nữa") if d > 0 else (("Hôm nay", "là ngày cao điểm") if d == 0 else ("Đã qua", "đợt sale đã kết thúc"))
        a(f"<div class=\"count\" id=\"countdown\" data-peak=\"{peak.isoformat()}\"><div class=\"big num\" id=\"cd-big\">{esc(big)}</div>"
          f"<div class=\"unit\" id=\"cd-unit\">{esc(unit)}</div><div class=\"when\">đến {esc(day_label(peak))}</div></div>")
    a("</div></section>")

    a("<main><div class=\"wrap\">")
    # Việc cần làm + tóm tắt
    a("<div class=\"grid2\">")
    a(f"<section class=\"card\" aria-labelledby=\"h-todo\"><h2 id=\"h-todo\">Việc cần làm <small>{len(todo)} việc, gấp trước</small></h2><ul class=\"todo\">")
    for r in todo:
        t = {"Gấp": "bad", "Trong tuần": "warn"}.get(str(r[3]), "mute")
        a(f"<li><span class=\"stripe {t}\"></span><div><div>{esc(r[0])}</div><div class=\"who\">{esc(r[1])} · hạn {esc(r[2])}</div></div>"
          f"<span class=\"pill {t}\">{esc(r[3])}</span></li>")
    a("</ul></section>")
    a("<section class=\"card\" aria-labelledby=\"h-sum\"><h2 id=\"h-sum\">Tóm tắt nhanh</h2><ul class=\"summary\">")
    for s in (summary or [])[:5]:
        a(f"<li>{esc(s)}</li>")
    a("</ul>")
    if plan_main:
        a("<h2 style=\"margin-top:18px\">Kế hoạch truyền thông</h2><ul class=\"summary\">")
        for s in plan_main[:3]:
            a(f"<li>{esc(s)}</li>")
        a("</ul>")
    a("</section></div>")

    # Video
    a(f"<section class=\"card\" aria-labelledby=\"h-vid\"><h2 id=\"h-vid\">Chuỗi video {esc(sale_name)} <small>bấm video để xem, nhạc đã có sẵn</small></h2><div class=\"videos\">")
    for i, v in enumerate(vids):
        a("<article class=\"vcard\"><div class=\"vmedia\">")
        if v["has"]:
            poster = f" poster=\"video/{v['code']}-anh-bia.jpg\"" if v["cover"] else ""
            a(f"<video controls preload=\"none\" playsinline{poster} aria-label=\"{esc(v['ten'])}\"><source src=\"video/{v['code']}.mp4\" type=\"video/mp4\"></video>")
        else:
            a(f"<div class=\"wait\"><strong>{esc(v['code'])}</strong>Chưa làm<br>{esc(v['ghi'])}</div>")
        a("</div><div class=\"vbody\">")
        a(f"<h3>{esc(v['ten'])}</h3><div class=\"meta\">{esc(v['ngay'])} · {esc(v['sp'])}</div>")
        a(f"<div><span class=\"pill {tone(v['tt'])}\">{esc(v['tt'])}</span></div>")
        if v["cap"] and v["has"]:
            cid = f"cap-{i}"
            a(f"<details><summary>Caption và hashtag</summary><p id=\"{cid}\">{esc(v['cap'][0])}\n{esc(v['cap'][1])}</p>"
              f"<button class=\"copy\" type=\"button\" data-target=\"{cid}\">Chép caption</button></details>")
        a("</div></article>")
    a("</div></section>")

    # Lịch sale + cần xác nhận
    a("<div class=\"grid2\">")
    a("<section class=\"card\" aria-labelledby=\"h-cal\"><h2 id=\"h-cal\">Lịch sale sắp tới <small>theo lịch sale nội bộ</small></h2><ul class=\"sales\">")
    for r in upcoming:
        d = r["dinh"].date()
        cls = " class=\"now\"" if match and r["ten"] == match["ten"] else ""
        run = f"{r['bat_dau']:%d/%m} – {r['ket_thuc']:%d/%m}" if r["bat_dau"] else ""
        a(f"<li{cls}><div class=\"date\"><div class=\"d num\">{d:%d}</div><div class=\"m\">Th{d.month}</div></div>"
          f"<div><div class=\"t\">{esc(r['ten'])}</div><div class=\"s\">{esc(THU[d.weekday()])} · chạy {esc(run)}"
          + (f" · {esc(r['muc'])}" if r["muc"] else "") + f"</div></div><div class=\"left num\" data-left=\"{d.isoformat()}\"></div></li>")
    a("</ul></section>")
    a(f"<section class=\"card\" aria-labelledby=\"h-need\"><h2 id=\"h-need\">Cần chủ shop xác nhận <small>{len(need)} mục</small></h2><div class=\"tablebox\"><table class=\"need\">")
    a("<thead><tr><th scope=\"col\">Nội dung</th><th scope=\"col\">Đang dùng</th><th scope=\"col\">Cần làm</th></tr></thead><tbody>")
    for r in need:
        a(f"<tr><td>{esc(r[0])}</td><td>{esc(r[1])}</td><td>{esc(r[2])}</td></tr>")
    a("</tbody></table></div></section></div>")

    # Sản phẩm
    a(f"<section class=\"card\" aria-labelledby=\"h-sp\"><h2 id=\"h-sp\">Sản phẩm trong video <small>{len(cards)} mã · giá theo danh mục, tồn kho theo file tồn kho</small></h2><div class=\"prods\">")
    for p, code, img, s in cards:
        a("<article class=\"prod\"><div class=\"img\">")
        a(f"<img src=\"{esc(img)}\" alt=\"{esc(p.get('TÊN SẢN PHẨM'))}\" loading=\"lazy\">" if img else "<span class=\"pill mute\">Chưa có ảnh</span>")
        a(f"</div><h3>{esc(p.get('TÊN SẢN PHẨM'))}</h3>")
        a(f"<div class=\"price\"><span class=\"now num\">{esc(money(p.get('GIÁ BÁN CAMP')) or money(p.get('GIÁ BÁN DAILY')))}</span>"
          f"<span class=\"old num\">{esc(money(p.get('GIÁ NIÊM YẾT')))}</span></div>")
        if s:
            try:
                q, lim = int(float(s[0])), int(float(s[1]))
                pct = max(4, min(100, int(q / max(lim * 3, 1) * 100)))
                t = "bad" if q < lim else "good"
                color = "var(--bad)" if q < lim else "var(--good)"
                a(f"<div class=\"bar\"><i style=\"width:{pct}%;background:{color}\"></i></div>"
                  f"<div class=\"stock\"><span class=\"num\">Tồn {q}</span><span>{'Sắp hết hàng' if q < lim else 'Đủ hàng'}</span></div>")
            except (TypeError, ValueError):
                pass
        link = p.get("LINK TIKTOK")
        a("<div class=\"tags\">" + ("<span class=\"pill good\">Có link TikTok</span>" if link else "<span class=\"pill warn\">Chưa có link TikTok</span>") + "</div>")
        a("</article>")
    a("</div></section>")
    a("</div></main>")
    a(f"<footer><div class=\"wrap\">Giá to là giá bán ngày sale theo danh mục sản phẩm, giá gạch là giá niêm yết. Video chỉ đưa giá sale khi file chốt sale ghi đã xác nhận. "
      f"Trang tự cập nhật sau mỗi lần chạy tác vụ video.</div></footer>")
    a(f"<script>{JS}</script></body></html>")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text("".join(h), encoding="utf-8")
    files.insert(0, {"as": "index.html", "path": str(OUT / "index.html")})
    (OUT / "danh-sach-file.json").write_text(json.dumps(files, ensure_ascii=False, indent=2), encoding="utf-8")
    size = sum(Path(f["path"]).stat().st_size for f in files) / 1e6
    print(f"Đã tạo {OUT / 'index.html'} cho đợt {sale_name}: {done}/{len(vids)} video, {len(cards)} sản phẩm, "
          f"{len(files)} file ({size:.1f} MB). Danh sách để đăng: {OUT / 'danh-sach-file.json'}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    build()
