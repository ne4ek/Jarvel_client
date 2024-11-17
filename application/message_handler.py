from telethon import events
import config
from application.meet_summarizer.meet_summarizer import MeetSummarizer
from application.promts import summarization_prompt
from icecream import ic
import os
from dotenv import load_dotenv
load_dotenv()

ADMIN_TELEGRAM_USERNAME = os.getenv("ADMIN_TELEGRAM_USERNAME")

@config.client.on(events.NewMessage)
async def message_handler(event: events.NewMessage.Event):
    if event.message.document and event.message.document.mime_type in ["video/webm", "video/mp4"]:
        ic("video docement")
        jarvel_message = await event.reply("Обрабатываю") 
        try:
            meet_summarizer =  MeetSummarizer(event, config.client, summarization_prompt=summarization_prompt)
            response = await meet_summarizer.summarize()
            await jarvel_message.edit(response)

        except Exception as e:
            await jarvel_message.edit("Ошибка обработки")            
            await config.client.send_message(ADMIN_TELEGRAM_USERNAME, f"Ошибка в {event.chat_id}")
            await config.client.send_message(ADMIN_TELEGRAM_USERNAME, str(e))
            ic(event.chat)
            raise e
        