# Content video AI đợt 11.11: TIVO Smart

*Lập ngày 02/11/2026. Toàn bộ 14 video đang ở trạng thái chờ duyệt.*

## Cảnh báo trước khi duyệt

1. **Chỉ B-26 có link TikTok trong số các mã đủ hàng.** `data/chot-sale.xlsx` chưa có phần chốt "Đang bán trên TikTok", nên video của MC1200, MC870, MC500 và A-014 chỉ dùng được khi chủ shop xác nhận các mã này đang bán trên TikTok.
2. **Giá và voucher chưa được xác nhận cho TikTok.** 4 video có giá (V9, V10, V11, V12) chưa được đăng cho đến khi chủ shop xác nhận. Voucher flash sale 50.000đ không được dùng trong bộ content này.
3. **Chưa có dữ liệu TikTok.** Cả 4 sheet trong `data/tiktok/du-lieu-tiktok.xlsx` chưa có dòng số liệu nào.
4. **Chưa có ảnh thật.** Cả 10 thư mục trong `data/anh-san-pham/` đều trống, nên chưa chuyển được sang viết bộ lệnh video.
5. **Kế hoạch 11.11 chưa được duyệt.** Danh sách video và ngày đăng lấy từ `output/1-ke-hoach/ke-hoach-truyen-thong-11-11.md`. V1 đăng ngày 03/11 khó kịp nếu chưa có ảnh và chưa duyệt content trong hôm nay.

**Giả định:**
- Giá camp áp dụng trong ngày 11/11, từ 00:00, theo giả định của kế hoạch, vì chưa có ngày áp dụng chính thức.
- Chọn sản phẩm và câu mở đầu là ước đoán, vì chưa có dữ liệu hiệu quả trên TikTok.
- Mỗi cảnh dài 3 đến 5 giây, vì `data/cong-cu-video.xlsx` chưa có giới hạn của công cụ.
- Khung LIVE 20:00 – 22:00 là khung dự kiến trong kế hoạch.

## Tổng hợp

| Mã | Sản phẩm | Ngày giờ đăng | Có giá | Cần xác nhận đang bán | Gợi ý quay thật |
|---|---|---|---|---|---|
| V1 | B-26 | 03/11, 18:00 | Không | Không | Không |
| V4 | MC1200 | 04/11, 18:00 | Không | MC1200 | Một phần |
| V2 | B-26 | 05/11, 18:00 | Không | Không | Không |
| V5 | MC870, MC1200 | 06/11, 18:00 | Không | MC870, MC1200 | Có |
| V6 | MC870 | 07/11, 09:00 | Không | MC870 | Không |
| V3 | B-26 | 07/11, 18:00 | Không | Không | Một phần |
| V7 | A-014 | 08/11, 18:00 | Không | A-014 | Có |
| V8 | MC500 | 09/11, 09:00 | Không | MC500 | Không |
| V9 | B-26, MC1200, MC870 | 09/11, 18:00; đăng lại 11/11, 18:00 | **Có** | MC1200, MC870 | Không |
| V10 | B-26, MC1200, MC870 | 10/11, 09:00 | **Có** | MC1200, MC870 | Không |
| V11 | B-26 | 11/11, 00:00 | **Có** | Không | Không |
| V12 | MC1200, MC870 | 11/11, 12:00 | **Có** | MC1200, MC870 | Không |
| V13 | B-26, MC1200, MC870 | 12/11, 18:00 | Không | MC1200, MC870 | Không |
| V14 | B-26 | 13/11, 18:00 | Không | Không | Có |

Nếu một mã chưa bán trên TikTok, bỏ cảnh và câu của mã đó khỏi video chung (V9, V10, V13). V5 và V12 chỉ dùng được khi cả hai mã đang bán.

**Không làm content:**

| Mã SP | Tồn / Ngưỡng | Lý do |
|---|---:|---|
| B-02PRO | 14 / 20 | Dưới ngưỡng cảnh báo |
| A-028 | 9 / 15 | Dưới ngưỡng cảnh báo |
| MC650 | 11 / 15 | Dưới ngưỡng cảnh báo |
| MPI480 | 28 / 10 | Tên ghi 480, danh mục ghi 500ml; cần chốt số đúng |
| MC570 | 41 / 15 | Đủ hàng nhưng không có trong danh sách video của kế hoạch |

**Khác với ý tưởng trong kế hoạch**, để làm được bằng video AI và không nêu thông tin ngoài danh mục:
- **V1, V2:** bỏ cảnh tay bấm và quay thao tác, thay bằng sản phẩm xoay kèm chữ giải thích.
- **V3:** bỏ cảnh mở hộp, vì danh mục chỉ ghi kèm 2 đầu bàn chải.
- **V4:** đổi câu mở đầu "ngoài đời to cỡ nào", vì AI không thể hiện đúng kích thước thật.
- **V5:** bỏ cảnh đổ nước đầy.
- **V14:** bỏ hướng dẫn đổi chế độ, vì danh mục không có cách thao tác. Bỏ câu "còn ưu đãi đến ngày..." vì chưa có ngày.

## Lưu ý chung khi dựng

- Mọi cảnh chỉ có sản phẩm và bối cảnh, không có người, khuôn mặt hay miệng.
- Không để AI tự vẽ chữ. Toàn bộ chữ trên màn hình được thêm khi dựng.
- Không có cảnh răng trắng lên, nướu thay đổi, trước và sau khi dùng hay hơi lạnh giả lập.
- Với B-26, Whitening, Sensitive, Gumcare chỉ là tên chế độ, không giải thích thành công dụng.
- Bình giữ nhiệt không nêu số giờ giữ nóng hoặc lạnh, vì danh mục không có thông số này.
- Kiểm tra lại tồn kho vào ngày đăng. Mã xuống dưới ngưỡng thì dừng video đó. Không dùng câu "sắp hết hàng" nếu chưa có số tồn thật sự thấp.

---

## V1: 5 chế độ của bàn chải điện B-26
- Sản phẩm, mã SP: Bàn chải điện Magic, B-26
- Giai đoạn và ngày đăng: Chuẩn bị, 03/11/2026, 18:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "Một cây bàn chải mà có tới 5 chế độ, bạn sẽ dùng chế độ nào?"

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | B-26 đứng giữa bàn đá sáng màu, máy tiến chậm vào | Một cây bàn chải mà có tới 5 chế độ, bạn sẽ dùng chế độ nào? | 5 chế độ, bạn chọn gì? |
| 2 | 3–8 | B-26 xoay chậm trên đế tròn | Clean, Whitening, Sensitive, Gumcare, Polish. | Clean / Whitening / Sensitive / Gumcare / Polish |
| 3 | 8–12 | Cận thân máy trong phòng tắm gọn gàng | Tần số rung 40.000 lần mỗi phút. | 40.000 lần/phút |
| 4 | 12–15 | B-26 đặt trên kệ, ánh sáng dịu | Bấm giỏ hàng xem B-26, nhớ lưu lại chờ 11.11 nhé. | Xem B-26 ở giỏ hàng |

- Lời kêu gọi mua: "Bấm giỏ hàng xem B-26, nhớ lưu lại chờ 11.11 nhé."
- Caption: Một cây bàn chải, 5 chế độ: Clean, Whitening, Sensitive, Gumcare, Polish. Bạn sẽ dùng chế độ nào? Bấm giỏ hàng xem B-26 nhé!
- Hashtag: #BanChaiDienMagic #MagicB26 #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột THÔNG TIN SẢN PHẨM
- Trạng thái: chờ duyệt

## V2: Smartimer 2 phút của B-26
- Sản phẩm, mã SP: Bàn chải điện Magic, B-26
- Giai đoạn và ngày đăng: Khởi động, 05/11/2026, 18:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "Bạn có biết mình đánh răng bao lâu không? Cây này tự đếm 2 phút."

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–4 | B-26 trên bồn rửa sáng sủa, máy lia ngang chậm | Bạn có biết mình đánh răng bao lâu không? Cây này tự đếm 2 phút. | Smartimer 2 phút |
| 2 | 4–9 | B-26 xoay chậm trên nền sáng | Cứ 30 giây lại nhắc bạn chuyển vùng. | Nhắc chuyển vùng sau mỗi 30 giây |
| 3 | 9–12 | Cận thân máy, ánh sáng buổi sáng | Pin 1.200mAh, dùng được 30 ngày. | Pin 1.200mAh, dùng 30 ngày |
| 4 | 12–15 | B-26 đặt trên kệ | Ghé giỏ hàng xem chi tiết nhé. | Xem ở giỏ hàng |

- Lời kêu gọi mua: "Ghé giỏ hàng xem chi tiết nhé."
- Caption: Smartimer 2 phút, nhắc chuyển vùng sau mỗi 30 giây, đỡ phải tự canh giờ khi đánh răng. Ghé giỏ hàng xem B-26 nhé!
- Hashtag: #BanChaiDienMagic #MagicB26 #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột THÔNG TIN SẢN PHẨM
- Trạng thái: chờ duyệt

## V3: B-26 có những gì
- Sản phẩm, mã SP: Bàn chải điện Magic, B-26
- Giai đoạn và ngày đăng: Khởi động, 07/11/2026, 18:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "Bàn chải điện 112g này có những gì?"

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | B-26 giữa khung hình, nền sáng, máy tiến chậm | Bàn chải điện 112g này có những gì? | Chỉ 112g |
| 2 | 3–7 | B-26 đặt cạnh 2 đầu bàn chải trên mặt bàn | Đi kèm 2 đầu bàn chải. | Kèm 2 đầu bàn chải |
| 3 | 7–12 | B-26 xoay chậm | Pin 1.200mAh dùng được 30 ngày, chống nước IPX7, bảo hành 12 tháng. | Pin 1.200mAh, 30 ngày / IPX7 / Bảo hành 12 tháng |
| 4 | 12–15 | B-26 trên kệ phòng tắm | Theo dõi shop để nhận nhắc sale 11.11 nhé. | Theo dõi shop chờ 11.11 |

- Lời kêu gọi mua: "Theo dõi shop để nhận nhắc sale 11.11 nhé."
- Caption: Nhẹ 112g, kèm 2 đầu bàn chải, pin 1.200mAh dùng được 30 ngày. Theo dõi shop để nhận nhắc sale 11.11 nhé!
- Hashtag: #BanChaiDienMagic #MagicB26 #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột THÔNG TIN SẢN PHẨM
- Nên quay thật: nếu muốn làm cảnh mở hộp, phải quay hộp và phụ kiện thật. Chủ shop quyết định.
- Trạng thái: chờ duyệt

## V4: Bình giữ nhiệt 1200ml
- Sản phẩm, mã SP: Bình giữ nhiệt Magic MC1200, MC1200
- Giai đoạn và ngày đăng: Khởi động, 04/11/2026, 18:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "Cần một chiếc bình dung tích lớn? Đây là bình 1200ml."

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–4 | MC1200 đứng trên bàn làm việc, máy tiến chậm | Cần một chiếc bình dung tích lớn? Đây là bình 1200ml. | 1200ml |
| 2 | 4–8 | MC1200 xoay chậm trên nền sáng | Vỏ ngoài inox 304, bên trong inox 316. | Vỏ inox 304 / Trong inox 316 |
| 3 | 8–12 | Lần lượt 3 màu Xám, Hồng, Xanh đứng thành hàng | Có 3 màu: xám, hồng, xanh. | Xám / Hồng / Xanh |
| 4 | 12–15 | MC1200 đặt trên bàn, ánh sáng dịu | Bấm giỏ hàng xem bình 1200ml nhé. | Xem ở giỏ hàng |

- Lời kêu gọi mua: "Bấm giỏ hàng xem bình 1200ml nhé."
- Caption: Bình 1200ml cho ai cần dung tích lớn, vỏ inox 304, bên trong inox 316, có 3 màu Xám, Hồng, Xanh. Bấm giỏ hàng xem nhé!
- Hashtag: #BinhGiuNhietMagic #MC1200 #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột THÔNG TIN SẢN PHẨM
- Nên quay thật: cảnh cầm bình trên tay để thấy kích thước thật, vì AI có thể làm sai tỷ lệ. Chủ shop quyết định.
- Trạng thái: chờ duyệt

## V5: 870ml hay 1200ml
- Sản phẩm, mã SP: Bình giữ nhiệt Magic MC870, MC870; Bình giữ nhiệt Magic MC1200, MC1200
- Giai đoạn và ngày đăng: Khởi động, 06/11/2026, 18:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "870ml hay 1200ml, bạn chọn bình nào?"

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | Hai bình đứng cạnh nhau trên bàn, máy tiến chậm | 870ml hay 1200ml, bạn chọn bình nào? | 870ml hay 1200ml? |
| 2 | 3–7 | MC870 xoay chậm | MC870 có 3 màu: vàng, hồng, xám. | MC870: Vàng / Hồng / Xám |
| 3 | 7–11 | MC1200 xoay chậm | MC1200 có 3 màu: xám, hồng, xanh. | MC1200: Xám / Hồng / Xanh |
| 4 | 11–15 | Hai bình đứng cạnh nhau, ánh sáng dịu | Bình luận lựa chọn của bạn nhé, cả hai đều ở giỏ hàng. | Bạn chọn bình nào? |

- Lời kêu gọi mua: "Bình luận lựa chọn của bạn nhé, cả hai đều ở giỏ hàng."
- Caption: 870ml hay 1200ml, bạn hợp với bình nào? Cả hai đều vỏ inox 304, bên trong inox 316. Bình luận lựa chọn của bạn và xem ở giỏ hàng nhé!
- Hashtag: #BinhGiuNhietMagic #MC870 #MC1200 #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột THÔNG TIN SẢN PHẨM
- Nên quay thật: cả video, vì cần thấy đúng chênh lệch kích thước giữa hai bình. Nếu dùng AI, phải kiểm tra kỹ tỷ lệ hai bình so với sản phẩm thật. Chủ shop quyết định.
- Trạng thái: chờ duyệt

## V6: Màu nào hợp với bạn
- Sản phẩm, mã SP: Bình giữ nhiệt Magic MC870, MC870
- Giai đoạn và ngày đăng: Khởi động, 07/11/2026, 09:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "Vàng, Hồng hay Xám: màu nào hợp với bạn?"

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | Ba bình 3 màu đứng thành hàng, máy lia ngang | Vàng, hồng hay xám: màu nào hợp với bạn? | Vàng / Hồng / Xám |
| 2 | 3–8 | Lần lượt từng màu xoay chậm trên nền sáng | Bình MC870, dung tích 870ml. | 870ml |
| 3 | 8–12 | Một bình trên bàn làm việc, ánh sáng tự nhiên | Vỏ ngoài inox 304, bên trong inox 316. | Vỏ inox 304 / Trong inox 316 |
| 4 | 12–15 | Ba bình đứng thành hàng | Chọn màu của bạn trong giỏ hàng nhé. | Chọn màu ở giỏ hàng |

- Lời kêu gọi mua: "Chọn màu của bạn trong giỏ hàng nhé."
- Caption: 870ml, 3 màu Vàng, Hồng, Xám: bạn chọn màu nào? Chọn màu của bạn trong giỏ hàng nhé!
- Hashtag: #BinhGiuNhietMagic #MC870 #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột THÔNG TIN SẢN PHẨM
- Trạng thái: chờ duyệt

## V7: Quạt cầm tay có mặt kim loại lạnh
- Sản phẩm, mã SP: Quạt sạc cầm tay mini, A-014
- Giai đoạn và ngày đăng: Khởi động, 08/11/2026, 18:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "Quạt cầm tay có mặt kim loại lạnh sau khoảng 3 – 5 giây."

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | A-014 đứng trên bàn học, máy tiến chậm | Quạt cầm tay có mặt kim loại lạnh sau khoảng 3 đến 5 giây. | Lạnh sau khoảng 3 – 5 giây |
| 2 | 3–7 | Cận mặt kim loại của quạt, không có hơi lạnh giả lập | Dùng công nghệ sò lạnh Peltier, vừa thổi gió vừa làm lạnh. | Sò lạnh Peltier |
| 3 | 7–12 | A-014 xoay chậm trên nền sáng | 5 cấp độ gió, pin 2.000mAh, dùng khoảng 6 đến 8 giờ tùy cấp độ. | 5 cấp gió / Pin 2.000mAh / Khoảng 6 – 8 giờ tùy cấp độ |
| 4 | 12–15 | A-014 đặt cạnh balo trên ghế | Bấm giỏ hàng xem A-014 nhé. | Xem ở giỏ hàng |

- Lời kêu gọi mua: "Bấm giỏ hàng xem A-014 nhé."
- Caption: Quạt cầm tay có mặt kim loại làm lạnh sau khoảng 3 – 5 giây, nhỏ gọn để mang theo. Bấm giỏ hàng xem A-014 nhé!
- Hashtag: #QuatSacMagic #MagicA014 #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột THÔNG TIN SẢN PHẨM
- Nên quay thật: cảnh quạt chạy, đổi cấp gió và đèn LED, vì cần thấy thao tác thật. Chủ shop quyết định.
- Trạng thái: chờ duyệt

## V8: Bình 500ml, 3 màu
- Sản phẩm, mã SP: Bình giữ nhiệt Magic MC500, MC500
- Giai đoạn và ngày đăng: Khởi động, 09/11/2026, 09:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "Bình 500ml, 3 màu, bạn chọn màu nào?"

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | Ba bình 3 màu đứng thành hàng, máy lia ngang | Bình 500ml, 3 màu, bạn chọn màu nào? | 500ml, 3 màu |
| 2 | 3–8 | Lần lượt Vàng, Hồng, Trắng xoay chậm | Vàng, hồng hay trắng. | Vàng / Hồng / Trắng |
| 3 | 8–12 | Một bình trên bàn làm việc, ánh sáng tự nhiên | Vỏ ngoài inox 304, bên trong inox 316. | Vỏ inox 304 / Trong inox 316 |
| 4 | 12–15 | Ba bình đứng thành hàng | Xem màu của bạn trong giỏ hàng nhé. | Xem màu ở giỏ hàng |

- Lời kêu gọi mua: "Xem màu của bạn trong giỏ hàng nhé."
- Caption: Bình 500ml với 3 màu Vàng, Hồng, Trắng, bạn chọn màu nào? Xem màu trong giỏ hàng nhé!
- Hashtag: #BinhGiuNhietMagic #MC500 #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột THÔNG TIN SẢN PHẨM
- Trạng thái: chờ duyệt

## V9: Giá ngày 11/11 của 3 sản phẩm
- Sản phẩm, mã SP: Bàn chải điện Magic, B-26; Bình giữ nhiệt Magic MC1200, MC1200; Bình giữ nhiệt Magic MC870, MC870
- Giai đoạn và ngày đăng: Khởi động, 09/11/2026, 18:00; đăng lại 11/11/2026, 18:00 kèm nhắc LIVE
- Thời lượng: 20 giây
- Câu mở đầu 3 giây: "Lưu lại giá ngày 11/11 của 3 sản phẩm này."

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | Ba sản phẩm trên bàn sáng, máy tiến chậm | Lưu lại giá ngày 11/11 của 3 sản phẩm này. | Giá ngày 11/11 |
| 2 | 3–8 | B-26 xoay chậm | Bàn chải điện B-26, voucher 90 nghìn, còn 419 nghìn. | B-26: 509.000đ, voucher 90.000đ, còn **419.000đ** / Áp dụng ngày 11/11 |
| 3 | 8–12 | MC1200 xoay chậm | Bình 1200ml, voucher 110 nghìn, còn 499 nghìn. | MC1200: 609.000đ, voucher 110.000đ, còn **499.000đ** / Áp dụng ngày 11/11 |
| 4 | 12–16 | MC870 xoay chậm | Bình 870ml, voucher 110 nghìn, còn 469 nghìn. | MC870: 579.000đ, voucher 110.000đ, còn **469.000đ** / Áp dụng ngày 11/11 |
| 5 | 16–20 | Ba sản phẩm đứng cạnh nhau | Lưu voucher, canh 0h ngày 11/11 nhé. | Lưu voucher, 0h ngày 11/11 |

- Lời kêu gọi mua: "Lưu voucher, canh 0h ngày 11/11 nhé."
- Caption: Giá ngày 11/11: B-26 từ 509.000đ, voucher 90.000đ còn 419.000đ. MC1200 từ 609.000đ, voucher 110.000đ còn 499.000đ. MC870 từ 579.000đ, voucher 110.000đ còn 469.000đ. Lưu voucher, canh 0h ngày 11/11 nhé!
- Hashtag: #BanChaiDienMagic #BinhGiuNhietMagic #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột GIÁ BÁN DAILY, VOUCHER, GIÁ BÁN CAMP
- Trạng thái: chờ duyệt

## V10: Còn 1 ngày đến 11/11
- Sản phẩm, mã SP: Bàn chải điện Magic, B-26; Bình giữ nhiệt Magic MC1200, MC1200; Bình giữ nhiệt Magic MC870, MC870
- Giai đoạn và ngày đăng: Khởi động, 10/11/2026, 09:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "Chỉ còn 1 ngày nữa là đến 11/11."

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | Ba sản phẩm trên bàn, ánh sáng ấm, máy tiến chậm | Chỉ còn 1 ngày nữa là đến 11/11. | Còn 1 ngày |
| 2 | 3–9 | Lần lượt B-26, MC1200, MC870 xoay chậm | B-26 còn 419 nghìn, MC1200 còn 499 nghìn, MC870 còn 469 nghìn, sau khi dùng voucher. | B-26: **419.000đ** / MC1200: **499.000đ** / MC870: **469.000đ** / Giá sau voucher, áp dụng ngày 11/11 |
| 3 | 9–12 | Ba sản phẩm đứng cạnh nhau | LIVE tối mai từ 20 giờ đến 22 giờ. | LIVE 20:00 – 22:00 ngày 11/11 |
| 4 | 12–15 | Cận B-26 và hai bình | Lưu voucher ngay hôm nay nhé. | Lưu voucher hôm nay |

- Lời kêu gọi mua: "Lưu voucher ngay hôm nay nhé."
- Caption: Còn 1 ngày đến 11/11! Giá sau voucher áp dụng ngày 11/11: B-26 419.000đ, MC1200 499.000đ, MC870 469.000đ. Lưu voucher ngay hôm nay nhé!
- Hashtag: #BanChaiDienMagic #BinhGiuNhietMagic #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột GIÁ BÁN CAMP; khung LIVE từ kế hoạch 11.11, mục 5 (dự kiến)
- Trạng thái: chờ duyệt

## V11: 0h, giá 11/11 của B-26 đã mở
- Sản phẩm, mã SP: Bàn chải điện Magic, B-26
- Giai đoạn và ngày đăng: Ngày sale, 11/11/2026, 00:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "0h rồi, giá 11/11 của B-26 đã mở."

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | B-26 trên nền tối sang, ánh đèn sáng dần | 0h rồi, giá 11/11 của B-26 đã mở. | 0h ngày 11/11 |
| 2 | 3–8 | B-26 xoay chậm | Giá 509 nghìn, voucher 90 nghìn, còn 419 nghìn. | 509.000đ, voucher 90.000đ, còn **419.000đ** / Áp dụng ngày 11/11 |
| 3 | 8–12 | Cận thân máy | 5 chế độ: Clean, Whitening, Sensitive, Gumcare, Polish. | Clean / Whitening / Sensitive / Gumcare / Polish |
| 4 | 12–15 | B-26 trên đế tròn | Bấm giỏ hàng để đặt ngay nhé. | Đặt ở giỏ hàng |

- Lời kêu gọi mua: "Bấm giỏ hàng để đặt ngay nhé."
- Caption: 0h ngày 11/11, B-26 từ 509.000đ, voucher 90.000đ còn 419.000đ. Áp dụng ngày 11/11. Bấm giỏ hàng để đặt ngay nhé!
- Hashtag: #BanChaiDienMagic #MagicB26 #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột GIÁ BÁN DAILY, VOUCHER, GIÁ BÁN CAMP, THÔNG TIN SẢN PHẨM
- Trạng thái: chờ duyệt

## V12: Giữa trưa 11/11, chọn bình nào
- Sản phẩm, mã SP: Bình giữ nhiệt Magic MC1200, MC1200; Bình giữ nhiệt Magic MC870, MC870
- Giai đoạn và ngày đăng: Ngày sale, 11/11/2026, 12:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "Giữa trưa 11/11, chọn bình nào đây?"

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | Hai bình trên bàn làm việc, nắng trưa qua cửa sổ | Giữa trưa 11/11, chọn bình nào đây? | Chọn bình nào? |
| 2 | 3–7 | MC870 xoay chậm | Bình 870ml, voucher 110 nghìn, còn 469 nghìn. | MC870: 579.000đ, voucher 110.000đ, còn **469.000đ** |
| 3 | 7–11 | MC1200 xoay chậm | Bình 1200ml, voucher 110 nghìn, còn 499 nghìn. | MC1200: 609.000đ, voucher 110.000đ, còn **499.000đ** |
| 4 | 11–15 | Hai bình đứng cạnh nhau | Bấm giỏ hàng nhé, tối nay 20 giờ có LIVE. | Áp dụng ngày 11/11 / LIVE 20:00 tối nay |

- Lời kêu gọi mua: "Bấm giỏ hàng nhé, tối nay 20 giờ có LIVE."
- Caption: Hôm nay 11/11: MC870 từ 579.000đ, voucher 110.000đ còn 469.000đ. MC1200 từ 609.000đ, voucher 110.000đ còn 499.000đ. Bấm giỏ hàng nhé, tối nay 20:00 có LIVE!
- Hashtag: #BinhGiuNhietMagic #MC870 #MC1200 #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: `san-pham.xlsx`, cột GIÁ BÁN DAILY, VOUCHER, GIÁ BÁN CAMP; khung LIVE từ kế hoạch 11.11, mục 5 (dự kiến)
- Trạng thái: chờ duyệt

## V13: Cảm ơn sau ngày 11/11
- Sản phẩm, mã SP: Bàn chải điện Magic, B-26; Bình giữ nhiệt Magic MC1200, MC1200; Bình giữ nhiệt Magic MC870, MC870
- Giai đoạn và ngày đăng: Sau sale, 12/11/2026, 18:00
- Thời lượng: 12 giây
- Câu mở đầu 3 giây: "Cảm ơn mọi người đã ủng hộ shop dịp 11/11."

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–4 | Ba sản phẩm trên bàn, ánh sáng ấm, máy tiến chậm | Cảm ơn mọi người đã ủng hộ shop dịp 11/11. | Cảm ơn bạn đã ủng hộ |
| 2 | 4–8 | Các thùng hàng trơn không chữ, không logo, xếp gọn trên kệ | Shop đang xử lý đơn và gửi đến bạn. | Shop đang xử lý đơn |
| 3 | 8–12 | Ba sản phẩm đứng cạnh nhau | Nhận hàng nhớ để lại đánh giá nhé. | Nhận hàng nhớ đánh giá nhé |

- Lời kêu gọi mua: "Nhận hàng nhớ để lại đánh giá nhé."
- Caption: Cảm ơn mọi người đã ủng hộ TIVO Smart dịp 11/11! Shop đang xử lý đơn và gửi đến bạn. Nhận hàng nhớ để lại đánh giá nhé!
- Hashtag: #TIVOSmart #Magic #TikTokShop1111 (cần kiểm tra)
- Thông tin lấy từ: kế hoạch 11.11, mục 4, V13
- Trạng thái: chờ duyệt

## V14: Xem nhanh tính năng B-26
- Sản phẩm, mã SP: Bàn chải điện Magic, B-26
- Giai đoạn và ngày đăng: Sau sale, 13/11/2026, 18:00
- Thời lượng: 15 giây
- Câu mở đầu 3 giây: "Mới nhận B-26? Xem nhanh các tính năng nhé."

| Cảnh | Giây | Hình ảnh | Lời đọc | Chữ trên màn hình |
|---|---|---|---|---|
| 1 | 0–3 | B-26 trên bồn rửa sáng sủa, máy tiến chậm | Mới nhận B-26? Xem nhanh các tính năng nhé. | Mới nhận B-26? |
| 2 | 3–8 | B-26 xoay chậm | Có 5 chế độ: Clean, Whitening, Sensitive, Gumcare, Polish. | Clean / Whitening / Sensitive / Gumcare / Polish |
| 3 | 8–12 | Cận thân máy | Smartimer 2 phút, nhắc chuyển vùng sau mỗi 30 giây. | Smartimer 2 phút / Nhắc sau mỗi 30 giây |
| 4 | 12–15 | B-26 trên kệ | Chưa có B-26? Bấm giỏ hàng xem nhé. | Xem ở giỏ hàng |

- Lời kêu gọi mua: "Chưa có B-26? Bấm giỏ hàng xem nhé."
- Caption: Mới nhận B-26? Máy có 5 chế độ và Smartimer 2 phút, nhắc chuyển vùng sau mỗi 30 giây. Chưa có B-26 thì bấm giỏ hàng xem nhé!
- Hashtag: #BanChaiDienMagic #MagicB26
- Thông tin lấy từ: `san-pham.xlsx`, cột THÔNG TIN SẢN PHẨM
- Nên quay thật: cảnh hướng dẫn đổi chế độ, vì danh mục không ghi cách thao tác và cần thao tác thật trên sản phẩm. Chủ shop quyết định.
- Trạng thái: chờ duyệt

---

## Cần chủ shop chốt

| # | Việc | Ảnh hưởng | Hạn |
|---|---|---|---|
| 1 | Điền "Đang bán trên TikTok" cho MC1200, MC870, MC500, A-014 trong `data/chot-sale.xlsx` | Quyết định V4, V5, V6, V7, V8, V12 và một phần V9, V10, V13 | 03/11 |
| 2 | Xác nhận giá và voucher cho TikTok, ngày áp dụng, đơn tối thiểu | V9, V10, V11, V12 | 03/11 |
| 3 | Duyệt content, gồm các cảnh gợi ý quay thật ở V3, V4, V5, V7, V14 | Chưa duyệt thì chưa viết được bộ lệnh video | 03/11 |
| 4 | Tải ảnh thật vào `data/anh-san-pham/<MÃ SP>/` | Chưa có ảnh thì dừng video của mã đó | 03/11 |
| 5 | Xác nhận khung LIVE 20:00 – 22:00 ngày 11/11 | V10, V12 và bản đăng lại của V9 | 09/11 |
| 6 | Xem hashtag chiến dịch 2026 trong Seller Center | Thay `#TikTokShop1111` nếu khác | 03/11 |
