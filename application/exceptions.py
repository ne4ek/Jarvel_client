from consts import MAX_FILE_SIZE_FOR_OPENAI_TRANSCRIBER

class FileSizeTooBigForOpenaiTranscriber(Exception):
    def __str__(self) -> str:
        return f"File is bigger that {MAX_FILE_SIZE_FOR_OPENAI_TRANSCRIBER} bytes."