from typing import Annotated, Optional, List
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
import motor.motor_asyncio
import os

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://nwillett:NWillett1234@serverlessinstance0.xveiv.mongodb.net/")

db = client.ITAD3602025
user_collection = db.get_collection("nwillett")

# Represent and ObjectId field in the database.
# It will be represented as a 'str' on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class User(BaseModel):
    """
    Container for a single user record.
    """
    
    # The primary key for the User model, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: EmailStr
    signup_date: datetime


@app.post("/register")
async def register_user(user: User):
    try:
        result = await user_collection.insert_one(user.dict())
        return {
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
