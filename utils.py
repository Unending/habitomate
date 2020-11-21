import time

def rateLimit(r):
    limit = r.headers["X-RateLimit-Remaining"]
    if limit == "0":
        print("sleeping 60s")
        time.sleep(60)
