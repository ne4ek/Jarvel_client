from telethon import events
from main import client

@client.on(events.NewMessage)
async def message_handler(event):
    if event.message.document and event.message.document.mime_type in ["video/webm", "video/mp4"]:
        pass