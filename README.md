# TIVO Agents

Shop TIVO Smart bán sản phẩm Magic. Chủ shop đăng video tiếp thị cho shop trên nick TikTok cá nhân.

| Thư mục | Nội dung |
|---|---|
| `Tivo-van-hanh-marketing-ai/` | Agent Marketing AI TikTok: lập kế hoạch, viết content, tạo video sale. Hướng dẫn trong `CLAUDE.md` của thư mục này |
| `lich-chay/` | Lệnh của các tác vụ tự chạy (`lenh-*.txt`) và file chạy thử `chay.ps1` |
| `Tivo-dashboard/` | Dashboard Next.js |

Agent vận hành Shopee đã gỡ ngày 19/11/2026. Bản sao lưu: `C:\agents\sao-luu-agent-shoppe-2026-11-19.zip` (không nằm trong repo).
Agent marketing chạy độc lập, chỉ dùng dữ liệu trong thư mục `data/` của nó. Video được tự lưu vào bản nháp TikTok Studio, chủ shop xem rồi tự bấm đăng (xem `Tivo-van-hanh-marketing-ai/quy-trinh/4-dang-tiktok.md`).

## Có trong repo

Repo chứa `data/` và `Tivo-dashboard/.env.local` có khóa bí mật.
Repo này phải luôn để riêng tư. Nếu mở công khai hoặc cho thêm người vào, phải đổi khóa Supabase và mật khẩu dashboard.

## Chạy trên máy này

Cài thư viện (chỉ cần làm một lần):

```powershell
python -m pip install openpyxl pandas pillow imageio-ffmpeg
```

Mở agent:

```powershell
Set-Location "C:\agents\tivo-agents\Tivo-van-hanh-marketing-ai"
claude
```

Hai tác vụ tự chạy hằng ngày trong app Claude (mục Tác vụ đã lên lịch):

| Tác vụ | Giờ | Lệnh | Kết quả |
|---|---|---|---|
| Lập Kế Hoạch Marketing ngày sale | 8:00 | `lich-chay/lenh-ke-hoach.txt` | Kế hoạch TikTok, `output/1-ke-hoach/` |
| Video AI TIKTOK ngày Sale | 8:30 | `lich-chay/lenh-video.txt` | Video MP4 có ảnh nền và nhạc, `output/3-video/` |

Chạy thử một tác vụ ngay trên máy:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\agents\tivo-agents\lich-chay\chay.ps1" -TacVu video   # hoặc ke-hoach
```
