from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..db import users
from passlib.hash import bcrypt

router = APIRouter()

class Signup(BaseModel):
    email: str
    name: str
    password: str

@router.post("/signup")
async def signup(payload: Signup):
    exists = await users.find_one({"email": payload.email})
    if exists:
        raise HTTPException(status_code=400, detail="User exists")
    user = {
        "email": payload.email,
        "name": payload.name,
        "password": bcrypt.hash(payload.password)
    }
    res = await users.insert_one(user)
    user["_id"] = str(res.inserted_id)
    user.pop("password")
    return {"user": user}