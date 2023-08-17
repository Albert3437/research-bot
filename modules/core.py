from modules.logger import logger
from modules.config import *
import asyncio
import aiohttp
from second_part import run as second_run

async def send_request(port):
    port += 5000
    url = f"http://localhost:{port}/receive"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            return await response.text()


async def finaly_code():
    loop = asyncio.get_event_loop()

    # Выполнение неасинхронной функции в отдельном потоке
    await loop.run_in_executor(None, second_run)


async def start():
    respons_list = []
    
    tasks = [send_request(port) for port in range(1, len(TOKEN_LIST)+1)]
    responses = await asyncio.gather(*tasks)
    
    for i, response in enumerate(responses, start=1):
        respons_list.append(i)

    if len(respons_list) == len(TOKEN_LIST):
        await finaly_code()