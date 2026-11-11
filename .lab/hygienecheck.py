#!/usr/bin/env python3
import json, os, re, subprocess, sys, time, urllib.parse, urllib.request, urllib.error
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
LOKI = "http://127.0.0.1:3197"
passed = failed = 0


def check(desc, ok, hint=""):
    global passed, failed
    if ok:
        passed += 1; print("PASS  " + desc, flush=True)
    else:
        failed += 1; print("FAIL  " + desc + (("   -> " + hint) if hint else ""), flush=True)


def get(path, **params):
    u = LOKI + path + ("?" + urllib.parse.urlencode(params) if params else "")
    return json.load(urllib.request.urlopen(u, timeout=30))


def count(expr, minutes=1):
    try:
        r = get("/loki/api/v1/query", query="sum(count_over_time(%s [%dm]))" % (expr, minutes), time=int(time.time()))["data"]["result"]
        return int(float(r[0]["value"][1])) if r else 0
    except urllib.error.HTTPError as e:
        return -1


def wait_for(fn, secs, step=5):
    end = time.time() + secs
    while time.time() < end:
        try:
            if fn():
                return True
        except Exception:
            pass
        time.sleep(step)
    return False


cfg = open("alloy/config.alloy").read()
code = "\n".join(l for l in cfg.split("\n") if not l.strip().startswith("//"))
print("== The pipeline ==")
check("alloy/config.alloy is written", "loki.write" in code and "loki.source.docker" in code, "see the TODO comments")
if "loki.write" not in code:
    sys.exit(1)
rc = subprocess.run(["docker", "compose", "up", "-d", "alloy"], capture_output=True, text=True)
subprocess.run(["docker", "compose", "restart", "alloy"], capture_output=True, text=True)
check("Alloy starts with your configuration", rc.returncode == 0 and wait_for(lambda: "Up" in subprocess.run(["docker", "compose", "ps", "alloy", "--format", "{{.Status}}"], capture_output=True, text=True).stdout, 30), subprocess.run(["docker", "compose", "logs", "--tail", "10", "alloy"], capture_output=True, text=True).stdout[-300:])
print("      waiting 75 seconds so that the last minute of logs was written by YOUR current configuration...")
time.sleep(75)
total = count('{service="shop"}')
check("lines arrive in Loki with the label service=shop (%d in the last minute)" % total, total > 0, "check the relabel rule and docker logs of alloy")
if total <= 0:
    sys.exit(1)

print("== Nothing sensitive is stored ==")
n = count('{service="shop"} |~ "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}"')
check("no e-mail address in any stored line (found %d)" % n, n == 0)
n = count('{service="shop"} |~ "[0-9]{13,19}"')
check("no card number (13 to 19 digits) in any stored line (found %d)" % n, n == 0)
n = count('{service="shop"} |~ "Bearer [A-Za-z0-9._-]{10,}"')
check("no bearer token in any stored line (found %d)" % n, n == 0)
check("the lines were REDACTED, not discarded: [REDACTED-EMAIL], [REDACTED-CARD] and Bearer [REDACTED] are present",
      count('{service="shop"} |= "[REDACTED-EMAIL]"') > 0 and count('{service="shop"} |= "[REDACTED-CARD]"') > 0 and count('{service="shop"} |= "Bearer [REDACTED]"') > 0)

print("== The noise is gone ==")
n = count('{service="shop"} |= "/healthz"')
check("no health-check line is stored (found %d)" % n, n == 0)
n = count('{service="shop"} |~ "\\"level\\": \\"debug\\""')
check("no debug line is stored (found %d)" % n, n == 0)
check("the useful lines are still there: order created, slow query, order failed",
      all(count('{service="shop"} |= "%s"' % t) > 0 for t in ("order created", "slow query", "order failed")))

print("== Stack traces ==")
joined = count('{service="shop"} |= "Traceback (most recent call last)" |= "ValueError: amount must be positive"')
orphans = count('{service="shop"} !~ "Traceback" |~ "^\\\\s+File"')
check("a stack trace is ONE entry: Traceback and the final ValueError line are in the same stored entry (found %d)" % joined, joined > 0, "stage.multiline with a firstline that matches `{` or `Traceback`")
check("no orphan trace line is stored on its own (found %d)" % orphans, orphans == 0)
n = count('{service="shop",level="error"} |= "Traceback"')
check("trace entries carry the label level=error", n > 0, "stage.match + stage.static_labels")

print("== Labels ==")
labels = set(get("/loki/api/v1/labels")["data"])
allowed = {"service", "level", "service_name"}
check("the stored streams carry only the labels service and level (found: %s)" % sorted(labels), labels <= allowed, "labels beyond %s: %s" % (sorted(allowed), sorted(labels - allowed)))
levels = set(get("/loki/api/v1/label/level/values")["data"]) if "level" in labels else set()
check("the level label has few values (found: %s)" % sorted(levels), 1 <= len(levels) <= 4 and "debug" not in levels)
p = open("PRIVACY.md").read()
check("PRIVACY.md is filled in (no TODO left)", "TODO" not in p and len(p.split()) > 70)
print()
print(("ALL CHECKS PASSED (%d/%d)" % (passed, passed)) if failed == 0 else ("%d check(s) failed, %d passed" % (failed, passed)))
sys.exit(1 if failed else 0)
