from pathlib import Path

import yaml

from .schmes import Config, BaseConfig, FastAPI, Scheduler, MySQLConfig


CONFIG_DIR = Path(__file__).parent
BASE_CONFIG = CONFIG_DIR / 'base.yaml'
MYSQL_CONFIG_FILE = CONFIG_DIR / 'mysql.yaml'


def get_config(config_path=None) -> BaseConfig:
    base_config = BaseConfig(**yaml.safe_load(BASE_CONFIG.read_text()))

    if config_path is None:
        return base_config

    if not config_path:
        raise ValueError(f'Bad config path: {config_path!r}')

    config_path = Path(config_path).with_suffix('.yaml')
    if not config_path.is_absolute():
        config_path = CONFIG_DIR / config_path

    if not config_path.exists():
        raise FileNotFoundError(f'Config file: {config_path} not found.')

    extra_config = Config(**yaml.safe_load(config_path.read_text()))

    fastapi_data = {
        **base_config.FAST_API.dict(exclude_none=True),
        **extra_config.FAST_API.dict(exclude_none=True),
    }

    scheduler_data = {
        **base_config.SCHEDULER.dict(exclude_none=True),
        **extra_config.SCHEDULER.dict(exclude_none=True),
    }

    fastapi_conf = FastAPI(**fastapi_data)
    scheduler_conf = Scheduler(**scheduler_data)

    config_data = {
        **base_config.dict(exclude_none=True),
        **extra_config.dict(exclude_none=True),
        'FAST_API': fastapi_conf,
        'SCHEDULER': scheduler_conf,
    }

    return Config(**config_data)


def get_db_config() -> MySQLConfig:
    config = MySQLConfig(**yaml.safe_load(MYSQL_CONFIG_FILE.read_text()))
    return config
