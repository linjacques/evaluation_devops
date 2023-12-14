from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .params import TradParams ,create_dic ,delete_dic
from .response import IndexResponse, getTradResponse, postTradResponse
from .models import Trad, DicLine,Dict ,Base
from .database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=IndexResponse)
def index():
    return {'msg': 'Hello World !'}

@app.post('/traduire un mot', response_model=postTradResponse)
def postTrad(params: TradParams, db: Session = Depends(get_db)):

    translate = list(params.word)
    id_dic = db.query(Dict).filter(Dict.name == params.dictionnary).first()
    traduction = []

    # cherche une valeur correspondant à la lettre saisie, dans la table DicLine
    for lettre in translate:
        valeur = db.query(DicLine).filter(DicLine.Key == lettre, DicLine.dictid == id_dic.dictid).first()
        if valeur:
            traduction += valeur.valeur
    
    print(traduction)
    trad = "".join(traduction)

    trad_db = Trad(word=params.word, trad=trad, dictionnary=params.dictionnary)
    db.add(trad_db)
    db.commit()

    return {
        'word': params.word,
        'dictionnary': params.dictionnary,
        'trad': trad
    }

@app.get("/trad/{word}", response_model=getTradResponse)
def trad(word: str):
    return {
        'word': word
    }

@app.post("/créer un encodeur")
def addict(params: create_dic, db: Session = Depends(get_db)):

    dico = Dict(name = params.dictionnary)
    db.add(dico)
    db.commit()
    db.refresh(dico)

    id_dic = db.query(Dict).filter(Dict.name == params.dictionnary).first()

    for Item in params.table :
        dictline_db = DicLine(Key=Item.key, valeur=Item.valeur, dictid=id_dic.dictid)
        db.add(dictline_db)
        db.commit()

    return {
        'création réussie du dico':params.dictionnary
    }

@app.post("/supprimer l'encodeur")
def deldict(params: delete_dic, db: Session = Depends(get_db)):

    id_dic = db.query(Dict).filter(Dict.name == params.dictionnary).first()
    
    if id_dic:
        delite = db.query(DicLine).filter(DicLine.dictid == id_dic.dictid).all()
        for line in delite:
            db.delete(line)
        db.delete(id_dic)
        db.commit()
    else:
        print("Aucun dictionnaire trouvé pour ce nom.")
    return {
        'Validation':params.dictionnary
    }