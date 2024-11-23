from application.meet_summarizer.online_video_transcriber import OnlineVideoTranscriber
from application.meet_summarizer.offline_video_transcriber import OfflineVideoTranscriber
from consts import DIRNAME, MAX_FILE_SIZE_FOR_OPENAI_TRANSCRIBER
from openai import AsyncOpenAI
import ffmpeg
import os
from icecream import ic
import asyncio
from dotenv import load_dotenv
load_dotenv()

class MeetSummarizer:
    def __init__(self, event, client, gpt_model="gpt-4o-mini", gpt_api_key=os.getenv("GPT_API_KEY"), summarization_prompt=""):    
        self.event = event
        self.client = client
        self.gpt_model = gpt_model
        self.openAI_client = AsyncOpenAI(api_key=gpt_api_key)
        self.summarization_prompt = summarization_prompt

    async def summarize(self) -> str:
        path = await self.__save_voice()
        transcribed_telegram_message = await self.__get_transcribed_telegram_message(path)

            
        context = [{"role": "system", "content": self.summarization_prompt},
                    {"role": "user", "content": transcribed_telegram_message}]
        
        response = await self.openAI_client.chat.completions.create(
            messages=context,
            model=self.gpt_model,
        )

        summarized_telegram_message = response.choices[0].message.content
        ic(summarized_telegram_message)
        return summarized_telegram_message

    async def __get_transcribed_telegram_message(self, path: str):
        try:
            file_size = os.path.getsize(path)
            ic(file_size)
            if file_size < MAX_FILE_SIZE_FOR_OPENAI_TRANSCRIBER:
                #TODO make custom error 
                raise ValueError
            transcriber = OnlineVideoTranscriber() 
            transcribed_telegram_message = await transcriber.transcribe(path)
        except Exception as e:
            os.remove(path)
            raise e
        os.remove(path)
        return transcribed_telegram_message
    

    async def __save_voice(self) -> str:

        file_name = self.event.message.document.attributes[0].file_name\
        if self.event.message.document.attributes else "unknown_file"

        temp = os.path.join(DIRNAME, "storage", file_name)
        await self.client.download_media(self.event.message, file=temp)
        fp_disk = os.path.join(DIRNAME, "storage", str(file_name).split(".")[0] + ".mp3")

        process = (ffmpeg.input(temp)
                   .output(fp_disk, format="mp3", bitrate='64k', ar=22050, ac=1)
                   .run_async(overwrite_output=True, quiet=True))

        ic("ffmpeg")
        await asyncio.get_event_loop().run_in_executor(None, process.wait)
        os.remove(temp)
        return fp_disk

