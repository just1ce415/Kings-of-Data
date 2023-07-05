import asyncio
import aiohttp
import os
import csv
import platform

if platform.system() == "Windows":
    DEL = "\\"
else:
    DEL = "/"

DATASET = "test"

async def download_image(session, url, save_path):
    async with session.get(url) as response:
        with open(save_path, 'wb') as file:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                file.write(chunk)

async def download_images(urls):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=6000)) as session:
        tasks = []
        for idx, value in enumerate(urls, start=0):
            if DATASET == "train":
                url1, url2, label = value
                save_path1 = f'data{DEL}{DATASET}{DEL}first{DEL}{idx}_{label}.jpg'
                save_path2 = f'data{DEL}{DATASET}{DEL}second{DEL}{idx}_{label}.jpg'
            else:
                id, url1, url2 = value
                save_path1 = f'data{DEL}{DATASET}{DEL}first{DEL}{id}.jpg'
                save_path2 = f'data{DEL}{DATASET}{DEL}second{DEL}{id}.jpg'
            task1 = asyncio.ensure_future(download_image(session, url1, save_path1))
            task2 = asyncio.ensure_future(download_image(session, url2, save_path2))
            tasks.extend([task1, task2])
        await asyncio.gather(*tasks)

def main(csv_path):
    # Read URLs from CSV
    urls = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if DATASET == "train":
                urls.append((row[0], row[1], row[2]))
            else:
                urls.append((row[0], row[1], row[2]))
    urls.pop(0)

    # Create output directories if they don't exist
    os.makedirs(f'data{DEL}{DATASET}{DEL}first', exist_ok=True)
    os.makedirs(f'data{DEL}{DATASET}{DEL}second', exist_ok=True)

    # Download images asynchronously
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_images(urls))

if __name__ == '__main__':
    main(f"data{DEL}{DATASET}{DEL}{DATASET}.csv")
