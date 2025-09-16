from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth, users, sacolas
from api.security import get_current_user, create_access_token
from api.middleware import AuthMiddleware
from api.config import SUPABASE_URL, SUPABASE_KEY, FRONTEND_URL
from dataclasses import dataclass

import requests
from supabase import create_client, Client
from uuid import UUID
from contextlib import asynccontextmanager
from datetime import timedelta


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando API...")
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    app.state.supabase_client = supabase_client
    
    yield
    print("Desligando API...")

app = FastAPI(lifespan=lifespan)


origins = [FRONTEND_URL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(AuthMiddleware)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(sacolas.router)
