import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 🔐 ضع التوكن الخاص بك هنا من BotFather
BOT_TOKEN = '7459794121:AAF74_PHzn1G-pI_fwGCdpjr3ursMrgNWuA'

# 📥 دالة لتحميل الفيديو من الرابط
def download_video(url: str, output_file: str):
    command = ["yt-dlp", "-f", "mp4", "-o", output_file, url]
    subprocess.run(command, check=True)

# ✂️ دالة لقص الفيديو وتحويله إلى Reels (مدة قصيرة + أبعاد 9:16)
def convert_to_reel(input_path: str, output_path: str):
    command = [
        "ffmpeg", "-i", input_path,
        "-t", "30",                      # ⏱️ مدته 30 ثانية
        "-vf", "scale=720:1280",         # 📐 أبعاد 9:16 (ريلز)
        "-c:a", "copy", output_path
    ]
    subprocess.run(command, check=True)

# 🧠 دالة التعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("أرسل رابط فيديو صالح من YouTube أو TikTok.")
        return

    await update.message.reply_text("🚀 جاري تحميل وتحويل الفيديو إلى Reels...")

    input_file = "temp_input.mp4"
    output_file = "reel_output.mp4"

    try:
        # تحميل الفيديو
        download_video(url, input_file)

        # تحويله إلى ريلز
        convert_to_reel(input_file, output_file)

        # إرسال النتيجة
        with open(output_file, "rb") as video:
            await update.message.reply_video(video, caption="🎬 تم تحويل الفيديو إلى Reels!")

    except subprocess.CalledProcessError as e:
        await update.message.reply_text("❌ حدث خطأ أثناء المعالجة. تأكد أن الرابط صحيح.")
    finally:
        if os.path.exists(input_file): os.remove(input_file)
        if os.path.exists(output_file): os.remove(output_file)

# ▶️ تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت يعمل الآن...")
    app.run_polling()
