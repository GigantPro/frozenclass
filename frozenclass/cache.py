from typing import Any, Callable, Optional
from datetime import time, datetime, timedelta


class CacheController:
    """The main class of the cache logic. Includes all caches logic"""
    def cache(*, ttl: Optional[time] = time(minute=10)) -> Callable:  # ( TTL_end, result )
        """Function-decorate for runtime caching.
The cache can either be overwritten or remain until the program terminates.

        :param ttl: Time-To-Live of cached valume, defaults to time(minute=10)
        :type ttl: time | None, optional
        :return: Decorated func
        :rtype: Callable
        """
        def wrapper_func(target_func: Callable) -> Callable:
            __cached_vals = {}


            def cached_func_with_time(*args, **kwargs) -> Any:
                cached_ = __cached_vals.get((*args, *kwargs), None)
                if cached_ and cached_[0] > datetime.now():
                    return cached_[1]

                result = target_func(*args, **kwargs)

                __cached_vals[(*args, *kwargs)] = \
                    (datetime.now() + timedelta(hours=ttl.hour, minutes=ttl.minute, seconds=ttl.second), result)

                return result


            def cached_func_without_time(*args, **kwargs) -> Any:
                try:
                    return __cached_vals[(*args, *kwargs)]
                except KeyError:
                    result = target_func(*args, **kwargs)
                    __cached_vals[(*args, *kwargs)] = result
                    return result


            return cached_func_with_time if ttl else cached_func_without_time
        return wrapper_func
