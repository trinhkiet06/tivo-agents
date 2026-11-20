# 3. Tạo video TikTok sale (tự động, không cần duyệt)

**Tài liệu gốc:** `quy-trinh/mau-video-tiktok.md`, gồm quy tắc bắt buộc, nhận diện, danh sách sản phẩm, dòng thời gian, mẫu chữ T01–T04, caption và checklist. **Đọc hết tài liệu đó trước.** File này chỉ nói cách áp dụng khi tác vụ chạy tự động. Chỗ nào hai file khác nhau thì tài liệu gốc thắng, trừ phần "Áp dụng khi chạy tự động" và phần "Video liệt kê nhiều sản phẩm" dưới đây.

Agent tự viết kịch bản và tự xuất video MP4, không chờ chủ shop duyệt. Video được lưu vào bản nháp TikTok, chủ shop tự xem và bấm đăng (`quy-trinh/4-dang-tiktok.md`).

## Video liệt kê nhiều sản phẩm

Từ bản này, **mỗi video T01–T04 liệt kê tất cả sản phẩm ở mục 3 của tài liệu gốc**, không còn chọn 1 sản phẩm chủ lực. Mỗi video vẫn giữ mục tiêu riêng theo mục 6 (T01 báo ngày sale, T02 ưu đãi, T03 lợi ích sản phẩm, T04 đếm ngược), chỉ phần giữa video đổi thành danh sách sản phẩm.

**Thứ tự sản phẩm:** theo thứ tự ở mục 3. Sản phẩm được đẩy mạnh trong kế hoạch truyền thông lên đầu. Cả 4 video của một campaign dùng cùng một thứ tự để khán giả nhận ra chuỗi.

**Sản phẩm bị bỏ khỏi danh sách:** chỉ khi không có ảnh `data/anh-san-pham/<MÃ SP>/<MÃ SP>-1.png`. Ghi tên sản phẩm bị bỏ vào sheet "Cần xác nhận". Còn lại 0 sản phẩm có ảnh thì không làm video, báo lý do.

**Sản phẩm thiếu LINK TIKTOK hoặc dưới ngưỡng tồn kho:** vẫn hiện trong video, nhưng không gắn vào giỏ hàng trong sheet Caption. Ghi vào "Cần xác nhận" để chủ shop thêm link hoặc nhập hàng trước ngày đăng.

**Dòng thời gian mới** (thay cho dòng thời gian 9 giây ở mục 5 của tài liệu gốc, N là số sản phẩm):

| Mốc | Nhịp | Nội dung |
|---|---|---|
| 0.0–1.5s | Nhịp 1, mở | Logo, `{CAMPAIGN}`, tiêu đề nhịp 1 |
| 1.5–3.0s | Nhịp 2, tem | Tem ngày, giờ, `x{X}` hoặc tem lợi ích theo mã kiểu, dòng phụ nhịp 2 |
| 3.0s – 3.0+N×T | Nhịp sản phẩm | Mỗi sản phẩm 1 khung: ảnh, tên, giá hoặc USP, số thứ tự `1/N` ở góc trên. Chuyển khung bằng hiệu ứng trượt ngang |
| 2.5s cuối | CTA | Lưới ảnh nhỏ tất cả sản phẩm, `NHẤN MUA NGAY`, dòng phụ, nhãn cuối (lật nhãn ở 1 giây cuối) |

- T là thời gian mỗi sản phẩm: **2 giây** nếu N ≤ 7, **1.5 giây** nếu N từ 8 đến 10.
- Tổng độ dài = 3 + N×T + 2.5 giây, **tối đa 20 giây**. N lớn hơn 10 thì làm 10 sản phẩm đầu, ghi các sản phẩm còn lại vào "Cần xác nhận".
- Khung sản phẩm ở T01, T02b, T04: tên sản phẩm + giá (theo bảng ở mục "Áp dụng khi chạy tự động"). T03: tên sản phẩm + USP1 rút gọn (tối đa 30 ký tự). T02a: tên sản phẩm + tem `MUA {X} TẶNG {Y}`, không hiện giá.
- Dòng điều kiện chữ nhỏ hiện suốt nhịp sản phẩm.

**Đầu ra:** thư mục `output/3-video/<tên-sale>/`, ví dụ `output/3-video/11-11/`
- `T01.mp4`, `T02.mp4`, `T03.mp4`, `T04.mp4`: video dọc 1080x1920, 30fps, dài theo công thức trên, có ảnh nền và nhạc miễn bản quyền (xem phần "Ảnh nền và nhạc"). **Video luôn là file .mp4.**
- `T01-anh-bia.jpg`…: ảnh bìa, công cụ tự lấy khung lưới sản phẩm ở nhịp CTA.
- `nguon/T01-kich-ban.json`…: kịch bản máy đọc, dùng để xuất lại video.
- `lich-dang-video.xlsx`: file Excel cho người đăng bài, JSON nguồn ở `nguon/lich-dang-video.json`.

**Công cụ:** `python cong-cu/tao-video.py <kịch bản>`, chạy từ thư mục `Tivo-van-hanh-marketing-ai`. Thêm `--kiem-tra` để chỉ xuất 1 ảnh gồm các khung chính (mở, tem, từng sản phẩm, CTA). Mẫu kịch bản ở `cong-cu/mau-kich-ban.json`.
- Công cụ đã làm sẵn nhận diện ở mục 4 của tài liệu gốc: nền gradient, vân ngang, đốm sáng, logo đầu khung, font Inter Black nén 84%, các hiệu ứng mờ, nảy, tem xoay -200°. Màu, họa tiết, chuyển khung, hình tem, khung chữ và hiệu ứng chuyển cảnh đổi theo phong cách sự kiện (xem phần dưới). **Video không hiện username @_tivo.official_ ở góc dưới phải** (chủ shop yêu cầu bỏ ngày 16/11/2026, thay cho dòng "Góc dưới phải" ở mục 4 của tài liệu gốc). Kịch bản, bảng Kịch bản và checklist không cần nhắc username trên video. Công cụ tự tính mốc thời gian theo số sản phẩm trong `san_pham`.
- Công cụ tự dừng nếu kịch bản còn ô trống `{…}`, `[X]`, có `@` trống, thiếu mục, `san_pham` rỗng, hoặc một sản phẩm không có ảnh.
- Nhận diện cố định nằm ở `cong-cu/thuong-hieu.json`: tên shop, username, logo, tem chính hãng, màu, dòng điều kiện mặc định. **Agent không sửa file này.**
- Không viết công cụ dựng video khác. Thiếu thư viện thì chạy `python -m pip install pillow imageio-ffmpeg`.

## Phong cách riêng cho từng sự kiện

Chủ shop yêu cầu ngày 16/11/2026: **mỗi sự kiện có phong cách video riêng** để tạo tính độc nhất. Yêu cầu này thay cho dòng "Kiểu edit video cố định 3 tháng" và "Bảng màu campaign" ở mục 8 của tài liệu gốc.
- Phần giữ nguyên ở mọi sự kiện: logo, font, bố cục, dòng thời gian, cách hiện giá.
- Phần đổi theo sự kiện: màu, họa tiết chuyển động, kiểu chuyển khung sản phẩm, hình tem, kiểu khung chữ, hiệu ứng chuyển cảnh.
- Cả 4 video T01–T04 của cùng một sự kiện dùng chung một phong cách để khán giả nhận ra chuỗi.
- Ảnh nền và nhạc cũng theo sự kiện (xem phần "Ảnh nền và nhạc").
- Các phong cách được định nghĩa sẵn trong `cong-cu/thuong-hieu.json`, mục `phong_cach`. Kịch bản chỉ ghi tên phong cách, công cụ tự áp dụng.

| Sự kiện trong lịch sale | `phong_cach` | Màu | Họa tiết | Chuyển khung | Tem | Khung chữ |
|---|---|---|---|---|---|---|
| Ngày đôi (1.1 không trùng Tết, 2.2 … 12.12) | `ngay-doi` | Đổi theo tháng, 11.11 là đỏ – vàng | Kim tuyến rơi | Trượt ngang | Sao nổ | Bo góc |
| Sale giữa tháng (ngày 15) | `giua-thang` | Đổi theo tháng | Bong bóng nổi | Trượt dọc | Thẻ giá | Viền màu |
| Sale Lương về (ngày 25) | `luong-ve` | Đổi theo tháng, tông xanh – vàng | Đồng xu rơi | Phóng to | Tròn | Vát góc |
| Black Friday | `black-friday` | Đen – vàng | Vệt sáng chéo | Trượt dọc | Hình thoi | Vát góc |
| Cyber Monday | `cyber-monday` | Tím than – xanh neon | Lưới neon | Trượt ngang | Hình thoi | Viền màu |
| Noel, Giáng sinh | `noel` | Xanh lá – đỏ – trắng | Tuyết rơi | Trượt ngang | Tròn | Bo góc |
| Tết Dương lịch | `tet-duong-lich` | Xanh navy – vàng | Pháo hoa | Phóng to | Sao nổ | Viền màu |
| Tết Nguyên đán | `tet-nguyen-dan` | Đỏ – vàng | Cánh hoa mai | Trượt dọc | Tròn | Vát góc |
| 20/11 | `20-11` | Hồng – trắng | Cánh hoa | Trượt ngang | Thẻ giá | Bo góc |
| Halloween | `halloween` | Tím – cam | Bong bóng | Phóng to | Hình thoi | Vát góc |

**Cách chọn:**
- Sự kiện trùng ngày lễ thì dùng phong cách ngày lễ. Ví dụ "Sale Lương Về + Giáng Sinh" dùng `noel`, "1.1 Sale Đầu Năm" dùng `tet-duong-lich`.
- `ngay-doi`, `giua-thang`, `luong-ve` cần thêm `"thang"` là số tháng của ngày cao điểm. Nhờ vậy 11.11 và 12.12, hay Lương về tháng 11 và tháng 12, có màu khác nhau.
- Sự kiện chưa có trong bảng: dùng phong cách gần nhất và ghi vào "Cần xác nhận" để chủ shop thêm phong cách mới. Agent không tự sửa `thuong-hieu.json`.

## Ảnh nền và nhạc

Chủ shop yêu cầu ngày 17/11/2026: video kèm **ảnh hợp với sự kiện** khi chiếu và **nhạc hợp sự kiện**, mỗi video một bài để không lặp lại. Yêu cầu này thay cho quy định "âm thanh im lặng, chọn nhạc trên TikTok".
- **Thư viện có sẵn trên máy:** `thu-vien/anh/<phong_cach>/` và `thu-vien/nhac/<phong_cach>/`. Mọi file đều là giấy phép **CC0 hoặc Public Domain** (dùng thương mại, không cần ghi công, nên đúng quy tắc "chỉ dùng nhạc có quyền" ở mục 1 điều 9 của tài liệu gốc), lấy từ nhiều nguồn: StockSnap, Wikimedia Commons (ảnh) và Freesound (nhạc), tra qua Openverse. Nguồn, tác giả, giấy phép và link gốc từng file ghi ở `thu-vien/giay-phep.json`.
- **Công cụ tự chọn**, agent không cần ghi gì thêm vào kịch bản:
  - Ảnh nền: 4 ảnh mỗi video, đổi theo cảnh (mở đầu, nửa đầu nhịp sản phẩm, nửa sau, CTA), phóng chậm và chuyển mờ, phủ màu của phong cách để chữ và sản phẩm vẫn rõ. Các video cùng đợt sale ưu tiên ảnh khác nhau.
  - Nhạc: 4 video cùng đợt sale dùng **4 bài khác nhau**. Ưu tiên bài ít được dùng nhất từ trước đến nay nên các đợt sau cũng ít lặp. Nhạc tự cắt đúng độ dài video, mở và tắt dần, chỉnh âm lượng đều.
  - Xuất lại đúng video cũ thì giữ nguyên ảnh và nhạc đã chọn. Nhật ký dùng ở `thu-vien/da-dung.json`.
- Công cụ in ra dòng "Ảnh nền: …" và "Nhạc: …" gồm tên bài, tác giả, giấy phép. Chép 2 dòng này vào sheet Thông số dựng.
- Thư mục của phong cách nào chưa có ảnh thì video dùng nền màu; chưa có nhạc thì video im lặng. Khi đó ghi vào "Cần xác nhận": "cần thêm ảnh/nhạc cho phong cách …".
- Trường tùy chọn trong kịch bản, chỉ dùng khi chủ shop yêu cầu: `"nhac": false` để video im lặng; `"nhac": "thu-vien/nhac/…/….mp3"` hoặc `"anh_nen": [ … ]` để chỉ định file.
- **Agent không tự tải ảnh hay nhạc trên mạng** và không dùng file ngoài thư viện. Thêm tư liệu do chủ shop yêu cầu, chạy `python cong-cu/tai-tu-lieu.py` (xem hướng dẫn đầu file).
- Lưu ý gửi người đăng (ghi ở sheet Cách đăng): nhạc đã có sẵn trong video. Khi đăng giữ nguyên âm thanh gốc. Nếu muốn dùng nhạc đang thịnh hành của TikTok, chọn nhạc trong thư viện **thương mại** của TikTok và giảm âm lượng âm thanh gốc về 0.

## Áp dụng khi chạy tự động

Tác vụ chạy theo lịch nên không hỏi lại người dùng được. Các ô ở mục 11 của tài liệu gốc lấy như sau. Mọi chỗ phải dùng giá trị mặc định đều ghi vào sheet "Cần xác nhận" của file Excel.

| Ô đầu vào | Lấy ở đâu | Khi thiếu hoặc chưa xác nhận |
|---|---|---|
| `{CAMPAIGN}`, loại campaign | Đợt sale gần nhất chưa qua trong `data/lich-sale-va-ngan-sach.xlsx`, sheet Lịch sale. Đặt tên theo quy tắc mục 7, ví dụ `SALE 11.11` | Không có đợt sale nào trong 7 ngày tới thì không làm video |
| `{NGÀY}`, `{HẠN}` | Ngày cao điểm, dạng `11.11` và `11/11/2026` | |
| `{GIỜ}` | Mốc đầu tiên trong cột Khung giờ sale chính, ví dụ `0h` | `0h` |
| Ngày đăng | Theo lịch video T01–T04 trong kế hoạch truyền thông nếu có | Mặc định: T01 trước ngày cao điểm 6 ngày, T02 trước 4 ngày, T03 trước 2 ngày, T04 trước 1 ngày, đăng lúc 18:00 |
| `{CÒN}` | Ngày cao điểm trừ ngày đăng | |
| Mã kiểu | T01, T02, T03, T04 | T02 dùng mẫu **T02a** chỉ khi file chốt sale có chương trình mua X tặng Y đã xác nhận, còn lại dùng **T02b** |
| Danh sách sản phẩm | Tất cả sản phẩm ở mục 3 của tài liệu gốc, theo phần "Video liệt kê nhiều sản phẩm" | Không còn sản phẩm nào có ảnh thì không làm video, báo lý do |
| `{ƯU ĐÃI}`, giá campaign | Xét **từng sản phẩm**. Chỉ coi là **đã xác nhận** khi `data/chot-sale.xlsx`, sheet Voucher, cột Trạng thái của sản phẩm đó ghi "Đã xác nhận". Khi đó `gia_campaign` là GIÁ BÁN CAMP, `gia_niem_yet` là GIÁ NIÊM YẾT trong danh mục | `gia_campaign` để `null`, `gia_niem_yet` là giá niêm yết. `{ƯU ĐÃI}` ở đầu nhịp sản phẩm: `GIÁ SỐC MỌI MÃ` nếu mọi sản phẩm đã xác nhận, còn lại `XEM ƯU ĐÃI TẠI GIỎ HÀNG`. `dieu_kien` là dòng điều kiện mặc định |
| `{X}`, `{Y}`, `{ĐK}` | File chốt sale | `{ĐK}` để trống thì dùng dòng điều kiện mặc định trong `cong-cu/thuong-hieu.json` |
| Tem "CHÍNH HÃNG" | `tem_chinh_hang` trong `cong-cu/thuong-hieu.json` | Đang tắt, agent không tự bật |
| Phong cách | Theo bảng ở phần "Phong cách riêng cho từng sự kiện" | Sự kiện chưa có phong cách thì dùng phong cách gần nhất, ghi vào Cần xác nhận |
| Nhạc, ảnh nền | Công cụ tự chọn từ thư viện miễn bản quyền theo phần "Ảnh nền và nhạc" | Thư viện của phong cách còn trống thì ghi vào Cần xác nhận |
| Logo | `cong-cu/thuong-hieu/logo.png` | Chưa có file thì công cụ ghi chữ TIVO SMART. Ghi "cần file logo" vào Cần xác nhận |
| Linh vật | `cong-cu/thuong-hieu/linh-vat.png` | Chưa có thì bỏ qua |

**Dữ liệu sản phẩm:**
- `{SP}`, `{USP1}`, `{USP2}`, `{USP3}` lấy ở **mục 3 của tài liệu gốc**, không lấy ở danh mục. Được rút gọn, nhưng không đổi nghĩa hay con số.
- Không dùng các chi tiết nằm trong phần "Lưu ý dữ liệu" của mục 3: màu của MC650, MC870, MPI480 và dung tích của MPI480.
- Ảnh dùng `data/anh-san-pham/<MÃ SP>/<MÃ SP>-1.png`. Đây là ảnh thật đã tách nền, đổi tên theo mã. Tên file ảnh ghi trong mục 3 là tên gốc, không có trên máy.

## Bước 1: Chọn video cần làm

1. Xác định campaign theo bảng trên và lịch đăng của 4 video T01–T04.
2. Làm mọi video có ngày đăng từ hôm nay đến 2 ngày tới mà chưa có file MP4. Bỏ qua thư mục `output/3-video/thu-nghiem/` (video chạy thử). Video đã quá ngày đăng mà chưa có file thì vẫn làm, ghi "đăng sớm nhất có thể", trừ khi ngày cao điểm đã qua.
3. Lập danh sách sản phẩm theo phần "Video liệt kê nhiều sản phẩm". Không còn sản phẩm nào có ảnh thì không làm video. Ghi lý do vào `lich-dang-video.xlsx`.

## Bước 2: Viết kịch bản

1. Chép `cong-cu/mau-kich-ban.json`. Điền chữ theo **mẫu chữ mục 6** đúng mã kiểu, thay hết ô trống theo mục 7 và bảng trên.
2. Các trường của kịch bản:

| Trường | Nội dung |
|---|---|
| `out` | `output/3-video/<tên-sale>/T0x.mp4` |
| `kieu` | `T01`, `T02a`, `T02b`, `T03` hoặc `T04` |
| `campaign` | `{CAMPAIGN}`, hiện ở đầu khung và khung mở |
| `san_pham` | Danh sách sản phẩm theo đúng thứ tự. Mỗi mục gồm `ma_sp`, `anh`, `ten_sp` (= `{sp}`), `gia_niem_yet`, `gia_campaign`, `dong_phu`. `dong_phu` để trống ở T01, T02b, T04 (công cụ tự hiện giá). Ở T03 là USP1 rút gọn, ở T02a là `MUA {X} TẶNG {Y}` |
| `giay_moi_sp` | `2` hoặc `1.5` theo số sản phẩm |
| `nhip1` | `tieu_de` và `phu`: tiêu đề và dòng phụ nhịp 1 |
| `nhip2` | `tieu_de`, `phu` và `tem`. `tem` là tem ngày `{NGÀY}` cho T01 và T02b, tem giờ `{GIỜ}` cho T04, `x{X}` cho T02a. Với T03, `tem` là danh sách 2 tem lợi ích chung (tối đa 16 ký tự), ví dụ `CHÍNH HÃNG TIVO`, `GIAO NHANH` (chỉ dùng khi đúng với dữ liệu) |
| `nhip_sp` | `tieu_de` = `{ƯU ĐÃI}`, hiện ở đầu nhịp sản phẩm. `nhan` = Nhãn |
| `cta` | `tieu_de` = `NHẤN MUA NGAY`, `phu` = `Xem <N> sản phẩm tại TIVO SMART`, `nhan_cuoi` = Nhãn cuối |
| `dieu_kien` | Dòng điều kiện, chữ nhỏ suốt nhịp sản phẩm |
| `con_ngay` | Chỉ cho T04: số `{CÒN}` |
| `mua_x` | Chỉ cho T02a: số `{X}` |
| `phong_cach` | Bắt buộc. Tên phong cách của sự kiện theo bảng ở phần "Phong cách riêng cho từng sự kiện" |
| `thang` | Số tháng của ngày cao điểm. Bắt buộc với `ngay-doi`, `giua-thang`, `luong-ve` |

3. **Chữ trên màn hình:**
   - Tiêu đề in hoa, mỗi dòng tối đa 18 ký tự, tối đa 2 dòng.
   - Tên sản phẩm trên khung sản phẩm tối đa 2 dòng, mỗi dòng tối đa 22 ký tự. Dài hơn thì rút gọn, giữ mã model.
   - Dòng phụ tối đa khoảng 60 ký tự.
   - Viết tiếng Việt có dấu.
4. **Nhãn có điều kiện:**
   - Nhãn `TỪ NAY – HẾT {HẠN}` của T02 chỉ dùng khi ưu đãi đã xác nhận cho ít nhất một sản phẩm. Nếu chưa, dùng `NGÀY SALE {NGÀY}`.
   - Dòng phụ nhịp 2 của T04 chỉ ghi "số lượng có hạn" khi file chốt sale đã có Số lượng dành cho TikTok. Nếu chưa, ghi `Mở deal · Ưu đãi theo thể lệ chương trình`.
5. Lưu thành `output/3-video/<tên-sale>/nguon/T0x-kich-ban.json`.

## Bước 3: Kiểm tra và xuất video

1. Chạy `python cong-cu/tao-video.py <kịch bản> --kiem-tra`. Mở ảnh `nguon/T0x-kiem-tra.jpg` để xem lại. Mỗi lần kiểm tra ghi đè ảnh cũ, không cần xóa.
2. Đối chiếu từng mục trong **checklist mục 10** của tài liệu gốc cho **từng khung sản phẩm**: chữ không tràn, dấu đúng, ảnh không méo hay bị che, giá và ưu đãi đúng dữ liệu của đúng sản phẩm, số thứ tự `1/N` đúng. Kiểm tra thêm lưới ảnh ở CTA đủ N sản phẩm. Sai thì sửa kịch bản và kiểm tra lại.
3. Chạy `python cong-cu/tao-video.py <kịch bản>` để xuất `T0x.mp4` và ảnh bìa. Kiểm tra file có dung lượng lớn hơn 0 và độ dài đúng công thức.

## Bước 4: File Excel lịch đăng video

`lich-dang-video.xlsx` viết cho người không rành công nghệ. File gồm mọi video của campaign, kể cả video đã làm ở lần chạy trước. Đây là phần "kết quả trả về" theo mục 12 của tài liệu gốc.

| Sheet | Nội dung |
|---|---|
| Lịch đăng | Ô số liệu (số video đã xong, chưa đến ngày, bị bỏ qua). Bảng: video (mã kiểu và mục tiêu), số sản phẩm, độ dài video, ngày giờ đăng (kèm thứ), tên file video, tình trạng (Chờ lưu nháp tô `vang`, Đã lưu nháp TikTok tô `xanh`, Bị bỏ qua tô `do`, Chưa đến ngày tô `xam`), ghi chú |
| Kịch bản | Bảng thời gian cho từng video đã làm: video, thời gian, nhịp, chữ trên màn hình (đã điền hết), hình ảnh và hiệu ứng. Mỗi video gồm: 1 dòng nhịp 1, 1 dòng nhịp 2, 1 dòng cho mỗi sản phẩm, 1 dòng CTA |
| Caption | Video, caption theo cấu trúc mục 9 (nhắc số sản phẩm, ví dụ "5 mẫu đang sale"), hashtag theo mục 9, nhãn nội dung AI (cần hay không, kèm lý do), **danh sách sản phẩm cần gắn giỏ hàng** (chỉ những sản phẩm có LINK TIKTOK, theo thứ tự trong video) |
| Kiểm tra | Checklist mục 10 cho từng video: mục kiểm tra, kết quả (Đạt tô `xanh`, Cần xác nhận tô `vang`), ghi chú |
| Thông số dựng | Tên phong cách sự kiện, màu nền gradient, màu tối, màu chữ, màu nhấn (mã HEX, lấy theo phong cách và tháng), font, họa tiết, kiểu chuyển khung, hình tem, kiểu khung chữ, hiệu ứng chuyển cảnh, ảnh nền và bài nhạc của từng video (tên bài, tác giả, giấy phép, theo dòng công cụ in ra) |
| Cách đăng | Ghi ngắn: video đã nằm trong bản nháp TikTok Studio (Posts > Drafts) của nick chủ shop, chủ shop xem lại rồi bấm Post; chưa lưu nháp thì nhắn "lưu nháp T0x" (`quy-trinh/4-dang-tiktok.md`). Kèm cách đăng tay dự phòng: mở file video, tải lên TikTok, giữ nguyên âm thanh gốc (nhạc đã có sẵn trong video), dán caption, gắn sản phẩm theo danh sách ở sheet Caption nếu nick gắn được, bật nhãn AI nếu sheet Caption ghi cần, đăng đúng giờ |
| Cần xác nhận | Những chỗ đang dùng giá trị mặc định: ưu đãi và giá TikTok của từng sản phẩm, sản phẩm thiếu ảnh, thiếu LINK TIKTOK hoặc dưới ngưỡng tồn kho, sản phẩm bị cắt vì quá 10, file logo, tem chính hãng, phong cách còn thiếu ảnh hoặc nhạc. Ghi rõ chủ shop cần làm gì để video sau đầy đủ hơn |

**Nhãn nội dung AI:**
- Video là đồ họa chuyển động từ ảnh sản phẩm thật (ảnh chỉ được tách nền), có chữ và hình vẽ đơn giản. Video không có hình người, cảnh hay giọng nói chân thực tạo bằng AI.
- Vì vậy theo mục 9, mặc định ghi "Không bắt buộc" kèm lý do trên.
- Ghi "Cần bật" nếu video có hình ảnh hoặc âm thanh chân thực do AI tạo.

## Không được làm

- Tất cả quy tắc ở mục 1 của tài liệu gốc.
- Không cảnh giả lập công dụng, trước và sau khi dùng, hay hứa công dụng y tế.
- Không người thật, giọng người thật, lời chứng thực của khách hàng hay chuyên gia.
- Không dùng logo hay hình ảnh của TikTok, Shopee hoặc thương hiệu khác.
- Không bấm Đăng trên TikTok, chỉ lưu nháp (xem `quy-trinh/4-dang-tiktok.md`). Không đổi giá hay voucher.
- Không gắn vào giỏ hàng sản phẩm không có LINK TIKTOK.
