import os
import threading
from time import sleep
import logging

from imagocms.app import create_app

import requests


def stay_awake():
    logging.basicConfig(filename='test.log', format='%(filename)s: %(message)s',
                        level=logging.DEBUG)
    logging.debug('stay_awake = sleeping')
    sleep(1620)
    logging.debug('stay_awake = sending request')
    requests.get("http://imagocms.herokuapp.com/")
    logging.debug('stay_awake = sending request - done')


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
    threading.Thread(target=stay_awake).start()
