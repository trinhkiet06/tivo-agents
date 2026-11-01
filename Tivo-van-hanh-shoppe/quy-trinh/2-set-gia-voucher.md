# 2. Set giá ngày sale và voucher

Mục tiêu: có bảng giá và bảng voucher sẵn sàng để người phụ trách nhập lên Kênh Người Bán.
Luôn làm theo thứ tự: chốt giá trước, rồi mới set voucher.
Agent không đăng nhập được Shopee, nên không tự đổi giá hay tạo voucher trên sàn.

**Cách tính giá của shop:**
- Giá daily là giá đặt trên sàn. Voucher ngày sale kéo giá về đúng giá camp: giá daily − voucher = giá camp.
- Giá camp là giá khách trả ngày sale, đã gồm voucher. Không lấy giá camp trừ voucher thêm lần nữa.
- Không vừa hạ giá trên sàn xuống giá camp vừa bật voucher ngày sale, vì khách sẽ được giảm hai lần.
- Flash sale dùng voucher toàn shop trong `data/chot-sale.xlsx`: giá khách trả = giá daily − mức voucher flash sale.
- Giả định: voucher flash sale không cộng dồn với voucher ngày sale. Chủ shop chưa xác nhận, nên phải nêu trong file ghi chú.

**Đầu ra trong `output/2-gia-voucher/`:**
- `gia-<tên-chương-trình>.csv`: bảng giá ngày sale.
- `voucher-<tên-chương-trình>.csv`: bảng voucher.
- `ghi-chu-<tên-chương-trình>.md`: thời gian, sản phẩm bị loại, điểm cần chốt và checklist.

## Đầu vào

- `output/1-ke-hoach/lich-sale-shopee.md`. Nếu chưa có hoặc chưa có giờ của chương trình này thì làm nhiệm vụ 1 trước.
- `data/san-pham.xlsx`: giá niêm yết, giá daily, giá camp, voucher ngày sale.
- `data/chot-sale.xlsx`: voucher flash sale, đơn tối thiểu, số lượng khuyến mãi và số lượng voucher đã chốt.
- `data/ton-kho.xlsx`: tồn kho và ngưỡng cảnh báo.
- `data/gia-von.xlsx`: giá vốn, dùng để kiểm tra giá có làm lỗ hay không.

## Phần A: Set giá ngày sale

1. Lấy thời gian bắt đầu và kết thúc của chương trình từ lịch sale.
2. Bỏ sản phẩm dưới ngưỡng cảnh báo và ghi rõ lý do.
3. Giá ngày sale lấy đúng cột GIÁ BÁN CAMP. Giá sau sale là GIÁ BÁN DAILY. Kiểm tra giá daily − voucher = giá camp.
4. Tính % giảm so với giá daily = (giá daily − giá sale) / giá daily.
5. Tính % giảm so với giá niêm yết = (giá niêm yết − giá sale) / giá niêm yết.
6. Điền số lượng khuyến mãi mà chủ shop đã chốt trong `data/chot-sale.xlsx`. Nếu chưa chốt thì đề xuất ở cột riêng và ghi căn cứ.
7. So mức giảm với điều kiện của chương trình nếu lịch sale có ghi. Không có điều kiện thì ghi "chưa có điều kiện để kiểm tra".

**Cột của file giá:** Chương trình, Bắt đầu, Kết thúc, Mã SP, Tên sản phẩm, Giá niêm yết, Giá daily, Voucher ngày sale, Giá ngày sale, % giảm so với daily, % giảm so với niêm yết, Số lượng khuyến mãi, Số lượng đề xuất, Giá sau sale, Trạng thái.

**Quy tắc giá:**
- Không tự đặt giá. Danh mục để trống giá camp thì để trống giá sale và ghi "cần bổ sung".
- Giá sale phải thấp hơn giá daily, và giá daily không cao hơn giá niêm yết. Sai thì đánh dấu "cần kiểm tra", không tự sửa.
- Giá daily − voucher khác giá camp thì đánh dấu "cần kiểm tra", không tự sửa.
- Giá camp không đạt điều kiện chương trình thì báo chủ shop. Giá khác danh mục chỉ ghi ở cột "Giá đề xuất" thêm vào cuối bảng, có căn cứ, sau khi chủ shop yêu cầu.
- Số lượng khuyến mãi không vượt phần tồn kho trên ngưỡng cảnh báo. Mức này = tồn kho hiện tại − ngưỡng cảnh báo.
- Có giá vốn thì so với giá khách trả thấp nhất. Giá khách trả thấp hơn giá vốn thì đánh dấu "cần kiểm tra".
- Ô giá vốn còn trống thì ghi rõ trong file ghi chú là chưa kiểm tra được lỗ lãi của mã đó.

## Phần B: Set voucher

1. Chọn chương trình và khung giờ từ lịch sale. Thời gian voucher phải nằm trong khung giờ đó.
2. Chỉ lấy sản phẩm có trong bảng giá ở phần A.
3. Ngày sale và ngày đặc biệt lấy mức voucher từ danh mục. Flash sale lấy mức voucher toàn shop từ `data/chot-sale.xlsx`.
4. Tính giá cuối khách trả = giá daily − voucher, cho đơn 1 sản phẩm. Ở ngày sale, giá cuối phải bằng giá camp.
5. Điền số lượng voucher mà chủ shop đã chốt trong `data/chot-sale.xlsx`. Nếu chưa chốt thì đề xuất ở cột riêng và ghi căn cứ.

**Cột của file voucher:** Chương trình, Loại (flash sale, ngày sale, ngày đặc biệt), Bắt đầu, Kết thúc, Mã SP, Tên sản phẩm, Giá daily, Voucher, Giá cuối, Đơn tối thiểu, Số lượng voucher, Số lượng đề xuất, Trạng thái.

**Quy tắc voucher:**
- Không tự đặt mức voucher. Nguồn để trống thì ghi "không có voucher" hoặc "cần bổ sung", không tự điền.
- Đơn tối thiểu lấy từ `data/chot-sale.xlsx`. Ô còn trống thì để trống và ghi "cần chủ shop chốt".
- Voucher toàn shop cũng áp dụng cho mã dưới ngưỡng tồn kho. Phải nêu các mã này trong file ghi chú để chủ shop quyết định.
- Số lượng voucher của một sản phẩm không vượt phần tồn kho trên ngưỡng cảnh báo.

## Quy tắc chung

- Lịch còn trạng thái Dự kiến thì nêu rõ, vì giờ có thể đổi.
- Trạng thái của cả hai bảng luôn là "chờ duyệt" cho đến khi chủ shop báo đã duyệt.

## Checklist trong file ghi chú

**Trước sale:**
- [ ] Chủ shop đã duyệt bảng giá và bảng voucher
- [ ] Giá trên sàn vẫn là giá daily, voucher đúng từng sản phẩm, khách không được giảm hai lần
- [ ] Thời gian bắt đầu và kết thúc đúng lịch sale
- [ ] Số lượng khuyến mãi và số lượng voucher đúng bảng
- [ ] Tính thử giá cuối của một đơn trên sàn, so với cột Giá cuối

**Sau sale:**
- [ ] Giá đã về đúng giá daily
- [ ] Voucher đã hết hạn hoặc đã tắt
