# TIVO Agents

| Thư mục | Nội dung |
|---|---|
| `Tivo-van-hanh-shoppe/` | Agent vận hành Shopee, 4 nhiệm vụ |
| `Tivo-van-hanh-marketing-ai/` | Agent Marketing AI TikTok, 3 nhiệm vụ |
| `Tivo-dashboard/` | Dashboard Next.js |

## Không có trong repo

Các mục sau không đưa lên GitHub, nên phải chép riêng sang máy khác:

- Thư mục `data/` của cả ba phần, gồm đơn hàng, tồn kho và danh mục sản phẩm.
- File `Tivo-dashboard/.env.local`, chứa khóa bí mật.

## Lấy về máy khác

Thay `<tài-khoản>` bằng tài khoản GitHub của bạn.

```powershell
Set-Location "C:\BaitapDevC\agents"
git clone https://github.com/<tài-khoản>/tivo-agents.git
```

Sau đó chép các thư mục `data/` vào đúng chỗ và chạy agent:

```powershell
python -m pip install openpyxl pandas
Set-Location "C:\BaitapDevC\agents\tivo-agents\Tivo-van-hanh-shoppe"
claude
```

Các lệnh khác nằm trong `LENH-POWERSHELL.md` của từng agent. Phần clone và commit trong đó viết cho hai repo cũ, nên hãy dùng lệnh ở đây thay thế.
