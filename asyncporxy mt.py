import random
import asyncio
from aiohttp import ClientSession
import threading

proxies = []

with open('proxies.txt') as f:
    proxies = f.read().splitlines()

async def fetch(url, session, i):
    try:
        async with session.get(url, proxy="http://"+proxies[i % 496]) as response:
            if response.status == 200:
                print(str(i) + ": " + str(response.status))
            elif response.status == 500:
                print(str(i) + ": " + "BIG HECK")
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


def worker():
    number = 2000
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(run(number))
    loop.run_until_complete(future)
    return


threads = []
for i in range(20):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
