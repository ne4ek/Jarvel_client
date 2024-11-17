import whisper
import torch
import asyncio
from application.entity.video_transcriber import VideoTranscriber
from icecream import ic



class OfflineVideoTranscriber(VideoTranscriber):
    def __init__(self, trancriber_model="small") -> None:
        self.trancriber_model = trancriber_model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"



    async def transcribe(self, path: str):
        ic(self.device)
        model = whisper.load_model(self.trancriber_model, device=self.device)
        
        result = await asyncio.to_thread(model.transcribe, path, word_timestamps=False)
        return result['text']