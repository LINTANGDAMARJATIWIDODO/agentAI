import urllib.request
import json

base_url = 'http://localhost:3001'

endpoints = [
    '/api/status',
    '/api/employees',
    '/api/departments',
    '/api/projects'
]

print("=== Testing NEXUS API Endpoints ===")
for ep in endpoints:
    url = base_url + ep
    try:
        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read().decode('utf-8'))
            if ep == '/api/status':
                print(f"HTTP 200 OK: {ep} -> Agents: {len(data.get('agents', []))}")
            elif ep == '/api/employees':
                print(f"HTTP 200 OK: {ep} -> Total employees: {data.get('total')}")
            elif ep == '/api/departments':
                print(f"HTTP 200 OK: {ep} -> Total facilities: {data.get('total_facilities')}")
            elif ep == '/api/projects':
                print(f"HTTP 200 OK: {ep} -> Total projects: {len(data.get('projects', []))}")
    except Exception as e:
        print(f"FAILED {ep}: {e}")
