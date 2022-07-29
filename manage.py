import os
import platform
import subprocess
import threading
from time import sleep
import logging

from imagocms.app import create_app

import requests


def ping(host: str) -> bool:
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]

    return subprocess.call(command) == 0


def stay_awake(host) -> None:
    while True:
        logging.debug("stay_awake = sleeping")
        sleep(1620)
        logging.debug("stay_awake = ping")
        if ping(host) is True:
            logging.debug("stay_awake = sending request - done")
        else:
            logging.debug("stay_awake = sending request - something went wrong")


def request(host):
    while True:
        logging.debug("request = sleeping")
        sleep(810)
        logging.debug("request = ping")
        r = requests.get(host)
        r = r.status_code
        if r == 200:
            logging.debug("request = sending request - done")
        else:
            logging.debug("request = sending request - something went wrong")


app = create_app()

if __name__ == "__main__":
    logging.basicConfig(format="%(filename)s: %(message)s", level=logging.DEBUG)
    port = int(os.environ.get("PORT", 5000))
    thread1 = threading.Thread(target=stay_awake, args=["https://imagocms.herokuapp.com/"])
    thread2 = threading.Thread(target=request, args=["http://www.pythonchallenge.com/"])
    threading = [thread1, thread2]

    for i in threading:
        i.start()

    app.run(debug=True, host="0.0.0.0", port=port)
