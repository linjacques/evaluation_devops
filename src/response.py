from pydantic import BaseModel


class IndexResponse(BaseModel):
    msg: str

class getTradResponse(BaseModel):
    word: str

class postTradResponse(BaseModel):
    word: str
    dictionnary: str
    trad: str

class Item(BaseModel):
    key: int
    valeur: str

    class Config:
        orm_mode = True
    