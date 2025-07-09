# VouchBot - Discord Vouch Management Bot

Bot Discord chuyên dụng để quản lý vouch (xác nhận giao dịch) và thu thập feedback từ khách hàng.

## Tính năng

- **Quản lý vouch**: Tạo thông báo vouch với thông tin chi tiết
- **Hệ thống đánh giá**: Cho phép khách hàng đánh giá từ 1-5 sao
- **Thu thập feedback**: Modal để khách hàng nhập feedback chi tiết
- **Tin nhắn riêng**: Tự động gửi thông báo hoàn thành đơn hàng
- **Cấu hình linh hoạt**: Thiết lập lời cảm ơn và kênh feedback tùy chỉnh

## Cài đặt

1. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd vouchbot
   ```

2. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Cấu hình bot**:
   - Copy `.env.example` thành `.env`
   - Thêm Discord bot token vào file `.env`:
     ```
     DISCORD_TOKEN=your_discord_bot_token_here
     ```

4. **Chạy bot**:
   ```bash
   python vouch_bot1.py
   ```

## Lệnh sử dụng

### `/setupvouch`
Thiết lập lời cảm ơn tùy chỉnh cho lệnh vouch.

### `/setupfeedback <channel>`
Chọn kênh để nhận feedback từ khách hàng.
- `channel`: Kênh Discord sẽ nhận feedback

### `/vouch <buyer> <quantity> <product> <price>`
Tạo thông báo vouch và khởi tạo hệ thống feedback.
- `buyer`: Người mua (mention Discord user)
- `quantity`: Số lượng sản phẩm
- `product`: Tên sản phẩm
- `price`: Giá sản phẩm

## Cách hoạt động

1. Admin sử dụng `/vouch` để tạo thông báo giao dịch
2. Bot gửi tin nhắn công khai với các nút đánh giá 1-5 sao
3. Bot tự động gửi DM cho khách hàng thông báo hoàn thành đơn hàng
4. Khách hàng click vào số sao để đánh giá
5. Modal hiện ra để khách hàng nhập feedback chi tiết
6. Feedback được gửi đến kênh đã cấu hình hoặc kênh gốc

## Yêu cầu

- Python 3.8+
- Discord.py 2.3.0+
- Bot Discord với quyền:
  - Send Messages
  - Use Slash Commands
  - Send Messages in Threads
  - Embed Links
  - Read Message History

## Testing

Trước khi chạy bot, bạn có thể test các components:

```bash
# Test syntax và imports
python test_syntax.py

# Test khởi động bot components
python test_bot_startup.py
```

## Cấu trúc file

- `vouch_bot1.py`: File chính chứa code bot
- `config.json`: File lưu cấu hình (tự động tạo)
- `requirements.txt`: Danh sách dependencies
- `.env`: File cấu hình token (cần tạo từ .env.example)
- `test_syntax.py`: Script test syntax và imports
- `test_bot_startup.py`: Script test khởi động bot
- `bot.log`: File log (tự động tạo khi chạy bot)