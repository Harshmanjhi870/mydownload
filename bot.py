from pyrogram import Client, filters
import os
from pyrogram.types import Message

# Bot Configuration
API_ID = 25981592  # Replace with your API_ID
API_HASH = "709f3c9d34d83873d3c7e76cdd75b866"  # Replace with your API_HASH
BOT_TOKEN = "7890579887:AAHSKvEYwD1HJRmrTssbanUlq7TGwOyBlSE"  # Replace with your bot token

app = Client("file_download_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# File Download Directory
DOWNLOAD_DIR = os.path.expanduser("~/storage/shared/TelegramDownloads/")

# Ensure download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

async def progress(current, total, message: Message):
    """
    Progress callback to show download percentage in real-time.
    """
    try:
        if total > 0:
            percentage = (current / total) * 100
            await message.edit_text(f"Downloading... {percentage:.2f}%")
    except ZeroDivisionError:
        pass  # Ignore division by zero error

@app.on_message(filters.command("download") & filters.reply)
async def download_file(client, message):
    reply = message.reply_to_message

    # Check if the replied message has a file
    if reply and (reply.document or reply.video or reply.audio or reply.photo):
        file_id = None
        file_name = None

        # Identify the file type
        if reply.document:
            file_id = reply.document.file_id
            file_name = reply.document.file_name
        elif reply.video:
            file_id = reply.video.file_id
            file_name = reply.video.file_name
        elif reply.audio:
            file_id = reply.audio.file_id
            file_name = reply.audio.file_name
        elif reply.photo:
            file_id = reply.photo.file_id
            file_name = "photo.jpg"  # Default name for photos

        if file_id:
            file_path = os.path.join(DOWNLOAD_DIR, file_name)
            progress_message = await message.reply_text("Starting download...")

            # Download the file with progress
            try:
                await client.download_media(
                    file_id,
                    file_path,
                    progress=progress,
                    progress_args=(progress_message,)
                )
                await progress_message.edit_text(f"✅ File downloaded successfully: `{file_name}`\nSaved at: `{file_path}`")
            except Exception as e:
                await progress_message.edit_text(f"❌ Error: {e}")
        else:
            await message.reply_text("❌ Could not find a valid file to download.")
    else:
        await message.reply_text("❌ Please reply to a file, video, or photo to download it.")

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Welcome! Reply to any file, video, or photo with /download to save it locally with progress updates."
    )

if __name__ == "__main__":
    app.run()
