import os, sys, urllib.request

port = os.getenv("PORT", "8080")
url = f"http://127.0.0.1:{port}/health"

try:
    with urllib.request.urlopen(url, timeout=2) as resp:
        # Exit 0 on HTTP 200 and JSON {"status":"ok"}
        ok = resp.status == 200
        if ok:
            data = resp.read().decode("utf-8")
            ok = '"status": "ok"' in data or '"status":"ok"' in data
        sys.exit(0 if ok else 1)
except Exception:
    sys.exit(1)