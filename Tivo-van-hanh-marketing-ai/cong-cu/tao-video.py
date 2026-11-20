"""Dựng video TikTok sale liệt kê nhiều sản phẩm theo mẫu của TIVO SMART.

Quy trình: quy-trinh/3-tao-video-ai.md (phần "Video liệt kê nhiều sản phẩm") và quy-trinh/mau-video-tiktok.md.

Cách chạy (từ thư mục Tivo-van-hanh-marketing-ai):
    python cong-cu/tao-video.py output/3-video/<tên-sale>/nguon/T01-kich-ban.json
    python cong-cu/tao-video.py <kịch bản> --kiem-tra    # chỉ xuất 1 ảnh gồm các khung chính để xem lại

Dòng thời gian (N sản phẩm, mỗi sản phẩm T giây):
    0.0–1.5s nhịp 1 mở · 1.5–3.0s nhịp 2 tem · 3.0s–3.0+N×T nhịp sản phẩm · 2.5s cuối CTA lưới sản phẩm.
    T = 2 giây nếu N ≤ 7, 1.5 giây nếu N từ 8 đến 10; tự giảm để tổng không quá 20 giây.

Mẫu kịch bản: cong-cu/mau-kich-ban.json. Nhận diện cố định (tên shop, username, logo, tem, màu):
cong-cu/thuong-hieu.json. Font Inter nằm trong cong-cu/font.
Kết quả: file MP4 theo "out" (1080x1920, 30fps) và <tên>-anh-bia.jpg lấy từ khung lưới sản phẩm ở nhịp CTA.
Ảnh nền và nhạc tự chọn từ thư viện miễn bản quyền thu-vien/anh/<phong_cach> và thu-vien/nhac/<phong_cach>
(4 video cùng đợt dùng 4 bài nhạc khác nhau, ưu tiên bài ít dùng nhất). Ghi "nhac": false để video im lặng,
hoặc "nhac"/"anh_nen" là đường dẫn file trong thu-vien để tự chọn. Nhật ký dùng: thu-vien/da-dung.json.
Cần: pip install pillow imageio-ffmpeg
"""
import json
import math
import random
import re
import subprocess
import sys
from pathlib import Path

import imageio_ffmpeg
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
MAX_DUR, MAX_SP = 20.0, 10
INTRO, CTA = 3.0, 2.5
SLIDE = 0.3             # thời gian trượt ngang giữa 2 sản phẩm
HERE = Path(__file__).parent
FONTS = {"black": "Inter-Black.ttf", "bold": "Inter-Bold.ttf", "semi": "Inter-SemiBold.ttf"}
SQUEEZE = 0.84          # nén ngang tiêu đề 84%
BEAT = 0.5              # nhịp đập giả định 120 BPM
KIEU = ("T01", "T02a", "T02b", "T03", "T04")
TEXT_FIELDS = ("campaign", "nhip1", "nhip2", "nhip_sp", "cta", "dieu_kien", "san_pham")

# Bố cục, tính theo vùng an toàn TikTok (chừa trên 150px, dưới khoảng 400px, phải khoảng 120px)
CX, CY = 540, 720                  # tâm vùng sản phẩm
PROD_BOX = (640, 640)
ZONE = (80, 390, 1000, 1055)       # vùng sản phẩm, dùng cho lưới CTA
PANEL = (70, 1090, 1010, 1470)     # vùng đặt chữ nền tối
PCY = (PANEL[1] + PANEL[3]) // 2
DK_Y = 1402                        # dòng điều kiện chữ nhỏ trong vùng chữ, phía trên nhãn
LABEL_Y = 1478                     # nhãn nằm trên mép dưới vùng chữ
RIBBON_Y = 318                     # dải {ƯU ĐÃI} ở đầu nhịp sản phẩm
# Không hiện username góc dưới phải: chủ shop yêu cầu bỏ ngày 16/11/2026
TEXT_W = 860

_fonts = {}


def font(kind, size):
    if (kind, size) not in _fonts:
        path = HERE / "font" / FONTS[kind]
        if not path.exists():
            path = Path("C:/Windows/Fonts/arialbd.ttf")
        _fonts[(kind, size)] = ImageFont.truetype(str(path), size)
    return _fonts[(kind, size)]


def rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def clamp(p):
    return min(max(p, 0.0), 1.0)


def seg(t, a, b):
    return clamp((t - a) / (b - a))


def ease(p):
    return 1 - (1 - clamp(p)) ** 3


def back(p):
    p = clamp(p)
    c1 = 1.70158
    return 1 + (c1 + 1) * (p - 1) ** 3 + c1 * (p - 1) ** 2


def bump(t):
    """Đập theo nhịp: 1 ngay đầu mỗi nhịp, giảm về 0 sau 0.15 giây."""
    return max(0.0, 1 - ((t % BEAT) / BEAT) / 0.3)


def shadow(img, radius=8, opacity=110, dy=4):
    pad = radius * 2
    out = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", img.size, (40, 0, 0, 0))
    sh.putalpha(img.getchannel("A").point(lambda v: v * opacity // 255))
    out.paste(sh, (pad, pad + dy), sh)
    out = out.filter(ImageFilter.GaussianBlur(radius))
    out.alpha_composite(img, (pad, pad))
    return out


def fade(img, a):
    if a >= 1:
        return img
    out = img.copy()
    out.putalpha(img.getchannel("A").point(lambda v: int(v * a)))
    return out


def line_img(text, f, color, squeeze=1.0, strike=False):
    asc, desc = f.getmetrics()
    pad = int(f.size * 0.2)
    w, h = int(f.getlength(text)) + 8, asc + desc + pad
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((4, pad + asc), text, font=f, fill=rgb(color), anchor="ls")
    if strike:
        y = pad + asc - f.size * 0.34
        d.line((2, y, w - 2, y), fill=rgb(color), width=max(3, f.size // 11))
    if squeeze != 1:
        img = img.resize((max(1, int(w * squeeze)), h), Image.LANCZOS)
    return img


def wrap(text, f, max_w, squeeze):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if f.getlength(trial) * squeeze <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if len(lines) == 2:                     # chia 2 dòng cho đều, tránh dòng sau chỉ còn 1 chữ
        words = text.split()
        best = min(range(1, len(words)),
                   key=lambda i: max(f.getlength(" ".join(words[:i])), f.getlength(" ".join(words[i:]))))
        lines = [" ".join(words[:best]), " ".join(words[best:])]
    return lines


def text_block(text, kind, size, color, max_w=TEXT_W, max_lines=2, squeeze=1.0, upper=False,
               min_size=26, strike=False, shade=True):
    text = " ".join(str(text).split())
    if upper:
        text = text.upper()
    while True:
        f = font(kind, size)
        lines = wrap(text, f, max_w, squeeze)
        fits = len(lines) <= max_lines and all(f.getlength(x) * squeeze <= max_w for x in lines)
        if fits or size <= min_size:
            break
        size -= 3
    imgs = [line_img(x, f, color, squeeze, strike) for x in lines]
    gap = -int(size * 0.16)
    w = max(i.width for i in imgs)
    h = sum(i.height for i in imgs) + gap * (len(imgs) - 1)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    y = 0
    for i in imgs:
        out.alpha_composite(i, ((w - i.width) // 2, y))
        y += i.height + gap
    out = out.crop(out.getbbox())
    return shadow(out) if shade else out


def pill(text, size, bg, fg, max_w=820):
    t = text_block(text, "black", size, fg, max_w=max_w, max_lines=1, squeeze=0.92, upper=True, shade=False)
    padx, pady = int(size * 0.85), int(size * 0.5)
    w, h = t.width + padx * 2, t.height + pady * 2
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle((0, 0, w - 1, h - 1), radius=h // 2, fill=rgb(bg))
    img.alpha_composite(t, (padx, pady))
    return shadow(img, 10, 120)


def stamp(text, r, bg, fg, shape="tron"):
    """Tem theo phong cách: tron (tròn), sao-no (hình sao nổ), the-gia (thẻ giá), khung-vuong (hình thoi)."""
    s, line = r * 2, max(2, r // 30)
    w, h, cx, text_w = s, s, r, r * 1.4
    if shape == "the-gia":
        w, h = int(r * 2.5), int(r * 1.3)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if shape == "sao-no":
        pts = []
        for i in range(36):
            rr = r if i % 2 == 0 else r * 0.84
            ang = math.pi * i / 18
            pts.append((r + rr * math.cos(ang), r + rr * math.sin(ang)))
        d.polygon(pts, fill=rgb(bg))
        m = r * 0.26
        d.ellipse((m, m, s - m, s - m), outline=rgb(fg), width=line)
        text_w = r * 1.3
    elif shape == "khung-vuong":
        d.polygon([(r, 0), (s, r), (r, s), (0, r)], fill=rgb(bg))
        m = r * 0.14
        d.polygon([(r, m), (s - m, r), (r, s - m), (m, r)], outline=rgb(fg), width=line)
        text_w = r * 1.05
    elif shape == "the-gia":
        k = h * 0.45
        d.polygon([(0, h / 2), (k, 0), (w, 0), (w, h), (k, h)], fill=rgb(bg))
        d.ellipse((k * 0.55 - 9, h / 2 - 9, k * 0.55 + 9, h / 2 + 9), fill=(0, 0, 0, 0))
        d.rectangle((k + 8, 8, w - 9, h - 9), outline=rgb(fg), width=line)
        cx, text_w = (k + w) / 2, w - k - 30
    else:
        d.ellipse((0, 0, s - 1, s - 1), fill=rgb(bg))
        m = int(r * 0.1)
        d.ellipse((m, m, s - 1 - m, s - 1 - m), outline=rgb(fg), width=line)
    t = text_block(text, "black", int(r * 0.42), fg, max_w=int(text_w), max_lines=3, squeeze=0.9,
                   upper=True, min_size=16, shade=False)
    img.alpha_composite(t, (int(cx - t.width / 2), (h - t.height) // 2))
    return shadow(img, 10, 120)


def star(size, color):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    c, k = size / 2, size * 0.12
    ImageDraw.Draw(img).polygon(
        [(c, 0), (c + k, c - k), (size, c), (c + k, c + k), (c, size), (c - k, c + k), (0, c), (c - k, c - k)],
        fill=color + (255,))
    return img


def gradient(th):
    top, bot = rgb(th["nen1"]), rgb(th["nen2"])
    col = Image.new("RGB", (1, H))
    for y in range(H):
        p = y / (H - 1)
        col.putpixel((0, y), tuple(int(top[i] + (bot[i] - top[i]) * p) for i in range(3)))
    return col.resize((W, H))


def background(th, khung="bo-goc"):
    """Lớp trang trí phủ lên nền: sọc mảnh, quầng sáng, khung chữ. Trả về ảnh RGBA trong suốt."""
    bg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lines = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lines)
    for y in range(0, H, 8):
        d.line((0, y, W, y), fill=(255, 255, 255, 10))
    bg.alpha_composite(lines)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    for x, y in ((0, 0), (W, 0), (0, H), (W, H)):
        d.ellipse((x - 260, y - 260, x + 260, y + 260), fill=rgb(th["nhan"]) + (55,))
    d.ellipse((CX - 420, CY - 420, CX + 420, CY + 420), fill=(255, 255, 255, 46))
    bg.alpha_composite(glow.filter(ImageFilter.GaussianBlur(110)))
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(panel)
    x0, y0, x1, y1 = PANEL
    if khung == "vat-goc":                               # khung vát góc
        c = 48
        d.polygon([(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1), (x0 + c, y1),
                   (x0, y1 - c), (x0, y0 + c)], fill=rgb(th["toi2"]) + (170,))
        d.line([(x0 + c, y0), (x1 - c, y0)], fill=rgb(th["nhan"]) + (230,), width=6)
    elif khung == "vien":                                # khung viền màu nhấn
        d.rounded_rectangle(PANEL, radius=28, fill=rgb(th["toi2"]) + (140,), outline=rgb(th["nhan"]) + (235,),
                            width=4)
    else:                                                # khung bo góc
        d.rounded_rectangle(PANEL, radius=44, fill=rgb(th["toi2"]) + (165,))
    bg.alpha_composite(panel)
    return bg


# ---------- Ảnh nền và nhạc miễn bản quyền (thư viện thu-vien/, tải bằng cong-cu/tai-tu-lieu.py) ----------
LIB = HERE.parent / "thu-vien"
USED = LIB / "da-dung.json"
PHOTO_MIX = 0.45                    # độ rõ ảnh nền so với màu sự kiện (0 = chỉ màu, 1 = ảnh gốc)
ZOOM = 1.1                          # ảnh nền to hơn khung 10% để chuyển động phóng chậm
XFADE = 0.4                         # thời gian chuyển giữa 2 ảnh nền


def lib_files(kind, style):
    folder = LIB / kind / style
    ext = (".jpg", ".jpeg", ".png") if kind == "anh" else (".mp3", ".ogg", ".wav", ".flac", ".m4a")
    return sorted(p for p in folder.glob("*") if p.suffix.lower() in ext) if folder.is_dir() else []


def pick_assets(spec, n_photos):
    """Chọn ảnh nền và bài nhạc cho video. Video khác trong cùng đợt sale không trùng nhạc, ít trùng ảnh;
    ưu tiên file ít được dùng nhất từ trước đến nay. Dựng lại đúng video cũ thì giữ nguyên lựa chọn."""
    style = spec.get("phong_cach") or spec.get("bang_mau") or ""
    out = Path(spec["out"]).as_posix()
    folder = Path(spec["out"]).parent.as_posix()
    used = json.loads(USED.read_text(encoding="utf-8")) if USED.exists() else {"anh": {}, "nhac": {}}
    rnd = random.Random(out)

    def choose(kind, count):
        files = [p.relative_to(HERE.parent).as_posix() for p in lib_files(kind, style)]
        log = used.get(kind, {})
        mine = [f for f in files if out in log.get(f, [])]
        if len(mine) >= count:
            return mine[:count]
        sib = {f for f in files for o in log.get(f, []) if o != out and o.rsplit("/", 1)[0] == folder}
        rnd.shuffle(files)
        files.sort(key=lambda f: (f in sib, len(log.get(f, []))))
        return files[:count]

    photos = spec.get("anh_nen")
    if photos is None:
        photos = choose("anh", n_photos)
    music = spec.get("nhac")
    if music is None:
        m = choose("nhac", 1)
        music = m[0] if m else None
    return [p for p in (photos or []) if Path(p).is_file()], (music if music and Path(music).is_file() else None)


def mark_used(spec, photos, music):
    out = Path(spec["out"]).as_posix()
    used = json.loads(USED.read_text(encoding="utf-8")) if USED.exists() else {"anh": {}, "nhac": {}}
    for kind, files in (("anh", photos), ("nhac", [music] if music else [])):
        log = used.setdefault(kind, {})
        for f in log.values():
            if out in f:
                f.remove(out)
        for f in files:
            log.setdefault(Path(f).as_posix(), []).append(out)
    LIB.mkdir(exist_ok=True)
    USED.write_text(json.dumps(used, ensure_ascii=False, indent=1), encoding="utf-8")


def describe_assets(photos, music):
    """Dòng mô tả ảnh nền và nhạc đã dùng, kèm giấy phép, để ghi vào sheet Thông số dựng."""
    lic_path = LIB / "giay-phep.json"
    lic = json.loads(lic_path.read_text(encoding="utf-8")).get("file", {}) if lic_path.exists() else {}

    def one(f):
        x = lic.get(Path(f).as_posix(), {})
        return f"{Path(f).as_posix()} ({x.get('ten', '?')} · {x.get('tac_gia', '?')} · {str(x.get('giay_phep', '?')).upper()})"
    lines = ["Ảnh nền: " + ("; ".join(one(p) for p in photos) if photos else "không có, dùng nền màu")]
    lines.append("Nhạc: " + (one(music) if music else "không có, âm thanh im lặng (chọn nhạc trên TikTok)"))
    return "\n".join(lines)


def prep_photo(path, grad):
    """Ảnh nền phủ màu sự kiện, làm mờ nhẹ để chữ và sản phẩm nổi lên."""
    im = Image.open(path).convert("RGB")
    bw, bh = int(W * ZOOM), int(H * ZOOM)
    s = max(bw / im.width, bh / im.height)
    im = im.resize((max(bw, int(im.width * s)), max(bh, int(im.height * s))), Image.LANCZOS)
    x, y = (im.width - bw) // 2, (im.height - bh) // 2
    im = im.crop((x, y, x + bw, y + bh)).filter(ImageFilter.GaussianBlur(3.5))
    im = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.85)).enhance(0.8)
    return Image.blend(grad.resize((bw, bh)), im, PHOTO_MIX)


def ken_burns(img, p, direction):
    """Phóng chậm (hoặc thu chậm) ảnh nền theo tiến độ p của cảnh."""
    k = (1 / ZOOM) + (1 - 1 / ZOOM) * (1 - p if direction else p)
    cw, ch = img.width * k, img.height * k
    x, y = (img.width - cw) / 2, (img.height - ch) / 2
    return img.resize((W, H), Image.BILINEAR, box=(x, y, x + cw, y + ch))


def resolve_style(brand, spec):
    """Phong cách của sự kiện: màu (đổi theo tháng nếu có), họa tiết, chuyển cảnh, tem, khung, hiệu ứng."""
    key = spec.get("phong_cach") or spec.get("bang_mau") or ""
    st = brand.get("phong_cach", {}).get(key, {})
    mau = dict(st.get("mau", {}))
    by_month, month = st.get("mau_theo_thang"), spec.get("thang")
    if by_month and isinstance(month, int):
        mau.update(by_month.get(str(month), {}) if isinstance(by_month, dict)
                   else by_month[(month - 1) % len(by_month)])
    th = {**brand["mau"], **mau}
    return th, {
        "hoa_tiet": st.get("hoa_tiet", "kim-tuyen"), "chuyen_canh": st.get("chuyen_canh", "truot-ngang"),
        "tem": st.get("tem", "tron"), "khung": st.get("khung", "bo-goc"), "hieu_ung": st.get("hieu_ung", "glitch"),
        "mau_hoa_tiet": st.get("mau_hoa_tiet") or th["nhan"],
    }


def motif(kind, th, color):
    """Họa tiết chuyển động theo sự kiện, vẽ sau nền và trước sản phẩm, chủ yếu ở hai bên mép và phía dưới."""
    rnd = random.Random(11)
    acc, white = rgb(color), (255, 255, 255)

    def margin_x():
        return rnd.randrange(20, 150) if rnd.random() < 0.5 else rnd.randrange(930, 1060)

    def sprite(w, h, draw):
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw(ImageDraw.Draw(img), w, h)
        return img

    if kind == "kim-tuyen":                             # kim tuyến rơi
        cols = [acc, white, rgb(th["kem"])]
        parts = [(margin_x(), rnd.uniform(0, H), rnd.uniform(110, 240), rnd.uniform(0, 6.28),
                  sprite(16, 7, lambda d, w, h, c=cols[i % 3]: d.rectangle((0, 0, w, h), fill=c + (230,))))
                 for i in range(28)]

        def draw(frame, t):
            for x, y0, v, ph, img in parts:
                y = (y0 + v * t) % (H + 40) - 20
                put(frame, img, x + 14 * math.sin(t * 2 + ph), y, 0.85, rot=(t * 200 + ph * 57) % 360)
    elif kind == "vong-tron":                           # bong bóng nổi lên
        parts = []
        for _ in range(18):
            r = rnd.randrange(10, 34)
            img = sprite(r * 2 + 4, r * 2 + 4, lambda d, w, h: (d.ellipse((2, 2, w - 3, h - 3), outline=acc + (200,),
                                                                           width=3),
                                                                d.ellipse((w * .3, h * .25, w * .45, h * .4),
                                                                          fill=white + (160,))))
            parts.append((margin_x(), rnd.uniform(0, H), rnd.uniform(60, 140), rnd.uniform(0, 6.28), img))

        def draw(frame, t):
            for x, y0, v, ph, img in parts:
                y = H + 40 - (y0 + v * t) % (H + 80)
                put(frame, img, x + 18 * math.sin(t * 1.5 + ph), y, 0.75)
    elif kind == "dong-xu":                             # đồng xu vàng rơi, xoay
        coin = sprite(44, 44, lambda d, w, h: (d.ellipse((0, 0, w - 1, h - 1), fill=acc + (255,)),
                                               d.ellipse((7, 7, w - 8, h - 8), outline=(140, 90, 0, 255), width=3)))
        parts = [(margin_x(), rnd.uniform(0, H), rnd.uniform(180, 320), rnd.uniform(0, 6.28), rnd.uniform(.6, 1.1))
                 for _ in range(16)]

        def draw(frame, t):
            for x, y0, v, ph, k in parts:
                y = (y0 + v * t) % (H + 60) - 30
                put(frame, coin, x, y, 0.9, k, sy=max(abs(math.cos(t * 5 + ph)), 0.08))
    elif kind == "tia-sang":                            # vệt sáng chéo quét qua nền
        band = Image.new("RGBA", (1700, 90), (0, 0, 0, 0))
        bd = ImageDraw.Draw(band)
        for y in range(90):
            bd.line((0, y, 1700, y), fill=acc + (int(70 * (1 - abs(y - 45) / 45)),))
        band = band.rotate(28, Image.BICUBIC, expand=True)

        def draw(frame, t):
            for i in range(3):
                p = ((t + i * 0.8) % 2.4) / 2.4
                put(frame, band, -500 + p * 2100, 300 + i * 520, 0.9)
    elif kind == "luoi-neon":                           # lưới neon phối cảnh phía dưới
        top = 1500
        def draw(frame, t):
            layer = Image.new("RGBA", (W, H - top), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            for i in range(-8, 9):
                d.line((540 + i * 40, 0, 540 + i * 260, H - top), fill=acc + (110,), width=2)
            for k in range(8):
                p = ((k + t * 1.2) % 8) / 8
                y = (H - top) * p * p
                d.line((0, y, W, y), fill=acc + (int(40 + 120 * p),), width=2)
            frame.paste(layer, (0, top), layer)
            for side in (60, 1020):                      # 2 vạch neon dọc hai bên
                ImageDraw.Draw(frame).line((side, 380, side, 1460), fill=tuple(int(c * .6) for c in acc), width=3)
    elif kind == "tuyet":                               # tuyết rơi
        flakes = {}
        for sz in (6, 9, 13):
            flakes[sz] = sprite(sz, sz, lambda d, w, h: d.ellipse((0, 0, w - 1, h - 1), fill=white + (235,)))
        parts = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(60, 160), rnd.uniform(0, 6.28),
                  rnd.choice((6, 9, 13))) for _ in range(46)]

        def draw(frame, t):
            for x, y0, v, ph, sz in parts:
                y = (y0 + v * t) % (H + 20) - 10
                put(frame, flakes[sz], x + 20 * math.sin(t + ph), y, 0.55 + sz / 30)
    elif kind == "phao-hoa":                            # pháo hoa nổ ở góc trên và phía dưới
        dot = sprite(10, 10, lambda d, w, h: d.ellipse((0, 0, w - 1, h - 1), fill=acc + (255,)))
        dot2 = sprite(8, 8, lambda d, w, h: d.ellipse((0, 0, w - 1, h - 1), fill=white + (255,)))
        spots = [(150, 360), (930, 330), (170, 1580), (900, 1640), (540, 1760)]

        def draw(frame, t):
            for i in range(4):
                cyc = (t + i * 0.45) / 1.8
                p = cyc % 1
                x, y = spots[(int(cyc) + i) % len(spots)]
                rr, a = 120 * ease(p), 1 - p
                for k in range(14):
                    ang = 2 * math.pi * k / 14 + i
                    put(frame, dot if k % 2 else dot2, x + rr * math.cos(ang), y + rr * math.sin(ang), a)
    else:                                               # hoa: cánh hoa bay chéo
        petal = sprite(30, 16, lambda d, w, h: d.ellipse((0, 0, w - 1, h - 1), fill=acc + (235,)))
        parts = [(margin_x(), rnd.uniform(0, H), rnd.uniform(70, 150), rnd.uniform(0, 6.28)) for _ in range(20)]

        def draw(frame, t):
            for x0, y0, v, ph in parts:
                y = (y0 + v * t) % (H + 40) - 20
                put(frame, petal, x0 + 30 * math.sin(t * 1.3 + ph), y, 0.85,
                    rot=(t * 90 + ph * 57) % 360)
    return draw


def transition(kind, p_in, p_out):
    """Chuyển khung sản phẩm: trả về (dx, dy, tỉ lệ, độ rõ)."""
    if kind == "truot-doc":
        return 0, 520 * (1 - p_in) - 520 * p_out, 1, min(1, p_in * 1.6) * (1 - p_out)
    if kind == "phong-to":
        return 0, 0, (0.6 + 0.4 * p_in) * (1 + 0.45 * p_out), p_in * (1 - p_out)
    return W * (1 - p_in) - W * p_out, 0, 1, 1


def scene_fx(frame, kind, k, rnd):
    """Hiệu ứng chuyển cảnh trước nhịp sản phẩm: glitch RGB, chớp sáng hoặc rung khung."""
    if kind == "chop-sang":
        return Image.blend(frame, Image.new("RGB", (W, H), (255, 255, 255)), 0.55 * k)
    if kind == "rung":
        out = frame.copy()
        out.paste(frame, (int(rnd.uniform(-22, 22) * k), int(rnd.uniform(-22, 22) * k)))
        return out
    return glitch(frame, k, rnd)


def load_png(path, box):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())
    s = min(box[0] / im.width, box[1] / im.height)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)


def put(frame, img, cx, cy, a=1.0, s=1.0, blur=0.0, rot=0.0, sy=1.0):
    if img is None or a <= 0.01 or s <= 0.01 or sy <= 0.01:
        return
    if s != 1 or sy != 1:
        img = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s * sy))), Image.BICUBIC)
    if rot:
        img = img.rotate(rot, Image.BICUBIC, expand=True)
    if blur > 0.5:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    img = fade(img, a)
    frame.paste(img, (int(cx - img.width / 2), int(cy - img.height / 2)), img)


def stack(items, top, bottom, gap=16):
    """Xếp dọc các ảnh vào giữa khoảng top–bottom, tự thu nhỏ nếu không vừa."""
    items = [i for i in items if i is not None]
    total = sum(i.height for i in items) + gap * (len(items) - 1)
    if total > bottom - top:
        k = (bottom - top - gap * (len(items) - 1)) / sum(i.height for i in items)
        items = [i.resize((max(1, int(i.width * k)), max(1, int(i.height * k))), Image.LANCZOS) for i in items]
        total = sum(i.height for i in items) + gap * (len(items) - 1)
    y = top + (bottom - top - total) / 2
    out = []
    for i in items:
        out.append((i, y + i.height / 2))
        y += i.height + gap
    return out


def draw_group(frame, group, cx=540, a=1.0, s=1.0, dy=0.0, blur=0.0, center=PCY):
    for img, cy in group:
        put(frame, img, cx, center + (cy - center) * s + dy, a, s, blur)


def glitch(frame, k, rnd):
    dx = int(16 * k) + 2
    r, g, b = frame.split()
    frame = Image.merge("RGB", (ImageChops.offset(r, dx, 0), g, ImageChops.offset(b, -dx, 0)))
    for _ in range(4):
        y, h = rnd.randrange(0, H - 90), rnd.randrange(16, 80)
        band = frame.crop((0, y, W, y + h))
        frame.paste(ImageChops.offset(band, rnd.randrange(-40, 41), 0), (0, y))
    return frame


def money(v):
    return f"{int(v):,}".replace(",", ".") + "đ"


def timing(spec):
    """Trả về (giây mỗi sản phẩm, tổng độ dài) theo số sản phẩm, không quá 20 giây."""
    n = len(spec["san_pham"])
    per = float(spec.get("giay_moi_sp") or (2 if n <= 7 else 1.5))
    per = min(per, (MAX_DUR - INTRO - CTA) / n)
    return per, INTRO + n * per + CTA


def grid_cells(n):
    zw, zh = ZONE[2] - ZONE[0], ZONE[3] - ZONE[1]

    def size(c):                                         # ảnh sản phẩm phần lớn dáng cao (rộng ≈ 0.45 cao)
        r = math.ceil(n / c)
        return min(zh / r, zw / c / 0.45)

    cols = max(range(1, n + 1), key=size)
    rows = math.ceil(n / cols)
    cw, ch = (ZONE[2] - ZONE[0]) / cols, (ZONE[3] - ZONE[1]) / rows
    cells = []
    for i in range(n):
        r, c = divmod(i, cols)
        in_row = min(cols, n - r * cols)                # hàng cuối thiếu thì căn giữa
        x0 = ZONE[0] + (ZONE[2] - ZONE[0] - in_row * cw) / 2
        cells.append((x0 + (c + 0.5) * cw, ZONE[1] + (r + 0.5) * ch))
    return cells, (cw * 0.86, ch * 0.86)


def check(spec):
    """Dừng nếu kịch bản sai: thiếu mục, còn ô trống {…} [X], '@' trống, hoặc ảnh không có thật."""
    errors, warns = [], []
    if spec.get("kieu") not in KIEU:
        errors.append(f"kieu phải là một trong {', '.join(KIEU)}")
    for key in ("out", "campaign", "nhip1", "nhip2", "nhip_sp", "cta"):
        if not spec.get(key):
            errors.append(f"thiếu mục {key}")
    sp = spec.get("san_pham")
    if not isinstance(sp, list) or not sp:
        errors.append("san_pham rỗng, cần ít nhất 1 sản phẩm")
        sp = []
    if len(sp) > MAX_SP:
        errors.append(f"san_pham có {len(sp)} sản phẩm, tối đa {MAX_SP}. Ghi các sản phẩm còn lại vào Cần xác nhận")
    for i, p in enumerate(sp, 1):
        name = p.get("ten_sp") or p.get("ma_sp") or f"sản phẩm {i}"
        if not p.get("ten_sp"):
            errors.append(f"sản phẩm {i} thiếu ten_sp")
        if not p.get("anh") or not Path(p["anh"]).exists():
            errors.append(f"{name}: không thấy ảnh {p.get('anh')}")
        if p.get("gia_campaign") and not p.get("gia_niem_yet"):
            errors.append(f"{name}: có gia_campaign thì phải có gia_niem_yet")
        if not p.get("dong_phu") and not p.get("gia_niem_yet"):
            errors.append(f"{name}: cần gia_niem_yet hoặc dong_phu")
        if len(str(p.get("ten_sp", ""))) > 44:
            warns.append(f"tên {name} dài hơn 2 dòng x 22 ký tự, nên rút gọn")
    if spec.get("kieu") == "T04" and not isinstance(spec.get("con_ngay"), int):
        errors.append("T04 cần con_ngay là số ngày còn lại")
    if spec.get("kieu") == "T02a" and not isinstance(spec.get("mua_x"), int):
        errors.append("T02a cần mua_x là số sản phẩm phải mua")
    brand = json.loads((HERE / "thuong-hieu.json").read_text(encoding="utf-8"))
    styles = [k for k in brand.get("phong_cach", {}) if not k.startswith("_")]
    key = spec.get("phong_cach") or spec.get("bang_mau")
    if not key:
        errors.append(f"thiếu phong_cach, chọn một trong: {', '.join(styles)}")
    elif key not in styles:
        errors.append(f"không có phong cách {key} trong cong-cu/thuong-hieu.json, chọn một trong: {', '.join(styles)}")
    elif brand["phong_cach"][key].get("mau_theo_thang") and not isinstance(spec.get("thang"), int):
        errors.append(f"phong cách {key} đổi màu theo tháng, cần ghi \"thang\" là số tháng của ngày cao điểm")

    if brand.get("che_do") == "quang-ba":                # tài khoản TikTok thường: không kêu gọi mua, không giá campaign
        banned = brand.get("tu_cam_quang_ba", [])

        def scan(v, path):
            if isinstance(v, str):
                for w in banned:
                    if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", v, re.IGNORECASE):
                        errors.append(f"video chỉ quảng bá, không được ghi \"{w}\" ở {path}: {v}")
            elif isinstance(v, dict):
                for k, x in v.items():
                    if k not in ("anh", "ma_sp"):
                        scan(x, f"{path}.{k}")
            elif isinstance(v, list):
                for i, x in enumerate(v):
                    scan(x, f"{path}[{i}]")

        for key in TEXT_FIELDS:
            scan(spec.get(key), key)
        for p in sp:
            if p.get("gia_campaign"):
                errors.append(f"{p.get('ten_sp')}: video chỉ quảng bá, gia_campaign phải để null (chỉ hiện giá niêm yết)")
        if spec.get("kieu") == "T02a":
            errors.append("video chỉ quảng bá không dùng mẫu T02a (mua X tặng Y), dùng T02b")

    music = spec.get("nhac")
    if music not in (None, False) and not (isinstance(music, str) and Path(music).is_file()):
        errors.append(f"không thấy file nhạc {music}. Bỏ trường nhac để công cụ tự chọn, hoặc ghi false để im lặng")
    for f in spec.get("anh_nen") or []:
        if not Path(f).is_file():
            errors.append(f"không thấy ảnh nền {f}")
    if key in styles:
        if not lib_files("anh", key):
            warns.append(f"thư viện chưa có ảnh nền cho phong cách {key}, video dùng nền màu. Ghi vào Cần xác nhận")
        if not lib_files("nhac", key) and music is None:
            warns.append(f"thư viện chưa có nhạc cho phong cách {key}, video im lặng. Ghi vào Cần xác nhận")

    def walk(v, path):
        if isinstance(v, str):
            if re.search(r"[{}\[\]]", v) or re.search(r"(^|\s)@(\s|$)", v):
                errors.append(f"còn ô trống chưa điền ở {path}: {v}")
        elif isinstance(v, dict):
            for k, x in v.items():
                if k != "anh":
                    walk(x, f"{path}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, f"{path}[{i}]")

    for key in TEXT_FIELDS:
        walk(spec.get(key), key)
    for key in ("nhip1", "nhip2", "nhip_sp", "cta"):
        title = str((spec.get(key) or {}).get("tieu_de", ""))
        if len(title) > 36:
            warns.append(f"tiêu đề {key} dài {len(title)} ký tự, nên tối đa 2 dòng x 18 ký tự: {title}")
    if sp and not errors:
        per, dur = timing(spec)
        if spec.get("giay_moi_sp") and per < float(spec["giay_moi_sp"]):
            warns.append(f"giảm còn {per:.2f} giây mỗi sản phẩm để video không quá {MAX_DUR:g} giây")
    return errors, warns


def build(spec):
    brand = json.loads((HERE / "thuong-hieu.json").read_text(encoding="utf-8"))
    th, style = resolve_style(brand, spec)
    kieu = spec["kieu"]
    n1, n2, nsp, cta = spec["nhip1"], spec["nhip2"], spec["nhip_sp"], spec["cta"]
    chu, kem, nhan, toi2 = th["chu"], th["kem"], th["nhan"], th["toi2"]
    sp = spec["san_pham"]
    n = len(sp)
    per, dur = timing(spec)
    c0 = INTRO + n * per                   # mốc bắt đầu CTA

    def title(text, size=88):
        return text_block(text, "black", size, chu, squeeze=SQUEEZE, upper=True, min_size=52)

    def sub(text, size=42):
        return text_block(text, "semi", size, kem, max_lines=2) if text else None

    grad = gradient(th)
    deco = background(th, style["khung"])
    # Ảnh nền đổi theo cảnh: mở đầu, nhịp sản phẩm (chia 2 đoạn), CTA
    marks = [0.0, INTRO, INTRO + n * per / 2, c0, dur]
    photo_paths, music = pick_assets(spec, len(marks) - 1)
    photos = [prep_photo(p, grad) for p in photo_paths]
    plain = grad.convert("RGBA")
    plain.alpha_composite(deco)
    plain = plain.convert("RGB")

    def bg_at(t):
        if not photos:
            return plain.copy()
        i = max(k for k in range(len(marks) - 1) if t >= marks[k] or k == 0)
        a, b = marks[i], marks[i + 1]
        img = ken_burns(photos[i % len(photos)], seg(t, a, b + XFADE), i % 2 == 0)
        if i + 1 < len(marks) - 1 and t > b - XFADE:         # chuyển mờ sang ảnh cảnh sau
            nxt = ken_burns(photos[(i + 1) % len(photos)], seg(t, b, marks[i + 2] + XFADE), (i + 1) % 2 == 0)
            img = Image.blend(img, nxt, seg(t, b - XFADE, b))
        img = img.convert("RGBA")
        img.alpha_composite(deco)
        return img.convert("RGB")
    draw_motif = motif(style["hoa_tiet"], th, style["mau_hoa_tiet"])
    logo_path = Path(brand.get("logo") or "")
    logo = (shadow(load_png(logo_path, (400, 110)), 8, 90) if logo_path.is_file()
            else text_block(brand["ten_shop"], "black", 64, chu, squeeze=SQUEEZE, upper=True))
    camp_pill = pill(spec["campaign"], 30, nhan, toi2)
    guide = Image.new("RGBA", (6, 60), (0, 0, 0, 0))
    for y in range(60):
        ImageDraw.Draw(guide).line((0, y, 5, y), fill=rgb(nhan) + (int(200 * (1 - y / 60)),))
    mascot_path = Path(brand.get("linh_vat") or "")
    mascot = load_png(mascot_path, (220, 220)) if mascot_path.is_file() else None
    seal = stamp("CHÍNH HÃNG", 70, kem, th["toi"], style["tem"]) if brand.get("tem_chinh_hang") else None

    # Ảnh sản phẩm: cỡ lớn cho khung từng sản phẩm, cỡ nhỏ cho lưới CTA
    big = [shadow(load_png(p["anh"], PROD_BOX), 18, 90, dy=14) for p in sp]
    cells, cell_box = grid_cells(n)
    thumbs = [shadow(load_png(p["anh"], (int(cell_box[0]), int(cell_box[1]))), 10, 80, dy=8) for p in sp]

    # Cụm ảnh mở đầu: tối đa 3 sản phẩm đầu
    hero = []
    if n == 1:
        hero = [(big[0], CX, CY)]
    elif n == 2:
        hero = [(shadow(load_png(sp[i]["anh"], (420, 560)), 16, 90, dy=12), x, CY) for i, x in ((0, 360), (1, 720))]
    else:
        side = [shadow(load_png(sp[i]["anh"], (360, 470)), 16, 90, dy=12) for i in (1, 2)]
        hero = [(side[0], 290, CY + 40), (side[1], 790, CY + 40),
                (shadow(load_png(sp[0]["anh"], (470, 620)), 18, 90, dy=14), CX, CY)]

    # Chữ nhịp 1, nhịp 2, CTA
    g1 = stack([title(n1["tieu_de"]), sub(n1.get("phu"))], PANEL[1], PANEL[3])
    s2 = sub(n2.get("phu"))
    g2 = stack([title(n2["tieu_de"]), s2], PANEL[1], PANEL[3])
    hl = None
    if s2 is not None:
        hl = Image.new("RGBA", (s2.width + 30, s2.height - 4), (0, 0, 0, 0))
        ImageDraw.Draw(hl).rounded_rectangle((0, 0, hl.width - 1, hl.height - 1), radius=hl.height // 2,
                                             fill=rgb(nhan) + (70,))
    gc = stack([title(cta["tieu_de"]), sub(cta.get("phu"))], PANEL[1], PANEL[3] - 30)
    ribbon = pill(nsp["tieu_de"], 40, nhan, toi2, max_w=560)
    dk = text_block(spec["dieu_kien"], "semi", 22, kem, max_w=880, max_lines=2, min_size=18) \
        if spec.get("dieu_kien") else None
    label_sp = pill(nsp["nhan"], 34, nhan, toi2) if nsp.get("nhan") else None
    label_end = pill(cta["nhan_cuoi"], 34, nhan, toi2)

    # Chữ từng khung sản phẩm: tên + giá, hoặc tên + dòng phụ (USP ở T03, MUA X TẶNG Y ở T02a)
    frames_sp = []
    for i, p in enumerate(sp):
        items, price = [text_block(p["ten_sp"], "black", 66, chu, max_w=860, squeeze=SQUEEZE, upper=True,
                                   min_size=40)], None
        if p.get("dong_phu"):
            items.append(pill(p["dong_phu"], 40, nhan, toi2) if kieu == "T02a"
                         else text_block(p["dong_phu"], "semi", 44, kem, max_lines=2))
        elif p.get("gia_campaign"):
            old = text_block(money(p["gia_niem_yet"]), "semi", 40, kem, max_w=360, max_lines=1, strike=True)
            new = text_block(money(p["gia_campaign"]), "black", 92, nhan, max_w=500, max_lines=1, squeeze=SQUEEZE)
            price = Image.new("RGBA", (old.width + new.width + 24, max(old.height, new.height)), (0, 0, 0, 0))
            price.alpha_composite(old, (0, (price.height - old.height) // 2 + 8))
            price.alpha_composite(new, (old.width + 24, (price.height - new.height) // 2))
            items.append(price)
        else:
            lab = text_block("Giá niêm yết", "semi", 34, kem, max_w=300, max_lines=1)
            val = text_block(money(p["gia_niem_yet"]), "black", 70, chu, max_w=500, max_lines=1, squeeze=SQUEEZE)
            price = Image.new("RGBA", (lab.width + val.width + 20, max(lab.height, val.height)), (0, 0, 0, 0))
            price.alpha_composite(lab, (0, (price.height - lab.height) // 2 + 6))
            price.alpha_composite(val, (lab.width + 20, (price.height - val.height) // 2))
            items.append(price)
        group = stack(items, PANEL[1] + 10, DK_Y - 30 if dk is not None else PANEL[3] - 30, gap=10)
        counter = pill(f"{i + 1}/{n}", 28, chu, toi2)
        frames_sp.append((group, price, counter))

    # Tem nhịp 2
    stamps = []
    tem = n2.get("tem")
    if kieu == "T03" and isinstance(tem, list):
        targets = [(CX - 330, CY + 170), (CX + 330, CY - 170)]
        stamps = [(stamp(x, 108, nhan, toi2, style["tem"]), targets[i]) for i, x in enumerate(tem[:2])]
    elif tem:
        stamps = [(stamp(str(tem), 118, nhan, toi2, style["tem"]), (CX + 280, CY - 250))]

    big_num = (text_block(str(spec["con_ngay"]), "black", 560, nhan, max_w=900, max_lines=1, squeeze=SQUEEZE)
               if kieu == "T04" else None)

    def frame_at(t, fi=0):
        frame = bg_at(t)
        draw_motif(frame, t)                             # họa tiết riêng của sự kiện
        if mascot is not None:
            put(frame, mascot, 160, 1700 - 14 * abs(math.sin(math.pi * t / BEAT)))

        # Đầu khung: logo, tên campaign, đường sáng dẫn mắt, tem chính hãng
        p = ease(seg(t, 0, 0.4))
        put(frame, logo, 540, 128 - 40 * (1 - p), p)
        put(frame, camp_pill, 540, 222 - 30 * (1 - p), p)
        if t < INTRO or t >= c0:
            put(frame, guide, 540, 292, p)
        if seal is not None:
            put(frame, seal, 120, 330, p, rot=-t * 14)

        # Nhịp 1 và 2: cụm ảnh mở đầu (T04: số ngày cỡ to ở nhịp 1)
        if t < INTRO + 0.15:
            p_in = ease(seg(t, 0, 0.4))
            out = ease(seg(t, 2.9, 3.1))
            a = p_in * (1 - out)
            if big_num is not None and t < 1.6:
                a *= seg(t, 1.35, 1.6)
            s = (1 + 0.04 * seg(t, 0.4, 1.5) + 0.05 * back(seg(t, 1.5, 1.8))) * (1 - 0.3 * out)
            for img, x, y in hero:
                put(frame, img, CX + (x - CX) * s, y - 70 * (1 - p_in) - 20 * seg(t, 0.4, 1.5), a, s,
                    18 * (1 - p_in))
        if big_num is not None and 0.2 <= t < 1.65:
            p = back(seg(t, 0.2, 0.5))
            put(frame, big_num, CX, CY, seg(t, 0.2, 0.35) * (1 - seg(t, 1.4, 1.6)),
                (0.6 + 0.4 * p) * (1 + 0.08 * bump(t)))
        if 1.5 <= t < 3.1:                               # tem nhịp 2 xoay -200° → 0°
            out = ease(seg(t, 2.85, 3.05))
            for img, (tx, ty) in stamps:
                p = ease(seg(t, 1.5, 1.95))
                b = back(seg(t, 1.5, 1.95))
                put(frame, img, CX + (tx - CX) * b, CY + (ty - CY) * b, seg(t, 1.5, 1.6) * (1 - out),
                    (0.3 + 0.7 * p) * (1 - 0.4 * out), rot=-200 * (1 - p))

        # Nhịp sản phẩm: mỗi sản phẩm 1 khung, chuyển khung theo phong cách sự kiện
        if INTRO <= t < c0 + 0.05:
            for i, (group, price, counter) in enumerate(frames_sp):
                si = INTRO + i * per
                start = si - SLIDE if i else si
                if not start <= t < si + per + 0.05:
                    continue
                last = i == n - 1
                p_in = ease(seg(t, start, start + SLIDE))
                p_out = 0 if last else ease(seg(t, si + per - SLIDE, si + per))
                dx, dy, ts, ta = transition(style["chuyen_canh"], p_in, p_out)
                a_last = (1 - ease(seg(t, c0 - SLIDE, c0)) if last else 1) * ta
                s_last = 1 - 0.3 * ease(seg(t, c0 - SLIDE, c0)) if last else 1
                pop = 1 + 0.03 * math.sin(math.pi * seg(t, si, si + per))
                put(frame, big[i], CX + dx, CY + dy, a_last, pop * s_last * ts)
                txt_s, txt_a = 1 + (ts - 1) * 0.3, a_last
                if style["chuyen_canh"] != "truot-ngang":    # chữ cũ tắt hẳn rồi chữ mới mới hiện, không chồng nhau
                    txt_a = (1 - ease(seg(t, c0 - SLIDE, c0)) if last else 1) * \
                        (clamp(2 * p_in - 1) if i else 1) * clamp(1 - 2 * p_out)
                for img, y in group:
                    s = 1 + 0.12 * math.sin(math.pi * seg(t, si + 0.3, si + 0.6)) if img is price else 1
                    put(frame, img, 540 + dx, y + dy * 0.35, txt_a, s * txt_s)
                if si - 0.05 <= t < si + per - 0.05 or (last and t < c0):
                    put(frame, counter, 950, RIBBON_Y, a_last, back(seg(t, si - 0.05, si + 0.2)))
            a = seg(t, INTRO, INTRO + 0.2) * (1 - seg(t, c0 - 0.2, c0))
            put(frame, ribbon, 540, RIBBON_Y, a, 0.7 + 0.3 * back(seg(t, INTRO, INTRO + 0.35)))
            if dk is not None:
                put(frame, dk, 540, DK_Y, a)

        # CTA: lưới ảnh tất cả sản phẩm
        if t >= c0 - 0.1:
            for k, (img, (x, y)) in enumerate(zip(thumbs, cells)):
                d = c0 + min(0.06 * k, 0.6)
                put(frame, img, x, y, seg(t, d, d + 0.12), back(seg(t, d, d + 0.35)) * (1 + 0.04 * bump(t)))

        # Vùng chữ
        if 0.2 <= t < 1.65:
            p_in, p_out = ease(seg(t, 0.2, 0.45)), seg(t, 1.4, 1.6)
            draw_group(frame, g1, a=p_in * (1 - p_out), dy=40 * (1 - p_in), blur=14 * p_out)
        if 1.5 <= t < 3.1:
            p_out = ease(seg(t, 2.85, 3.05))
            s = (0.85 + 0.15 * back(seg(t, 1.5, 1.8))) * (1 - 0.4 * p_out)
            a = seg(t, 1.5, 1.65) * (1 - p_out)
            if hl is not None:
                put(frame, hl, 540, PCY + (g2[1][1] - PCY) * s, a * seg(t, 1.9, 2.2), s)
            draw_group(frame, g2, a=a, s=s)
        if t >= c0:
            draw_group(frame, gc, a=seg(t, c0, c0 + 0.15), s=0.8 + 0.2 * back(seg(t, c0, c0 + 0.3)))

        # Nhãn: hiện từ nhịp sản phẩm, lật dọc 0.2 giây thành nhãn cuối ở 1 giây cuối
        flip = dur - 1.0
        if t >= INTRO + 0.2 and (label_sp is not None or t >= flip):
            if t < flip:
                blink = 1.0 if kieu != "T04" or t >= c0 or (t % BEAT) < BEAT * 0.6 else 0.35
                put(frame, label_sp, 540, LABEL_Y, seg(t, INTRO + 0.2, INTRO + 0.35) * blink,
                    back(seg(t, INTRO + 0.2, INTRO + 0.45)))
            elif t < flip + 0.2:
                p = seg(t, flip, flip + 0.2)
                put(frame, label_sp if p < 0.5 and label_sp is not None else label_end, 540, LABEL_Y,
                    sy=max(abs(math.cos(math.pi * p)), 0.02))
            else:
                put(frame, label_end, 540, LABEL_Y, s=1 + 0.08 * bump(t))

        k = math.sin(math.pi * seg(t, 2.9, 3.15))         # hiệu ứng chuyển cảnh 0.25 giây trước nhịp sản phẩm
        if k > 0.05:
            frame = scene_fx(frame, style["hieu_ung"], k, random.Random(fi))
        return frame

    return frame_at, per, dur, photo_paths, music


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit("Cách dùng: python cong-cu/tao-video.py <file-kich-ban.json> [--kiem-tra]")
    spec = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    errors, warns = check(spec)
    for w in warns:
        print("Lưu ý:", w)
    if errors:
        sys.exit("Kịch bản chưa đúng:\n- " + "\n- ".join(errors))
    frame_at, per, dur, photos, music = build(spec)
    n = len(spec["san_pham"])
    out = Path(spec["out"])
    out.parent.mkdir(parents=True, exist_ok=True)
    cover_t = dur - 0.5

    if "--kiem-tra" in sys.argv:
        times = [0.9, 2.4] + [INTRO + i * per + per * 0.55 for i in range(n)] + [cover_t]
        cols = 5 if len(times) > 8 else 4
        rows = math.ceil(len(times) / cols)
        tw, tht = 270, 480
        sheet = Image.new("RGB", (cols * (tw + 10) + 10, rows * (tht + 10) + 10), (30, 30, 30))
        for i, t in enumerate(times):
            f = frame_at(t, int(t * FPS)).resize((tw, tht), Image.LANCZOS)
            sheet.paste(f, (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (tht + 10)))
        folder = out.parent / "nguon"
        folder.mkdir(exist_ok=True)
        path = folder / f"{out.stem}-kiem-tra.jpg"
        sheet.save(path, quality=88)
        print(describe_assets(photos, music))
        print(f"Đã xuất ảnh kiểm tra {path}: nhịp 1, nhịp 2, {n} khung sản phẩm, CTA. "
              f"Video sẽ dài {dur:.1f} giây ({per:g} giây mỗi sản phẩm). Mỗi lần kiểm tra ghi đè, không cần xóa.")
        return

    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           *(["-stream_loop", "-1", "-t", f"{dur + 6:.3f}", "-i", str(music)] if music else
             ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=44100:cl=stereo"]),
           "-map", "0:v", "-map", "1:a", "-t", f"{dur:.3f}",
           *(["-af", "silenceremove=start_periods=1:start_threshold=-38dB,"
                     f"atrim=0:{dur:.3f},"
                     f"afade=t=in:d=0.25,afade=t=out:st={dur - 1.2:.2f}:d=1.2,"
                     "loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100"] if music else []),
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-movflags", "+faststart", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    cover = None
    for fi in range(int(round(dur * FPS))):
        t = fi / FPS
        frame = frame_at(t, fi)
        if cover is None and t >= cover_t:
            cover = frame
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("Lỗi khi xuất video.")
    cover.save(out.with_name(out.stem + "-anh-bia.jpg"), quality=90)
    mark_used(spec, photos, music)
    print(f"Đã tạo {out} ({dur:.1f} giây, {n} sản phẩm, 1080x1920, 30fps) và ảnh bìa {out.stem}-anh-bia.jpg")
    print(describe_assets(photos, music))


if __name__ == "__main__":
    main()
