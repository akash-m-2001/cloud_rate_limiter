import time
import redis

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

MAX_REQUESTS = 5
WINDOW_SECONDS = 10

def allow_request(key: str) -> bool:
    now = int(time.time())
    window_key = f"{key}:{now // WINDOW_SECONDS}"

    count = r.incr(window_key)

    # if this is the first hit in this window, set expiry
    if count == 1:
        r.expire(window_key, WINDOW_SECONDS)

    return count <= MAX_REQUESTS
