#!/usr/bin/env bash
# Reads what ended up in Loki and checks it is clean. Run with: ./verify.sh
cd "$(dirname "$0")" || exit 1
curl -fs http://127.0.0.1:3197/ready 2>/dev/null | grep -q ready || { echo "Loki is not running. Run ./setup.sh first." >&2; exit 1; }
exec python3 .lab/hygienecheck.py
