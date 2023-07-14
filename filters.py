from aiogram.filters import Filter
from aiogram.types import Message

import db

class AdminFilter(Filter):
    async def __call__(self, message: Message):
        return db.admins.check_admin(message.from_user.id)