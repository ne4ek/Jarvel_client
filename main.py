from telethon import TelegramClient, events, sync



client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage)
async def handle_new_message(event):
    if event.message.document and event.message.document.mime_type in ["video/webm", "video/mp4"]:
        pass

with client:
    client.run_until_disconnected()
