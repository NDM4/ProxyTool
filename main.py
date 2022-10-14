import os
import argparse
import requests
from threading import Lock
from time import time, gmtime, strftime
from multiprocessing.dummy import Pool as ThreadPool


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

http, socks4, socks5 = 0, 0, 0

banner = """{}                              
 _____                 _____         _ 
|  _  |___ ___ _ _ _ _|_   _|___ ___| |
|   __|  _| . |_'_| | | | | | . | . | |
|__|  |_| |___|_,_|_  | |_| |___|___|_|
                  |___|                
                         {}Author{}: {}NDM4

{}""".format(bcolors.OKCYAN, bcolors.UNDERLINE, bcolors.ENDC,bcolors.BOLD, bcolors.ENDC)

def printing(line):
    lock.acquire()
    print(line)
    lock.release()

def save(line, file):
    lock.acquire()
    with open(file, "a+") as f:
        f.write(line + "\n")
    lock.release()

def check(proxy):
    for protocol in ["http", "socks4", "socks5"]:
        try:
            proxies = {
                "http": "{}://{}".format(protocol, proxy),
                "https": "{}://{}".format(protocol, proxy)
            }
            r = requests.post("https://httpbin.org/ip", proxies=proxies, timeout=7)
            printing(f"[{bcolors.WARNING}{protocol.upper()}{bcolors.ENDC}] [{bcolors.OKGREEN}LIVE{bcolors.ENDC}] {proxy}")
            globals()[protocol] += 1 # easy and weird (?) way to do that
            save(proxy, protocol.upper() + ".txt")
            return
        except Exception:
            continue

    printing(f"[{bcolors.FAIL}DEAD{bcolors.ENDC}] {proxy}")

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    parser = argparse.ArgumentParser(description="ProxyTool")
    parser.add_argument('-i', '--input', type=str, help="Input file (proxy list)", required=True)
    parser.add_argument('-t', '--threads', type=int, help="Threads", default=100)

    args = parser.parse_args()

    with open(args.input, "r") as f:
        proxylist = f.read().splitlines()

    lock = Lock()
    start_time = time()
    pool = ThreadPool(processes=args.threads)
    pool.imap_unordered(func=check, iterable=proxylist)
    pool.close()
    pool.join()

    t = strftime("%H:%M:%S", gmtime(time() - start_time))
    print()
    print(f"[{bcolors.OKCYAN}*{bcolors.ENDC}] Checking time: {t}")
    print(f"[{bcolors.OKCYAN}*{bcolors.ENDC}] Speed: {round(len(proxylist) / (time() - start_time), 2)} proxies/s")
    print()
    print(f"[{bcolors.OKCYAN}*{bcolors.ENDC}] HTTP: {http}")
    print(f"[{bcolors.OKCYAN}*{bcolors.ENDC}] SOCKS4: {socks4}")
    print(f"[{bcolors.OKCYAN}*{bcolors.ENDC}] SOCKS5: {socks5}")
