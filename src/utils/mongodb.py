from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional, TypeAlias, Union

if TYPE_CHECKING:
    from flask import Flask
    from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

    MotorDB: TypeAlias = AsyncIOMotorDatabase  # type: ignore
    MotorCollection: TypeAlias = AsyncIOMotorCollection  # type: ignore

    from pymongo.results import InsertOneResult, DeleteResult
    from pymongo.typings import _DocumentType as DocumentType

    ReturnData: TypeAlias = DocumentType  # type: ignore
    from flask_bcrypt import Bcrypt

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


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
                    {"email": email},
                ]
            }
        )
        if data:
            return False

        return_data: InsertOneResult = await col.insert_one(
            {"username": username, "email": email, **kwargs}
        )
        if return_data.acknowledged:
            cache_data = {
                "_id": return_data.inserted_id,
                "username": username,
                "email": email,
                **kwargs,
            }
            self.cache[username] = cache_data
            self.cache[email] = cache_data
            self.cache[str(return_data.inserted_id)] = cache_data
            return True

        return True

    async def get_user(self, *, username: str) -> Union[Dict, None]:  # type: ignore
        try:
            return self.cache[username]
        except KeyError:
            col: MotorCollection = self.get_collection("login", "users")
            data: DocumentType = await col.find_one({"username": username})  # type: ignore
            if data:
                self.cache[data["username"]] = data
                self.cache[data["email"]] = data
                self.cache[data["_id"]] = data
                return dict(data)

        return None

    async def get_user_by_id(self, *, _id: str) -> Union[Dict, None]:  # type: ignore
        try:
            return self.cache[_id]
        except KeyError:
            col: MotorCollection = self.get_collection("login", "users")
            data: DocumentType = await col.find_one({"_id": ObjectId(_id)})  # type: ignore
            if data:
                self.cache[data["username"]] = data
                self.cache[data["email"]] = data
                self.cache[data["_id"]] = data
                return dict(data)

        return None

    async def get_user_by_email(self, *, email: str) -> Union[Dict, None]:  # type: ignore
        try:
            return self.cache[email]
        except KeyError:
            col: MotorCollection = self.get_collection("login", "users")
            data: DocumentType = await col.find_one({"email": email})  # type: ignore
            if data:
                self.cache[data["username"]] = data
                self.cache[data["email"]] = data
                self.cache[data["_id"]] = data
                return dict(data)

        return None

    async def verify_password(self, *, username_or_email: str, password: str) -> bool:
        user = (await self.get_user(username=username_or_email)) or (
            await self.get_user_by_email(email=username_or_email)
        )
        return (
            self.bcrypt.check_password_hash(user["password"], password)
            if user
            else False
        )

    async def delete_user(self, *, username_or_email: str) -> bool:
        data: DeleteResult = await self.mongo.login.users.delete_one(
            {"$or": [{"username": username_or_email}, {"email": username_or_email}]}
        )

        if data.deleted_count:
            self._delete_from_cache(username_or_email=username_or_email)
            return True

        return False

    def _check_username_or_email(self, *, username_or_email: str) -> Optional[str]:
        data = self.cache[username_or_email]
        if data["email"] == username_or_email:
            return "email"
        if data["username"] == username_or_email:
            return "username"

    def _delete_from_cache(self, *, username_or_email: str) -> None:
        data = self.cache[username_or_email]
        del self.cache[data["username"]]
        del self.cache[data["email"]]
