import os
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(override=True)
app = FastAPI()

DATABASE_URL = str(os.getenv('DATABASE_URL'))

origins = [
    str(os.getenv('APP_URL')),
    str(os.getenv('DEV_URL'))
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)