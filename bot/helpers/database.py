import datetime

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from bot.config import DATABASE_URL, SUDO_USERS
from bot.logging import LOGGER


class DatabaseHelper:
    def __init__(self):
        self.__err = False
        self.__client = None
        self.__db = None
        self.__collection = None
        self.__collection2 = None
        self.__connect()

    def __connect(self):
        try:
            self.__client = MongoClient(DATABASE_URL)
            self.__db = self.__client["MFBot"]
            self.__collection = self.__db["users"]
            self.__collection2 = self.__db["sudo_users"]
            self.__err = False
        except PyMongoError as err:
            LOGGER(__name__).error(f"Error in DB connection: {err}")
            self.__err = True

    async def auth_user(self, user_id: int):
        if self.__err:
            return
        self.__collection2.insert_one({"sudo_user_id": user_id})
        self.__client.close()
        LOGGER(__name__).info(f"Added {user_id} to Sudo Users List!")
        return f"<b><i>Successfully added {user_id} to Sudo Users List!</i></b>"

    async def unauth_user(self, user_id: int):
        if self.__err:
            return
        self.__collection2.delete_many({"sudo_user_id": user_id})
        self.__client.close()
        LOGGER(__name__).info(f"Removed {user_id} from Sudo Users List!")
        return f"<b><i>Successfully removed {user_id} from Sudo Users List!</i></b>"

    def new_user(self, user_id):
        return dict(
            id=user_id,
            join_date=datetime.date.today().isoformat(),
            last_used_on=datetime.date.today().isoformat(),
        )

    async def get_user(self, user_id: int):
        if self.__err:
            return
        user = self.__collection.find_one({"id": user_id})
        if user is not None:
            return user
        await self.add_user(user_id)
        self.__client.close()
        return user

    async def add_user(self, user_id: int):
        if self.__err:
            return
        user = self.new_user(user_id)
        self.__collection.update_one({"id": user["id"]}, {"$set": {"join_date": user["join_date"], "last_used_on": user["last_used_on"]}}, upsert=True)
        self.__client.close()

    async def is_user_exist(self, user_id: int):
        if self.__err:
            return
        user = await self.get_user(user_id)
        return True if user else False

    async def total_users_count(self):
        if self.__err:
            return
        count = self.__collection.count_documents({})
        self.__client.close()
        return count

    async def get_all_users(self):
        if self.__err:
            return
        all_users = self.__collection.find({"id"})
        self.__client.close()
        return all_users

    async def delete_user(self, user_id: int):
        if self.__err:
            return
        if self.__collection.find_one({"id": int(user_id)}):
            self.__collection.delete_many({"id": user_id})
        self.__client.close()

    async def update_last_used_on(self, user_id: int):
        if self.__err:
            return
        self.__collection.update_one(
            {"id": user_id},
            {"$set": {"last_used_on": datetime.date.today().isoformat()}}, upsert=True
        )
        self.__client.close()

    async def get_last_used_on(self, user_id: int):
        if self.__err:
            return
        user = await self.get_user(user_id)
        return user.get("last_used_on", datetime.date.today().isoformat())

    async def get_bot_started_on(self, user_id: int):
        if self.__err:
            return
        user = await self.get_user(user_id)
        return user.get("join_date", datetime.date.today().isoformat())

    def load_sudo_users(self):
        if self.__err:
            return
        sudo_users = self.__collection2.find().sort("sudo_user_id")
        for sudo_user in sudo_users:
            SUDO_USERS.add(sudo_user["sudo_user_id"])
        LOGGER(__name__).info(f"Successfully Loaded Sudo Users from DB!")
        self.__client.close()


if DATABASE_URL is not None:
    DatabaseHelper().load_sudo_users()
