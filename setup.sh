#!/usr/bin/env bash
# Starts the noisy shop and Loki (Alloy starts too, with an empty pipeline). Run: ./setup.sh
set -u
cd "$(dirname "$0")"
for c in docker curl python3; do command -v "$c" >/dev/null || { echo "MISSING: $c"; exit 1; }; done
docker info >/dev/null 2>&1 || { echo "Docker is not running."; exit 1; }
docker compose version >/dev/null 2>&1 || { echo "Docker Compose v2 is missing."; exit 1; }
if (exec 3<>/dev/tcp/127.0.0.1/3197) 2>/dev/null; then echo "Port 3197 is in use on your machine."; exit 1; fi
docker compose up -d shop loki >/dev/null 2>&1 || { echo "could not start the services"; exit 1; }
for _ in $(seq 1 60); do curl -fs http://127.0.0.1:3197/ready 2>/dev/null | grep -q ready && break; sleep 2; done
echo "The shop is logging. Look at what it writes:   docker logs hygiene-shop | head -30"
echo "Loki is on http://localhost:3197.   Write alloy/config.alloy, then:   docker compose up -d alloy   (and docker compose restart alloy after each change)"
