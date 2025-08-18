import asyncio
from time import sleep
from fastapi import APIRouter, status
import httpx


from c14_ping.schemas.ping_response import PingResponse

router = APIRouter(prefix='/ping')


@router.get('', response_model=PingResponse, status_code=status.HTTP_200_OK)
async def ping():
    print("Pingou!")

    async def fire_and_forget():
        async with httpx.AsyncClient() as client:
            try:
                await client.get("http://192.168.209.219:3000/pong")
            except Exception as e:
                print("Erro na chamada fire-and-forget:", e)

    # dispara a tarefa e não espera o resultado
    asyncio.create_task(fire_and_forget())

    return PingResponse()
