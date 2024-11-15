from pydantic import BaseModel

class ImageQueryRequest(BaseModel):
    user_message: str