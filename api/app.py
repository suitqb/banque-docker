# api/app.py
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, condecimal
from sqlalchemy.exc import SQLAlchemyError
from db import SessionLocal, engine, Base
from models import Compte

app = FastAPI(
    title="API Banque",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
)

Base.metadata.create_all(bind=engine)

router = APIRouter()

class CompteCreate(BaseModel):
    nom: str
    solde_initial: condecimal(max_digits=12, decimal_places=2) = 0

class Mouvement(BaseModel):
    montant: condecimal(gt=0, max_digits=12, decimal_places=2)

class CompteOut(BaseModel):
    id: int
    nom: str
    solde: condecimal(max_digits=12, decimal_places=2)
    class Config:
        from_attributes = True

@router.post("/comptes", response_model=CompteOut, summary="creerCompte")
def creer_compte(payload: CompteCreate):
    db = SessionLocal()
    try:
        c = Compte(nom=payload.nom, solde=payload.solde_initial)
        db.add(c)
        db.commit()
        db.refresh(c)
        return c
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/comptes/{compte_id}", response_model=CompteOut, summary="consulterCompte")
def consulter_compte(compte_id: int):
    db = SessionLocal()
    try:
        c = db.get(Compte, compte_id)
        if not c:
            raise HTTPException(status_code=404, detail="Compte introuvable")
        return c
    finally:
        db.close()

@router.post("/comptes/{compte_id}/depot", response_model=CompteOut, summary="deposerArgent")
def deposer_argent(compte_id: int, payload: Mouvement):
    db = SessionLocal()
    try:
        c = db.get(Compte, compte_id)
        if not c:
            raise HTTPException(status_code=404, detail="Compte introuvable")
        c.solde = c.solde + payload.montant
        db.commit()
        db.refresh(c)
        return c
    finally:
        db.close()

@router.post("/comptes/{compte_id}/retrait", response_model=CompteOut, summary="retirerArgent")
def retirer_argent(compte_id: int, payload: Mouvement):
    db = SessionLocal()
    try:
        c = db.get(Compte, compte_id)
        if not c:
            raise HTTPException(status_code=404, detail="Compte introuvable")
        if c.solde < payload.montant:
            raise HTTPException(status_code=400, detail="Solde insuffisant")
        c.solde = c.solde - payload.montant
        db.commit()
        db.refresh(c)
        return c
    finally:
        db.close()

@router.delete("/comptes/{compte_id}", summary="effacerCompte")
def effacer_compte(compte_id: int):
    db = SessionLocal()
    try:
        c = db.get(Compte, compte_id)
        if not c:
            raise HTTPException(status_code=404, detail="Compte introuvable")
        db.delete(c)
        db.commit()
        return {"message": "Compte supprimé"}
    finally:
        db.close()

# Monte toutes les routes sous /api
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "service": "api-banque"}
