import time
from pyrogram import Client,filters
from bot.bot import Bot
from pyrogram.types import Message,ChatPermissions
import traceback,time
from bot.database.models.admin_db import get_admin
from bot.utils.markup import back_markup,empty_markup
from bot import (LOGGER,LOG_CHANNEL,SUDO_USERS,BOT_ID)
from bot.utils.grouputils import delete_messages,delete_warn_message,is_group_admin,unban_member
from bot.database.models.ban_db import add_ban_user,get_ban_user_data,remove_ban,get_ban_user,add_spam,get_spam_text
from bot.utils.custom_filters import admin_only

@Bot.on_message((filters.text | filters.media) & filters.group , group=1)
async def ban_users_group(bot : Client, message : Message):
    _,users=get_ban_user_data()
    u=[]
    for i in users:
        u.append(i.user_id)
    if message.from_user.id in u :
        await message.delete()
        return
    
    spam=get_spam_text()
    text=message.text
    if any(word.lower() in text.lower()  for word in spam):
        add_ban_user(message.from_user.id,message.from_user.first_name)
        await message.delete()
        return
    
@Bot.on_message(filters.command('addban') & filters.private & admin_only)
async def add_ban_user_handler(bot : Client, message : Message):
    try:
        user=await bot.ask(message.from_user.id,"Forward any message of the user to make admin",reply_markup=back_markup())
        if user.text=='🚫 Cancel':
            await bot.send_message(message.from_user.id,'Cancelled',reply_markup=empty_markup())
        else:
            
            add_ban_user(user.forward_from.id,user.forward_from.first_name)
            LOGGER.info(f"{user.forward_from.id} marked as ban by {message.from_user.id}")
            await bot.send_message(message.from_user.id," Added Sucessfully",reply_markup=empty_markup())
    except Exception as e:
            LOGGER.error(e)
            await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',parse_mode='html')
            await bot.send_message(message.from_user.id,'Aww :( , Something went wrong',reply_markup=empty_markup())
            
@Bot.on_message(filters.command('getbanneduser') & filters.private & admin_only)
async def get_ban_user_handler(bot : Client, message : Message):
    count,users=get_ban_user_data()
    data=""
    for user in users:
        data+=f"<a href=\'tg://user?id={user.user_id}'>{user.name}</a>\n"
    await bot.send_message(message.from_user.id,f"Total : {count}\n\n{data}")
    
@Bot.on_message(filters.command('ban') & filters.group)
async def globalban(bot: Client,message : Message  ):
    is_admin=await is_group_admin(bot,message)
    print(message)
    if is_admin:
        if message.reply_to_message:
            reply_id=message.reply_to_message.message_id
            user_id=message.reply_to_message.from_user.id
            
            if len(message.text.split(" "))>=2:
                reason = message.text.split(None, 1)[1]
            else:
                reason = None
            
        elif not message.reply_to_message:
            m=await message.reply_text("Tell me user whom I should ban !")
            await delete_messages(m,message)
            return
        
        if user_id == BOT_ID:
            m=await message.reply_text("why would I ban myself?")
            await delete_messages(m,message)
            return
        
        if user_id is is_admin:
            m=await message.reply_text("I don't ban admins")
            await delete_messages(m,message)
            return
        
        m=await message.reply_text((
            f'<a href="tg://user?id={user_id}">{message.reply_to_message.from_user.first_name}</a> has been globally banned\n'
            f'Reason : {reason}'),reply_to_message_id=reply_id)
        LOGGER.info(f"{message.from_user.id} globally banned {user_id} from {message.chat.id}")
        add_ban_user(user_id,message.reply_to_message.from_user.first_name)
        await bot.kick_chat_member(message.chat.id,user_id)
        await delete_warn_message(message.reply_to_message)
        await  delete_messages(m,message)
        await message.stop_propagation()
    else:
        m= await message.reply("You don't rights to ban")
        await delete_messages(m,message)
        return
    


@Bot.on_message(filters.command('unban') & filters.private& admin_only)
async def global_unban(bot: Client,message : Message  ):
    try:
        user=await bot.ask(message.from_user.id,"Forward any message of the user to make ban",reply_markup=back_markup())
        if user.text=='🚫 Cancel':
            await bot.send_message(message.from_user.id,'Cancelled',reply_markup=empty_markup())
        else:
            user_id=user.forward_from.id
            if not get_ban_user(user_id):
                await bot.send_message(message.chat.id,"This user not banned")
                return
            remove_ban(user_id)
            await unban_member(bot,user_id)
            LOGGER.info(f"{user.forward_from.id} marked as unban by {message.from_user.id}")
            await bot.send_message(message.from_user.id," Removed Sucessfully",reply_markup=empty_markup())
    except Exception as e:
            LOGGER.error(e)
            await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',parse_mode='html')
            await bot.send_message(message.from_user.id,'Aww :( , Something went wrong',reply_markup=empty_markup())
            
@Bot.on_message(filters.command('spamtext') & filters.private& admin_only)
async def spam_text(bot: Client,message : Message  ):
    if not len(message.text.split(" ")) >= 1:
        await bot.send_message(message.chat.id,"Usage <code>/spamtext [list of text]</code>")
        return
    texts=message.text[11:].split(',')
    for i in texts:
        print(i)
        add_spam(i.lower())
    await bot.send_message(message.chat.id,"Added Sucessfully")
    return

    
@Bot.on_message(filters.command('getspamtext')& filters.private& admin_only)
async def get_spam_message(bot: Client,message : Message  ):
    spam=get_spam_text()
    if not spam:
        await bot.send_message(message.chat.id,"No Spam messages/text added so far")
    with open('spam.txt','w') as file:
        for i in spam:
            file.write(f"{i}\n________________________________\n")
    await bot.send_document(message.chat.id,'spam.txt',caption=f"Total Text : {len(spam)}")
    
    
