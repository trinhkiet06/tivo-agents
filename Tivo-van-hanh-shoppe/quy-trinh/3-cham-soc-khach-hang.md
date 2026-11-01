# 3. Chăm sóc khách hàng

Mục tiêu: trả lời khách đúng thông tin và tìm hiểu lý do các đơn bị hủy.
Agent không vào được chat Shopee. Agent soạn tin nháp, nhân viên đọc lại rồi gửi.

## Nguồn để trả lời

| Câu hỏi về | Đọc ở đâu |
|---|---|
| Sản phẩm, thông số | Cột THÔNG TIN SẢN PHẨM trong `data/san-pham.xlsx` |
| Bảo hành, đổi trả, hoàn tiền, vận chuyển | `data/chinh-sach-shop.xlsx` |
| Giá, voucher | `data/san-pham.xlsx` và `output/2-gia-voucher/` |
| Còn hàng hay không | `data/ton-kho.xlsx` |
| Giờ và ngày sale | `output/1-ke-hoach/lich-sale-shopee.md` |
| Livestream | `data/livestream.xlsx` |
| Mẫu câu trả lời | `output/3-cskh/mau-tra-loi.md` |

Đọc lại các nguồn này mỗi lần trả lời, vì giờ sale và thông tin livestream có thể đã đổi.

## Trả lời câu hỏi của khách

- Trả lời ngắn, đúng câu hỏi và xưng hô như mẫu.
- Chỉ dùng thông tin có trong các nguồn trên. Không có thì trả lời shop sẽ kiểm tra lại, không đoán.
- Giờ sale còn trạng thái Dự kiến thì không báo như chắc chắn.
- `data/livestream.xlsx` không có dòng Đã chốt hoặc đã cũ thì không báo giờ live và ưu đãi live, chuyển nhân viên kiểm tra.
- Giá camp đã gồm voucher ngày sale. Không báo khách lấy giá camp trừ voucher thêm lần nữa.
- Không hứa hoàn tiền, đền bù hay quà tặng ngoài chính sách hiện hành.
- Không cam kết công dụng y tế hay hiệu quả quá mức cho sản phẩm chăm sóc răng miệng.
- Không dẫn khách ra ngoài Shopee. Không xin đánh giá 5 sao hay đổi quà lấy đánh giá.
- Câu hỏi mới hay gặp thì đề xuất thêm vào `output/3-cskh/mau-tra-loi.md`.

## Hỏi lý do đơn bị hủy

**Đầu ra:** `output/3-cskh/hoi-ly-do-huy-<yyyy-mm-dd>.md`

1. Lọc đơn trạng thái "Đã hủy" trong `data/don-hang-thang.xlsx`, theo khoảng ngày được yêu cầu. Mặc định là 7 ngày gần nhất có dữ liệu.
2. Bỏ các đơn đã có Lý do hoặc đã có Ngày đã hỏi khách trong `data/ly-do-huy.xlsx`.
3. Với mỗi đơn, soạn tin theo mẫu "Hỏi lý do hủy đơn". Không có thông tin khách thì chỉ ghi mã đơn, nhân viên tra trên Shopee.
4. Nhân viên gửi tin, ghi Ngày đã hỏi khách và câu trả lời vào `data/ly-do-huy.xlsx`.

Quy tắc khi hỏi:
- Chỉ hỏi một lần cho mỗi đơn. Khách không trả lời thì ghi "khách không phản hồi".
- Lịch sự, không trách khách, không ép đặt lại đơn.
- Không tự đoán lý do. Chỉ lý do do khách trả lời hoặc do Shopee ghi mới được đưa vào báo cáo.
