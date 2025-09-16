from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from api.security import get_current_user

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")

        if token:
            user = get_current_user(authorization=token)
            if user:
                request.state.user = user
            else:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        response = await call_next(request)
        return response