#!/usr/bin/env bash
# Toggle an eww popover (volume|wifi), closing the other one.
# Usage: toggle.sh volume|wifi|close
win="$1"
dur=0.25   # keep in sync with the revealer :duration in eww.yuck

# start the daemon on demand (it is killed again once nothing is open)
if ! eww ping >/dev/null 2>&1; then
  [ "$win" = close ] && exit 0
  eww daemon >/dev/null 2>&1
  for _ in $(seq 50); do eww ping >/dev/null 2>&1 && break; sleep 0.05; done
fi
open=$(eww active-windows 2>/dev/null | grep -E '^(volume|wifi):')

# slide out whatever is open, then close it
if [ -n "$open" ]; then
  eww update reveal=false
  sleep "$dur"
fi
eww close volume wifi >/dev/null 2>&1
eww update vol_open=false wifi_open=false wifi_pw_ssid= wifi_msg= wifi_pw=

# nothing left open: stop the daemon to free its memory
[ "$win" = close ] && { eww kill >/dev/null 2>&1; exit 0; }

# open the requested one (unless it was the one just closed) and slide it in
if ! grep -q "^$win:" <<<"$open"; then
  eww update "${win/volume/vol}_open=true"
  eww open "$win"
  sleep 0.03
  eww update reveal=true
else
  # same button clicked again: popup closed, free the memory
  eww kill >/dev/null 2>&1
fi
