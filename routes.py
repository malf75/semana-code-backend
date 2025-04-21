import uvicorn
import os
from setup.settings import app
from fastapi.responses import RedirectResponse
from fastapi import Depends
from sqlmodel import Session, SQLModel
from database.database import get_db, engine
from typing import Annotated

db = Annotated[Session, Depends(get_db)]
SQLModel.metadata.create_all(engine)

@app.get("/")
def redirect_index():
    return RedirectResponse("/docs")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
