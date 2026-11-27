"""Tiny file/exec server that runs INSIDE the rented GPU pod.
Every request must carry header X-Token equal to env RENDER_TOKEN.
  PUT  /file?path=rel     upload (body = bytes)      GET /file?path=rel  download
  POST /exec              body = shell command, runs in background, returns job id
  GET  /job?id=N          {"done":bool,"rc":int|null,"log_tail":str}
Root dir: /workspace/job
"""
import http.server, json, os, subprocess, threading, urllib.parse

ROOT = '/workspace/job'; TOKEN = os.environ['RENDER_TOKEN']; JOBS = {}
os.makedirs(ROOT, exist_ok=True)

def safe(p):
    full = os.path.realpath(os.path.join(ROOT, p))
    if not full.startswith(ROOT + '/'): raise ValueError('bad path')
    return full

class H(http.server.BaseHTTPRequestHandler):
    def _auth(self):
        if self.headers.get('X-Token') != TOKEN:
            self.send_response(403); self.end_headers(); return False
        return True
    def _send(self, code, body, ctype='application/json'):
        b = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code); self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_PUT(self):
        if not self._auth(): return
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        dst = safe(q['path'][0]); os.makedirs(os.path.dirname(dst), exist_ok=True)
        n = int(self.headers['Content-Length'])
        with open(dst, 'wb') as f:
            while n > 0:
                chunk = self.rfile.read(min(n, 1 << 20)); f.write(chunk); n -= len(chunk)
        self._send(200, {'ok': True, 'bytes': os.path.getsize(dst)})
    def do_GET(self):
        if not self._auth(): return
        u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query)
        if u.path == '/file':
            with open(safe(q['path'][0]), 'rb') as f: self._send(200, f.read(), 'application/octet-stream')
        elif u.path == '/job':
            j = JOBS[int(q['id'][0])]
            with open(j['log'], 'rb') as f: tail = f.read()[-4000:].decode('utf-8', 'replace')
            self._send(200, {'done': j['p'].poll() is not None, 'rc': j['p'].poll(), 'log_tail': tail})
        elif u.path == '/ping':
            self._send(200, {'ok': True})
        else:
            self._send(404, {'err': 'not found'})
    def do_POST(self):
        if not self._auth(): return
        cmd = self.rfile.read(int(self.headers['Content-Length'])).decode()
        jid = len(JOBS) + 1; log = f'{ROOT}/job_{jid}.log'
        p = subprocess.Popen(['bash', '-lc', cmd], cwd=ROOT, stdout=open(log, 'wb'), stderr=subprocess.STDOUT)
        JOBS[jid] = {'p': p, 'log': log}; self._send(200, {'id': jid})

http.server.ThreadingHTTPServer(('0.0.0.0', 8000), H).serve_forever()
