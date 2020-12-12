import asyncio
import logging
import sys

from aiohttp import web

from .routes import setup_routes
from .settings import get_config


def init_app(loop, argv=None):
    app = web.Application(loop=loop)

    app['config'] = get_config(argv)

    # setup views and routes
    setup_routes(app)

    return app


def main(loop):
    logging.basicConfig(level=logging.DEBUG)

    # try:
    #     loop = asyncio.get_event_loop()
    # except RuntimeError:
    #     loop = asyncio.new_event_loop()

    app = init_app(loop)

    config = app['config']

    runner = web.AppRunner(app)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(
        runner,
        host=config['host'],
        port=config['port']
    )
    loop.run_until_complete(site.start())

    logging.info(f'Server started at: http://{config["host"]}:{config["port"]}')

    loop.run_forever()


if __name__ == '__main__':
    main(asyncio.get_event_loop())
