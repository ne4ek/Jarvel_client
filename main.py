from dotenv import load_dotenv
import os
from config import client
from icecream import ic
from application.message_handler import *

load_dotenv()

PHONE_NUMBER = os.getenv("PHONE_NUMBER")
ADMIN_TELEGRAM_USERNAME = os.getenv("ADMIN_TELEGRAM_USERNAME")

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE_NUMBER)
        await client.sign_in(PHONE_NUMBER, 'your_verification_code')
    await client.send_message(ADMIN_TELEGRAM_USERNAME, "yep")
    ic("Connected to Telegram!")


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
        client.run_until_disconnected()
