from unicodedata import name
from fastapi import FastAPI, Depends, Request, Form, status

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    items = db.query(models.Inventory).all()
    return templates.TemplateResponse("base.html",
                                      {"request": request, "item_list": items})

@app.post("/add")
def add(request: Request, title: str = Form(...), quantity: int = Form(...), db: Session = Depends(get_db)):
    new_invetory = models.Inventory(name=title, quantity=quantity)
    db.add(new_invetory)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/update/{item_id}")
def update(request: Request, item_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Inventory).filter(models.Inventory.id == item_id).first()
    todo.complete = not todo.complete
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.get("/delete/{item_id}")
def delete(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Inventory).filter(models.Inventory.id == item_id).first()
    db.delete(item)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)