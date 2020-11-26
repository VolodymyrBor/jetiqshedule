import io
import zipfile

import requests
from invoke import task, sudo
from yarl import URL

from visitor.drivers import DRIVERS_DIR, CHROMEDRIVER_PATH

CHROME_PLATFORM = 'linux64'
CHROME_VERSION = '86.0.4240.22'
CHROME_DRIVER_URL = URL('https://chromedriver.storage.googleapis.com')

@task
def downland_chrome(_):
    driver_url = CHROME_DRIVER_URL.with_path(CHROME_VERSION) / f'chromedriver_{CHROME_PLATFORM}.zip'
    response = requests.get(str(driver_url))

    buffer = io.BytesIO(response.content)
    with zipfile.ZipFile(buffer) as chrome_zip:
        chrome_zip.extractall(DRIVERS_DIR)

    if CHROME_PLATFORM.startswith('linux'):
        sudo(f'chmod +x {CHROMEDRIVER_PATH}')

    print('Chrome had downloaded.')
