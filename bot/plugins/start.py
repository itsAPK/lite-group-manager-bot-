from pyrogram import filters,Client
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.models.admin_db import get_admin
from bot import (LOGGER,LOG_CHANNEL,SUDO_USERS)
from bot.utils.custom_filters import admin_only

print(SUDO_USERS)

@Bot.on_message(filters.command('start') & filters.private & admin_only)
async def start_handler(bot : Bot , message : Message):
    data=f"""
Hello {message.chat.first_name}

<b>In Bot Commands: </b>

<code>/setwelcome</code> - To set Welcome Message
<code>/getwelcome</code> - To see Welcome Message
<code>/addbutton</code> - To add buttons
<code>/getbuttons</code> - To get all buttons
<code>/deletebutton [button_id]</code> - To delete button
<code>/addadmin</code> - To add new admins
<code>/getadmins</code> - To get admins
<code>/removeadmin</code> - To remove admin
<code>/getgroups</code> - To get group details which using this bot
<code>/setwarn [limit]</code> - To Set warning limit
<code>/setwarnmode [mode]</code> - To set warn mode (kick,ban,mute)
<code>/warnsettings</code> - To get total warns 
<code>/addban</code> - To  ban user (Bot will delete their message )
<code>/unban</code> - To remove ban 
<code>/getbanneduser</code> - To get Banned users list
<code>/spamtext [list of text]</code> - Add spam text (sperated by commos)
<code>/getspamtext</code> - To get list of spam text
<code>/settask </code> -  Schedule periodic message
<code>/gettasks </code> - Get the list of scheduled task
<code>/removetask [task_id]</code> - Delete Scheduled task
<code>/removealltask</code> - remove all schedule task
<code>/gettaskinfo [task_id]</code> - To get specifc task info

<b>In Group Commands : </b>

<code>/warn [reason]</code> - To Warns user (admin only)
<code>/removewarn</code> - To remove user previous warns
<code>/resetwarn</code> - To reset all warning of user
<code>/ban [reason]</code> - Works same as global ban

"""
    await bot.send_message(message.chat.id,data)