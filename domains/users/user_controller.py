from fastapi import Depends, status
from sqlalchemy.orm import Session
from config.database.db import get_db
from common.base.baseController import BaseController
from domains.users.user_service import UserService
from domains.users.dto.user_dto import CreateUserDTO, UpdateUserDTO


# Cukup passing prefix dan tags di sini, BaseController yang akan membuat routernya!
class UserController(BaseController, prefix="/users", tags=["Users"]):
    _user_service = UserService()

    @classmethod
    def register_routes(cls):
        @cls.router.get("/", status_code=status.HTTP_200_OK)
        def get_all(db: Session = Depends(get_db)):
            try:
                users = cls._user_service.get_all_users(db)
                return cls.handle_success(
                    data=users, message="Users retrieved successfully"
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.post("/", status_code=status.HTTP_201_CREATED)
        def create(user_data: CreateUserDTO, db: Session = Depends(get_db)):
            try:
                user = cls._user_service.create_user(db, user_data)
                return cls.handle_success(
                    data=user,
                    message="User created successfully",
                    status_code=status.HTTP_201_CREATED,
                )
            except ValueError as error:
                cls.handle_error(
                    detail=str(error), status_code=status.HTTP_400_BAD_REQUEST
                )
            except Exception as error:
                cls.handle_error(detail=str(error))

        @cls.router.put("/{user_id}", status_code=status.HTTP_200_OK)
        def update_user(
            user_id: str, update_data: UpdateUserDTO, db: Session = Depends(get_db)
        ):
            try:
                user = cls._user_service.update_user(db, user_id, update_data)
                if not user:
                    cls.handle_error(
                        detail=f"User with id {user_id} not found",
                        status_code=status.HTTP_404_NOT_FOUND,
                    )
                return cls.handle_success(
                    data=user, message="User updated successfully"
                )
            except ValueError as error:
                cls.handle_error(
                    detail=str(error), status_code=status.HTTP_400_BAD_REQUEST
                )
            except Exception as error:
                cls.handle_error(detail=str(error))


UserController.register_routes()
