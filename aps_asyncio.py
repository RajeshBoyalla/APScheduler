from aiohttp import ClientSession, ClientResponseError
import asyncio
import logging
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler


logging.getLogger().setLevel(logging.INFO)


async def fetch(session, url):
    try:
        async with session.get(url, timeout=15) as response:
            resp = await response.read()
    except ClientResponseError as e:
        logging.warning(e.code)
    except asyncio.TimeoutError:
        logging.warning('Timeout')
    except Exception as e:
        logging.warning(e)
    else:
        return resp
    return


async def job():

    # list of sample endpoints to query 
    urls = [
        'http://ip.jsontest.com/',
        'http://headers.jsontest.com/',
        'http://date.jsontest.com',
        'http://echo.jsontest.com/insert-key-here/insert-value-here/key/value',
        'http://validate.jsontest.com/?json=[JSON-code-to-validate]',
        'http://code.jsontest.com',
        'http://cookie.jsontest.com/',
        'http://ip.jsontest.com/?callback=showIP',
    ]
    tasks = []
    # try to use one client session
    async with ClientSession() as session:
       
        for each in urls:
            task = asyncio.ensure_future(fetch(session, each))
            tasks.append(task)
        # await response outside the for loop
        responses = await asyncio.gather(*tasks)
    logging.info(responses)
    # Call a method that inserts reponses into a database table that will be read by django
    # or return responses for further processing


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, 'interval', seconds=30)
    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass