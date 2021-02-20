from configs import get_db_config

from tortoise import Tortoise

db_config = get_db_config()

TORTOISE_ORM = {
    'connections': {
        'mysql': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': db_config.HOST,
                'port': db_config.PORT,
                'user': db_config.USERNAME,
                'password': db_config.PASSWORD,
                'database': db_config.DATABASE,
            }
        }
    },
    'apps': {
        'lesson_schedule': {
            'models': ['lesson_schedule.models'],
            'default_connection': 'mysql',
        },
        'visit_scheduler': {
            'models': ['visit_scheduler.models'],
            'default_connection': 'mysql',
        },
        'auth': {
            'models': ['auth.models'],
            'default_connection': 'mysql',
        },
        'aerich': {
            'models': ['aerich.models'],
            'default_connection': 'mysql',
        },
    }
}


async def setup():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def shutdown():
    await Tortoise.close_connections()
