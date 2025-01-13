from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from src.services.auth_service import AuthService
from src.utils.db import get_async_session # get_db_connection #get_db
from src.utils.enums import Action
from pydantic import BaseModel, Field
from humps import camelize


router = APIRouter()


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        populate_by_name = True


class CheckPermissionsRequest(CamelModel):
    token: str
    required_action: str
    targer_action: str
    query: Optional[str] = None


class LoginRequest(CamelModel):
    username: str
    password: str

class UpdatePassword(CamelModel):
    username: str
    session: str
    new_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "session": "your-session-string",
                "newPassword": "your-new-password"
            }
        }

class LoginResponse(CamelModel):
    access_token: str
    id_token: str
    refresh_token: str

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db=Depends(get_async_session)):
    try:
        auth_service  = AuthService(db)
        result = auth_service.login(request.username, request.password)
        return LoginResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/update-password")
async def login(request: UpdatePassword, db=Depends(get_async_session)):
    try:
        auth_service  = AuthService(db)
        result = await auth_service.update_pasword(request.username, request.session, request.new_password)
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/authorize")
async def check_permissions(request: CheckPermissionsRequest, db=Depends(get_async_session)):
    if request.required_action == Action.QUERY.value and request.query is None:
        raise HTTPException(status_code=400, detail="Query parameter is required for 'query' action")

    auth_service = AuthService(db)
    user_id = auth_service.verify_token(request.token)
    if auth_service.check_permissions(user_id, request.required_action, request.targer_action, request.query):
        return {"message": "Permission granted"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")

def setup_routes(app):
    app.include_router(router, tags=["auth"]) #prefix="/auth",