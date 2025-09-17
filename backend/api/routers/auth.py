from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from api.security import get_current_user, create_access_token
from api.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, FRONTEND_URL, API_URL
from oauthlib.oauth2 import WebApplicationClient
import requests

router = APIRouter(prefix="/auth", tags=["auth"])

from dataclasses import dataclass

@dataclass
class GoogleHosts:
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    certs: str

oauth = WebApplicationClient(GOOGLE_CLIENT_ID)

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

@router.get("/login")
async def login(request: Request, redirect_url: str | None = None):
    hosts = get_google_oauth_hosts()
    
    if not redirect_url:
        redirect_url = f"{FRONTEND_URL}/auth-callback"
    

    google_redirect_uri = f"{API_URL}/auth/callback"
    
    # Debug logs
    print(f"API_URL: {API_URL}")
    print(f"FRONTEND_URL: {FRONTEND_URL}")
    print(f"redirect_url (frontend): {redirect_url}")
    print(f"google_redirect_uri: {google_redirect_uri}")
    
    redirect_uri = oauth.prepare_authorization_request(
        authorization_url=hosts.authorization_endpoint,
        redirect_url=google_redirect_uri,
        scope=["openid", "email", "profile"],
        state=redirect_url  # Passamos a redirect_url do frontend como state
    )
    return {"auth_url": redirect_uri}

@router.get("/callback")
async def callback(request: Request, code: str, state: str | None = None):
    hosts = get_google_oauth_hosts()
    
    google_redirect_uri = f"{API_URL}/auth/callback"
    
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': google_redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    print("Fazendo requisição para obter tokens...")
    try:
        token_res = requests.post(hosts.token_endpoint, data=token_data)
        token_res.raise_for_status()
        print("Token obtido com sucesso!")
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
            
            # Usar a redirect_url do state se fornecida, senão usar o padrão
            if state and state.startswith(('http://', 'https://', 'trashkan://', 'exp://')):
                frontend_callback_url = f"{state}?token={access_token}"
            else:
                frontend_callback_url = f"{FRONTEND_URL}/auth-callback?token={access_token}"
            
            print(f"Redirecionando para: {frontend_callback_url}")    
            return RedirectResponse(url=frontend_callback_url)
                    
        except Exception as supabase_error:
            print(f"Supabase user creation error: {supabase_error}")
        
        if state and state.startswith(('http://', 'https://', 'trashkan://')):
            error_url = f"{state}?error=supabase_error"
        else:
            error_url = f"{FRONTEND_URL}/auth-callback?error=supabase_error"
        
        return RedirectResponse(url=error_url)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f'Erro no fluxo OAuth: {e}')