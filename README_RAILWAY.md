# Deploy VouchBot lên Railway

## Hướng dẫn Deploy

### 1. Chuẩn bị
- Tài khoản Railway (https://railway.app)
- Repository GitHub chứa source code bot
- Discord Bot Token

### 2. Các bước deploy

#### Bước 1: Tạo project mới trên Railway
1. Đăng nhập vào Railway
2. Click "New Project"
3. Chọn "Deploy from GitHub repo"
4. Chọn repository chứa bot code

#### Bước 2: Cấu hình Environment Variables
Trong Railway dashboard, vào tab "Variables" và thêm:
```
DISCORD_TOKEN=your_discord_bot_token_here
```

#### Bước 3: Deploy
- Railway sẽ tự động detect và build project
- Bot sẽ được deploy và chạy tự động

### 3. Files đã được tạo cho Railway

- `Procfile`: Định nghĩa command để chạy bot
- `railway.json`: Cấu hình Railway deployment
- `runtime.txt`: Chỉ định phiên bản Python
- `.dockerignore`: Loại trừ files không cần thiết khi build
- `requirements.txt`: Dependencies của project

### 4. Monitoring

- Xem logs: Railway Dashboard > Deployments > View Logs
- Restart bot: Railway Dashboard > Settings > Restart

## 🚀 Tính năng Railway

- **Auto-restart**: Bot tự động khởi động lại khi gặp lỗi
- **Health Check**: Endpoint `/health` để Railway monitor bot
- **Environment validation**: Kiểm tra token trước khi khởi động
- **Optimized logging**: Logging được tối ưu cho Railway (stdout)
- **Error handling**: Xử lý lỗi HTTPException và interaction acknowledgment
- **Optimized build**: Build process được tối ưu với .dockerignore
- **Comprehensive logging**: Log chi tiết cho việc debug

### 5. Lưu ý quan trọng

- Bot sẽ tự động restart khi có lỗi (tối đa 10 lần)
- Đảm bảo Discord Token được set đúng trong Environment Variables
- Bot cần quyền Administrator trong Discord server để hoạt động đầy đủ

### 6. Troubleshooting

**Bot không online:**
- Kiểm tra logs trong Railway dashboard
- Verify Discord Token
- Kiểm tra bot permissions trong Discord server

**Lỗi deployment:**
- Kiểm tra requirements.txt có đầy đủ dependencies
- Verify Python version compatibility
- Check Railway build logs

### 7. Commands cần setup sau khi deploy

1. `/setupfeedback` - Chọn kênh nhận feedback
2. `/setupvouch` - Thiết lập lời cảm ơn

Bot sẽ sẵn sàng sử dụng với lệnh `/vouch` sau khi setup xong!