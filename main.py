import os
from pyrogram import Client, filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL
import asyncio

API_ID = '22419004'
API_HASH = '34982b52c4a83c2af3ce8f4fe12fe4e1'
BOT_TOKEN = '7845997152:AAFIoE9hO-nLQm2r1pMtWemmU8wzRNrfzVg'
COOKIE_FILE = 'cookies.txt'

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Base options for yt-dlp, using Netscape cookie
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'cookies': COOKIE_FILE,
    'noplaylist': True,
    'quiet': True
}

async def download_and_send(client, message, song_name, quality='bestaudio'):
    await message.reply_text(f"Searching for **{song_name}**...")

    ydl_opts['format'] = quality
    ydl_opts['progress_hooks'] = [lambda d: on_progress(d, message)]

    with YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(f"ytsearch:{song_name}", download=True)
            file_path = ydl.prepare_filename(result['entries'][0])
            await message.reply_audio(audio=file_path, title=result['entries'][0]['title'])

            os.remove(file_path)  # Clean up after sending

        except Exception as e:
            await message.reply_text(f"⚠️ Error: {e}")

def on_progress(d, message):
    if d['status'] == 'downloading':
        percentage = d['_percent_str']
        file_size = d['_total_bytes_str']
        message_text = f"Downloading... {percentage} of {file_size}"
        asyncio.run_coroutine_threadsafe(message.edit_text(message_text), app.loop)

@app.on_message(filters.command("download"))
async def download_music(client, message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /download [song name] [optional: quality]")
        return

    song_name = " ".join(args[1:-1] if len(args) > 2 else args[1:])
    quality = args[-1] if args[-1] in ['bestaudio', '128', '320'] else 'bestaudio'

    await download_and_send(client, message, song_name, quality)

@app.on_message(filters.command("source"))
async def switch_source(client, message: Message):
    sources = {
        "yt": "YouTube",
        "sc": "SoundCloud"
    }
    source_key = message.text.split()[1].lower() if len(message.text.split()) > 1 else None

    if source_key in sources:
        ydl_opts['source_address'] = sources[source_key]
        await message.reply_text(f"Source switched to **{sources[source_key]}**.")
    else:
        await message.reply_text("Invalid source. Available options: yt (YouTube), sc (SoundCloud)")

app.run()
