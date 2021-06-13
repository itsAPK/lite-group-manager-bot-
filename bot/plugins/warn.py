import time
from pyrogram import Client,filters
from bot.bot import Bot
from pyrogram.types import Message,ChatPermissions
import traceback,time
from bot.database.models.admin_db import get_admin
from bot.utils.markup import back_markup,empty_markup
from bot import (LOGGER,LOG_CHANNEL,SUDO_USERS,BOT_ID)
from bot.utils.grouputils import is_group_admin,delete_messages,delete_warn_message
from bot.database.models.warn_db import (set_warn_mode,
                                        set_warn_limit,
                                        total_warned_user,
                                        total_warns,
                                        warn_user,
                                        remove_warn,
                                        reset_warn,
                                        get_user_warn_count,
                                        get_warn_settings
                                        )
from bot.utils.custom_filters import admin_only





@Bot.on_message(filters.command('warn') & filters.group)
async def warn_group(bot : Client, message : Message):
    is_admin=await is_group_admin(bot,message)
    limit,mode=get_warn_settings()
    if is_admin:
        if message.reply_to_message:
            reply_id=message.reply_to_message.message_id
            user_id=message.reply_to_message.from_user.id
            
            if len(message.text.split(" "))>=2:
                reason = message.text.split(None, 1)[1]
            else:
                reason = None
            
        elif not message.reply_to_message:
            m=await message.reply_text("Tell me user whom I should warn !")
            await delete_messages(m,message)
            return
        
        if user_id == BOT_ID:
            m=await message.reply_text("why would I warn myself?")
            await delete_messages(m,message)
            return
        
        if user_id is is_admin:
            m=await message.reply_text("I don't warn admins")
            await delete_messages(m,message)
            return
        
        user_warns=warn_user(message.chat.id,user_id)
        if user_warns >= limit:
            if mode == 'kick':
                await bot.kick_chat_member(message.chat.id,user_id,until_date=int(time.time() + 86400))
            if mode == 'mute':
                await bot.restrict_chat_member(message.chat.id,user_id,ChatPermissions(),until_dat=int(time.time()) + 3600)
            if mode == 'ban':
                await bot.kick_chat_member(message.chat.id,user_id)
                
        m=await message.reply_text(
                (f'<a href="tg://user?id={user_id}">{message.reply_to_message.from_user.first_name}</a> has been warned ({user_warns}/{limit})'
                f'\n<b>Reason for last warn</b>:\n{reason}'),reply_to_message_id=reply_id)
        
        await delete_warn_message(message.reply_to_message)
        await  delete_messages(m,message)
        await message.stop_propagation()
    else:
        m=await message.reply("You don't rights to warn")
        await delete_messages(m,message)
        return
    
    
    
@Bot.on_message(filters.command('removewarn') & filters.group)
async def remove_warn_group(bot : Client, message : Message):
    is_admin=await is_group_admin(bot,message)
    if is_admin:
        if message.reply_to_message:
            user_id=message.reply_to_message.from_user.id
            
        elif not message.reply_to_message:
            m=await message.reply_text("Tell me user whom I should warn !")
            await delete_messages(m,message)
            return
        
        if user_id == BOT_ID:
            m=await message.reply_text("why would I warn myself?")
            await delete_messages(m,message)
            return
        
        if user_id is is_admin:
            m=await message.reply_text("I don't warn admins")
            await delete_messages(m,message)
            return
        
        user_warned=get_user_warn_count(message.chat.id,user_id)
        if not user_warned:
            await m.reply_text("User has no warnings!")
            await delete_messages(m,message)
            return
        
        remove_warn(message.chat.id,user_id)
        m=await message.reply_text(f'<a href="tg://user?id={user_id}">{message.reply_to_message.from_user.first_name}</a> Previous Warning has been  removed')
        await delete_messages(m,message)
    
@Bot.on_message(filters.command('resetwarn') & filters.group)
async def warn_reset(bot : Client, message : Message):
    is_admin=await is_group_admin(bot,message)
    if is_admin:
        if not message.reply_to_message:
            m=await message.reply_text("Tell me user whom I should reset warn !")
            await delete_messages(m,message)
            return
    name=message.reply_to_message.from_user.first_name
    user_id=message.reply_to_message.from_user.id
    reset_warn(message.chat.id,user_id)
    m=await message.reply_text(f'Warnings have been reset for <a href="tg://user?id={user_id}">{name}</a>')
    await  delete_messages(m,message)  
  

@Bot.on_message(filters.command('setwarn') & filters.private & admin_only)
async def set_warn_limit_handler(bot : Client, message : Message):
    text=message.text.split(" ")
    if len(text) ==2:
        set_warn_limit(int(text[1]))
        await bot.send_message(message.chat.id,f"Warn Limit has been set to: {text[1]}")
    else:
        await bot.send_message(message.chat.id,'<code> Usage /setwarn <limit> </code>')
    
@Bot.on_message(filters.command('setwarnmode') & filters.private & admin_only)
async def set_warn_mode_handler(bot : Client, message : Message):
    text=message.text.split(" ")
    if len(text) ==2:
        set_warn_mode(str(text[1]))
        await bot.send_message(message.chat.id,f"Warn Mode has been set to: {text[1]}")
    else:
        await bot.send_message(message.chat.id,'<code> Usage /setwarnmode <mode> </code>')

@Bot.on_message(filters.command('warnsettings') & filters.private & admin_only)
async def warn_settings_handler(bot : Client, message : Message):
    limit,mode=get_warn_settings()
    total=total_warns()
    user=total_warned_user()
    await bot.send_message(message.chat.id,f"""
Warn Limit : {limit}
Warn Mode : {mode}

<b> -----------------------  </b>

Total Warns : {total}
Total Users Warned : {user}
""")