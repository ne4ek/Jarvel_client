from openai import AsyncOpenAI
from application.entity.video_transcriber import VideoTranscriber
import os
from icecream import ic
from dotenv import load_dotenv
load_dotenv()


class OnlineVideoTranscriber(VideoTranscriber):
    def __init__(self, trancriber_model="whisper-1", promt="", gpt_api_key=os.getenv("GPT_API_KEY")):
        self.openAI_client = AsyncOpenAI(api_key=gpt_api_key)
        self.trancriber_model = trancriber_model 
        self.promt = promt

    async def transcribe(self, path: str):
        with open(path, "rb") as saved_file:
            transcription = await self.openAI_client.audio.transcriptions.create(
                model = self.trancriber_model,
                file = saved_file,
                response_format="text",
                prompt=self.promt,
            )
            ic(transcription)
            return transcription