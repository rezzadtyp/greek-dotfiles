#!/usr/bin/env bash
# Step brightness by an absolute amount (works around brightnessctl 0.5 jumping to 100% on "+N%").
# Usage: brightness.sh up|down [step]
step="${2:-5}"
cur=$(brightnessctl -m | cut -d, -f4 | tr -d %)
case "$1" in
  up)   new=$((cur + step)); [ "$new" -gt 100 ] && new=100 ;;
  down) new=$((cur - step)); [ "$new" -lt 1 ] && new=1 ;;
  *)    exit 1 ;;
esac
brightnessctl -q set "${new}%"
