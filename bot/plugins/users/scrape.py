import datetime
import time
from re import search

from pyrogram import Client, filters
from pyrogram.types import Message

from bot.config import BOT_USERNAME, COMMAND_PREFIXES, LOG_CHANNEL
from bot.helpers.database import DatabaseHelper
from bot.helpers.decorators import user_commands
from bot.helpers.functions import get_readable_time
from bot.logging import LOGGER
from bot.modules.bypasser import htpmovies, privatemoviez
from bot.modules.gdrive_direct import pahe
from bot.modules.lists import *
from bot.modules.pasting import telegraph_paste
from bot.modules.regex import *
from bot.modules.scraper import *

prefixes = COMMAND_PREFIXES
commands = ["scrape", f"scrape@{BOT_USERNAME}"]


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def scrape(client, message: Message):
    """
    Extract Direct Links from Supported Sites
    """
    if len(message.command) != 2:
        await message.reply_text("Sorry, Could not understand your Input!")
        return
    msg_arg = message.text.replace("  ", " ")
    msg_args = msg_arg.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    if len(msg_args) > 1:
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
    elif msg_args.count == (0 or 1) or reply_to is None:
        return "Bot could not retrieve your Input!"

    if url is not None:
        if url.startswith("http://"):
            url = url.replace("http://", "https://")
        elif not url.startswith("https://"):
            url = "https://" + url
    else:
        return "Bot could not retrieve your URL!"

    valid_url = is_a_url(url)
    if valid_url is not True:
        return "You did not seem to have entered a valid URL!"
    uname = message.from_user.mention
    uid = f"<code>{message.from_user.id}</code>"
    user_id = message.from_user.id
    if not await DatabaseHelper().is_user_exist(user_id):
        await DatabaseHelper().add_user(user_id)
        try:
            join_dt = await DatabaseHelper().get_bot_started_on(user_id)
            msg = f"<i>A New User has started the Bot: {message.from_user.mention}.</i>\n\n<b>Join Time</b>: {join_dt}"
            await client.send_message(chat_id=LOG_CHANNEL, text=msg)
        except BaseException:
            pass
    last_used_on = await DatabaseHelper().get_last_used_on(user_id)
    if last_used_on != datetime.date.today().isoformat():
        await DatabaseHelper().update_last_used_on(user_id)
    start = time.time()
    msg_text = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Processing your URL.....</b>"
    msg = await message.reply_text(
        text=msg_text, disable_web_page_preview=True, quote=True
    )
    LOGGER(__name__).info(f" Received : {cmd} - {url}")
    time.sleep(1)
    if (
        "workers.dev" in url
        or "0:/" in url
        or "1:/" in url
        or "2:/" in url
        or "3:/" in url
        or "4:/" in url
        or "5:/" in url
        or "6:/" in url
    ):
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Bhadoo Index</i>"
        await msg.edit(text=abc)
        res = index_scrap(url)
        des_url = telegraph_paste(res)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "atishmkv." in url or "atish.mkv" in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>AtishMKV</i>"
        await msg.edit(text=abc)
        des_url = atishmkv_scrap(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "cinevez." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Cinevez</i>"
        await msg.edit(text=abc)
        des_url = cinevez_scrap(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "cinevood." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Cinevood</i>"
        await msg.edit(text=abc)
        des_url = cinevood_scrap(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "filecrypt." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Filecrypt</i>"
        await msg.edit(text=abc)
        des_url = filecrypt_scrap(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "htpmovies." in url and "/exit.php?url=" in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>HTP Movies</i>"
        await msg.edit(text=abc)
        des_url = htpmovies(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "igg-games." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>IGG Games</i>"
        await msg.edit(text=abc)
        des_url = igggames_scrape(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "moviesdrama." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Movies Drama</i>"
        await msg.edit(text=abc)
        des_url = moviesdrama_scrap(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "olamovies." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>OlaMovies</i>"
        await msg.edit(text=abc)
        des_url = olamovies_scrap(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "psa." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>PSA</i>"
        await msg.edit(text=abc)
        """ des_url = psa_scrap(url)
      time_taken = get_readable_time(time.time() - start)
      LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
      xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>" """
        xyz = "<b>PSA Scraper has been patched for now!</b>"
    elif "taemovies." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>TaeMovies</i>"
        await msg.edit(text=abc)
        des_url = taemovies_scrap(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "teleguflix." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>TeleguFlix</i>"
        await msg.edit(text=abc)
        des_url = teleguflix_scrap(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "toonworld4all." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>ToonWorld4all</i>"
        await msg.edit(text=abc)
        des_url = toonworld4all_scrap(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "sharespark." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Sharespark</i>"
        await msg.edit(text=abc)
        des_url = sharespark_scrap(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "privatemoviez." in url and "/secret?data=" in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Privatemoviez</i>"
        await msg.edit(text=abc)
        des_url = privatemoviez(url)
        time_taken = get_readable_time(time.time() - start)
        LOGGER(__name__).info(f" Destination : {cmd} - {des_url}")
        xyz = f"<b>Telegraph URL(with Result):\n</b> {des_url}\n\n<i>Time Taken : {time_taken}</i>"
    elif "pahe." in url:
        abc = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n\n<b>Link Type</b> : <i>Pahe</i>"
        await msg.edit(text=abc)
        res = pahe(url)
        LOGGER(__name__).info(f" Destination : {cmd} - {res}")
        xyz = f"<b>Direct Gdrive Link :\n</b>{res}"
    elif any(x in url for x in yandisk_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in fmed_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in sbembed_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in directdl_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link Generator</b>\n\n<i>Use it with /direct command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in linkvertise_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Short Link Bypasser</b>\n\n<i>Use it with /bypass command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in bypass_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Short Link Bypasser</b>\n\n<i>Use it with /bypass command followed by Link</i>"
        await msg.edit(text=err)
        return
    elif any(x in url for x in adfly_list):
        err = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Short Link Bypasser</b>\n\n<i>Use it with /bypass command followed by Link</i>"
        await msg.edit(text=err)
        return
    else:
        await msg.delete()
        xyz = "This Command does not support this Link!"
    time.sleep(1)
    await message.reply_text(text=xyz, disable_web_page_preview=True, quote=True)
    try:
        msg = f"<b><i>User:</i></b> {uid}\n<i>User URL:</i> {url}\n<i>Destination URL:</i> {res}\n\n<b><i>Time Taken:</i></b> {time_taken}"
        await client.send_message(chat_id=LOG_CHANNEL, text=msg)
    except BaseException:
        pass
