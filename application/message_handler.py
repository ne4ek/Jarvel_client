from telethon import events
from meet_summarizer.meet_summarizer import MeetSummarizer
import sys
import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config

@config.client.on(events.NewMessage)
async def message_handler(event: events.NewMessage.Event):
    if event.message.document and event.message.document.mime_type in ["video/webm", "video/mp4"]:
        meet_summarizer =  MeetSummarizer(event, config.client)
        response = await meet_summarizer.summarize()
        await event.reply(response)