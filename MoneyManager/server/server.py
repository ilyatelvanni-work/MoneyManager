import asyncio
import logging
import sys
from pathlib import Path

from aiohttp import web

from MoneyManager.db_connection import init_engine, get_engine, Base
from MoneyManager.api import API

SQLALCHEMY_LOGGER = 'sqlalchemy'
SYSTEM_LOGGER = 'System'
OPEN_AI = 'OpenAI'

api = API()


async def prepare_db() -> None:
    await init_engine()

    engine = await get_engine()

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # TODO: REMOVE_ME
        await conn.run_sync(Base.metadata.create_all)

    # await character.DataGenerator().add_default_character()


async def logging_middleware(app, handler):
    log = logging.getLogger(SYSTEM_LOGGER)

    async def middleware_handler(request: web.Request):
        # Log the request method and URL
        log.info(f"{request.method} {request.url}")
        # Log the request parameters
        if request.method == "GET":
            log.info(f"Params: {request.query}")
        elif request.method == "POST":
            log.info(f"Params: {await request.json()}")
        # Call the next handler in the chain
        response = await handler(request)
        return response

    return middleware_handler


async def index_html_handler(request: web.Request) -> web.Response:
    return web.FileResponse(Path(__file__).parent / 'index.html')


# async def character_handler(request: web.Request) -> web.Response:
#     id_ = 1
#     return web.Response(
#         content_type="application/json", charset="utf-8", text=await api.api_get_character_by_id(id_)
#     )

# async def dialog_get_handler(request: web.Request) -> web.Response:
#     character_id = 1
#     return web.Response(
#         status=200, content_type="application/json", charset="utf-8",
#         text=await api.get_chain_of_messages_for_character(character_id)
#     )

# async def dialog_post_handler(request: web.Request) -> web.Response:
#     params: dict[str, int | str] = await request.json()
#     return web.Response(
#         status=200, content_type="application/json", charset="utf-8",
#         text=await api.send_message_for_character(params['character_id'], params['message'])
#     )

async def api_currency_get_handler(request: web.Request) -> web.Response:
    return web.Response(
        status=200, content_type='application/json', charset='utf-8', text=await api.get_currency()
    )

async def api_category_get_handler(request: web.Request) -> web.Response:
    return web.Response(
        status=200, content_type='application/json', charset='utf-8', text=await api.get_category()
    )

async def api_account_get_handler(request: web.Request) -> web.Response:
    return web.Response(
        status=200, content_type='application/json', charset='utf-8', text=await api.get_account()
    )

async def api_transaction_post_handler(request: web.Request) -> web.Response:
    params: dict[str, int | str] = await request.json()
    return web.Response(
        status=200, content_type='application/json', charset='utf-8', text=await api.create_transaction(**params)
    )

def init_logging() -> None:
    standart_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def set_logger(logger_name: str, logging_level: int) -> None:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging_level)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(standart_formatter)
        logger.addHandler(stream_handler)

    set_logger(SQLALCHEMY_LOGGER, logging.INFO)
    set_logger(SYSTEM_LOGGER, logging.INFO)
    set_logger(OPEN_AI, logging.INFO)


def main() -> None:

    init_logging()

    asyncio.run(prepare_db())
    app = web.Application()  # middlewares=[middlewares.handle_exception, middlewares.access, middlewares.set_request_id])
    app.middlewares.append(logging_middleware)

    # add_static_resources(app)

    app.router.add_get('/', index_html_handler)
    app.add_routes([web.static('/resources', Path(__file__).parent / 'resources')])

    app.router.add_get('/api/currency', api_currency_get_handler)
    app.router.add_get('/api/category', api_category_get_handler)
    app.router.add_get('/api/account', api_account_get_handler)

    app.router.add_post('/api/transaction', api_transaction_post_handler)

    # app.router.add_get('/api/character', character_handler)
    # app.router.add_get('/api/dialog', dialog_get_handler)

    # app.router.add_post('/api/dialog', dialog_post_handler)
    

    # app.router.add_get('/character', handler_RENAMEME)
    web.run_app(app, host='localhost', port='4433')


if __name__ == '__main__':
    main()
