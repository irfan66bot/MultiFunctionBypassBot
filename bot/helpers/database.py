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
        self.__connect()

    def __connect(self):
        try:
            self.__client = MongoClient(DATABASE_URL)
            self.__db = self.__client["MFBot"]
            self.__collection = self.__db["users"]
        except PyMongoError as err:
            LOGGER(__name__).error(err)
            self.__err = True

    def auth_user(self, user_id: int):
        if self.__err:
            return
        self.__collection.insert_one({"user_id": user_id})
        self.__client.close()
        LOGGER(__name__).info(f"Added {user_id} to Sudo Users List!")
        return f"<b><i>Successfully added {user_id} to Sudo Users List!</i></b>"

    def unauth_user(self, user_id: int):
        if self.__err:
            return
        self.__collection.delete_many({"user_id": user_id})
        self.__client.close()
        LOGGER(__name__).info(f"Removed {user_id} from Sudo Users List!")
        return f"<b><i>Successfully removed {user_id} from Sudo Users List!</i></b>"

    def load_users(self):
        if self.__err:
            return
        users = self.__collection.find().sort("user_id")
        for user in users:
            SUDO_USERS.add(user["user_id"])
        self.__client.close()


if DATABASE_URL is not None:
    DatabaseHelper().load_users()
