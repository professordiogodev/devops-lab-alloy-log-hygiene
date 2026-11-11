#!/usr/bin/env bash
# Removes the containers, network and volumes. Run with: ./teardown.sh
cd "$(dirname "$0")" || exit 1
docker compose down -v --remove-orphans 2>&1 | tail -3
echo "Now run ./verify-teardown.sh"
