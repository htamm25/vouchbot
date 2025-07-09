# 🚀 Hướng dẫn Deploy VouchBot lên Railway

## ✅ Chuẩn bị trước khi deploy

### 1. Kiểm tra các file cần thiết
Đảm bảo các file sau đã có trong project:
- ✅ `vouch_bot1.py` - Main bot file
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Railway process configuration
- ✅ `railway.json` - Railway deployment config
- ✅ `runtime.txt` - Python version
- ✅ `.dockerignore` - Build optimization
- ✅ `.gitignore` - Git ignore rules
- ✅ `.env.example` - Environment variables template

### 2. Chuẩn bị Discord Bot Token
1. Truy cập [Discord Developer Portal](https://discord.com/developers/applications)
2. Tạo hoặc chọn application của bạn
3. Vào tab "Bot" và copy token
4. **LƯU Ý**: Không share token này với ai!

## 🚀 Deploy lên Railway

### Bước 1: Tạo Repository trên GitHub
1. Tạo repository mới trên GitHub
2. Upload tất cả files (trừ `.env` và `config.json`)
3. Commit và push code

### Bước 2: Deploy trên Railway
1. Truy cập [Railway.app](https://railway.app)
2. Đăng nhập bằng GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Chọn repository vừa tạo
5. Railway sẽ tự động detect và deploy

### Bước 3: Cấu hình Environment Variables
1. Trong Railway dashboard, vào tab "Variables"
2. Thêm các biến sau:
   ```
   DISCORD_TOKEN=your_bot_token_here
   LOG_LEVEL=INFO
   ```
3. Click "Deploy" để áp dụng thay đổi

### Bước 4: Kiểm tra Deployment
1. Vào tab "Deployments" để xem trạng thái
2. Vào tab "Logs" để xem bot logs
3. Tìm dòng: `✅ Bot đang chạy: YourBotName`
4. Kiểm tra health endpoint: `https://your-app.railway.app/health`

## 🔧 Tính năng đã tối ưu cho Railway

### ✅ Health Check
- Endpoint `/health` để Railway monitor bot
- Tự động báo cáo trạng thái bot

### ✅ Logging tối ưu
- Sử dụng stdout logging (Railway preferred)
- Configurable log level qua `LOG_LEVEL`
- Không tạo file log trên Railway

### ✅ Error Handling
- Xử lý lỗi HTTPException
- Tránh lỗi "Interaction already acknowledged"
- Graceful error recovery

### ✅ Environment Detection
- Tự động detect Railway environment
- Khởi động health server khi cần
- Tối ưu cho production deployment

## 🐛 Troubleshooting

### Bot không khởi động
1. Kiểm tra `DISCORD_TOKEN` trong Variables
2. Xem logs để tìm lỗi cụ thể
3. Đảm bảo bot có đủ permissions

### Health check failed
1. Kiểm tra PORT environment variable
2. Đảm bảo bot đã khởi động hoàn tất
3. Test endpoint `/health` manually

### Commands không hoạt động
1. Kiểm tra bot permissions trong Discord server
2. Xem logs để tìm lỗi sync commands
3. Restart deployment nếu cần

## 📝 Lưu ý quan trọng

- ⚠️ **KHÔNG** commit file `.env` lên GitHub
- 🔄 Railway sẽ tự động restart bot khi có lỗi
- 📊 Monitor bot qua Railway dashboard
- 🔧 Có thể adjust log level qua `LOG_LEVEL` variable
- 💾 Config sẽ được lưu persistent trên Railway

## 🎉 Hoàn thành!

Sau khi deploy thành công:
1. Bot sẽ tự động online trong Discord server
2. Sử dụng `/setupvouch` để cấu hình lời cảm ơn
3. Sử dụng `/setupfeedback` để chọn kênh feedback
4. Test với `/vouch` command

**Chúc mừng! VouchBot của bạn đã sẵn sàng hoạt động trên Railway! 🎊**