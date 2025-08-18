from fastapi import FastAPI
from c14_ping.api.api_router import api_router

app = FastAPI(
    title='Ping do Pong'
)

app.include_router(api_router)
