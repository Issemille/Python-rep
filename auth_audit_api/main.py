from fastapi import FastAPI, Header, HTTPException, Depends 
from pydantic import BaseModel, validator
from database import conn, cursor, cursor2
from datetime import datetime
from passlib.context import CryptContext 
import sqlite3
import uuid


tokens = {}

def check_auth(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return "You are logged in, Very Nice!"


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class User(BaseModel):
    username: str
    password: str

    @validator("password")
    def password_must_be_short_enough(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long")
        if len(v) < 8:
            raise ValueError("Password too short")
        return v



app = FastAPI()


@app.post("/users")
def create_user(user: User):
    
    password_hash = pwd_context.hash(user.password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (user.username, password_hash, datetime.utcnow().isoformat())
        )
        conn.commit()
        return {"message": "User created successfully"}
    except sqlite3.IntegrityError:
        return {"error": "Username already exists"}
    

@app.get("/people")
def get_people(auth = Depends(check_auth)):
    cursor.execute("SELECT username, created_at FROM users")
    rows = cursor.fetchall()

    users=[]

    for row in rows:
        users.append({"username": row[0], "created_at": row[1]})
    
    return users



@app.post("/login")
def login(user: User):
    
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (user.username,))
    
    row = cursor.fetchone()

    if row is None:
        cursor2.execute("INSERT INTO logs (username, result, timestamp) VALUES (?, ?, ?)", 
                        (user.username, "Failed", datetime.utcnow().isoformat()))
        conn.commit()
        return {"error": "Invalid username or password"}
        
    if not pwd_context.verify(user.password, row[0]):
        cursor2.execute("INSERT INTO logs (username, result, timestamp) VALUES (?, ?, ?)", 
                        (user.username, "Failed", datetime.utcnow().isoformat()))
        conn.commit()
        return {"error": "Invalid username or password"}
        
    

    token = str(uuid.uuid4())
    cursor2.execute("INSERT INTO logs (username, result, timestamp) VALUES (?, ?, ?)", (user.username, "Successful", datetime.utcnow().isoformat()))    
    tokens[token] = user.username
    conn.commit()
    return {"message": "Login successful", "Your very secure and important token": token}




@app.get("/audit")
def get_logs(auth = Depends(check_auth)):
    cursor2.execute("SELECT username, result, timestamp FROM logs")
    rows = cursor2.fetchall()

    logs = []

    for row in rows:
        logs.append({"username": row[0], "result": row[1], "timestamp": row[2]})
    
    return logs


@app.get("/")

def root():
    return{"WHAT": "IS", "GOING": "ON?"}


