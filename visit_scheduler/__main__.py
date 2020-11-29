from configs import get_config
from visit_scheduler.run import run_scheduler


if __name__ == '__main__':
    config = get_config()
    run_scheduler(config)
