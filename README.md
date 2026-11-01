# TIVO Agents

| Thư mục | Nội dung |
|---|---|
| `Tivo-van-hanh-shoppe/` | Agent vận hành Shopee, 4 nhiệm vụ |
| `Tivo-van-hanh-marketing-ai/` | Agent Marketing AI TikTok, 3 nhiệm vụ |
| `Tivo-dashboard/` | Dashboard Next.js |

## Không có trong repo

Các mục sau không đưa lên GitHub, nên phải chép riêng sang máy khác:

- File `Tivo-van-hanh-shoppe/data/gia-von.xlsx`, chứa giá vốn.
- Thư mục `Tivo-dashboard/data/`.
- File `Tivo-dashboard/.env.local`, chứa khóa bí mật.

Thư mục `data/` của hai agent đã có trong repo. Repo này phải luôn để riêng tư.

## Lấy về máy khác

Thay `<tài-khoản>` bằng tài khoản GitHub của bạn.

```powershell
Set-Location "C:\BaitapDevC\agents"
git clone https://github.com/<tài-khoản>/tivo-agents.git
```

Sau đó chép các file ở trên vào đúng chỗ và chạy agent:

```powershell
python -m pip install openpyxl pandas
Set-Location "C:\BaitapDevC\agents\tivo-agents\Tivo-van-hanh-shoppe"
claude
```

Các lệnh khác nằm trong `LENH-POWERSHELL.md` của từng agent. Phần clone và commit trong đó viết cho hai repo cũ, nên hãy dùng lệnh ở đây thay thế.
