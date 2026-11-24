#!/bin/bash

CURRENT_SONG="$HOME/.config/waybar/scripts/current_song.sh"

zscroll -l 15 -p " | " --delay 0.2 \
    --match-command "playerctl status" \
    --match-text "Playing" "--scroll 1" \
    --match-text "Paused" "--before-text ' ' --scroll 0" \
    --match-text "Stopped" "--before-text ' ' --scroll 0" \
    --update-interval 1 \
    --update-check true "$CURRENT_SONG"
