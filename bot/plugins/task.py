from pyrogram import filters,Client
from bot.bot import Bot,BOT_TOKEN
from bot.sched import scheduler,jobstores
from pyrogram.types import Message
import traceback,time,uuid
import requests
from bot.database.models.admin_db import get_admin,get_group_id
from bot.utils.markup import (back_markup,empty_markup)
from bot import (LOGGER,LOG_CHANNEL,SUDO_USERS,)
from bot.utils.grouputils import delete_messages
from bot.database.models.settings_db import add_task,delete_task,get_task_data,delete_all_task
from bot.utils.custom_filters import admin_only


@Bot.on_message(filters.command('settask')& filters.private & admin_only)
async def set_task_handler(bot : Client,message:Message):
    text_message=await bot.ask(message.chat.id,"Send message text (Use html tags to set markdown)",reply_markup=back_markup())
    if text_message.text=='🚫 Cancel':
            await bot.send_message(message.from_user.id,'Cancelled',reply_markup=empty_markup())
            return
    time=await bot.ask(message.chat.id,"Set minutes <code>[format MM]</code>",reply_markup=back_markup())
    if time.text=='🚫 Cancel':
        await bot.send_message(message.from_user.id,'Cancelled',reply_markup=empty_markup())
        return
    else:
        id_=await genrate_id()
        scheduler.add_job(send_message, 'interval', minutes=int(time.text),id=id_,kwargs={'text': text_message.text})
        add_task(id_,text_message.text)
        await bot.send_message(message.chat.id,f'New message Scheduled for every {int(time.text)} Minutes\n\nID : <code>{id_}</code>',reply_markup=empty_markup())

@Bot.on_message(filters.command('gettasks')& filters.private & admin_only)
async def get_text_handler(bot : Client,message:Message):
    jobs = ""
    j=scheduler.get_jobs()
    for job in j :
        j=str(job.trigger)
        jobs+=f"ID : <code>{job.id}</code> {j[8:]} \n"
    await bot.send_chat_action(message.chat.id,'typing') 
    await bot.send_message(message.chat.id,f"Total task : {len(j)}\n\n{jobs}")


@Bot.on_message(filters.command('removetask')& filters.private & admin_only)
async def remove_task_handler(bot : Client,message:Message):
    text=message.text.split(" ")
    if not len(text) > 1:
        await bot.send_message(message.chat.id,"Usage : <code> /removetask [task_id]</code>")
        return
    scheduler.remove_job(job_id=text[1])
    delete_task(text[1])
    await bot.send_message(message.chat.id,"Task Removed")
    
    
@Bot.on_message(filters.command('removealltask')& filters.private & admin_only)
async def remove_all_task_handler(bot : Client,message:Message):
    scheduler.remove_all_jobs()
    delete_all_task()
    await bot.send_message(message.chat.id,"All Task Removed")
    
@Bot.on_message(filters.command('gettaskinfo')& filters.private & admin_only)
async def get_task_info_handler(bot : Client,message:Message):
    text=message.text.split(" ")
    print(len(text))
    if not len(text) > 1:
        await bot.send_message(message.chat.id,"Usage : <code> /gettaskinfo [task_id]</code>")
        return
    
    data=get_task_data(task_id=text[1])
    if data:
        await bot.send_message(message.chat.id,data.text)
        return
    await bot.send_message(message.chat.id,"Task Not found")
    
def send_message(text=None):
    
    LOGGER.info("SENDING SCHEDULER MESSAGE")
    grp=get_group_id()
    print(text)
    parse_mode='HTML'
    #I have know idea  how to fix .Just an alternative
    for i in grp:
        print(i)
        url_req = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={str(i)}&text={text}&parse_mode={parse_mode}"
        results = requests.get(url_req)
        print(results.json())
                
  
    
async def genrate_id():
    
    return uuid.uuid4().hex[:8]
"""@Bot.on_message(filters.new_chat_members)
async def group_text_handler(bot : Client,message:Message):
    text=get_text_message()
    await bot.send_chat_action(message.chat.id,'typing')
    await bot.send_message(message.chat.id,f"Hello<b> {message.chat.first_name}</b>,\n\n{text}",reply_markup=promo_button_markup())
    await delete_messages(bot,message)"""