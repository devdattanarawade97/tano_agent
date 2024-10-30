from pydantic import BaseModel

class DocsQueryRequest(BaseModel):
    user_query: str
    relevant_docs:str