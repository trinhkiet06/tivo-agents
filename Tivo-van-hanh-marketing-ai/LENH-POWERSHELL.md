# Ghi chú lệnh PowerShell để chạy agent trên máy 1

Đây là bản của agent Marketing AI TikTok, đã cập nhật theo cấu trúc 3 nhiệm vụ.
Các lệnh viết cho Windows PowerShell 5.1. Sửa `C:\BaitapDevC\agents\tivo-agents` thành đường dẫn thật trên máy của bạn.

## Bước 1: Làm trên máy này trước khi rời đi

Toàn bộ code và `data` của hai agent nằm chung trong repo `tivo-agents`. Nếu `git status` còn thay đổi, chạy các lệnh này để đưa lên GitHub:

```powershell
Set-Location "C:\BaitapDevC\agents\tivo-agents"
git status
git add -A
git commit -m "Cap nhat truoc khi chuyen sang may 1"
git push
```

Repo chứa cả `gia-von.xlsx`, `Tivo-dashboard\data` và `Tivo-dashboard\.env.local` có khóa bí mật, nên phải luôn để riêng tư.

## Bước 2: Lấy về máy 1

Nếu máy 1 chưa có thư mục `tivo-agents`:

```powershell
New-Item -ItemType Directory -Force "C:\BaitapDevC\agents"
Set-Location "C:\BaitapDevC\agents"
git clone https://github.com/trinhkiet06/tivo-agents.git
```

Nếu máy 1 đã có thư mục này:

```powershell
Set-Location "C:\BaitapDevC\agents\tivo-agents"
git pull
```

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
Nếu máy 1 cũng vậy, hãy chạy lệnh cài thư viện ở bảng trên hoặc dùng Python có sẵn thư viện.

## Bước 4: Chạy agent

Mỗi agent chạy trong thư mục của nó. Cách khác là mở đúng thư mục đó trong VS Code và dùng tiện ích Claude Code.

```powershell
Set-Location "C:\BaitapDevC\agents\tivo-agents\Tivo-van-hanh-shoppe"
claude
```

```powershell
Set-Location "C:\BaitapDevC\agents\tivo-agents\Tivo-van-hanh-marketing-ai"
claude
```

Với agent TikTok, gõ yêu cầu bằng lời theo 3 nhiệm vụ:

```text
Tra cứu lịch sale TikTok 60 ngày tới
Lập kế hoạch truyền thông cho đợt 12.12
Tạo content video AI cho đợt 12.12
Tạo bộ lệnh video AI cho video V1 của đợt 12.12
```

Muốn chạy một lệnh rồi thoát, không mở phiên trò chuyện:

```powershell
claude -p "Dữ liệu hiện có làm được những việc nào, thiếu file nào?"
```

## Bước 5: Chép file giữa hai agent

Hai agent không tự đọc thư mục của nhau. Khi cập nhật tồn kho hoặc bảng giá, chạy các lệnh này:

```powershell
Set-Location "C:\BaitapDevC\agents\tivo-agents"
Copy-Item "Tivo-van-hanh-shoppe\data\ton-kho.xlsx" "Tivo-van-hanh-marketing-ai\data\ton-kho.xlsx" -Force
Copy-Item "Tivo-van-hanh-shoppe\data\san-pham.xlsx" "Tivo-van-hanh-marketing-ai\data\san-pham.xlsx" -Force
```

## Bước 6: Chạy dashboard

File `.env.local` và `data` đã có sẵn sau khi clone, nên chỉ cần chạy các lệnh dưới. `npm run load` ghi dữ liệu vào Supabase mà dashboard đang dùng.

```powershell
Set-Location "C:\BaitapDevC\agents\tivo-agents\Tivo-dashboard"
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
| `git push` hỏi đăng nhập | Đăng nhập tài khoản GitHub sở hữu repo khi được hỏi |

## Tình trạng kiểm tra

Đã chạy trên máy 2: `git commit`, `git push`, các lệnh kiểm tra ở Bước 3.
Agent TikTok theo 3 nhiệm vụ chưa được chạy thử.
Chưa chạy thử: `git clone` trên máy 1, các lệnh cài đặt, `npm run load`, `npm run dev`.
