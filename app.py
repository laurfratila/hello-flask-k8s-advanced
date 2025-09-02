import os
import threading
import time
from flask import Flask, jsonify

app = Flask(__name__)

# Config via env vars (will come from ConfigMap/Secret in K8s)
APP_MESSAGE = os.getenv("APP_MESSAGE", "Hello from the advanced Flask app!")
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "not-set")  # demo: will come from a Secret
INTERVAL_SEC = int(os.getenv("INTERVAL_SEC", "30"))  # how often to write
DATA_DIR = os.getenv("DATA_DIR", "/data")
COUNTER_FILE = os.path.join(DATA_DIR, "counter.txt")
PORT = int(os.getenv("PORT", "8080"))

os.makedirs(DATA_DIR, exist_ok=True)

# background writer
def writer_loop():
    count = 0
    while True:
        count += 1
        with open(COUNTER_FILE, "a", encoding="utf-8") as f:
            f.write(f"{int(time.time())},{count}\n")
        time.sleep(INTERVAL_SEC)

@app.get("/")
def root():
    # show message and whether secret is set (not its value)
    has_secret = SECRET_TOKEN != "not-set"
    return jsonify({
        "message": APP_MESSAGE,
        "secret_present": has_secret,
        "counter_file": COUNTER_FILE
    })

@app.get("/health")
def health():
    # simple health signal: app alive and data dir writable
    try:
        test_path = os.path.join(DATA_DIR, ".healthcheck")
        with open(test_path, "w") as f:
            f.write("ok")
        os.remove(test_path)
        status = "ok"
    except Exception as e:
        status = f"error: {e}"
    return jsonify({"status": status})

if __name__ == "__main__":
    t = threading.Thread(target=writer_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=PORT)