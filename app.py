from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

import requests
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", None)
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", None)
APP_DEBUG = os.getenv("APP_DEBUG", "0")


async def index(request):
    body = await request.json()
    print(body)
    try:
        if "it" in body["message"]["text"].lower():
            reply = "Pardon me, what do you mean by 'it' exactly? Please avoid ambiguous words and phrases. Your loving bot friend. Saving you time, and removing the perils of ambiguity ❤️."  # noqa: E501
            requests.get(
                f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={reply}",
                timeout=10,  # noqa: E501
            )
    except KeyError as e:
        print(e)
        print("Ignoring probably non message update")
    return PlainTextResponse("OK")


async def health(request):
    return PlainTextResponse("OK")


routes = [
    Route("/", index, methods=["GET", "POST"]),
    Route("/health", health),
]


if APP_DEBUG == "1" or APP_DEBUG.lower() == "true":
    debug = True
else:
    debug = False

app = Starlette(debug=debug, routes=routes)
