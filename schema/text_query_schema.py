from pydantic import BaseModel

class TextQueryRequest(BaseModel):
    user_message: str