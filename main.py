from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models 
from database import engine, SessionLocal, Base, get_db

app = FastAPI()

# 1. GET /api/objects : Liste paginée
@app.get("/api/objects")
def read_pokemons(page: int = 1, db: Session = Depends(get_db)):
    limit = 20
    skip = (page - 1) * limit
    # On utilise models.Pokemon car on a fait "import models"
    return db.query(models.Pokemon).offset(skip).limit(limit).all()

# 2. GET /api/objects/{id} : Un seul objet
@app.get("/api/objects/{id}")
def read_pokemon(id: int, db: Session = Depends(get_db)):
    pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == id).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon non trouvé")
    return pokemon

# 3. POST /api/objects : Insertion + Calcul
@app.post("/api/objects")
def create_pokemon(data: dict, db: Session = Depends(get_db)):
    # Création de l'instance
    new_pkmn = models.Pokemon(**data)
    db.add(new_pkmn)
    db.commit()
    db.refresh(new_pkmn)
    
    # CALCUL : Ratio expérience par unité de poids
    ratio = new_pkmn.base_experience / new_pkmn.weight if new_pkmn.weight > 0 else 0
    
    return {"status": "Créé", "pokemon": new_pkmn, "ratio_experience": ratio}

# 4. PUT /api/objects/{id} : Modification
@app.put("/api/objects/{id}")
def update_pokemon(id: int, data: dict, db: Session = Depends(get_db)):
    db_pkmn = db.query(models.Pokemon).filter(models.Pokemon.id == id).first()
    if not db_pkmn:
        raise HTTPException(status_code=404, detail="Pokémon non trouvé")
    
    for key, value in data.items():
        setattr(db_pkmn, key, value)
        
    db.commit()
    db.refresh(db_pkmn)
    return db_pkmn

# 5. DELETE /api/objects/{id} : Suppression
@app.delete("/api/objects/{id}")
def delete_pokemon(id: int, db: Session = Depends(get_db)):
    db_pkmn = db.query(models.Pokemon).filter(models.Pokemon.id == id).first()
    if not db_pkmn:
        raise HTTPException(status_code=404, detail="Pokémon non trouvé")
    
    db.delete(db_pkmn)
    db.commit()
    return {"message": "Pokémon supprimé"}