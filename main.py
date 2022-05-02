import os
import urldl
from gofile import uploadFile
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 


Bot = Client(
    "GoFile-Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    
    await update.reply_text(
        text=f"""Hello {update.from_user.mention},
        Please send a media for gofile.io stream link.\n
        Made by @FayasNoushad""",
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & (filters.media | filters.text))
async def filter(bot, update):
    
    if update.text:
        if not update.text.startswith("http://") or not update.text.startswith("https://"):
            return
    
    message = await update.reply_text(
        text="`Processing...`",
        quote=True,
        disable_web_page_preview=True
    )
    
    try:
        
        await message.edit_text(
            text="`Downloading...`",
            disable_web_page_preview=True
        )
        if update.text:
            media = urldl.download(url)
        else:
            media = await update.download()
        
        await message.edit_text(
            text="`Uploading...`",
            disable_web_page_preview=True
        )
        response = uploadFile(media)
        
        try:
            os.remove(media)
        except:
            pass
    
    except Exception as error:
        
        await message.edit_text(
            text=f"Error :- `{error}`",
            disable_web_page_preview=True
        )
        return
    
    text = f"**File Name:** `{response['fileName']}`" + "\n"
    text += f"**Download Page:** `{response['downloadPage']}`" + "\n"
    text += f"**Direct Download Link:** `{response['directLink'] + '/' + response['fileName']}`" + "\n"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Open Link", url=response['downloadPage']),
                InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={response['downloadPage']}")
            ],
            [
                InlineKeyboardButton(text="Join Updates Channel", url="https://telegram.me/FayasNoushad")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


Bot.run()
