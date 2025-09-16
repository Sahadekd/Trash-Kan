from fastapi import APIRouter, Depends, HTTPException, Request
from uuid import UUID

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def get_users(request: Request):
    supabase_client = request.app.state.supabase_client

    try:
        users = supabase_client.table("user").select("*").execute()
        return {"users": users.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase error: {e}")

@router.get("/{user_id}")
async def get_user(request: Request, user_id: UUID):
    supabase_client = request.app.state.supabase_client

    try:
        user = supabase_client.table("user").select("*").eq("id", user_id).single().execute()
        if not user.data:
            raise HTTPException(status_code=404, detail="User not found")
        return user.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supabase error: {e}")