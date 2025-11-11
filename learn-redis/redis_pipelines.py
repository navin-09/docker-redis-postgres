# pipeline_benchmark.py
import redis
import time

r = redis.Redis(decode_responses=True)

N = 10000

def no_pipeline():
    start = time.perf_counter()
    for i in range(N):
        r.set(f"np:key:{i}", i)
    end = time.perf_counter()
    return end - start

def with_pipeline():
    start = time.perf_counter()
    pipe = r.pipeline()
    for i in range(N):
        pipe.set(f"p:key:{i}", i)
    pipe.execute()
    end = time.perf_counter()
    return end - start

if __name__ == "__main__":
    t1 = no_pipeline()
    print(f"No pipeline time for {N} sets: {t1:.3f}s")
    t2 = with_pipeline()
    print(f"With pipeline time for {N} sets: {t2:.3f}s")
    print(f"Speedup: {t1 / t2:.1f}x")
