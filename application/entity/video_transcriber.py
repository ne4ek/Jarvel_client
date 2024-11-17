from abc import ABC, abstractmethod

class VideoTranscriber(ABC):

    @abstractmethod
    def __init__(self) -> None: pass

    @abstractmethod
    def transcribe(self, path: str) -> str: pass