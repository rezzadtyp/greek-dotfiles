#!/usr/bin/env python3
"""Audio state + actions for the eww sound popover."""
import json, subprocess, sys

def run(*a):
    return subprocess.run(a, capture_output=True, text=True).stdout.strip()

def vol(target):
    out = run("wpctl", "get-volume", target)  # "Volume: 0.83 [MUTED]"
    try:
        v = round(float(out.split()[1]) * 100)
    except (IndexError, ValueError):
        v = 0
    return v, "MUTED" in out

def status():
    v, m = vol("@DEFAULT_AUDIO_SINK@")
    mv, mm = vol("@DEFAULT_AUDIO_SOURCE@")
    default = run("pactl", "get-default-sink")
    try:
        sinks = json.loads(run("pactl", "-f", "json", "list", "sinks") or "[]")
    except json.JSONDecodeError:
        sinks = []
    devices = [{"name": s["name"], "label": s.get("description", s["name"]),
                "active": s["name"] == default} for s in sinks]
    icon = "󰝟" if m or v == 0 else ("󰕿" if v < 34 else "󰖀" if v < 67 else "󰕾")
    print(json.dumps({"vol": v, "muted": m, "icon": icon,
                      "mic": mv, "micmuted": mm, "devices": devices}, ensure_ascii=False))

cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
if cmd == "status":
    status()
elif cmd == "set":
    subprocess.run(["wpctl", "set-volume", "-l", "1.0", "@DEFAULT_AUDIO_SINK@", f"{int(float(sys.argv[2]))}%"])
elif cmd == "setmic":
    subprocess.run(["wpctl", "set-volume", "-l", "1.0", "@DEFAULT_AUDIO_SOURCE@", f"{int(float(sys.argv[2]))}%"])
elif cmd == "mute":
    subprocess.run(["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"])
elif cmd == "mutemic":
    subprocess.run(["wpctl", "set-mute", "@DEFAULT_AUDIO_SOURCE@", "toggle"])
elif cmd == "device":
    subprocess.run(["pactl", "set-default-sink", sys.argv[2]])
