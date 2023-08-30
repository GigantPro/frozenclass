from datetime import time
from time import sleep
import pytest

from frozenclass import CacheController


@pytest.mark.asyncio
async def test_cache_with_time():
    b = 1

    @CacheController.cache(ttl=time(second=1), is_async=True)
    async def test_cache():
        return b

    res = await test_cache()
    assert res == 1

    b = 2
    res = await test_cache()
    assert res == 1

    sleep(1)
    res = await test_cache()
    assert res == 2


@pytest.mark.asyncio
async def test_cache_without_time():
    b = 1

    @CacheController.cache(ttl=None, is_async=True)
    async def test_cache():
        return b

    res = await test_cache()
    assert res == 1

    b = 2
    res = await test_cache()
    assert res == 1

    sleep(1)
    res = await test_cache()
    assert res == 1
