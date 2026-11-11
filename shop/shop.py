"""PROVIDED. A shop service that logs far too much, in every bad way. It writes to stdout, like a container should."""
import json, random, sys, time

rnd = random.Random()
EMAILS = ["ana.silva@example.com", "bruno.costa@example.org", "chloe.martin@example.net", "dmitri.volkov@example.com"]
CARDS = ["4111111111111111", "5500005555555559", "378282246310005", "6011111111111117"]
TOKENS = ["eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhbmEifQ.4Q9m3TqZc8", "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJicnVubyJ9.Zk2x8Lp0Rt"]


def emit(level, msg, **kw):
    o = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()), "level": level, "msg": msg}
    o.update(kw)
    print(json.dumps(o), flush=True)


def boom():
    print("Traceback (most recent call last):", flush=True)
    print('  File "/app/shop.py", line 41, in handle_order', flush=True)
    print("    charge(order)", flush=True)
    print('  File "/app/payments.py", line 17, in charge', flush=True)
    print('    raise ValueError("amount must be positive")', flush=True)
    print("ValueError: amount must be positive", flush=True)


i = 0
while True:
    i += 1
    emit("info", "request", route="/healthz", status=200, request_id="req_%d" % rnd.getrandbits(24))
    emit("debug", "cache lookup", key="menu:%d" % rnd.randint(1, 50), hit=rnd.random() < 0.8)
    emit("debug", "serializer ready", took_ms=rnd.randint(1, 5))
    if i % 2 == 0:
        e, c, t = rnd.choice(EMAILS), rnd.choice(CARDS), rnd.choice(TOKENS)
        emit("info", "order created for %s paid with card %s" % (e, c), route="/api/orders", status=201, order_id="ord_%06x" % rnd.getrandbits(24),
             request_id="req_%d" % rnd.getrandbits(24), auth="Bearer " + t)
    if i % 5 == 0:
        emit("warn", "slow query", route="/api/menu", duration_ms=rnd.randint(300, 900), request_id="req_%d" % rnd.getrandbits(24))
    if i % 9 == 0:
        emit("error", "order failed for %s" % rnd.choice(EMAILS), route="/api/orders", status=500, request_id="req_%d" % rnd.getrandbits(24))
        boom()
    time.sleep(0.5)
