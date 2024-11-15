from telethon import TelegramClient, events, sync
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")


client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE_NUMBER)
        await client.sign_in(PHONE_NUMBER, 'your_verification_code')
    print("Connected to Telegram!")


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
        client.run_until_disconnected()
