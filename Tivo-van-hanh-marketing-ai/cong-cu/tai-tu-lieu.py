"""Tải ảnh nền và nhạc MIỄN BẢN QUYỀN (CC0 hoặc Public Domain) về thư viện để dựng video.

Nguồn: Openverse (api.openverse.org) gom ảnh từ StockSnap, Rawpixel, Wikimedia Commons, Flickr...
và nhạc từ Freesound. Chỉ nhận giấy phép CC0 / Public Domain Mark: dùng thương mại, không cần ghi công.

Cách chạy (từ thư mục Tivo-van-hanh-marketing-ai, cần mạng):
    python cong-cu/tai-tu-lieu.py anh <phong_cach> "<từ khóa tiếng Anh>" [số lượng] [nguồn]
        nguồn ảnh mặc định stocksnap (ảnh chụp chuyên nghiệp); có thể ghi wikimedia, rawpixel, flickr hoặc tat-ca
    python cong-cu/tai-tu-lieu.py nhac <phong_cach> "<từ khóa tiếng Anh>" [số lượng]
    python cong-cu/tai-tu-lieu.py bo <đường dẫn file trong thu-vien>   # loại 1 file, lần sau không tải lại

Kết quả: thu-vien/anh/<phong_cach>/, thu-vien/nhac/<phong_cach>/ và thu-vien/giay-phep.json
(nguồn, tác giả, giấy phép, link gốc của từng file để chứng minh khi cần).
Tác vụ tự động KHÔNG chạy file này; chỉ chạy khi chủ shop muốn thêm tư liệu.
"""
import io
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "thu-vien"
LOG = LIB / "giay-phep.json"
API = "https://api.openverse.org/v1"
UA = {"User-Agent": "video-tool/1.0"}
OK = {"cc0", "pdm"}
MIN_S, MAX_S = 20, 240          # nhạc dài 20 giây đến 4 phút


def get(url, raw=False):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                data = r.read()
                return data if raw else json.loads(data)
        except Exception:
            if i == 2:
                raise
            time.sleep(2)


def load_log():
    if LOG.exists():
        return json.loads(LOG.read_text(encoding="utf-8"))
    return {"_ghi_chu": "Giấy phép từng file trong thư viện. Chỉ nhận CC0 / Public Domain.", "file": {}, "bo": []}


def save_log(log):
    LIB.mkdir(exist_ok=True)
    if LOG.exists():                                  # gộp với bản trên đĩa, phòng khi chạy song song
        disk = json.loads(LOG.read_text(encoding="utf-8"))
        gone = set(log["bo"])
        gone |= set(disk.get("bo", []))
        merged = {**disk.get("file", {}), **log["file"]}
        log["file"] = {k: v for k, v in merged.items() if v["id"] not in gone}
        log["bo"] = sorted(gone)
    LOG.write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")


def big_url(x):
    u = x["url"]
    if "upload.wikimedia.org/wikipedia/commons/" in u and "/thumb/" not in u:
        name = u.rsplit("/", 1)[1]
        return u.replace("/commons/", "/commons/thumb/") + f"/1280px-{name}"
    return u


def search(kind, query, page, source):
    params = {"q": query, "license": "cc0,pdm", "page_size": 20, "page": page}
    if kind == "anh":
        params.update(size="large", mature="false")
    if source:
        params["source"] = source
    return get(f"{API}/{'images' if kind == 'anh' else 'audio'}/?" + urllib.parse.urlencode(params))["results"]


def fetch(kind, style, query, count, source=""):
    log = load_log()
    known = {v["id"] for v in log["file"].values()} | set(log["bo"])
    folder = LIB / kind / style
    folder.mkdir(parents=True, exist_ok=True)
    got, page = 0, 1
    while got < count and page <= 6:
        results = search(kind, query, page, source)
        if not results:
            break
        for x in results:
            if got >= count:
                break
            if x["id"] in known or x.get("license") not in OK:
                continue
            try:
                if kind == "anh":
                    if min(x.get("width") or 0, x.get("height") or 0) < 900:
                        continue
                    im = Image.open(io.BytesIO(get(big_url(x), raw=True))).convert("RGB")
                    k = 1600 / max(im.size)
                    if k < 1:
                        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
                    path = folder / f"{x['source']}-{x['id'][:8]}.jpg"
                    im.save(path, quality=90)
                else:
                    sec = (x.get("duration") or 0) / 1000
                    if not MIN_S <= sec <= MAX_S:
                        continue
                    url = x["url"] if x["url"].endswith(".mp3") else (x.get("alt_files") or [{}])[0].get("url", x["url"])
                    path = folder / f"{x['source']}-{x['id'][:8]}.mp3"
                    path.write_bytes(get(url, raw=True))
            except Exception as e:
                print("  bỏ qua", x.get("title"), e)
                continue
            log["file"][path.relative_to(ROOT).as_posix()] = {
                "id": x["id"], "ten": x.get("title"), "tac_gia": x.get("creator"), "nguon": x.get("source"),
                "giay_phep": x.get("license"), "link_goc": x.get("foreign_landing_url"), "tu_khoa": query}
            known.add(x["id"])
            got += 1
            print(f"  + {path.relative_to(ROOT).as_posix()}  {x.get('title')}")
        page += 1
    save_log(log)
    print(f"Đã tải {got} file {kind} cho phong cách {style} (từ khóa: {query}).")


def drop(rel):
    log = load_log()
    rel = Path(rel).as_posix()
    info = log["file"].pop(rel, None)
    if info:
        log["bo"].append(info["id"])
    p = ROOT / rel
    if p.exists():
        p.unlink()
    save_log(log)
    print("Đã loại", rel)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "bo":
        for rel in a[1:]:
            drop(rel)
    elif len(a) >= 3 and a[0] in ("anh", "nhac"):
        source = a[4] if len(a) > 4 else ("stocksnap" if a[0] == "anh" else "")
        fetch(a[0], a[1], a[2], int(a[3]) if len(a) > 3 else 8, "" if source == "tat-ca" else source)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
