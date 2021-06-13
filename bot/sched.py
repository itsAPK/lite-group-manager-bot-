from pytz import utc
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from bot import DATABASE_URI,STRING_SESSION,API_HASH,APP_ID,BOT_TOKEN
from pyrogram import Client

#app=Client('me',api_hash=API_HASH,api_id=APP_ID,bot_token=BOT_TOKEN)

jobstores = {
    'default': SQLAlchemyJobStore(url=DATABASE_URI)
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

