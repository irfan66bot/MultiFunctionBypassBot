import datetime
from re import search
from time import sleep, time

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from bot.config import *
from bot.helpers.database import DatabaseHelper
from bot.helpers.decorators import user_commands
from bot.helpers.functions import forcesub, get_readable_time
from bot.logging import LOGGER
from bot.modules import bypasser
from bot.modules.lists import *
from bot.modules.regex import *

prefixes = COMMAND_PREFIXES
commands = ["bypass", f"bypass@{BOT_USERNAME}"]


async def send_bypass_message(cmd, link_type, url, uname, uid, msg):
    LOGGER(__name__).info(f" Received : {cmd} - {link_type} - {url}")
    a = f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>Bot has received the following link</b>‌ :\n<code>{url}</code>\n<b>Link Type</b> : <i>{link_type}</i>"
    await msg.edit(text=a)


async def send_bypass_message2(start, cmd, res, message, uid, url, client):
    time_taken = get_readable_time(time() - start)
    LOGGER(__name__).info(f" Destination : {cmd} - {res}")
    b = f"<b>Bypassed Result :\n</b>{res}\n\n<i>Time Taken : {time_taken}</i>"
    await message.reply_text(text=b, disable_web_page_preview=True, quote=True)
    try:
        logmsg = f"<b><i>User:</i></b> {uid}\n<i>User URL:</i> {url}\n<i>Command:</i> {cmd}\n<i>Destination URL:</i> {res}\n\n<b><i>Time Taken:</i></b> {time_taken}"
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=logmsg,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True,
        )
    except Exception as err:
        LOGGER(__name__).error(f"BOT Log Channel Error: {err}")


@Client.on_message(filters.command(commands, **prefixes))
@user_commands
async def bypass(client, message: Message):
    """
    Bypass Various Supported Shortened URLs
    """
    global link_type
    fsub = await forcesub(client, message)
    if not fsub:
        return
    msg_arg = message.text.replace("  ", " ")
    msg_args = msg_arg.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    global url, cmd
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
        err2 = "<b><i>You did not seem to have entered a valid URL!</i></b>"
        await message.reply_text(text=err2, disable_web_page_preview=True, quote=True)
        return

    uname = message.from_user.mention
    uid = f"<code>{message.from_user.id}</code>"
    user_id = message.from_user.id
    if not await DatabaseHelper().is_user_exist(user_id):
        await DatabaseHelper().add_user(user_id)
        try:
            join_dt = await DatabaseHelper().get_bot_started_on(user_id)
            startmsg = f"<i>A New User has started the Bot: {message.from_user.mention}.</i>\n\n<b>Join Time</b>: {join_dt}"
            await client.send_message(
                chat_id=LOG_CHANNEL,
                text=startmsg,
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
    if "adrinolinks." in url:
        link_type = "AdrinoLinks"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.adrinolinks(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "droplink." in url or "droplinks." in url:
        link_type = "DropLinks"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.droplink(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "dulink." in url:
        link_type = "Dulink"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.dulink(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "ez4short." in url:
        link_type = "Ez4Short"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.ez4short(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "gplink." in url or "gplinks." in url:
        link_type = "GPLinks"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.gplinks(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "krownlinks." in url:
        link_type = "KrownLinks"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.krownlinks(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif any(x in url for x in linkvertise_list):
        link_type = "Linkvertise"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.linkvertise(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif any(x in url for x in adfly_list):
        link_type = "AdFly"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.adfly(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "gyanilinks." in url or "gyanilink" in url:
        link_type = "GyaniLinks"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.gyanilinks(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "htpmovies." in url and "/exit.php?url" in url:
        link_type = "HTPMovies GDL"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.htpmovies(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "privatemoviez." in url and "/secret?data=" in url:
        link_type = "PrivateMoviez DL"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.privatemoviez(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "hypershort." in url:
        link_type = "HyperShort"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.hypershort(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "sirigan.my.id" in url:
        link_type = "Sirigan.my.id"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.sirigan(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "ouo.io" in url or "ouo.press" in url:
        link_type = "Ouo"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.ouo(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif any(x in url for x in shst_list):
        link_type = "Shorte.st"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.shorte(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "rocklinks." in url:
        link_type = "RockLinks"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.rocklinks(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif ("gtlinks." or "loan.kinemaster.cc/?token=" or "theforyou.in/?token=") in url:
        url = url.replace("&m=1", "")
        link_type = "GTLinks"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.gtlinks(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "gyanilinks." in url:
        link_type = "GyaniLinks"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.gyanilinks(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "shareus." in url:
        link_type = "Shareus"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.shareus(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "short2url." in url:
        link_type = "Short2url"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.short2url(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "shortingly." in url:
        link_type = "Shortingly"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.shortingly(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "tnlink." in url:
        link_type = "TnLink"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.tnlink(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif "xpshort." in url:
        link_type = "XpShort"
        await send_bypass_message(cmd, link_type, url, uname, uid, msg)
        res = await bypasser.xpshort(url)
        sleep(1)
        await send_bypass_message2(start, cmd, res, message, uid, url, client)
    elif any(x in url for x in yandisk_list):
        err3 = (
            f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link "
            f"Generator</b>\n\n<i>Use it with /direct command followed by Link</i> "
        )
        await msg.edit(text=err3)
        return
    elif any(x in url for x in fmed_list):
        err4 = (
            f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link "
            f"Generator</b>\n\n<i>Use it with /direct command followed by Link</i> "
        )
        await msg.edit(text=err4)
        return
    elif any(x in url for x in sbembed_list):
        err5 = (
            f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link "
            f"Generator</b>\n\n<i>Use it with /direct command followed by Link</i> "
        )
        await msg.edit(text=err5)
        return
    elif any(x in url for x in directdl_list):
        err6 = (
            f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Direct Link "
            f"Generator</b>\n\n<i>Use it with /direct command followed by Link</i> "
        )
        await msg.edit(text=err6)
        return
    elif any(x in url for x in scrape_list):
        err7 = (
            f"<b>Dear</b> {uname} (ID: {uid}),\n\n<b>This Link is Supported by the Site Scraper</b>\n\n<i>Use it "
            f"with /scrape command followed by Link</i> "
        )
        await msg.edit(text=err7)
        return
    else:
        try:
            link_type = "Script Generic"
            await send_bypass_message(cmd, link_type, url, uname, uid, msg)
            res = await bypasser.script(url)
            sleep(1)
            await send_bypass_message2(start, cmd, res, message, uid, url, client)
        except BaseException:
            err = "<b><i>Could not find Bypass for your URL!</i></b>"
            await msg.edit(text=err)
            return
