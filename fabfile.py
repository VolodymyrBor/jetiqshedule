import io
import logging
import zipfile
from pathlib import Path

import requests
from yarl import URL
from invoke import sudo
from fabric import task, Connection

from configs import CONFIG_DIR
from visitor.drivers import DRIVERS_DIR, CHROMEDRIVER_PATH


CHROME_PLATFORM = 'linux64'
CHROME_VERSION = '86.0.4240.22'
CHROME_DRIVER_URL = URL('https://chromedriver.storage.googleapis.com')

HOST = 'jetiq'
CONFIG_FILENAME = 'prod.yaml'

TMP_DIR = Path('/tmp/')
ROOT_REMOTE = Path('/home/jetiq/jetiq-sheduler')
CONFIG_DIR_REMOTE = ROOT_REMOTE / 'configs'
REMOTE_CONFIG_FILE = CONFIG_DIR_REMOTE / 'new.yaml'
LOCAl_CONFIG_FILE = CONFIG_DIR / CONFIG_FILENAME
CONF_IN_TMP = TMP_DIR / CONFIG_FILENAME

logging.basicConfig(level='INFO')
log = logging.getLogger('fab')


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


@task()
def upload_config(_):
    if not LOCAl_CONFIG_FILE.exists():
        raise FileNotFoundError(f'Config file: {LOCAl_CONFIG_FILE} not found.')

    with Connection(host=HOST, user='ubuntu') as conn:
        conn.put(str(LOCAl_CONFIG_FILE), str(REMOTE_CONFIG_FILE))
