from datetime import timedelta, datetime
from telethon import TelegramClient, events
import config
import asyncio

client = TelegramClient("meal_reminder_bot", config.API_ID, config.API_HASH).start(bot_token=config.BOT_TOKEN)

reminder_times =[
    {"hour": 14, "minute": 0, "message": "It's time for the first meal!"},
    {"hour": 19, "minute": 0, "message": "It's time for the second meal!"},
    {"hour": 00, "minute": 0, "message": "It's time for the night meal!"}
]

def get_next_reminder_time():
    now = datetime.now()
    for reminder in reminder_times:
        reminder_time = now.replace(hour=reminder["hour"], minute=reminder["minute"], second=0, microsecond=0)
        if reminder_time >= now :
           return reminder_time, reminder["message"]
    first_reminder = reminder_times[0]
    reminder_time = (now + timedelta(days=1)).replace(hour=first_reminder["hour"], minute=first_reminder["minute"],second=0, microsecond=0)
    return reminder_time, first_reminder["message"]


async def send_reminders(chat_id):
    while True:
        next_time, message = get_next_reminder_time()
        time_to_wait = (next_time - datetime.now()).total_seconds()
        await asyncio.sleep(time_to_wait)
        await client.send_message(chat_id, message)

@client.on(events.NewMessage(pattern="(?i)/start"))
async def handler_start(event):
    await event.respond("Hi! I will remind you to take the meals at 14:00, 19:00, 00:00.")
    asyncio.create_task(send_reminders(event.chat_id))


if __name__ == "__main__":
    print("Bot started...")
    client.run_until_disconnected()


    

