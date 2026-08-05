from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests
import re

app = FastAPI(
    title="TV Player API"
)

# Allow requests from any website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "Running"
    }


@app.get("/episode")
def episode(day: str, month: str, year: str):

    page = f"https://thisaitv.com/onna-irukka-kaththukkanum-{day}-{month}-{year}/"

    html = requests.get(
        page,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    ).text

    match = re.search(
        r'"contentUrl":"https:\\/\\/cdn\.tamilnxt\.com\\/videos\\/.*?-([a-f0-9]{6})\\/index\.m3u8"',
        html
    )

    if not match:
        return {
            "success": False,
            "message": "Episode not found"
        }

    code = match.group(1)

    video = f"https://cdn.tamilnxt.com/videos/onna-irukka-kaththukkanum-{day}-{month}-{year}-{code}/index.m3u8"

    return {
        "success": True,
        "code": code,
        "url": video
    }
