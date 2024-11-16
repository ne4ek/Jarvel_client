from openai import AsyncOpenAI
from dotenv import load_dotenv
import torch
import os
load_dotenv()


class VideoTranscriber:
    def __init__(self, trancriber_model="whisper-1", promt="", gpt_api_key=os.getenv("GPT_API_KEY")):
        self.openAI_client = AsyncOpenAI(gpt_api_key)
        self.trancriber_model = trancriber_model 
        self.promt = promt

    '''Transcribe only 'mp3' '''
    async def transcribe(self, path: str):
        saved_file = open(path, "rb")
        transcription = await self.openAI_client.audio.transcriptions.create(
            model = self.trancriber_model,
            file = saved_file,
            response_format="text",
            prompt=self.promt,
        )
        return transcription