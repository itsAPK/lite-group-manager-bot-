
import asyncio
from bot.database.models.admin_db import get_admin,get_group_id

async def delete_messages(bot_message,message):
    await asyncio.sleep(30)
    await bot_message.delete()
    await message.delete()

        
async def is_group_admin(bot,message):
        user=await bot.get_chat_member(message.chat.id,message.from_user.id)
        if user.status in ['creator','administrator']:
            return True
        else:
            False

async def delete_warn_message(message):
    await message.delete()
    
    
async def unban_member(bot,user_id):
    groups=get_group_id()
    for group in groups:
        await bot.unban_chat_member(group,user_id)