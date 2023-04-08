from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, TypeAlias, Union

if TYPE_CHECKING:
    from flask import Flask
    from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

    MotorDB: TypeAlias = AsyncIOMotorDatabase  # type: ignore
    MotorCollection: TypeAlias = AsyncIOMotorCollection  # type: ignore

    from pymongo.results import InsertOneResult
    from pymongo.typings import _DocumentType as DocumentType

    ReturnData: TypeAlias = DocumentType  # type: ignore
    from flask_bcrypt import Bcrypt

from motor.motor_asyncio import AsyncIOMotorClient


class DB:
    def __init__(self, *, flask_app: Flask, mongo_uri: str, bcrypt: Bcrypt) -> None:
        self.app = flask_app
        self.mongo = AsyncIOMotorClient(mongo_uri)
        self.bcrypt = bcrypt

        from src.utils import Cache  # Imagine having circular imports

        self.cache: "Dict[Any, Any]" = Cache()

    def get_db(self, db_name: str) -> MotorDB:
        return self.mongo[db_name]

    def get_collection(self, db_name: str, collection_name: str) -> MotorCollection:
        return self.mongo[db_name][collection_name]

    async def register_user(self, *, username: str, email: str, **kwargs: Any) -> bool:
        col: MotorCollection = self.get_collection("login", "users")

        if username in self.cache or email in self.cache:
            return False

        data: DocumentType = await col.find_one(  # type: ignore
            {
                "$or": [
                    {"username": username},
                    # {"email": email},
                ]
            }
        )
        if data:
            return False

        return_data: InsertOneResult = await col.insert_one(
            {"username": username, "email": email, **kwargs}
        )
        if return_data.acknowledged:
            self.cache[username] = {
                "_id": return_data.inserted_id,
                "username": username,
                "email": email,
                **kwargs,
            }
            # self.cache[email] = {"username": username, "email": email, **kwargs}
            return True

        return True

    async def get_user(self, *, username: str) -> Union[Dict, DocumentType]:  # type: ignore
        try:
            return self.cache[username]
        except KeyError:
            col: MotorCollection = self.get_collection("login", "users")
            return await col.find_one({"username": username})

    # async def get_user_by_email(self, *, email: str) -> Any:
    #     try:
    #         return self.cache[email]
    #     except KeyError:
    #         col: MotorCollection = self.get_collection("login", "users")
    #         return await col.find_one({"email": email})

    async def verify_password(self, *, username: str, password: str) -> bool:
        user = await self.get_user(username=username)
        return (
            self.bcrypt.check_password_hash(user["password"], password)
            if user
            else False
        )
