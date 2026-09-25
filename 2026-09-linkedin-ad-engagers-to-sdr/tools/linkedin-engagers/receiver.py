#!/usr/bin/env python3
"""Local receiver for scrape payloads. The LinkedIn page POSTs JSON here (fetch mode:'no-cors'),
so Chrome's one-automatic-download-per-site block never applies.
  python3 receiver.py [port]     -> writes raw/<name>.json ; GET /ping -> ok
"""
import http.server, json, pathlib, re, sys, time, urllib.parse
RAW = pathlib.Path(__file__).parent / "raw"; RAW.mkdir(exist_ok=True)
class H(http.server.BaseHTTPRequestHandler):
    def _ok(self, body=b"ok"):
        self.send_response(200); self.send_header("Content-Type", "text/plain")
        self.send_header("Access-Control-Allow-Origin", "*"); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "d" not in q: return self._ok()
        name = re.sub(r"[^A-Za-z0-9_.-]", "", (q.get("name") or ["payload"])[0]) or "payload"
        if not name.endswith(".json"): name += ".json"
        body = q["d"][0].encode()
        try: json.loads(body)
        except Exception: name = name.replace(".json", ".bad.txt")
        (RAW / name).write_bytes(body); time.sleep(2.0)
        # send the tab back to LinkedIn so it never rests on a localhost page
        self.send_response(302); self.send_header("Location", "https://www.linkedin.com/feed/"); self.end_headers()
    def do_OPTIONS(self): self._ok()
    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        name = re.sub(r"[^A-Za-z0-9_.-]", "", (q.get("name") or ["payload"])[0]) or "payload"
        if not name.endswith(".json"): name += ".json"
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        try: json.loads(body)
        except Exception: name = name.replace(".json", ".bad.txt")
        (RAW / name).write_bytes(body); time.sleep(2.0)
        # send the tab back to LinkedIn so it never rests on a localhost page
        self.send_response(302); self.send_header("Location", "https://www.linkedin.com/feed/"); self.end_headers()
    def log_message(self, *a): pass
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8871
class S(http.server.HTTPServer): pass
srv = S(("127.0.0.1", port), H)
srv.RequestHandlerClass.rbufsize = -1
srv.serve_forever()
