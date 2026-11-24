#!/bin/bash

PLAYER_STATUS=$(playerctl status 2>/dev/null)
# Replace &'s in artist name/song title with +'s to avoid parsing issues
ARTIST=$(playerctl metadata artist 2>/dev/null | sed 's/&/+/g') 
TITLE=$(playerctl metadata title 2>/dev/null | sed 's/&/+/g')

if [[ $PLAYER_STATUS == "Paused" ]]; then
    echo "⏸ ${ARTIST} - ${TITLE}"
elif [[ $PLAYER_STATUS == "Playing" ]]; then
    echo "▶ ${ARTIST} - ${TITLE}"
elif [[ $PLAYER_STATUS == "Stopped" ]]; then
    echo "󰐊 No Music Playing"
else
   echo "󰐊 Music Player Offline"
fi
