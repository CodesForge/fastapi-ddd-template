from fastapi import APIRouter, Depends, HTTPException
from App.presentation.api.deps import get_register_user_handler, get_user_repository
from App.application.auth.handlers import RegisterUserHandler
from App.infrastructure.db.repositories.user_repository import SQLAlchemyUserRepository
from App.presentation.schemas.users import UserResponse, CreateUserRequest, GetUserByEmail, GetUserByEmailResponse, GetUserByid, UserModel
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
        ), queue="testing_queue")
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

@router.post("/get-user-by-email", status_code=201, response_model=GetUserByEmailResponse)
async def get_user_by_email_handler(
    request: GetUserByEmail,
    user_repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
):
    try:
        user = await user_repository.get_user_by_email(
            request.email
        )
        return {
            "status": "success",
            "message": "The user has been successfully found!",
            "user": UserModel(
                id=user.id,
                email=user.email.value,
                password_hash=user.password_hash.value,
                is_active=user.is_active,
                created_at=user.created_at,
            )
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in user search: {str(e)}",
        )

@router.post("/get-user-by-id", status_code=201, response_model=GetUserByEmailResponse)
async def get_user_by_email_handler(
    request: GetUserByid,
    user_repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
):
    try:
        user = await user_repository.get_user_by_id(
            request.id,
        )
        return {
            "status": "success",
            "message": "The user has been successfully found!",
            "user": UserModel(
                id=user.id,
                email=user.email.value,
                password_hash=user.password_hash.value,
                is_active=user.is_active,
                created_at=user.created_at,
            )
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in user search: {str(e)}",
        )
        