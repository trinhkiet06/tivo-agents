# 1. Lập kế hoạch: tra cứu giờ và ngày sale

Mục tiêu: có một lịch sale Shopee đáng tin để dùng cho việc set giá, set voucher và trả lời khách.

**Đầu ra:** `output/1-ke-hoach/lich-sale-shopee.md`. Mỗi lần tra cứu thì cập nhật file này và ghi ngày tra cứu.

## Cần tra cứu

Lấy hôm nay làm mốc, tra trong 60 ngày tới, trừ khi chủ shop nêu khoảng khác.

| Loại | Gồm | Bắt buộc ghi |
|---|---|---|
| Giờ flash sale | Các khung flash sale của Shopee trong ngày thường và ngày sale | Giờ bắt đầu, giờ kết thúc |
| Ngày sale | Ngày đôi, sale giữa tháng, sale ngày lương | Ngày và giờ bắt đầu, ngày và giờ kết thúc |
| Ngày sale đặc biệt | 11.11, 12.12, Black Friday, Tết và các dịp lớn khác | Ngày và giờ bắt đầu, ngày và giờ kết thúc |

Ghi thêm hạn đăng ký và điều kiện tham gia nếu tìm được.

## Thứ tự nguồn

1. `data/lich-sale.xlsx`, do người phụ trách chép từ Kênh Người Bán. Chỉ dòng ghi Chính thức mới được coi là chính thức.
2. Trang và thông báo chính thức của Shopee Việt Nam, gồm Học viện Shopee.
3. Báo điện tử và trang tin thương mại điện tử uy tín.
4. Blog và hội nhóm nhà bán hàng, chỉ để tham khảo và phải ghi là nguồn không chính thức.

## Trạng thái

- **Chính thức:** có từ dòng Chính thức của nguồn 1, từ nguồn 2, hoặc có ít nhất 2 nguồn uy tín khớp nhau.
- **Dự kiến:** suy theo thông lệ hoặc chỉ có nguồn không chính thức.
- **Chưa tìm thấy:** không có thông tin. Giờ nào chưa tìm thấy thì để trống, không tự điền.
- Nếu các nguồn mâu thuẫn, liệt kê cả hai và chọn nguồn chính thức hơn.
- Nếu không truy cập được web, nói rõ và chỉ dùng nguồn 1.

## Mẫu đầu ra

```markdown
# Lịch sale Shopee
Ngày tra cứu: dd/mm/yyyy | Khoảng tra cứu: dd/mm – dd/mm/yyyy

## Giờ flash sale
| Áp dụng | Giờ bắt đầu | Giờ kết thúc | Trạng thái | Nguồn |

## Ngày sale
| Tên | Bắt đầu (ngày, giờ) | Kết thúc (ngày, giờ) | Hạn đăng ký | Trạng thái | Nguồn |

## Ngày sale đặc biệt
| Tên | Bắt đầu (ngày, giờ) | Kết thúc (ngày, giờ) | Hạn đăng ký | Trạng thái | Nguồn |

## Cần chủ shop kiểm tra trên Kênh Người Bán
```
