import random
import asyncio
from aiohttp import ClientSession

proxies = []

with open('proxies.txt') as f:
    proxies = f.read().splitlines()

async def fetch(url, session, i):
    try:
        async with session.get(url, proxy="http://"+proxies[i % 496]) as response:
            print(str(i) + ": " + str(response.status))
            return await response.read()
    except:
        print("fuck")

async def bound_fetch(sem, url, session, proxy):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session, proxy)


async def run(r):
    url = ""
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for i in range(r):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session, i))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

number = 2000
loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(number))
loop.run_until_complete(future)
