from pydantic import BaseModel


class Item(BaseModel):
    key: str
    valeur: str

    class Config:
        orm_mode = True

class TradParams(BaseModel):
    word: str
    dictionnary: str

class create_dic(BaseModel):
    dictionnary: str
    table: list[Item]

    class Config:
        orm_mode = True

class delete_dic(BaseModel):
    dictionnary: str

    class Config:
            orm_mode = True
    
