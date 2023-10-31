from typing import Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from pymongo import MongoClient
from tgbot.misc.logger import encode_user_message


class LoggingMiddleware(BaseMiddleware):
    def __init__(self, mongo: MongoClient):
        self.mongo: MongoClient = mongo

    async def __call__(self, handler, message: Message, data: Dict[str, Any]):
        log = encode_user_message(message)
        self.mongo.logs.insert_one(log)
        return await handler(message, data)