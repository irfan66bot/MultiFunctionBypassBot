import asyncio
import datetime
import io
import time
import traceback

from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    PeerIdInvalid,
    UserIsBlocked,
)

from bot.config import LOG_CHANNEL
from bot.helpers.database import DatabaseHelper
from bot.logging import LOGGER


class Broadcast:
    def __init__(self, client, broadcast_message):
        self.client = client
        self.broadcast_message = broadcast_message

        self.cancelled = False
        self.progress = dict(total=0, current=0, failed=0, success=0)

    def get_progress(self):
        return self.progress

    def cancel(self):
        self.cancelled = True

    async def _send_msg(self, user_id):
        try:
            await self.broadcast_message.copy(chat_id=user_id)
            return 200, None
        except FloodWait as e:
            await asyncio.sleep(e.x + 1)
            return self._send_msg(user_id)
        except InputUserDeactivated as e:
            LOGGER(__name__).error(e)
            return 400, f"{user_id} : deactivated\n"
        except UserIsBlocked as e:
            LOGGER(__name__).error(e)
            return 400, f"{user_id} : blocked the bot\n"
        except PeerIdInvalid as e:
            LOGGER(__name__).error(e)
            return 400, f"{user_id} : user id invalid\n"
        except Exception as e:
            LOGGER(__name__).error(e, exc_info=True)
            return 500, f"{user_id} : {traceback.format_exc()}\n"

    async def start(self):
        all_users = await DatabaseHelper().get_all_users()
        start_time = time.time()
        total_users = await DatabaseHelper().total_users_count()
        done = 0
        failed = 0
        success = 0
        log_file = io.BytesIO()
        log_file.name = f"{datetime.datetime.utcnow()}_broadcast.txt"
        broadcast_log = ""
        async for user in all_users:
            await asyncio.sleep(0.5)
            sts, msg = await self._send_msg(user_id=int(user["id"]))
            if msg is not None:
                broadcast_log += msg
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await DatabaseHelper().delete_user(user["id"])
            done += 1
            self.progress.update(dict(current=done, failed=failed, success=success))
            if self.cancelled:
                break
        log_file.write(broadcast_log.encode())
        completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
        await asyncio.sleep(3)
        if not self.cancelled:
            update_text = f"#Broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.\nStatus: Completed"
        else:
            update_text = f"#Broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.\nStatus: Cancelled"
        if failed == 0:
            await self.client.send_message(
                chat_id=LOG_CHANNEL,
                text=update_text,
            )
        else:
            await self.client.send_document(
                chat_id=LOG_CHANNEL,
                document=log_file,
                caption=update_text,
            )
