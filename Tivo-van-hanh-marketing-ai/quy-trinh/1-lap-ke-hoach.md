# 1. Lập kế hoạch: tra cứu ngày sale và kế hoạch truyền thông

**Đầu ra:**
- `output/1-ke-hoach/lich-sale-tiktok.md`: lịch tra cứu được, cập nhật mỗi lần tra và ghi ngày tra cứu.
- `output/1-ke-hoach/ke-hoach-truyen-thong-<tên-sale>.md`: kế hoạch cho từng đợt sale.

## Bước 1: Tra cứu ngày sale

Lấy hôm nay làm mốc, tra TikTok Shop Việt Nam trong 60 ngày tới.

| Loại | Gồm |
|---|---|
| Ngày sale | Ngày đôi, sale giữa tháng, sale ngày lương |
| Ngày sale đặc biệt | 11.11, 12.12, Black Friday, Tết, 8.3, 20.10, 20.11 và các dịp lớn khác |

Với mỗi chương trình, ghi tên, ngày bắt đầu và kết thúc, ngày đỉnh, khung giờ vàng, hạn đăng ký, điều kiện, trạng thái, link nguồn và ngày tra cứu.

**Thứ tự nguồn:**
1. Seller Center, Học viện TikTok Shop và thông báo chính thức của TikTok Shop.
2. Báo điện tử và trang tin thương mại điện tử uy tín.
3. Blog và hội nhóm nhà bán hàng, chỉ để tham khảo và phải ghi là nguồn không chính thức.

**Trạng thái:**
- **Chính thức:** có nguồn từ TikTok Shop, hoặc ít nhất 2 nguồn uy tín khớp nhau.
- **Dự kiến:** suy theo thông lệ hoặc chỉ có nguồn không chính thức.
- Không tìm được thì ghi "chưa tìm thấy công bố". Nguồn mâu thuẫn thì liệt kê cả hai và chọn nguồn chính thức hơn.
- Không truy cập được web thì nói rõ và chỉ dùng `data/lich-sale-va-ngan-sach.xlsx`.

## Bước 2: Chọn đợt sale

- Chủ shop chỉ định thì dùng đợt đó.
- Nếu không, chọn đợt gần nhất mà ngày đỉnh còn ít nhất 7 ngày, ưu tiên ngày sale đặc biệt.
- Đối chiếu `data/lich-sale-va-ngan-sach.xlsx`. Ngày lệch thì báo chủ shop. File không có ngân sách thì đề xuất và ghi "chờ duyệt".

## Bước 3: Mốc thời gian

Gọi D là ngày đỉnh của đợt sale. **Giả định:** "trước 1 tuần" tính theo ngày đỉnh. Nếu đợt sale bắt đầu sớm hơn D-7 thì cảnh báo ở đầu kế hoạch.

| Mốc | Việc phải xong |
|---|---|
| Trước D-7 | Kế hoạch được duyệt, content và video AI sẵn sàng |
| D-7 đến D-1 | Đăng video khởi động, nhá sản phẩm, đếm ngược, nhắc lưu voucher |
| D | Đăng video theo khung giờ vàng |
| D+1 đến D+3 | Video cảm ơn, tổng kết hiệu quả |

Nếu đã trễ hơn D-7, vẫn lập kế hoạch rút gọn và đặt cảnh báo lên đầu.

## Nội dung kế hoạch truyền thông

1. **Thông tin đợt sale:** tên, ngày giờ, trạng thái, hạn đăng ký, nguồn, cảnh báo.
2. **Mục tiêu và ngân sách:** lấy từ file nội bộ, không có thì ghi là đề xuất.
3. **Sản phẩm đẩy mạnh:** căn cứ dữ liệu TikTok, tồn kho và phần kho đã chốt trong `data/chot-sale.xlsx`, kèm giá daily, voucher và giá camp.
4. **Sản phẩm không đẩy:** nêu lý do.
5. **Thông điệp chính:** mỗi giai đoạn một thông điệp.
6. **Lịch truyền thông D-7 đến D+3:** bảng gồm ngày, giờ, mã video, sản phẩm, thông điệp, trạng thái.
7. **Danh sách video cần làm:** mã video V1, V2, ... để chuyển sang nhiệm vụ 2.
8. **Cần chủ shop chốt:** nêu rõ từng việc và hạn.
