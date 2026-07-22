#!/usr/bin/env python3
"""CI self-check: the public daemon binary must start as an MCP server and
advertise its tools. Expects the binary at ./airgov_daemon (the workflow
downloads it first). Fails if the server won't start or lists too few tools."""
import json
import subprocess
import sys
import threading
import time

p = subprocess.Popen(
    ["./airgov_daemon", "mcp"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    text=True, bufsize=1,
)
out = []
threading.Thread(target=lambda: [out.append(l) for l in p.stdout], daemon=True).start()

for m in (
    {"jsonrpc": "2.0", "id": 1, "method": "initialize",
     "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "ci", "version": "1"}}},
    {"jsonrpc": "2.0", "method": "notifications/initialized"},
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
):
    p.stdin.write(json.dumps(m) + "\n")
    p.stdin.flush()
    time.sleep(0.6)
time.sleep(2)
p.terminate()

tools = []
for ln in out:
    try:
        o = json.loads(ln)
    except Exception:
        continue
    if o.get("id") == 2 and "result" in o:
        tools = [t.get("name") for t in o["result"].get("tools", [])]

print("tools advertised:", tools)
if len(tools) < 10:
    print(f"FAIL: expected >= 10 tools, got {len(tools)}", file=sys.stderr)
    sys.exit(1)
print("OK - MCP server starts and introspects.")
