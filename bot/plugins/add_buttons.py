from pyrogram import filters,Client
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.models.admin_db import get_admin
from bot.utils.markup import (back_markup,empty_markup)
from bot import (LOGGER,LOG_CHANNEL,SUDO_USERS)
from bot.database.models.settings_db import add_button,get_buttons,delete_button
from bot.utils.custom_filters import admin_only


@Bot.on_message(filters.command('addbutton')& filters.private & admin_only)
async def add_button_handler(bot : Client,message:Message):
    btn_name=await bot.ask(message.chat.id,"<b>✅ Send Button name</b>",reply_markup=back_markup())
    if btn_name.text=='🚫 Cancel':
            await bot.send_message(message.chat.id,"Terminated",reply_markup=empty_markup())
    else:
        btn_link=await bot.ask(message.chat.id,"<b>✅ Send Link for button</b>",reply_markup=back_markup())
        if btn_link.text=='🚫 Cancel':
            await bot.send_message(message.chat.id,"Terminated",reply_markup=empty_markup())
        else:
                add_button(btn_name.text,btn_link.text)
                await bot.send_message(message.chat.id,("<b>✅ Button added Sucessfully</b>\n\n"
                                                                f"Name : {btn_name.text}\n"
                                                                f"URL : {btn_link.text}")
                                        ,reply_markup=empty_markup())
                
@Bot.on_message(filters.command('deletebutton')& filters.private & admin_only)
async def delete_button_handler(bot : Client,message:Message):
    try:
        buuton_id=message.text.split(" ")[1]
        delete_button(buuton_id)
        await bot.send_message(message.chat.id,"Button deleted sucessfully")
    except IndexError:
        await bot.send_message(message.chat.id,"Invalid Button ID <code>/deletebutton <button id> </code>")
    except Exception as e:
        LOGGER.error(e)
        await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',parse_mode='html')
        await bot.send_message(message.from_user.id,'Aww :( , Something went wrong',reply_markup=empty_markup())

@Bot.on_message(filters.command('getbuttons')& filters.private & admin_only)
async def get_button_handler(bot : Client,message:Message):
    button=get_buttons()
    text=""
    for i in button:
        text+=f"Button ID : {i.id}\nName : {i.name}\nURL : {i.url}"
    await bot.send_message(message.chat.id,f"Buttons List : \n\n{text}")
        