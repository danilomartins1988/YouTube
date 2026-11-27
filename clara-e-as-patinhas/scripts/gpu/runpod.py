"""Rent a RunPod GPU pod, render there, bring results back, shut it down.
The RunPod API key is NEVER in this repo or sandbox: the session's network proxy injects it
for rest.runpod.io (we send 'Authorization: Bearer dummy').

  python scripts/gpu/runpod.py create [--gpu "NVIDIA GeForce RTX 4090"] [--cloud SECURE|COMMUNITY]
  python scripts/gpu/runpod.py status
  python scripts/gpu/runpod.py push <local_path> <remote_rel>      # upload one file
  python scripts/gpu/runpod.py run "<shell cmd>"                   # start a job on the pod
  python scripts/gpu/runpod.py wait <job_id>
  python scripts/gpu/runpod.py pull <remote_rel> <local_path>
  python scripts/gpu/runpod.py stop | terminate                    # ALWAYS terminate at the end
State (pod id, render token) lives in the scratchpad, not in git.
"""
import base64, json, os, secrets, sys, time, requests

API = 'https://rest.runpod.io/v1'
HDR = {'Authorization': 'Bearer dummy', 'Content-Type': 'application/json'}
STATE = os.environ.get('GPU_STATE', '/tmp/claude-0/-home-user-YouTube/d850b732-f9ee-5afb-a405-beaa03bb820f/scratchpad/gpu_pod.json')
BLENDER_URL = 'https://download.blender.org/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz'

def load():
    return json.load(open(STATE)) if os.path.exists(STATE) else {}
def save(s):
    json.dump(s, open(STATE, 'w'))

def pod_url(s): return f"https://{s['pod_id']}-8000.proxy.runpod.net"
def ph(s): return {'X-Token': s['token']}

def create(gpu='NVIDIA GeForce RTX 4090', cloud='SECURE'):
    s = load()
    if s.get('pod_id'): sys.exit(f"pod already exists: {s['pod_id']} (terminate first)")
    token = secrets.token_hex(24)
    server = base64.b64encode(open(os.path.join(os.path.dirname(__file__), 'pod_server.py'), 'rb').read()).decode()
    boot = (
        'set -e; export DEBIAN_FRONTEND=noninteractive; apt-get update -qq; '
        'apt-get install -y -qq python3 curl xz-utils ffmpeg libxi6 libxrender1 libxkbcommon0 libsm6 libgl1 libegl1 libxxf86vm1 libxfixes3 >/dev/null; '
        f'mkdir -p /opt /workspace/job; curl -sL {BLENDER_URL} | tar -xJ -C /opt; ln -sf /opt/blender-4.0.2-linux-x64/blender /usr/local/bin/blender; '
        f'echo {server} | base64 -d > /opt/pod_server.py; exec python3 /opt/pod_server.py')
    body = {
        'name': 'kids-render', 'imageName': 'nvidia/cuda:12.2.2-runtime-ubuntu22.04',
        'gpuTypeIds': [gpu], 'gpuCount': 1, 'cloudType': cloud,
        'containerDiskInGb': 30, 'volumeInGb': 0, 'ports': ['8000/http'],
        'env': {'RENDER_TOKEN': token, 'NVIDIA_DRIVER_CAPABILITIES': 'all'},
        'dockerStartCmd': ['bash', '-c', boot],
    }
    r = requests.post(f'{API}/pods', headers=HDR, json=body, timeout=60)
    print(r.status_code, r.text[:800]); r.raise_for_status()
    pod = r.json(); save({'pod_id': pod['id'], 'token': token, 'created': time.time(), 'gpu': gpu})
    print('pod', pod['id'], 'cost/h', pod.get('costPerHr'))

def status():
    s = load(); r = requests.get(f"{API}/pods/{s['pod_id']}", headers=HDR, timeout=60)
    d = r.json(); print(json.dumps({k: d.get(k) for k in ('id', 'desiredStatus', 'costPerHr', 'gpu', 'machine')}, default=str)[:800])
    try:
        print('server:', requests.get(pod_url(s) + '/ping', headers=ph(s), timeout=20).text)
    except Exception as e:
        print('server not up yet:', e)
    print(f"running for {(time.time() - s['created']) / 3600:.2f} h")

def push(local, remote):
    s = load()
    with open(local, 'rb') as f:
        r = requests.put(pod_url(s) + '/file', params={'path': remote}, data=f, headers=ph(s), timeout=600)
    print(r.status_code, r.text)

def run(cmd):
    s = load(); r = requests.post(pod_url(s) + '/exec', data=cmd.encode(), headers=ph(s), timeout=60); print(r.text)

def wait(jid, every=30):
    s = load()
    while True:
        j = requests.get(pod_url(s) + '/job', params={'id': jid}, headers=ph(s), timeout=60).json()
        print(j['log_tail'][-600:], flush=True)
        if j['done']: print('rc', j['rc']); return
        time.sleep(every)

def pull(remote, local):
    s = load(); r = requests.get(pod_url(s) + '/file', params={'path': remote}, headers=ph(s), timeout=1200, stream=True)
    r.raise_for_status()
    with open(local, 'wb') as f:
        for c in r.iter_content(1 << 20): f.write(c)
    print('saved', local, os.path.getsize(local))

def stop():
    s = load(); print(requests.post(f"{API}/pods/{s['pod_id']}/stop", headers=HDR, timeout=60).text)

def terminate():
    s = load(); r = requests.delete(f"{API}/pods/{s['pod_id']}", headers=HDR, timeout=60)
    print(r.status_code, r.text); 
    if r.ok: print(f"terminated after {(time.time() - s['created']) / 3600:.2f} h"); os.remove(STATE)

if __name__ == '__main__':
    a = sys.argv[1:]; c = a[0]
    if c == 'create':
        kw = {}
        if '--gpu' in a: kw['gpu'] = a[a.index('--gpu') + 1]
        if '--cloud' in a: kw['cloud'] = a[a.index('--cloud') + 1]
        create(**kw)
    else:
        {'status': status, 'push': push, 'run': run, 'wait': wait, 'pull': pull, 'stop': stop, 'terminate': terminate}[c](*a[1:])
