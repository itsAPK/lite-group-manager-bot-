from pyrogram import filters ,Client
from bot.database.models.admin_db import get_admin
from pyrogram.types import Message
from bot import SUDO_USERS

async def admin_check_func(_, __, message: Message):
    if message.from_user.id == int(SUDO_USERS) or message.from_user.id in get_admin() :
    
        return True
    
    

admin_only=filters.create(admin_check_func,name='admin_only')