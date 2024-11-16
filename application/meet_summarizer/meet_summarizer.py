from video_transcriber import VideoTranscriber
from consts import DIRNAME
import ffmpeg
import os

class MeetSummarizer:
    def __init__(self, event, client):
        self.event = event
        self.client = client

    async def summarize(self) -> str:
        fp_disk = self.__save_voice(self.event)
        transcriber = VideoTranscriber()
        transcribed_telegram_message = await transcriber.transcribe(fp_disk)
        os.remove(fp_disk)
        return transcribed_telegram_message

    async def __save_voice(self) -> str:

        file_name = self.event.message.document.attributes[0].file_name\
        if self.event.message.document.attributes else "unknown_file"

        temp = os.path.join(DIRNAME, "storage", file_name)
        await self.client.download_media(self.event.message, file=temp)
        fp_disk = os.path.join(DIRNAME, "storage", str(file_name).split(".")[0], "mp3")
        ffmpeg.input(temp).output(fp_disk, format="mp3").run(overwrite_output=True, quiet=True)
        os.remove(temp)
        return fp_disk

