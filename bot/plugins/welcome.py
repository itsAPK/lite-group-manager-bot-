from pyrogram import filters,Client
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.models.admin_db import get_admin
from bot.utils.markup import (back_markup,empty_markup,promo_button_markup)
from bot import (LOGGER,LOG_CHANNEL,SUDO_USERS)
from bot.utils.grouputils import delete_messages
from bot.database.models.settings_db import set_welcome_message,get_welcome_message,get_buttons
from bot.utils.custom_filters import admin_only


@Bot.on_message(filters.command('setwelcome')& filters.private & admin_only)
async def set_welcome_handler(bot : Client,message:Message):
    text_message=await bot.ask(message.chat.id,"Send Welcome message text (Use html tags to set markdown)",reply_markup=back_markup())
    if text_message.text=='🚫 Cancel':
            await bot.send_message(message.from_user.id,'Cancelled',reply_markup=empty_markup())
    else:
        set_welcome_message(text_message.text)
        await bot.send_message(message.chat.id,'Welcome message set sucessfully (To preview : /getwelcome )',reply_markup=empty_markup())

@Bot.on_message(filters.command('getwelcome')& filters.private & admin_only)
async def get_welcome_handler(bot : Client,message:Message):
    text=get_welcome_message()
    if not text:
        await bot.send_message(message.chat.id,"Welocme Message Not Set")
        return
    
    await bot.send_chat_action(message.chat.id,'typing')
    if get_buttons():
        await bot.send_message(message.chat.id,f"Hello<b> {message.chat.first_name}</b>,\n\n{text.text}",reply_markup=promo_button_markup())
    else:
        await bot.send_message(message.chat.id,f"Hello<b> {message.chat.first_name}</b>,\n\n{text.text}")
    

@Bot.on_message(filters.new_chat_members)
async def group_welcome_handler(bot : Client,message:Message):
    text=get_welcome_message()
    if not text:
        return
    
    await bot.send_chat_action(message.chat.id,'typing')
    if get_buttons():
        m=await bot.send_message(message.chat.id,f"Hello<b> {message.from_user.first_name}</b>,\n\n{text}",reply_markup=promo_button_markup())
    else:
        m=await bot.send_message(message.chat.id,f"Hello<b> {message.from_user.first_name}</b>,\n\n{text}")
    await delete_messages(m,message)
    


    