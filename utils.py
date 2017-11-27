import asyncio

import aioredis
import aiohttp

REDIS_EXPIRE_TIME = 7 * 24 * 3600


async def get_mmr(r, steam_id, type_='solo'):
    return await r.get('%d%s' % (steam_id, type_))


async def set_mmr(r, steam_id, type_, mmr):
    return await r.setex('%d%s' % (steam_id, type_), REDIS_EXPIRE_TIME, mmr)


async def request_profile(steam_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'https://api.opendota.com/api/players/%d' % steam_id
        ) as result:
            return await result.json()


async def get_cached_mmr(r, steam_id, type_='solo'):
    cached_mmr = await get_mmr(r, steam_id, type_=type_)
    if cached_mmr:
        return cached_mmr

    data = await request_profile(steam_id)
    solo_mmr = data.get('solo_competitive_rank', None)
    team_mmr = data.get('competitive_rank', None)
    estimate_mmr = data.get('mmr_estimate', {}).get('estimate', None)

    if type_ == 'solo':
        mmr = solo_mmr
    elif type_ == 'team':
        mmr = team_mmr
    else:
        mmr = estimate_mmr
    await asyncio.wait([
        set_mmr(r, steam_id, 'solo', solo_mmr),
        set_mmr(r, steam_id, 'team', team_mmr),
        set_mmr(r, steam_id, 'estimate', estimate_mmr)])
    return mmr
