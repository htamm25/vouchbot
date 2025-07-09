import os
import json
import logging
import asyncio
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging - optimized for Railway
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Railway prefers stdout logging
    ]
)
logger = logging.getLogger(__name__)

# Add file logging only if not on Railway
if not os.getenv('RAILWAY_ENVIRONMENT'):
    file_handler = logging.FileHandler('bot.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(file_handler)

# --- Cấu hình file lưu settings ---
CONFIG_FILE = "config.json"

# Load/Save config
def load_config() -> dict:
    """Load configuration from JSON file with error handling"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config_data = json.load(f)
                logger.info("Configuration loaded successfully")
                return config_data
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding config file: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            return {}
    logger.info("Config file not found, creating new configuration")
    return {}

def save_config(cfg: dict) -> None:
    """Save configuration to JSON file with error handling"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=4)
        logger.info("Configuration saved successfully")
    except Exception as e:
        logger.error(f"Error saving config file: {e}")

# Khởi tạo config
config = load_config()

# Health check server for Railway
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'bot_ready': bot.is_ready() if 'bot' in globals() else False
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default HTTP server logs
        pass

def start_health_server():
    """Start health check server for Railway"""
    port = int(os.getenv('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"Health check server starting on port {port}")
    server.serve_forever()

# Modal để thiết lập lời cảm ơn
class ThankYouModal(discord.ui.Modal, title="Thiết lập Lời Cảm Ơn"):
    thankyou = discord.ui.TextInput(
        label="Lời cảm ơn",
        style=discord.TextStyle.paragraph
    )

    def __init__(self, guild_id: int):
        super().__init__()
        self.guild_id = str(guild_id)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            guild_cfg = config.get(self.guild_id, {})
            guild_cfg["thankyou"] = self.thankyou.value
            config[self.guild_id] = guild_cfg
            save_config(config)
            logger.info(f"Thank you message set for guild {self.guild_id}")
            await interaction.response.send_message("✅ Đã thiết lập lời cảm ơn thành công!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error setting thank you message: {e}")
            await interaction.response.send_message("❌ Có lỗi xảy ra khi thiết lập lời cảm ơn!", ephemeral=True)

# Modal thu thập feedback sau khi user bấm sao
class FeedbackModal(discord.ui.Modal, title="Gửi Feedback"):
    feedback = discord.ui.TextInput(
        label="Feedback",
        style=discord.TextStyle.paragraph
    )

    def __init__(self, buyer: discord.Member, stars: int, quantity: int, product: str, price: str, origin_channel: discord.TextChannel, original_message: discord.Message):
        super().__init__()
        self.buyer = buyer
        self.stars = stars
        self.quantity = quantity
        self.product = product
        self.price = price
        self.origin_channel = origin_channel
        self.original_message = original_message

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Tạo embed theo mẫu với màu #fc44c2
            embed = discord.Embed(
                title=f"Đã mua: {self.product}",
                description=f"> • {self.feedback.value}",
                color=0xfc44c2
            )
            embed.set_author(name="Cảm ơn quý khách đã ủng hộ !!!", icon_url=self.buyer.display_avatar.url)
            embed.set_thumbnail(url=self.buyer.display_avatar.url)
            
            # Thêm phần đánh giá với emoji sao
            star_icons = "<a:TwinklingStar:1388826311346356226>" * self.stars
            embed.add_field(name="Đánh giá", value=star_icons, inline=False)
            
            # Sử dụng server avatar cho footer
            server_icon = interaction.guild.icon.url if interaction.guild.icon else None
            embed.set_footer(text="LewLewStore • discord.gg/lewlewstore", icon_url=server_icon)

            # Xác định kênh feedback
            guild_cfg = config.get(str(interaction.guild_id), {})
            chan_id = guild_cfg.get("feedback_channel")
            target = interaction.guild.get_channel(chan_id) if chan_id else self.origin_channel

            if target:
                await target.send(f"Feedback của {self.buyer.mention}:", embed=embed)
                logger.info(f"Feedback sent for {self.buyer.id} with {self.stars} stars")
                
                # Cập nhật tin nhắn gốc
                try:
                    new_content = (
                        "**LewLewStore** đã ghi nhận feedback của bạn\n\n"
                        "Cảm ơn bạn đã tin tưởng và sử dụng dịch vụ tại **LewLewStore**"
                    )
                    await self.original_message.edit(content=new_content, view=None)
                    logger.info(f"Original message updated for {self.buyer.id}")
                except Exception as e:
                    logger.error(f"Error updating original message: {e}")
                
                await interaction.response.send_message("✅ Cảm ơn feedback của bạn!", ephemeral=True)
            else:
                logger.error(f"Could not find target channel for feedback")
                await interaction.response.send_message("❌ Không thể gửi feedback, vui lòng thử lại!", ephemeral=True)
        except Exception as e:
            logger.error(f"Error submitting feedback: {e}")
            await interaction.response.send_message("❌ Có lỗi xảy ra khi gửi feedback!", ephemeral=True)

# Button 1-5 sao
class StarButton(discord.ui.Button):
    def __init__(self, stars: int):
        super().__init__(label=f"{stars} sao", style=discord.ButtonStyle.primary, custom_id=f"star_{stars}")
        self.stars = stars

    async def callback(self, interaction: discord.Interaction):
        try:
            # Kiểm tra xem người click có phải là buyer không
            view: VouchView = self.view  # type: ignore
            if interaction.user.id != view.buyer.id:
                await interaction.response.send_message("❌ Chỉ người mua mới có thể đánh giá!", ephemeral=True)
                return
                
            modal = FeedbackModal(
                buyer=view.buyer,
                stars=self.stars,
                quantity=view.quantity,
                product=view.product,
                price=view.price,
                origin_channel=view.origin_channel,
                original_message=view.original_message
            )
            await interaction.response.send_modal(modal)
            logger.info(f"Feedback modal opened for {view.buyer.id} with {self.stars} stars")
        except Exception as e:
            logger.error(f"Error in star button callback: {e}")
            await interaction.response.send_message("❌ Có lỗi xảy ra!", ephemeral=True)

# View chứa các star button
class VouchView(discord.ui.View):
    def __init__(self, buyer: discord.Member, quantity: int, product: str, price: str, origin_channel: discord.TextChannel):
        super().__init__(timeout=None)
        self.buyer = buyer
        self.quantity = quantity
        self.product = product
        self.price = price
        self.origin_channel = origin_channel
        self.original_message = None  # Sẽ được set sau khi gửi message
        for i in range(1, 6):
            self.add_item(StarButton(i))

# Khởi tạo bot với intents
intents = discord.Intents.default()
intents.message_content = False  # Không cần message content cho slash commands
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    try:
        # Sync tất cả slash commands
        synced = await bot.tree.sync()
        logger.info(f"Bot {bot.user} đã sẵn sàng! Đã sync {len(synced)} slash commands")
        print(f"✅ Bot đang chạy: {bot.user}")
    except Exception as e:
        logger.error(f"Error during bot startup: {e}")

@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Command error: {error}")

@bot.event
async def on_application_command_error(interaction: discord.Interaction, error):
    logger.error(f"Application command error: {error}")
    
    # Handle specific Discord HTTP exceptions
    if isinstance(error, discord.errors.HTTPException):
        if error.code == 40060:  # Interaction has already been acknowledged
            logger.warning(f"Interaction already acknowledged for user {interaction.user.id}")
            return
    
    # Only respond if interaction hasn't been responded to yet
    if not interaction.response.is_done():
        try:
            await interaction.response.send_message("❌ Có lỗi xảy ra khi thực hiện lệnh!", ephemeral=True)
        except discord.errors.HTTPException as e:
            if e.code != 40060:  # Ignore "already acknowledged" errors
                logger.error(f"Failed to send error response: {e}")
    else:
        try:
            await interaction.followup.send("❌ Có lỗi xảy ra khi thực hiện lệnh!", ephemeral=True)
        except discord.errors.HTTPException as e:
            logger.error(f"Failed to send followup error response: {e}")

# /setupvouch: modal để nhập lời cảm ơn
@bot.tree.command(name="setupvouch", description="Thiết lập lời cảm ơn cho lệnh vouch")
async def setupvouch(interaction: discord.Interaction):
    try:
        # Kiểm tra quyền admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Bạn cần quyền Administrator để sử dụng lệnh này!", ephemeral=True)
            return
            
        await interaction.response.send_modal(ThankYouModal(interaction.guild_id))
        logger.info(f"Setup vouch modal opened by {interaction.user.id} in guild {interaction.guild_id}")
    except Exception as e:
        logger.error(f"Error in setupvouch command: {e}")
        await interaction.response.send_message("❌ Có lỗi xảy ra!", ephemeral=True)

# /setupfeedback: chọn kênh nhận feedback
@bot.tree.command(name="setupfeedback", description="Chọn kênh để gửi feedback")
@app_commands.describe(channel="Kênh sẽ nhận feedback")
async def setupfeedback(interaction: discord.Interaction, channel: discord.TextChannel):
    try:
        # Kiểm tra quyền admin
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Bạn cần quyền Administrator để sử dụng lệnh này!", ephemeral=True)
            return
            
        # Kiểm tra bot có quyền gửi tin nhắn trong kênh không
        if not channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message(f"❌ Bot không có quyền gửi tin nhắn trong {channel.mention}!", ephemeral=True)
            return
            
        guild_cfg = config.get(str(interaction.guild_id), {})
        guild_cfg["feedback_channel"] = channel.id
        config[str(interaction.guild_id)] = guild_cfg
        save_config(config)
        
        logger.info(f"Feedback channel set to {channel.id} in guild {interaction.guild_id}")
        await interaction.response.send_message(f"✅ Đã thiết lập kênh feedback: {channel.mention}", ephemeral=True)
    except Exception as e:
        logger.error(f"Error in setupfeedback command: {e}")
        await interaction.response.send_message("❌ Có lỗi xảy ra!", ephemeral=True)

# /vouch: gửi thông báo và DM buyer
@bot.tree.command(name="vouch", description="Gửi thông tin vouch và khởi tạo feedback")
@app_commands.describe(
    buyer="Người mua",
    quantity="Số lượng",
    product="Sản phẩm",
    price="Giá"
)
async def vouch(
    interaction: discord.Interaction,
    buyer: discord.Member,
    quantity: int,
    product: str,
    price: str
):
    try:
        # Validation
        if quantity <= 0:
            await interaction.response.send_message("❌ Số lượng phải lớn hơn 0!", ephemeral=True)
            return
            
        if len(product.strip()) == 0:
            await interaction.response.send_message("❌ Tên sản phẩm không được để trống!", ephemeral=True)
            return
            
        if len(price.strip()) == 0:
            await interaction.response.send_message("❌ Giá không được để trống!", ephemeral=True)
            return
            
        if buyer.bot:
            await interaction.response.send_message("❌ Không thể tạo vouch cho bot!", ephemeral=True)
            return
            
        guild_cfg = config.get(str(interaction.guild_id), {})
        thankyou = guild_cfg.get("thankyou", "Cảm ơn")

        # Tạo tin nhắn thường thay vì embed
        vouch_text = (
            f"🎉 **Giao dịch thành công!**\n\n"
            f"{thankyou} {buyer.mention}\n\n"
            f"**LewLewStore** xin bạn một ít phút để đánh giá dịch vụ tại đây nhé !!! chúng mình luôn muốn lắng nghe góp ý của các bạn và cải thiện dịch vụ tại **LewLewStore**\n\n"
            f"```+vouch {buyer.mention} x{quantity} {product} {price} vnd legit```\n"
            f"- Mình xin chút ít thời gian của bạn để ủng hộ mình 1 vouch bằng cách sao chép nội dung ở trên và dán ở <#1294909151515774999> hoặc 1 feedback bằng nút bên dưới (có thể cả vừa vouch và feeddback nếu bạn muốn)"
        )
        
        # Tạo view và gửi tin nhắn
        view = VouchView(buyer, quantity, product, price, interaction.channel)
        await interaction.response.send_message(
            content=vouch_text,
            view=view
        )
        
        # Lưu original message vào view
        original_message = await interaction.original_response()
        view.original_message = original_message
        
        logger.info(f"Vouch created for {buyer.id} by {interaction.user.id} in guild {interaction.guild_id}")

        # Gửi DM cho buyer
        dm_text = (
            f"<:giveaway1:1388824182237958155>Đơn hàng **{product}** của bạn đã hoàn thành\n\n"
            f"Bạn hãy vào {interaction.channel.mention} để xác nhận đơn hàng và dành chút ít thời gian để đánh giá, góp ý dịch vụ bên mình bạn nhé !!!"
        )
        try:
            await buyer.send(dm_text)
            logger.info(f"DM sent successfully to {buyer.id}")
        except discord.Forbidden:
            logger.warning(f"Could not send DM to {buyer.id} - DMs disabled")
            # Thông báo trong channel nếu không gửi được DM
            await interaction.followup.send(
                f"⚠️ Không thể gửi tin nhắn riêng cho {buyer.mention}. "
                "Vui lòng kiểm tra cài đặt tin nhắn riêng của bạn.",
                ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error sending DM to {buyer.id}: {e}")
            
    except Exception as e:
        logger.error(f"Error in vouch command: {e}")
        if not interaction.response.is_done():
            await interaction.response.send_message("❌ Có lỗi xảy ra khi tạo vouch!", ephemeral=True)
        else:
            await interaction.followup.send("❌ Có lỗi xảy ra khi tạo vouch!", ephemeral=True)

# Chạy bot
if __name__ == "__main__":
    try:
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            logger.error("DISCORD_TOKEN environment variable not found")
            print("❌ Lỗi: Không tìm thấy DISCORD_TOKEN trong biến môi trường!")
            print("💡 Hướng dẫn:")
            print("   1. Tạo file .env từ .env.example")
            print("   2. Thêm token bot Discord vào file .env")
            print("   3. Hoặc đặt biến môi trường DISCORD_TOKEN")
            exit(1)
        
        # Start health check server in background thread (for Railway)
        if os.getenv('RAILWAY_ENVIRONMENT') or os.getenv('PORT'):
            health_thread = Thread(target=start_health_server, daemon=True)
            health_thread.start()
            logger.info("Health check server started for Railway deployment")
            
        logger.info("Starting VouchBot...")
        print("🚀 Đang khởi động VouchBot...")
        bot.run(token)
        
    except discord.LoginFailure:
        logger.error("Invalid Discord token")
        print("❌ Token Discord không hợp lệ!")
        print("💡 Vui lòng kiểm tra lại token trong file .env")
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n👋 Bot đã được dừng bởi người dùng")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Lỗi nghiêm trọng: {e}")
        print("💡 Vui lòng kiểm tra log file 'bot.log' để biết thêm chi tiết")
