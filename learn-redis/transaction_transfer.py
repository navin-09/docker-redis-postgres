# transaction_transfer.py
import redis

r = redis.Redis(decode_responses=True)

def setup():
    r.set("wallet:A", 200)
    r.set("wallet:B", 50)
    print("Initial:", r.get("wallet:A"), r.get("wallet:B"))

def transfer(sender, receiver, amount):
    # WATCH + MULTI/EXEC pattern to do safe transfer
    with r.pipeline() as pipe:
        while True:
            try:
                pipe.watch(sender, receiver)
                s = int(pipe.get(sender) or 0)
                if s < amount:
                    pipe.unwatch()
                    return False, f"Insufficient funds: {s} < {amount}"

                pipe.multi()
                pipe.decrby(sender, amount)
                pipe.incrby(receiver, amount)
                pipe.execute()
                return True, "Transfer successful"
            except redis.WatchError:
                # someone changed the keys, retry
                continue

if __name__ == "__main__":
    setup()
    ok, msg = transfer("wallet:A", "wallet:B", 70)
    print(msg)
    print("After:", r.get("wallet:A"), r.get("wallet:B"))
