#!/usr/bin/env bash
# switch_workspace.sh - switch Hyprland workspace from Waybar click
# Accepts a single argument: workspace name or index
ws="$1"
if [ -z "$ws" ]; then
  exit 0
fi

# Hyprland: dispatch a workspace command
if command -v hyprctl >/dev/null 2>&1; then
  hyprctl dispatch workspace "$ws"
else
  echo "hyprctl not found" >&2
  exit 1
fi
