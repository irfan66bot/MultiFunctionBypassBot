import datetime
import glob
import os
import urllib.request

import img2pdf
from pyrogram import Client, filters
from pyrogram.types import Message

from bot.config import *
from bot.helpers.database import DatabaseHelper
from bot.helpers.decorators import user_commands

opener = urllib.request.build_opener()
opener.addheaders = [
    (
        "User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"),
    (
        "Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"),
    ("Accept-Encoding", "gzip, deflate, br"),
    ("Accept-Language", "en-US,en;q=0.5"),
    ("Connection", "keep-alive"),
    ("Upgrade-Insecure-Requests", "1"),
]
urllib.request.install_opener(opener)


prefixes = COMMAND_PREFIXES
cmds = ["image2pdf", f"image2pdf@{BOT_USERNAME}"]
cmds2 = ["rename", f"rename@{BOT_USERNAME}"]
cmds3 = ["tgupload", f"tgupload@{BOT_USERNAME}"]
cmds4 = ["webss", f"webss@{BOT_USERNAME}"]


@Client.on_message(filters.command(cmds, **prefixes))
@user_commands
async def image2pdf(client, message: Message):
    msg = message.text.split(" ", 1)[1].rsplit(" ", 1)
    data = msg[1].replace("['", "").replace("']", "").replace(";", "").split("', '")
    name = msg[2]
    user_id = message.from_user.id
    if not await DatabaseHelper().is_user_exist(user_id):
        await DatabaseHelper().add_user(user_id)
        try:
            join_dt = await DatabaseHelper().get_bot_started_on(user_id)
            msg = f"<i>A New User has started the Bot: {message.from_user.mention}.</i>\n\n<b>Join Time</b>: {join_dt}"
            await client.send_message(chat_id=LOG_CHANNEL, text=msg)
        except:
            pass
    last_used_on = await DatabaseHelper().get_last_used_on(user_id)
    if last_used_on != datetime.date.today().isoformat():
        await DatabaseHelper().update_last_used_on(user_id)
    os.mkdir(name)
    for _ in data:
        flnm = f"{name}/{data.index(_)}"
        urllib.request.urlretrieve(_, flnm + ".jpg")
    with open(f"{name}s.pdf", "wb") as f:
        f.write(img2pdf.convert(glob.glob(f"{name}/*.jpg")))
    await message.reply_document(f"{name}s.pdf")


@Client.on_message(filters.command(cmds2, **prefixes))
@user_commands
async def rename(client, message: Message):
    if not message.reply_to_message:
        await message.reply("Please reply to a file/document")
    user_id = message.reply_to_message.id
    if not await DatabaseHelper().is_user_exist(user_id):
        await DatabaseHelper().add_user(user_id)
        try:
            join_dt = await DatabaseHelper().get_bot_started_on(user_id)
            msg = f"<i>A New User has started the Bot: {message.from_user.mention}.</i>\n\n<b>Join Time</b>: {join_dt}"
            await client.send_message(chat_id=LOG_CHANNEL, text=msg)
        except:
            pass
    last_used_on = await DatabaseHelper().get_last_used_on(user_id)
    if last_used_on != datetime.date.today().isoformat():
        await DatabaseHelper().update_last_used_on(user_id)
    try:
        filename = message.text.replace(message.text.split(" ")[0], "")
    except Exception as e:
        await message.reply(f"{e}")
        return
    reply = message.reply_to_message
    if reply:
        x = await message.reply_text("Downloading.....")
        path = await reply.download(file_name=filename)
        await x.edit("Uploading.....")
        await message.reply_document(path)
        os.remove(path)


@Client.on_message(filters.command(cmds3, **prefixes))
@user_commands
async def tgupload(client, message: Message):
    if message.reply_to_message:
        address = message.reply_to_message.text
    else:
        try:
            address = message.text.split()[1]
        except BaseException:
            await message.reply_text("Please Reply to a Url")
            return
    user_id = message.from_user.id
    if not await DatabaseHelper().is_user_exist(user_id):
        await DatabaseHelper().add_user(user_id)
        try:
            join_dt = await DatabaseHelper().get_bot_started_on(user_id)
            msg = f"<i>A New User has started the Bot: {message.from_user.mention}.</i>\n\n<b>Join Time</b>: {join_dt}"
            await client.send_message(chat_id=LOG_CHANNEL, text=msg)
        except:
            pass
    last_used_on = await DatabaseHelper().get_last_used_on(user_id)
    if last_used_on != datetime.date.today().isoformat():
        await DatabaseHelper().update_last_used_on(user_id)
    x = await message.reply_text("Uploading to telegram...")
    try:
        if address.startswith("http"):
            if address.endswith((".jpg", ".png", ".jpeg")):
                await message.reply_photo(address)
                await message.reply_document(address)
            elif address.endswith((".mp4", ".mkv", ".mov")):
                if len(str(message)) > 2:
                    await message.reply_document(address)
                else:
                    await message.reply_video(address)
            else:
                await message.reply_document(address)
        else:
            if True:
                await message.reply_document(address)
        await x.delete()
    except BaseException:
        await message.reply("No such File/Directory/Link")
        return


@Client.on_message(filters.command(cmds4, **prefixes))
@user_commands
async def takess(client, message: Message):
    try:
        if len(message.command) != 2:
            await message.reply_text("Give A Url To Fetch Screenshot.")
            return
        url = message.text.split(None, 1)[1]
        user_id = message.from_user.id
        if not await DatabaseHelper().is_user_exist(user_id):
            await DatabaseHelper().add_user(user_id)
            try:
                join_dt = await DatabaseHelper().get_bot_started_on(user_id)
                msg = f"<i>A New User has started the Bot: {message.from_user.mention}.</i>\n\n<b>Join Time</b>: {join_dt}"
                await client.send_message(chat_id=LOG_CHANNEL, text=msg)
            except:
                pass
        last_used_on = await DatabaseHelper().get_last_used_on(user_id)
        if last_used_on != datetime.date.today().isoformat():
            await DatabaseHelper().update_last_used_on(user_id)
        m = await message.reply_text("**Taking Screenshot**")
        await m.edit("**Uploading**")
        try:
            await message.reply_photo(
                photo=f"https://webshot.amanoteam.com/print?q={url}", quote=False
            )
        except BaseException:
            return await m.edit("Sorry, Unable to Generate SS.")
        await m.delete()
    except Exception as e:
        await message.reply_text(f"Unknown Error Occurred!\nERROR: {e}")
        return
