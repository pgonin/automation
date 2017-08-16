#!/usr/bin/env python
try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
except ImportError:
    print("Please install python-requests")
    raise SystemExit(1)
import argparse
import time

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# This assumes we'll never need a proxy to reach velum..
PROXIES = {
  "http": None,
  "https": None,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Wait for velum to start')
    parser.add_argument('url', metavar='url', help='URL of dashboard')
    parser.add_argument('--timeout', help='Max time to wait for Velum to start, defaults to 10min', default=10, type=int)
    args = parser.parse_args()

    counter = 1

    timeout = time.time() + args.timeout * 60

    while True:
        counter += 1
        if time.time() > timeout:
            print("Timed out waiting for Velum to start")
            raise SystemExit(1)
        try:
            r = requests.get(args.url, verify=False, proxies=PROXIES)
        except requests.exceptions.ConnectionError:
            if counter%5 == 0:
                print("Waiting for Velum to start")
            time.sleep(10)
            continue
        if 'Log In' in r.text:
            print("Velum started!")
            break
        else:
            if counter%5 == 0:
                print("Waiting for Velum to initialize")
                time.sleep(10)
