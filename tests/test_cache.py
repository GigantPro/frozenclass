import sqlite3
from datetime import time
from time import sleep
from timeit import timeit

from frozenclass import CacheController


def test_cache_with_time():
    b = 1

    @CacheController.cache(ttl=time(second=1))
    def test_cache():
        return b

    assert test_cache() == 1

    b = 2
    assert test_cache() == 1

    sleep(1)
    assert test_cache() == 2


def test_cache_without_time():
    b = 1

    @CacheController.cache(ttl=None)
    def test_cache():
        return b

    assert test_cache() == 1

    b = 2
    assert test_cache() == 1

    sleep(1)
    assert test_cache() == 1

def test_speed():
    base = sqlite3.connect('test_saves/test.db')
    cur = base.cursor()

    base.execute('CREATE TABLE IF NOT EXISTS test (number PRIMARY KEY, value)')
    try:
        [cur.execute('INSERT INTO test VALUES (?, ?)', (i, i ** 2)) for i in range(1000)]
    except:  # pylint: disable=bare-except
        pass
    base.commit()

    @CacheController.cache(ttl=time(second=1))
    def test_cache(cur):
        return cur.execute('SELECT * FROM test').fetchall()

    def test_cache_without_lib(cur):  # pylint: disable=possibly-unused-variable
        return cur.execute('SELECT * FROM test').fetchall()

    assert (timeit('test_cache(cur)', globals=locals(), number=1000) / 1000) < .00001
    assert(timeit('test_cache(cur)', globals=locals(), number=1000) / 1000) < \
                (timeit('test_cache_without_lib(cur)', globals=locals(), number=1000) / 1000)


    @CacheController.cache(ttl=None)
    def test_cache(cur):  # pylint: disable=function-redefined
        return cur.execute('SELECT * FROM test').fetchall()

    def test_cache_without_lib(cur):  # pylint: disable=function-redefined
        return cur.execute('SELECT * FROM test').fetchall()

    assert (timeit('test_cache(cur)', globals=locals(), number=1000) / 1000) < .00001
    assert(timeit('test_cache(cur)', globals=locals(), number=1000) / 1000) < \
                (timeit('test_cache_without_lib(cur)', globals=locals(), number=1000) / 1000)
