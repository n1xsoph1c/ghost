import asyncio
import logging
import os
import random
import requests
import time
from concurrent.futures import ThreadPoolExecutor

websites = {"test": "http://koncept-tech.com", "mine": "http://gamisticstudio.com"}

async def download_homepage(site_name, url):
    try:
        logging.info(f"[!] Downloading homepage of {site_name}: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "websites", f"{site_name}.html")
        
        with open(file_path, "wb") as f:
            f.write(response.content)
        
        logging.info(f"[!] Downloaded homepage of {site_name} to {file_path}")
    except Exception as e:
        logging.error(f"[x] Failed to download homepage of {site_name}: {e}")

async def delete_homepage(site_name):
    try:
        logging.info(f"[!] Deleting homepage of {site_name}")
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "websites", f"{site_name}.html")
        os.remove(file_path)
        logging.info(f"[!] Deleted homepage of {site_name}")
    except Exception as e:
        logging.error(f"[x] Failed to delete homepage of {site_name}: {e}")

async def handle_site(site_name, url):
    try:
        await download_homepage(site_name, url)
        await delete_homepage(site_name)
        logging.info(f"[+] Successfully completed tasks for {site_name}")
    except Exception as e:
        logging.error(f"[x] Failed to process {site_name}: {e}")

def run_asyncio_tasks(site_name, url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(handle_site(site_name, url))
    finally:
        loop.close()

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    num_threads = len(websites)
    logging.info(f"[!] Using {num_threads} threads!\n")

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        while True:
            futures = []
            for site_name, url in websites.items():
                futures.append(executor.submit(run_asyncio_tasks, site_name, url))

            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"[x] Thread execution failed: {e}")

            rand_sleep = random.randint(1, 2)
            logging.info(f"\n[!] All tasks done! Restarting in {rand_sleep} seconds...\n")
            time.sleep(rand_sleep)

if __name__ == "__main__":
    main()
