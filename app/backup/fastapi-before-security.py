from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from . import models, database, schemas, crud


# initiate fastapi
app = FastAPI(
    title='Plisca API',
    description='Ini adalah API',
    version='1.5.9',
    openapi_tags=[
        {
            "name": "api user",
            "description": "api kepada user"
        },
        {
            "name": "api layers",
            "description": "api untuk layers"
        }
    ]
)
templates = Jinja2Templates(directory="app/templates")

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Connect Database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Home page
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/users", response_model=list[schemas.User], tags=["api user"])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.post("/users/", response_model=schemas.User, tags=["api user"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User, tags=["api user"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    selected_user = crud.get_user(db, user_id=user_id)
    return selected_user


@app.put("/users/{user_id}", response_model=schemas.User, tags=["api user"])
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    selected_user = crud.update_user(db, user_id=user_id, user=user)
    if selected_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return selected_user


@app.delete("/users/{user_id}", response_model=schemas.User, tags=["api user"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    selected_user = crud.delete_user(db, user_id=user_id)
    if selected_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return selected_user


# -- Layer API --
@app.get("/layers", response_model=list[schemas.LayerBase], tags=["api layers"])
def read_layers(db: Session = Depends(get_db)):
    return crud.get_layers(db)
