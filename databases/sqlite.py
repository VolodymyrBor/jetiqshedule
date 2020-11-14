from tortoise import Tortoise


TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.sqlite',
            'credentials': {
                'file_path': 'db.sqlite3',
            }
        }
    },
    'apps': {
        'schedule': {
            'models': ['schedule.models'],
            'default_connection': 'default',
        }
    }
}


async def setup():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def shutdown():
    await Tortoise.close_connections()
