import os
import json
from replit import db
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List
import httpx
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import uuid
import asyncio
import datetime
import uvicorn
import time
from datetime import datetime

dt = datetime.strptime('2019-12-04T10:20:30.400', '%Y-%m-%dT%H:%M:%S.%f')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api_key_header = APIKeyHeader(name="Authorization", scheme_name="Bearer")

MANTON_MODEL_NAMES = {
    "gpt-3.5-turbo-1106": "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo" : "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613" : "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-0301" : "gpt-3.5-turbo-0301",
}

def verify_nyx_api_key(thothaiapikey):
    target_thothkey = thothaiapikey.replace("Bearer ", "")
    if os.environ['MASTER_KEY'] in target_thothkey:
        return True
    found_item = find_api_key(target_thothkey)

    if found_item:
        reset_time = datetime.fromisoformat(found_item["reset_time"])
        if found_item["requests"] >= 600 and datetime.now() - reset_time < timedelta(days=1):
            return False
        else:
            if datetime.now() - reset_time >= timedelta(days=1):
                found_item["requests"] = 0
                found_item["reset_time"] = datetime.now().isoformat()
                db[key] = found_item
            return True
    else:
        return False

def find_api_key(target_thothkey):
    for key, item in db.items():
        if "nyxkey" in item and item["nyxkey"] == target_thothkey:
            return item
    return None

def generate_nyx_api_key(key, discord_id):
    newkeydata = {
        "nyxkey": key,
        "requests": 0,
        "reset_time": str(datetime.now().isoformat())
    }
    db[discord_id] = newkeydata

class Message(BaseModel):
    role: str
    content: str

class RequestBody(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: int = 4097
    temperature: float = 0.7
    stream: bool = False

async def process_manton_completions(body: RequestBody):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("OPEN_AI_KEY")}'
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(url, headers=headers, json=body.dict())
        if body.stream:
            async for chunk in resp.aiter_bytes():
                yield chunk
        elif resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        else:
            yield resp.content

@app.get("/")
def read_root():
    return {"Heyyy!": "Welcome to NyX AI! Join our Discord server: https://discord.com/invite/9bqRWAP74f"}

@app.post("/openai/chat/completions")
async def get_completions(body: RequestBody, key: str = Depends(api_key_header)):
    if not verify_nyx_api_key(key):
        raise HTTPException(status_code=401, detail="Invalid API key or daily limit reached")
    target_thothkey = key.replace("Bearer ", "")
    found_item = find_api_key(target_thothkey)

    if found_item:
        found_item["requests"] += 5
        db[key] = found_item

    manton_model_name = MANTON_MODEL_NAMES.get(body.model)
    if manton_model_name:
        body.model = manton_model_name
        if body.stream:
            return StreamingResponse(process_manton_completions(body), media_type="text/event-stream")
        else:
            async for chunk in process_manton_completions(body):
                return json.loads(chunk)
    else:
        raise HTTPException(status_code=400, detail="Invalid model name")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
