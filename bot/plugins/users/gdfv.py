import datetime
from re import search
from time import sleep, time

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from bot.helpers.database import DatabaseHelper
from bot.helpers.decorators import user_commands
from bot.helpers.functions import forcesub, get_readable_time
from bot.logging import LOGGER
from bot.modules.gdrive_direct import *
from bot.modules.regex import *

prefixes = COMMAND_PREFIXES
commands = ["gd", f"gd@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def gd(client, message: Message):
    """
    Get GDrive Links for various Drive File Sharer
    """
    global res, time_taken
    fsub = await forcesub(client, message)
    if not fsub:
        return
    msg_arg = message.text.replace("  ", " ")
    msg_args = msg_arg.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    cmd = ""
    url = ""
    if len(msg_args) > 1:
        if len(message.command) != 2:
            await message.reply_text("Sorry, Could not understand your Input!")
            return
        cmd = msg_args[0]
        url = msg_args[1]
    elif reply_to is not None:
        try:
            reply_text = search(URL_REGEX, reply_to.text)[0]
        except BaseException:
            reply_text = (
                search(URL_REGEX, reply_to.caption.markdown)[0]
                .replace("\\", "")
                .split("*")[0]
            )
        url = reply_text.strip()
        cmd = msg_args[0]
    elif message.command == (0 or 1) or reply_to is None:
        err = "<b><i>Please send a URL or reply to an URL to proceed!</i></b>"
        await message.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return

    valid_url = is_a_url(url)
    if valid_url is not True:
        err = "<b><i>You did not seem to have entered a valid URL!</i></b>"
        await message.reply_text(text=err, disable_web_page_preview=True, quote=True)
        return

    uname = message.from_user.mention
    uid = f"<code>{message.from_user.id}</code>"
    user_id = message.from_user.id
    if not await DatabaseHelper().is_user_exist(user_id):
        await DatabaseHelper().add_user(user_id)
        try:
            join_dt = await DatabaseHelper().get_bot_started_on(user_id)
            msg = f"<i>A New User has started the Bot: {message.from_user.mention}.</i>\n\n<b>Join Time</b>: {join_dt}"
            await client.send_message(
                chat_id=LOG_CHANNEL,
                text=msg,
                parse_mode=enums.ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception as err:
            LOGGER(__name__).error(f"BOT Log Channel Error: {err}")
    last_used_on = await DatabaseHelper().get_last_used_on(user_id)
    if last_used_on != datetime.date.today().isoformat():
        await DatabaseHelper().update_last_used_on(user_id)
    start = time()
    msg_text = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Processing your URL.....</b>"
    msg = await message.reply_text(
        text=msg_text, disable_web_page_preview=True, quote=True
    )
    LOGGER(__name__).info(f" Received : {cmd} - {url}")
    sleep(1)
    is_gdtot = is_gdtot_link(url)
    is_drivehubs = is_drivehubs_link(url)
    is_unified = is_unified_link(url)
    is_udrive = is_udrive_link(url)
    is_sharer = is_sharer_link(url)
    if is_gdtot:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>GDTot</i>"
        await msg.edit(text=abc)
        res = gdtot(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif is_drivehubs:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>DriveHubs</i>"
        await msg.edit(text=abc)
        res = drivehubs(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif is_unified:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>AppDrive Look-Alike</i>"
        await msg.edit(text=abc)
        res = unified(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif is_udrive:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>HubDrive Look-Alike</i>"
        await msg.edit(text=abc)
        res = udrive(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif is_sharer:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Sharer.pw</i>"
        await msg.edit(text=abc)
        res = sharerpw(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif "pahe." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Pahe</i>"
        await msg.edit(text=abc)
        res = pahe(url)
        time_taken = get_readable_time(time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    elif "drive.google.com" in url:
        await msg.delete()
        xyz = "You have entered a Google Drive Link!"
    else:
        await msg.delete()
        xyz = "This Command does not support this Link!"
    sleep(1)
    await message.reply_text(text=xyz, disable_web_page_preview=True, quote=True)
    try:
        msg = f"<b><i>User:</i></b> {uid}\n<i>User URL:</i> {url}\n<i>Destination URL:</i> {res}\n\n<b><i>Time Taken:</i></b> {time_taken}"
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=msg,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except Exception as err:
        LOGGER(__name__).error(f"BOT Log Channel Error: {err}")
