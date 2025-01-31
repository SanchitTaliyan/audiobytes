from pydantic import BaseModel

__all__ = (
    "TextToSpeechRegisterRequest",
)

class TextToSpeechBase(BaseModel):
    pass

class TextToSpeechRegisterRequest(TextToSpeechBase):
    text: str
