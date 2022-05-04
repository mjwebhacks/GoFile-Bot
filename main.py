import os
import urldl
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from gofile import uploadFile


Bot = Client(
    "GoFile-Bot",
    bot_token = "",
    api_id = ,
    api_hash = ""
)


@Bot.on_message(filters.private & filters.command("start"))
async def start(bot, update):
    await update.reply_text(
        text=f"Hello {update.from_user.mention}, Please send a media for gofile.io stream link.\n\nMade by @mjlearning",
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
            quote=True,
            disable_web_page_preview=True
        )
        return
    text = f"**File Name:** `{response['fileName']}`" + "\n"
    text += f"**Download Page:** `{response['downloadPage']}`" + "\n"
    text += f"**Direct Download Link:** `{response['directLink']}`" + "\n"
    text += f"**Info:** `{response['info']}`"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Open Link", url=response['directLink']),
                InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url={response['directLink']}")
            ],
            [
                InlineKeyboardButton(text="Join Updates Channel", url="https://telegram.me/mjwebhack")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


Bot.run()
