from fastapi import APIRouter, Depends, HTTPException, Request
from uuid import UUID

router = APIRouter(prefix="/sacola", tags=["sacola"])

@router.post("/")
async def create_sacola(request: Request, cod_identificador: str):
    supabase_client = request.app.state.supabase_client
    current_user = request.state.user
    try:
        new_sacola = supabase_client.table("sacola").insert({
            "user_id": current_user.get("id"),
            "codigo_identificador": cod_identificador
        }).execute()
        return new_sacola.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase error: {e}")
    
@router.post("/sacola/{sacola_id}/descartar")
async def discard_sacola(request: Request, sacola_id: UUID):
    supabase_client = request.app.state.supabase_client
    
    try:
        supabase_client.table("sacola").update({"status": "descartada"}).eq("id", sacola_id).execute()
        return {"detail": "Sacola descartada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase error: {e}")