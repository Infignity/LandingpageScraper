from typing import Optional
from pydantic import BaseModel


class TranslationRequest(BaseModel):
    '''basemodel translator'''
    url: str
    tag: str
    id: Optional[int] = None,
    text: str
