import hmac
import hashlib
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Header
from jose import JWTError, jwt
from api.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, get_supabase_client

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        email: Optional[str] = payload.get("email")
        if user_id is None or email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"user_id": user_id, "email": email, "payload": payload}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

async def get_current_user(authorization: str):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    token = authorization.split(" ")[1]
    
    try:
        token_data = verify_token(token)
        
        supabase = get_supabase_client()
        user = supabase.table("user").select("*").eq("id", token_data["user_id"]).execute()
        
        if not user.data:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        print(user.data)
        return user.data[0] 
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erro na autenticação: {str(e)}")


def gerar_codigo_verificador(token_len=6, assinatura_len=4):
    """
    Gera um código verificador curto e amigável: TOKEN-ASSINATURA
    TOKEN: 6 caracteres alfanuméricos
    ASSINATURA: 4 caracteres base32
    """
    alfabeto = string.ascii_uppercase + string.digits
    token = ''.join(secrets.choice(alfabeto) for _ in range(token_len))
    assinatura_bytes = hmac.new(JWT_SECRET_KEY.encode(), token.encode(), hashlib.sha256).digest()
    assinatura_b32 = hashlib.sha1(assinatura_bytes).digest().hex().upper()[:assinatura_len]
    return f"{token}-{assinatura_b32}"

def validar_codigo_verificador(codigo):
    """
    Valida o código verificador no formato TOKEN-ASSINATURA
    """
    try:
        token, assinatura = codigo.split("-")
        assinatura_bytes = hmac.new(JWT_SECRET_KEY.encode(), token.encode(), hashlib.sha256).digest()
        assinatura_esperada = hashlib.sha1(assinatura_bytes).digest().hex().upper()[:len(assinatura)]
        return hmac.compare_digest(assinatura, assinatura_esperada)
    except Exception:
        return False

