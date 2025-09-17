# Configurações compartilhadas
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL","")
SUPABASE_KEY = os.getenv("SUPABASE_KEY","")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID","")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET","")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY","")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

FRONTEND_URL = os.getenv("FRONTEND_URL","http://localhost:8081")

API_URL = os.getenv("API_URL")

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)