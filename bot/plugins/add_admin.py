from pyrogram import filters,Client
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.models.admin_db import (get_admin,
                                            add_admin,
                                            total_admins,
                                            get_admin_info,
                                            remove_admin
                                    
                                        )
from bot.utils.markup import (back_markup,empty_markup)
from bot import (LOGGER,LOG_CHANNEL,SUDO_USERS)
from bot.utils.custom_filters import admin_only


@Bot.on_message(filters.command('addadmin') & filters.private & admin_only)
async def add_admin_handler(bot:Client,message:Message):
    print(get_admin())
    try:
        add_admins=await bot.ask(message.from_user.id,"Forward any message of the user to make admin",reply_markup=back_markup())
        if add_admins.text=='🚫 Cancel':
            await bot.send_message(message.from_user.id,'Cancelled',reply_markup=empty_markup())
        else:
            
            add_admin(add_admins.forward_from.id,add_admins.forward_from.username,add_admins.forward_from.first_name)
            LOGGER.info(f"{add_admins.forward_from.id} added as admin by {message.from_user.id}")
            await bot.send_message(message.from_user.id,"Admin Added Sucessfully",reply_markup=empty_markup())
    except Exception as e:
            LOGGER.error(e)
            await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',parse_mode='html')
            await bot.send_message(message.from_user.id,'Aww :( , Something went wrong',reply_markup=empty_markup())

@Bot.on_message(filters.command('getadmins')& filters.private & admin_only)
async def get_admins_handler(bot : Client,message:Message):
    info=get_admin_info()
    if not info:
        await bot.send_message(message.chat.id,"No admins")
        return
    await bot.send_message(message.chat.id,info)

@Bot.on_message(filters.command('removeadmin')& filters.private & admin_only)
async def remove_admin_handler(bot : Client,message:Message):
    try:
        remove_admins=await bot.ask(message.from_user.id,"Forward any message of the user to remove admin",reply_markup=back_markup())
        if remove_admins.text=='🚫 Cancel':
            await bot.send_message(message.from_user.id,'Cancelled',reply_markup=empty_markup())
        else:
            remove_admin(remove_admins.forward_from.id)
            LOGGER.info(f"{remove_admins.forward_from.id} removed from admin by {message.from_user.id}")
            await bot.send_message(message.from_user.id,"Admin Removed Sucessfully",reply_markup=empty_markup())
    except Exception as e:
            LOGGER.error(e)
            await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',parse_mode='html')
            await bot.send_message(message.from_user.id,'Aww :( , Something went wrong',reply_markup=empty_markup())