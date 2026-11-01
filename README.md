# TIVO Agents

| Thư mục | Nội dung |
|---|---|
| `Tivo-van-hanh-shoppe/` | Agent vận hành Shopee, 4 nhiệm vụ |
| `Tivo-van-hanh-marketing-ai/` | Agent Marketing AI TikTok, 3 nhiệm vụ |
| `Tivo-dashboard/` | Dashboard Next.js |

## Có trong repo

Repo chứa cả `data/`, `gia-von.xlsx` và `Tivo-dashboard/.env.local` có khóa bí mật.
Repo này phải luôn để riêng tư. Nếu mở công khai hoặc cho thêm người vào, phải đổi khóa Supabase và mật khẩu dashboard.

## Lấy về máy khác

Thay `<tài-khoản>` bằng tài khoản GitHub của bạn.

```powershell
Set-Location "C:\BaitapDevC\agents"
git clone https://github.com/<tài-khoản>/tivo-agents.git
```

Sau đó chạy agent:

```powershell
python -m pip install openpyxl pandas
Set-Location "C:\BaitapDevC\agents\tivo-agents\Tivo-van-hanh-shoppe"
claude
```

Các lệnh khác nằm trong `LENH-POWERSHELL.md` của từng agent.
