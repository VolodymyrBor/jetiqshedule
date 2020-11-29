from pathlib import Path

import yaml

from .schmes import Config, BaseConfig


CONFIG_DIR = Path(__file__).parent
BASE_CONFIG = CONFIG_DIR / 'base.yaml'


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

    base_data = base_config.dict()
    extra_data = extra_config.dict(exclude_none=True)
    return Config(**base_data, **extra_data)
