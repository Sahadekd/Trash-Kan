from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from api.security import get_current_user, create_access_token
from api.config import get_supabase_client, SUPABASE_URL, SUPABASE_KEY,GOOGLE_CLIENT_ID,GOOGLE_CLIENT_SECRET
from dataclasses import dataclass
from oauthlib.oauth2 import WebApplicationClient
import requests
from supabase import create_client, Client
from uuid import UUID
from contextlib import asynccontextmanager
from datetime import timedelta


oauth = WebApplicationClient(GOOGLE_CLIENT_ID)

@dataclass
class GoogleHosts:
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    certs: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    app.state.supabase_client = supabase_client
    
    yield
    

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_google_oauth_hosts() -> GoogleHosts:
    try:
        hosts = requests.get("https://accounts.google.com/.well-known/openid-configuration")
        hosts.raise_for_status()
        data = hosts.json()
        return GoogleHosts(
            authorization_endpoint=data.get("authorization_endpoint"),
            token_endpoint=data.get("token_endpoint"),
            userinfo_endpoint=data.get("userinfo_endpoint"),
            certs=data.get("jwks_uri")
        )
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch Google OAuth configuration: {e}")

@app.get("/auth/login")
async def login():
    hosts = get_google_oauth_hosts()
    redirect_uri = oauth.prepare_authorization_request(
        authorization_url=hosts.authorization_endpoint,
        redirect_url="http://localhost:8000/auth/callback",
        scope=["openid", "email", "profile"]
    )
    return {"auth_url": redirect_uri}

@app.get("/auth/callback")
async def callback(request: Request, code: str):
    hosts = get_google_oauth_hosts()
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': 'http://localhost:8000/auth/callback',
        'grant_type': 'authorization_code'
    }
    try:
        token_res = requests.post(hosts.token_endpoint, data=token_data)
        token_res.raise_for_status()
        tokens = token_res.json()
        access_token = tokens.get('access_token')
        if not access_token:
            raise HTTPException(status_code=400, detail='Token de acesso não recebido.')
        userinfo_res = requests.get(
            hosts.userinfo_endpoint,
            headers={'Authorization': f'Bearer {access_token}'}
        )
        userinfo_res.raise_for_status()
        userinfo = userinfo_res.json()
        
        try:
            user_email = userinfo.get('email')
            user_name = userinfo.get('name')
            google_id = userinfo.get('sub')
            
            supabase_client = request.app.state.supabase_client

            existing_user = supabase_client.table("user").select("*").eq("email", user_email).execute()
            
            if not existing_user.data:
                user_data = supabase_client.table("user").insert({
                    "email": user_email,
                    "username": user_name,
                    "google_id": google_id
                }).execute()
                user_id = user_data.data[0]["id"]
            else:
                user_id = existing_user.data[0]["id"]
                
            access_token = create_access_token(
                data={"sub": str(user_id), "email": user_email}
            )
            
            return {"access_token": access_token, "token_type": "bearer"}
                    
        except Exception as supabase_error:
            print(f"Supabase user creation error: {supabase_error}")
        
        return RedirectResponse(url="http://localhost:5500/welcome")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f'Erro no fluxo OAuth: {e}')

@app.get("/user")
async def get_users(request: Request):
    supabase_client = request.app.state.supabase_client

    try:
        users = supabase_client.table("user").select("*").execute()
        return {"users": users.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase error: {e}")
    
@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: UUID):
    supabase_client = request.app.state.supabase_client

    try:
        user = supabase_client.table("user").select("*").eq("id", user_id).single().execute()
        if not user.data:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user": user.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase error: {e}")

from pydantic import BaseModel


@app.post("/sacola")
async def create_sacola(request: Request, cod_identificador: str):
    supabase_client = request.app.state.supabase_client
    current_user = request.state.user
    try:
        new_sacola = supabase_client.table("sacola").insert({
            "user_id": current_user.get("id"),
            "codigo_identificador": cod_identificador
        }).execute()
        return {"sacola": new_sacola.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase error: {e}")
    
@app.post("/sacola/{sacola_id}/descartar")
async def discard_sacola(request: Request, sacola_id: UUID):
    supabase_client = request.app.state.supabase_client
    
    try:
        supabase_client.table("sacola").update({"status": "descartada"}).eq("id", sacola_id).execute()
        return {"detail": "Sacola descartada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase error: {e}")