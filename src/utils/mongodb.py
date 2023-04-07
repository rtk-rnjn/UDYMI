from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from flask import Flask
    from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

    MotorDB: TypeAlias = AsyncIOMotorDatabase  # type: ignore
    MotorCollection: TypeAlias = AsyncIOMotorCollection  # type: ignore

from motor.motor_asyncio import AsyncIOMotorClient


class DB:
    def __init__(self, *, flask_app: Flask, mongo_uri: str) -> None:
        self.app = flask_app
        self.mongo = AsyncIOMotorClient(mongo_uri)

    def get_db(self, db_name: str) -> MotorDB:
        return self.mongo[db_name]

    def get_collection(self, db_name: str, collection_name: str) -> MotorCollection:
        return self.mongo[db_name][collection_name]
