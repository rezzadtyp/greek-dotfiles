#!/usr/bin/env python3
"""Wi-Fi state + actions for the eww wifi popover."""
import json, re, subprocess, sys

def run(*a):
    return subprocess.run(a, capture_output=True, text=True)

def split(line):
    # nmcli -t escapes ':' as '\:'
    return [p.replace("\\:", ":") for p in re.split(r"(?<!\\):", line)]

def status():
    enabled = run("nmcli", "radio", "wifi").stdout.strip() == "enabled"
    nets, seen, current = [], set(), ""
    if enabled:
        out = run("nmcli", "-t", "-f", "IN-USE,SSID,SIGNAL,SECURITY",
                  "dev", "wifi", "list", "--rescan", "no").stdout
        known = set(run("nmcli", "-t", "-f", "NAME", "con", "show").stdout.split("\n"))
        for line in out.splitlines():
            f = split(line)
            if len(f) < 4 or not f[1] or f[1] in seen:
                continue
            seen.add(f[1])
            use, ssid, sig, sec = f[0] == "*", f[1], int(f[2] or 0), f[3]
            if use:
                current = ssid
            icon = "󰤨" if sig > 75 else "󰤥" if sig > 50 else "󰤢" if sig > 25 else "󰤟"
            nets.append({"ssid": ssid, "signal": sig, "icon": icon, "active": use,
                         "secure": sec not in ("", "--"), "known": ssid in known})
        nets.sort(key=lambda n: (not n["active"], -n["signal"]))
    print(json.dumps({"enabled": enabled, "current": current, "networks": nets[:8]}, ensure_ascii=False))

def eww(*a):
    subprocess.run(["eww", *a])

cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
if cmd == "status":
    status()
elif cmd == "toggle":
    on = run("nmcli", "radio", "wifi").stdout.strip() == "enabled"
    run("nmcli", "radio", "wifi", "off" if on else "on")
elif cmd == "rescan":
    eww("update", "wifi_msg=Scanning…")
    run("nmcli", "dev", "wifi", "rescan")
    eww("update", "wifi_msg=")
elif cmd == "click":
    # args: ssid secure known active
    ssid, secure, known, active = sys.argv[2], sys.argv[3] == "true", sys.argv[4] == "true", sys.argv[5] == "true"
    if active:
        eww("update", f"wifi_msg=Disconnecting…")
        run("nmcli", "con", "down", "id", ssid)
        eww("update", "wifi_msg=")
    elif known or not secure:
        eww("update", f"wifi_msg=Connecting to {ssid}…")
        r = run("nmcli", "con", "up", "id", ssid) if known else run("nmcli", "dev", "wifi", "connect", ssid)
        eww("update", "wifi_msg=" + ("" if r.returncode == 0 else "Connection failed"))
    else:
        eww("update", f"wifi_pw_ssid={ssid}", "wifi_msg=")
elif cmd == "connect":
    ssid, pw = sys.argv[2], sys.argv[3]
    eww("update", "wifi_pw_ssid=", f"wifi_msg=Connecting to {ssid}…")
    r = run("nmcli", "dev", "wifi", "connect", ssid, "password", pw)
    if r.returncode != 0:
        run("nmcli", "con", "delete", "id", ssid)
    eww("update", "wifi_msg=" + ("" if r.returncode == 0 else "Wrong password or failed"))
