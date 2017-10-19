from sanic import Sanic
from sanic import response

import aioredis

from jinja2 import Environment, PackageLoader, select_autoescape

import utils

app = Sanic(__name__)

template_env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=True,
)

mmr_template = template_env.get_template('mmr_badge.jinja2')


@app.listener('before_server_start')
async def before_server_start(app, loop):
    app.redis_pool = await aioredis.create_pool(
        ('localhost', 6379), minsize=5, maxsize=10, loop=loop
    )


@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    app.redis_pool.close()
    await app.redis_pool.wait_closed()


@app.route('/')
def index(request):
    return response.html('Hello, world!')


@app.route('/<steam_id:int>/<type_>.svg')
async def mmr_badge(request, steam_id, type_):
    if not type_ in ('team', 'solo', 'estimate'):
        raise
    async with request.app.redis_pool.get() as r:
        mmr = int(await utils.get_cached_mmr(r, steam_id, type_))
    rendered_template = await mmr_template.render_async(mmr=mmr, )
    return response.html(rendered_template)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
