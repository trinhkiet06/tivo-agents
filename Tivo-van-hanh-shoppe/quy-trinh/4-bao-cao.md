# 4. Báo cáo

**Đầu ra:** `output/4-bao-cao/ngay-<yyyy-mm-dd>.md`, `tuan-<năm>-<số tuần>.md` hoặc `thang-<yyyy-mm>.md`. Số tuần lấy theo ngày cuối kỳ, tính theo tuần ISO. Không ghi đè báo cáo của kỳ khác.

**Đầu vào:** `data/don-hang-thang.xlsx`, `data/don-cho-gui.xlsx`, `data/ton-kho.xlsx`, `data/san-pham.xlsx`, ghép bằng Mã SP.

Mặc định là 7 ngày gần nhất có dữ liệu, so với 7 ngày liền trước. Kỳ chưa đủ ngày thì nói rõ và so với kỳ có cùng số ngày.

## Quy ước tính

Dùng đúng các quy ước này để số liệu các kỳ so được với nhau. Đếm đơn theo mã đơn duy nhất, tính theo ngày đặt hàng.

| Chỉ số | Cách tính |
|---|---|
| Doanh thu | Tổng "Tổng tiền" của đơn có trạng thái khác "Đã hủy" |
| Doanh thu thực nhận | Doanh thu trừ đơn "Hoàn trả" |
| Tỷ lệ hủy, tỷ lệ hoàn | Số đơn "Đã hủy" hoặc "Hoàn trả" / tổng số đơn của kỳ |

| Nhóm đơn | Trạng thái trong dữ liệu |
|---|---|
| Đang chờ gửi | Lấy từ `data/don-cho-gui.xlsx`, ghi kèm ngày xuất dữ liệu. File trống thì ghi "chưa có dữ liệu" và không tính thay bằng trạng thái khác |
| Đang giao | "Đang giao", nêu riêng vì chưa biết kết quả |
| Đã gửi thành công | "Hoàn thành" |
| Bị hủy | "Đã hủy" |
| Hoàn trả | "Hoàn trả", nêu riêng |

## Nội dung báo cáo (đúng thứ tự)

1. **Top 3 sản phẩm win:** kèm số liệu và lưu ý tồn kho.
2. **Doanh thu:** doanh thu, doanh thu thực nhận, so với kỳ trước.
3. **Hiệu quả sản phẩm:** bảng mọi sản phẩm gồm số lượng, doanh thu, doanh thu thực nhận, thay đổi so với kỳ trước, tỷ lệ hủy, tỷ lệ hoàn, tồn kho.
4. **Đơn hàng:** số đơn và tỷ lệ của từng nhóm ở bảng trên, kèm danh sách mã đơn đang chờ gửi nếu có.
5. **Đơn bị hủy:** danh sách mã đơn, sản phẩm và lý do từ `data/ly-do-huy.xlsx`. Chưa có lý do thì ghi "chưa có lý do", rồi đề xuất làm phần hỏi lý do ở nhiệm vụ 3.

## Cách chọn top 3 sản phẩm win

1. Xếp sản phẩm theo doanh thu thực nhận của kỳ, từ cao xuống thấp.
2. Bỏ sản phẩm bán dưới 5 sản phẩm trong kỳ.
3. Bỏ sản phẩm có tỷ lệ hủy cộng tỷ lệ hoàn trên 20%.
4. Lấy 3 sản phẩm đầu. Doanh thu bằng nhau thì sản phẩm bán nhiều hơn đứng trước.

Chủ shop có thể đổi hai ngưỡng 5 sản phẩm và 20%. Sản phẩm win đang dưới ngưỡng tồn kho vẫn giữ trong top 3, nhưng phải cảnh báo kèm số ngày còn bán được. Số ngày này = tồn kho / số bán trung bình mỗi ngày của kỳ, ghi rõ là ước tính.

Báo cáo không tính lợi nhuận khi `data/gia-von.xlsx` còn trống.
