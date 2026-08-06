from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests
import re

app = FastAPI(
    title="TV Player API"
)

# Enable CORS
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

    try:

        response = requests.get(
            page,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0 Safari/537.36"
                )
            },
            timeout=15
        )

        html = response.text

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

    # Find every contentUrl in the page
    matches = re.findall(
        r'"contentUrl"\s*:\s*"((?:https:\\/\\/)[^"]+?index\.m3u8)"',
        html
    )

    if not matches:
        return {
            "success": False,
            "message": "Video URL not found"
        }

    # Use the first match
    video = matches[0].replace("\\/", "/")

    code_match = re.search(
        r"-([a-f0-9]{6})/index\.m3u8$",
        video
    )

    code = code_match.group(1) if code_match else ""

    return {
        "success": True,
        "code": code,
        "url": video
    }
