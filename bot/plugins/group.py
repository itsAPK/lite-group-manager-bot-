from pyrogram import filters,Client
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.models.admin_db import get_admin,add_group,remove_group,get_group
from bot.utils.markup import (back_markup,empty_markup,promo_button_markup)
from bot import (LOGGER,LOG_CHANNEL,SUDO_USERS)

from bot.utils.custom_filters import admin_only


@Bot.on_chat_member_updated()
async def newgroup(bot : Client, message : Message):
    
    try:
        if message.new_chat_member.status=='kicked':
            LOGGER.info(f" Group Removed {message.chat.title} by {message.new_chat_member.invited_by.id}")
            remove_group(message.chat.id)
        if message.new_chat_member.status=='administrator':
            LOGGER.info(f"New Group Added {message.chat.title} by {message.new_chat_member.invited_by.id}")
            add_group(id=message.chat.id,
                username=message.chat.username,
                name=message.chat.title,
                added_by=message.new_chat_member.invited_by.id)
    except AttributeError:
        pass

@Bot.on_message(filters.command('getgroups') & filters.private & admin_only)
async def get_groups(bot : Client, message : Message):
    text=get_group()
    await bot.send_message(message.chat.id,text)
    
