from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Question(BaseModel):
    id: str
    question: Optional[str] = ""

@app.get("/echo/")
async def get_echo(id: str = '0', q: str = ""):
    return {"id": id, "answer": q}

@app.post("/echo/")
async def post_echo(q: Question):
    return {"id": q['id'], "answer": q['question']}