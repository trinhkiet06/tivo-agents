# Ghi chú lệnh PowerShell để chạy agent trên máy cũ

Đây là bản của agent Shopee, đã cập nhật theo cấu trúc 4 nhiệm vụ.
Các lệnh viết cho Windows PowerShell 5.1. Sửa `C:\BaitapDevC\agents\agents` thành đường dẫn thật trên máy của bạn.

## Bước 1: Làm trên máy này trước khi rời đi

Thay đổi của agent chưa được commit. Hai lệnh dưới đây đưa quy trình mới lên GitHub.

```powershell
Set-Location "C:\BaitapDevC\agents\agents\Tivo-van-hanh-shoppe"
git add -A
git commit -m "Cau truc lai agent Shopee theo 4 nhiem vu"
git push

Set-Location "C:\BaitapDevC\agents\agents\Tivo-van-hanh-marketing-ai"
git add -A
git commit -m "Them bo 35 nhiem vu van hanh"
git push
```

Thư mục `data` bị `.gitignore` bỏ qua nên không lên GitHub. Hãy nén để mang đi bằng USB hoặc Drive riêng.

```powershell
Set-Location "C:\BaitapDevC\agents\agents"
Compress-Archive -Path "Tivo-van-hanh-shoppe\data"       -DestinationPath "data-shopee.zip"
Compress-Archive -Path "Tivo-van-hanh-marketing-ai\data" -DestinationPath "data-marketing.zip"
```

Dashboard không có git nên cũng phải nén. Lệnh này bỏ qua thư mục nặng và file `.env.local`.

```powershell
Get-ChildItem "Tivo-dashboard" -Force |
  Where-Object { $_.Name -notin @("node_modules", ".next", ".env.local") } |
  Compress-Archive -DestinationPath "tivo-dashboard.zip"
```

File `.env.local` chứa khóa bí mật. Hãy chép riêng qua kênh an toàn và đừng đưa lên GitHub.

## Bước 2: Lấy về máy cũ

Nếu máy cũ chưa có code:

```powershell
New-Item -ItemType Directory -Force "C:\BaitapDevC\agents\agents"
Set-Location "C:\BaitapDevC\agents\agents"
git clone https://github.com/trinhkiet06/Tivosmart-agent-operating.git Tivo-van-hanh-shoppe
git clone https://github.com/trinhkiet06/Tivosmart-agent-marketing.git Tivo-van-hanh-marketing-ai
```

Nếu máy cũ đã có code, chạy lệnh này trong từng thư mục agent:

```powershell
git pull
```

Chép các file zip vào `C:\BaitapDevC\agents\agents`, rồi giải nén:

```powershell
Set-Location "C:\BaitapDevC\agents\agents"
Expand-Archive "data-shopee.zip"    -DestinationPath "Tivo-van-hanh-shoppe" -Force
Expand-Archive "data-marketing.zip" -DestinationPath "Tivo-van-hanh-marketing-ai" -Force
New-Item -ItemType Directory -Force "Tivo-van-hanh-marketing-ai\data\tiktok"
Expand-Archive "tivo-dashboard.zip" -DestinationPath "Tivo-dashboard" -Force
```

`-Force` sẽ ghi đè file trùng tên trong thư mục đích. Nếu `data` trên máy cũ mới hơn, hãy sao lưu trước khi giải nén.

## Bước 3: Kiểm tra và cài công cụ

```powershell
git --version
node --version
python --version
python -c "import openpyxl; print('openpyxl', openpyxl.__version__)"
Get-Command claude
```

Cài phần còn thiếu:

| Thiếu | Lệnh hoặc cách cài |
|---|---|
| Thư viện đọc Excel | `python -m pip install openpyxl pandas` |
| Claude Code dạng lệnh | `npm install -g @anthropic-ai/claude-code` |
| Git, Node, Python | Cài từ trang chủ của từng công cụ |

Trên máy này, Python mặc định chưa có `openpyxl`. Bản Anaconda tại `C:\Annaconda\python.exe` thì có.
Nếu máy cũ cũng vậy, hãy chạy lệnh cài thư viện ở bảng trên hoặc dùng Python có sẵn thư viện.

## Bước 4: Chạy agent

Mỗi agent chạy trong thư mục của nó. Cách khác là mở đúng thư mục đó trong VS Code và dùng tiện ích Claude Code.

```powershell
Set-Location "C:\BaitapDevC\agents\agents\Tivo-van-hanh-shoppe"
claude
```

```powershell
Set-Location "C:\BaitapDevC\agents\agents\Tivo-van-hanh-marketing-ai"
claude
```

Với agent Shopee, gõ yêu cầu bằng lời theo 4 nhiệm vụ:

```text
Tra cứu lịch flash sale và ngày sale Shopee 60 ngày tới
Set giá và voucher cho đợt 11.11
Soạn trả lời cho khách hỏi: tăm nước có chống nước không?
Soạn tin hỏi lý do các đơn bị hủy tuần này
Làm báo cáo kỳ 24/10 - 30/10/2026
```

Muốn chạy một lệnh rồi thoát, không mở phiên trò chuyện:

```powershell
claude -p "Dữ liệu hiện có làm được những việc nào, thiếu file nào?"
```

## Bước 5: Chép file giữa hai agent

Hai agent không tự đọc thư mục của nhau. Khi cập nhật tồn kho, chạy lệnh này:

```powershell
Set-Location "C:\BaitapDevC\agents\agents"
Copy-Item "Tivo-van-hanh-shoppe\data\ton-kho.xlsx" "Tivo-van-hanh-marketing-ai\data\ton-kho.xlsx" -Force
```

## Bước 6: Chạy dashboard

Tạo lại `Tivo-dashboard\.env.local` trước, rồi chạy các lệnh dưới. `npm run load` ghi dữ liệu vào Supabase mà dashboard đang dùng.

```powershell
Set-Location "C:\BaitapDevC\agents\agents\Tivo-dashboard"
npm install
npm run load
npm run dev
```

## Xử lý lỗi thường gặp

| Hiện tượng | Lệnh xử lý |
|---|---|
| PowerShell chặn `npm` hoặc `claude` vì chính sách chạy script | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Tiếng Việt hiện sai trong cửa sổ lệnh | `chcp 65001` rồi `$env:PYTHONUTF8 = "1"` |
| Báo không tìm thấy `claude` ngay sau khi cài | Đóng và mở lại cửa sổ PowerShell |
| Claude báo model cần usage credits | Đổi model: `claude --model claude-opus-5-5`, hoặc gõ `/model` trong phiên |
| `git push` hỏi đăng nhập | Đăng nhập tài khoản GitHub sở hữu hai repo khi được hỏi |

## Tên file dữ liệu

File danh mục của agent Shopee đã đổi từ `THÔNG TIN SẢN PHẨM.xlsx` thành `data/san-pham.xlsx`. Nếu máy kia còn tên cũ, hãy đổi tên trong thư mục `data` của agent Shopee:

```powershell
Set-Location "C:\BaitapDevC\agents\agents\Tivo-van-hanh-shoppe\data"
Get-ChildItem -Filter "TH*.xlsx" | Rename-Item -NewName "san-pham.xlsx"
```

## Tình trạng kiểm tra

Đã chạy thử trên máy này: nén và giải nén vào thư mục tạm, các lệnh kiểm tra ở Bước 3, `Copy-Item` vào thư mục tạm.
Trong 4 nhiệm vụ của agent Shopee, mới chạy thử nhiệm vụ báo cáo trong một bản sao tạm. Ba nhiệm vụ còn lại chưa chạy thử.
Chưa chạy thử: `git commit`, `git push`, `git clone`, các lệnh cài đặt, `npm run load`, `npm run dev`.
Lần này không có gì được cài thêm hay đổi cấu hình trên máy này.
