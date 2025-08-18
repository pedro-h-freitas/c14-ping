import asyncio
from time import sleep
from fastapi import APIRouter, status
import httpx


from c14_ping.schemas.ping_response import PingResponse

router = APIRouter(prefix='/ping')

global count_var
count_var = 0


@router.get('', response_model=PingResponse, status_code=status.HTTP_200_OK)
async def ping():

    print("Foi pingado!")

    global count_var
    count_var += 1

    async def fire_and_forget():
        async with httpx.AsyncClient() as client:
            try:
                await client.get("http://192.168.209.154:3000/pong")
            except Exception as e:
                print("Erro na chamada fire-and-forget:", e)

    # dispara a tarefa e não espera o resultado
    asyncio.create_task(fire_and_forget())

    return PingResponse()


@router.get('/count', status_code=status.HTTP_200_OK)
def count():
    global count_var
    return count_var
