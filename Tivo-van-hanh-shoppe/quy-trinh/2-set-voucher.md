# 2. Set voucher cho giờ flash sale và ngày sale

Mục tiêu: có bảng voucher sẵn sàng để người phụ trách nhập lên Kênh Người Bán.
Agent không đăng nhập được Shopee, nên không tự tạo voucher trên sàn.

**Đầu ra:** `output/2-voucher/voucher-<tên-chương-trình>.csv` và `output/2-voucher/voucher-<tên-chương-trình>.md`.

## Đầu vào

- `output/1-ke-hoach/lich-sale-shopee.md`. Nếu chưa có hoặc chưa có giờ của chương trình này thì làm nhiệm vụ 1 trước.
- `data/san-pham.xlsx`: giá camp và voucher.
- `data/ton-kho.xlsx`: tồn kho và ngưỡng cảnh báo.

## Cách làm

1. Chọn chương trình và khung giờ từ lịch sale. Thời gian voucher phải nằm trong khung giờ đó.
2. Bỏ sản phẩm dưới ngưỡng cảnh báo và ghi rõ lý do.
3. Lấy giá camp và mức voucher đúng từ danh mục.
4. Tính giá cuối khách trả = giá camp − voucher, cho đơn 1 sản phẩm.
5. Điền số lượng voucher mà chủ shop đã chốt. Nếu chưa chốt thì đề xuất ở cột riêng và ghi căn cứ.

## Cột của file CSV

Chương trình, Loại (flash sale, ngày sale, ngày đặc biệt), Bắt đầu, Kết thúc, Mã SP, Tên sản phẩm, Giá camp, Voucher, Giá cuối, Đơn tối thiểu, Số lượng voucher, Số lượng đề xuất, Trạng thái.

## Quy tắc

- Không tự đặt mức voucher. Danh mục để trống thì ghi "không có voucher" hoặc "cần bổ sung", không tự điền.
- Đơn tối thiểu không có trong dữ liệu. Để trống và ghi "cần chủ shop chốt".
- Số lượng voucher của một sản phẩm không vượt phần tồn kho trên ngưỡng cảnh báo.
- Lịch còn trạng thái Dự kiến thì nêu rõ, vì giờ có thể đổi.
- Trạng thái luôn là "chờ duyệt" cho đến khi chủ shop báo đã duyệt.
- Chưa có giá vốn nên không kiểm tra được voucher có làm lỗ hay không. Phải ghi rõ điều này trong file `.md`.

## File `.md` kèm theo

Gồm thời gian chương trình, sản phẩm bị loại kèm lý do, điểm cần chủ shop chốt và checklist kiểm tra sau khi nhập lên sàn.
