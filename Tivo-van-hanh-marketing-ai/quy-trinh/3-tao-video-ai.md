# 3. Tạo video AI

**Đầu ra:** thư mục `output/3-video/<tên-sale>/`
- `V1-bo-lenh.md`: bộ lệnh và tài liệu dựng của từng video.
- `V1.mp4`: video hoàn chỉnh do người phụ trách lưu vào.
- `kiem-tra.md`: kết quả kiểm tra của từng video.

**Đầu vào:** content đã duyệt ở `output/2-content/`, ảnh ở `data/anh-san-pham/<MÃ SP>/`, danh sách ảnh ở `data/anh-san-pham.xlsx`, thông tin công cụ ở `data/cong-cu-video.xlsx`.

Agent chưa được kết nối công cụ tạo video AI nên không tự xuất ra file video. Nếu sau này có công cụ kết nối, phải hỏi chủ shop trước khi chạy vì có thể mất phí.

## Bước 1: Kiểm tra trước khi làm

- Content chưa duyệt thì dừng và báo.
- Sản phẩm chưa có ảnh thật thì dừng video đó và báo thiếu. Không tả sản phẩm theo tưởng tượng.
- `data/cong-cu-video.xlsx` chưa có tên công cụ thì viết bộ lệnh dùng chung cho video dọc 9:16 và ghi rõ giả định.

## Bước 2: Viết bộ lệnh cho từng video

Mỗi cảnh trong content có một phần gồm:

| Mục | Nội dung |
|---|---|
| Cảnh và thời lượng | Theo content, không vượt giới hạn của công cụ |
| Ảnh tham chiếu | Đường dẫn ảnh thật trong `data/anh-san-pham/` |
| Prompt | Bối cảnh, chủ thể, chuyển động máy, ánh sáng, tỷ lệ 9:16. Viết bằng tiếng Anh nếu công cụ làm tốt hơn với tiếng Anh |
| Điều cần tránh | Chữ, logo giả, biến dạng sản phẩm, đổi màu, thêm chi tiết không có |

Cuối bộ lệnh ghi: lời đọc tiếng Việt, chữ trên màn hình kèm thời điểm hiện, gợi ý nhạc, thứ tự ghép cảnh, caption và hashtag.

## Bước 3: Người phụ trách tạo video

1. Đưa ảnh tham chiếu và prompt từng cảnh vào công cụ video AI.
2. Ghép cảnh, thêm lời đọc và chữ trên màn hình bằng phần mềm dựng.
3. Lưu thành `output/3-video/<tên-sale>/V1.mp4`.

## Bước 4: Kiểm tra trước khi đăng

Agent không xem được nội dung video nếu không có công cụ phù hợp. Nếu vậy, agent lập checklist trong `kiem-tra.md` và người phụ trách tự đánh dấu. Không đánh dấu đạt thay người xem.

- [ ] Hình dáng, màu sắc, nút bấm và logo giống sản phẩm thật
- [ ] Không có chữ sai hoặc chữ do AI tự vẽ
- [ ] Giá, voucher và thời điểm áp dụng khớp danh mục và kế hoạch
- [ ] Không có cảnh giả lập công dụng hay trước và sau khi dùng
- [ ] Không có khuôn mặt hoặc giọng người thật khi chưa được đồng ý
- [ ] Không có người giả đóng vai khách hàng hoặc chuyên gia
- [ ] Sản phẩm vẫn còn đủ tồn kho vào ngày đăng
- [ ] Bật nhãn nội dung do AI tạo khi đăng trên TikTok
- [ ] Chủ shop đã duyệt bản cuối
