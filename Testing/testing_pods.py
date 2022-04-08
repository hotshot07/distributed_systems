import requests 
import time 
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import random 

username = '91915068467'
password = '535f61b0'

def get_token(i):
    start = time.time()
    response = requests.post('http://20.224.88.180:3000/login', auth=(username, password))
    end = time.time() - start
    print(response.status_code, end)
    return (response.status_code, end)
    
def http_get_with_requests_parallel():
    results = []
    executor = ThreadPoolExecutor(max_workers=1000)
    for result in executor.map(get_token, range(100000)) :
        results.append(result)
    return Counter([x[0] for x in results]) , [x[1] for x in results]



if __name__  == '__main__':
    results, t = http_get_with_requests_parallel()
    print(results)
    print(f"Min time:{min(t)}")
    print(f"Max time:{max(t)}")
    print(f"Avg time:{sum(t)/len(t)}")
    print(f"Median time: {sorted(t)[len(t)//2]}")









# import aiohttp
# import asyncio
# from aiohttp import BasicAuth

# async def main():

#     async with aiohttp.ClientSession() as session:
#         async with session.post('http://20.224.88.180:3000/login/', auth=BasicAuth(username,password)) as response:

#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])

#             html = await response.text()
#             print(html)

# loop = asyncio.get_event_loop()

# loop.run_until_complete(main())



# for x in range(100000):
#     response = requests.post("", auth=(username, password))
#     print(response.status_code)
#     print(response.cookies)
    