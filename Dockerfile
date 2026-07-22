# Containerized run of the Proofpane MCP server, for automated directory checks
# (e.g. Glama). It pulls the PUBLIC prebuilt daemon binary — no private source
# required — and runs it in stdio `mcp` mode. Introspection (initialize +
# tools/list) works with no pairing/config; it advertises 13 tools.
FROM debian:bookworm-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Public, single-file PyInstaller Linux x86_64 binary. Override with
# --build-arg DAEMON_URL=... if the path ever changes.
ARG DAEMON_URL=https://app.proofpane.com/daemon/airgov_daemon-linux-x86_64
RUN curl -fsSL "$DAEMON_URL" -o /usr/local/bin/airgov_daemon \
 && chmod +x /usr/local/bin/airgov_daemon

# stdio MCP server. Tool *calls* that route to the cloud need a paired device
# token (intentionally absent here); introspection does not.
ENTRYPOINT ["airgov_daemon"]
CMD ["mcp"]
