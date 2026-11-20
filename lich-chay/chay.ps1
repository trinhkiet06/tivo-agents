# Chạy một tác vụ TIVO bằng Claude, ghi kết quả vào lich-chay\nhat-ky\.
# Cách dùng: powershell -ExecutionPolicy Bypass -File chay.ps1 -TacVu ke-hoach|video
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('ke-hoach', 'video')]
    [string]$TacVu
)

$goc = 'C:\agents\tivo-agents'
$thuMuc = 'Tivo-van-hanh-marketing-ai'

$utf8 = New-Object System.Text.UTF8Encoding $false
$OutputEncoding = $utf8
[Console]::OutputEncoding = $utf8

$nhatKy = Join-Path $goc 'lich-chay\nhat-ky'
New-Item -ItemType Directory -Force $nhatKy | Out-Null
$log = Join-Path $nhatKy ('{0}-{1:yyyy-MM-dd-HHmm}.txt' -f $TacVu, (Get-Date))

$lenh = Get-Content (Join-Path $goc "lich-chay\lenh-$TacVu.txt") -Raw -Encoding UTF8
Set-Location (Join-Path $goc $thuMuc)

# Chỉ cho phép đọc, ghi file trong thư mục agent, chạy Python và tra cứu web.
$congCu = 'Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Bash(python:*),Bash(ls:*),Bash(mkdir:*),mcp__claude-artifacts__get_artifact,mcp__claude-artifacts__publish_files'

"Bắt đầu: $(Get-Date -Format 'dd/MM/yyyy HH:mm')  |  Tác vụ: $TacVu  |  Thư mục: $thuMuc`n" | Out-File $log -Encoding utf8
$lenh | & "$env:APPDATA\npm\claude.cmd" -p --permission-mode acceptEdits --allowedTools $congCu 2>&1 |
    Out-File $log -Encoding utf8 -Append
"`nKết thúc: $(Get-Date -Format 'dd/MM/yyyy HH:mm')" | Out-File $log -Encoding utf8 -Append
