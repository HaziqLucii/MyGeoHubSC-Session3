from fastapi import FastAPI, HTTPException, Depends, Request, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse
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
            "name": "Users API",
            "description": "api kepada user"
        },
        {
            "name": "Layers API",
            "description": "api untuk layers"
        },
        {
            "name": "Security",
            "description": "api untuk Security"
        },
        {
            "name": "Custom HTML",
            "description": "URL bagi segala custom html"
        }
    ]
)

# initiate custom template directory
templates = Jinja2Templates(directory="app/templates")

# initiate tempat token generated
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create database tables
models.Base.metadata.create_all(bind=database.engine)


# Connect Database
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -- FastAPI Security --
@app.post("/token", tags=["Security"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Use a simple token as the user's ID (or any unique attribute)
    access_token = str(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, int(token))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# -- CUSTOM HTML --
# Home page
@app.get("/", response_class=HTMLResponse, tags=["Custom HTML"])
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Login page
@app.get("/login", response_class=HTMLResponse, tags=["Custom HTML"])
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse, tags=["Security"])
async def login(request: Request, db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...)):
    user = crud.authenticate_user(db, username, password)
    if not user:
        error_message = "Incorrect username or password"
        return templates.TemplateResponse("login.html", {"request": request, "error_message": error_message})

    # Here you would typically generate a JWT token or session and redirect to a protected page
    # For this example, we will just redirect to the home page
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value="your_generated_token_here")  # Set your token
    return response

# Logout
@app.get("/logout", tags=["Security"])
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="access_token")
    return response


# -- USERS API --
@app.get("/users", response_model=list[schemas.User], tags=["Users API"])
def read_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.get_users(db)


@app.post("/users/", response_model=schemas.User, tags=["Users API"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User, tags=["Users API"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    selected_user = crud.get_user(db, user_id=user_id)
    return selected_user


@app.put("/users/{user_id}", response_model=schemas.User, tags=["Users API"])
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    selected_user = crud.update_user(db, user_id=user_id, user=user)
    if selected_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return selected_user


@app.delete("/users/{user_id}", response_model=schemas.User, tags=["Users API"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    selected_user = crud.delete_user(db, user_id=user_id)
    if selected_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return selected_user


# -- Layer API --
@app.get("/layers", response_model=list[schemas.LayerBase], tags=["Layers API"])
def read_layers(db: Session = Depends(get_db)):
    return crud.get_layers(db)
