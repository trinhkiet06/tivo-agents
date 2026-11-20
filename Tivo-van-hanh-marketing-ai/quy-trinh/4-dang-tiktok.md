# 4. Đưa video vào bản nháp TikTok

Chủ shop chọn ngày 19/11/2026: agent tự **lưu video vào mục Bản nháp (Drafts)** trên nick TikTok cá nhân của chủ shop. Chủ shop dùng nick này để tiếp thị cho shop. Agent làm bằng trình duyệt Chrome (tiện ích Claude in Chrome) qua TikTok Studio. **Agent không bao giờ bấm Đăng (Post).** Chủ shop tự mở bản nháp, xem lại và bấm đăng.

- Nick: ghi trong `cong-cu/nick-tiktok.txt` (hiện là TIVO Smart, @_tivo.smart_).
- Bản nháp trên TikTok Studio chỉ chủ shop thấy, mở được trên mọi máy tính. Tối đa 30 bản nháp, tự xóa sau 60 ngày (theo thông báo của TikTok Studio).
- Lần chạy thử thành công ngày 19/11/2026 với video T01 Black Friday.

## Khi nào làm

- Ngay sau khi tác vụ video xuất xong MP4, nếu phiên làm việc có công cụ Claude in Chrome. Không có thì bỏ qua, và nhắc chủ shop nhắn "lưu nháp T0x" khi mở Claude có kết nối Chrome.
- Khi chủ shop nhắn "lưu nháp T01", "lưu nháp T01, T02 Black Friday"...
- Mỗi video chỉ lưu nháp một lần. Tình trạng trong lịch đăng là "Đã lưu nháp TikTok" thì không lưu lại, trừ khi chủ shop yêu cầu.

## Cần có sẵn

- Chrome đã bật tiện ích Claude in Chrome, đã đăng nhập Claude.
- Chủ shop đã **tự đăng nhập** TikTok trên Chrome. Agent không hỏi, không nhập, không lưu mật khẩu hay mã xác minh.
- Gặp trang đăng nhập, mã xác minh, captcha hay cảnh báo bảo mật thì dừng và báo chủ shop.

## Các bước

1. Đọc `output/3-video/<tên-sale>/nguon/lich-dang-video.json`. Lấy của video: file MP4, caption, hashtag.
2. **Bản tải lên:** công cụ tải file của Chrome chỉ nhận file dưới 10 MB. Tạo bản nén trong `output/3-video/<tên-sale>/ban-dang-tiktok/T0x.mp4`, ghi đè nếu đã có:
   `python -c "import imageio_ffmpeg,subprocess,sys; subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-i',sys.argv[1],'-c:v','libx264','-crf','24','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',sys.argv[2]],check=True)" <file gốc> <bản tải lên>`
   Vẫn trên 10 MB thì tăng `-crf` lên 26.
3. Mở tab mới vào `https://www.tiktok.com/tiktokstudio/upload`. Kiểm tra đúng nick trong `cong-cu/nick-tiktok.txt`: mở `https://www.tiktok.com/profile`, trang sẽ chuyển sang `@<nick>`. Sai nick hoặc chưa đăng nhập thì dừng, báo chủ shop.
4. Tìm ô chọn file ẩn (file-input) và tải bản tải lên vào đó bằng công cụ tải file. Không bấm nút "Select videos", vì nút đó mở cửa sổ chọn file mà agent không thao tác được.
5. TikTok có thể hiện bảng "Turn on automatic content checks?" hoặc bảng giới thiệu tính năng. Bấm **Cancel** hoặc **Got it**. Không bấm "Turn on", vì nút đó đổi cài đặt tài khoản.
6. Ô Description (mô tả): xóa chữ mặc định (tên file), gõ caption, thêm 1 dấu cách, rồi gõ hashtag, đúng như trong lịch đăng. Không tự viết thêm.
7. Không đổi các cài đặt khác: quyền xem, thời điểm đăng, âm thanh. Giữ nguyên âm thanh gốc của video.
8. Bấm **Save draft**. Kiểm tra trang chuyển sang `tiktokstudio/content?tab=draft` và bản nháp mới có đúng caption.
9. Đóng tab. Ghi tình trạng **Đã lưu nháp TikTok** (kèm ngày giờ) cho video đó trong `nguon/lich-dang-video.json`. Chạy lại `python cong-cu/xuat-excel.py` và cập nhật trang Claude video.

## Chủ shop đăng từ bản nháp

Mở TikTok Studio trên máy tính (tiktok.com/tiktokstudio), vào **Posts**, chọn tab **Drafts**, bấm sửa bản nháp. Xem lại video và caption, gắn sản phẩm nếu nick gắn được, chọn đăng ngay hoặc hẹn giờ, rồi bấm **Post**.

## Không được làm

- Không bấm **Post** hay hẹn giờ đăng. Chỉ được làm việc này khi chủ shop nhắn rõ "đăng T0x ngay" hoặc "hẹn giờ T0x", và phải gửi ảnh chụp màn hình để chủ shop xác nhận trước khi bấm.
- Không lưu nháp video thử trong `output/3-video/thu-nghiem/`, trừ khi chủ shop yêu cầu.
- Không sửa, xóa hay ẩn bài đã đăng hoặc bản nháp cũ. Không trả lời bình luận, không nhắn tin, không đổi hồ sơ hay cài đặt tài khoản.
- Không bấm quảng cáo, quảng bá trả phí hay bất kỳ nút nào tốn tiền.
- TikTok báo vi phạm, trùng bản quyền nhạc hay lỗi tải lên: dừng, báo chủ shop. Không tự thử cách khác.
- Trang đơ hoặc công cụ Chrome lỗi 2–3 lần liên tiếp: dừng, báo chủ shop.
