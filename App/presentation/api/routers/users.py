from fastapi import APIRouter, Depends, HTTPException
from App.presentation.api.deps import get_register_user_handler
from App.application.auth.handlers import RegisterUserHandler
from App.presentation.schemas.users import UserResponse, CreateUserRequest
from App.application.auth.commands import RegisterUserCommand
from typing import Annotated

router = APIRouter(
    prefix="/users",
)

@router.post("/add-user", status_code=201, response_model=UserResponse)
async def get_user_handler(
    request: CreateUserRequest,
    handler: Annotated[RegisterUserHandler, Depends(get_register_user_handler)],
):
    try:
        await handler.handle(cmd=RegisterUserCommand(
            email=request.email,
            password=request.password 
        ))
        return {
            "status": "success",
            "message": "The user has been successfully added!",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to register the user: {str(e)}",
        )