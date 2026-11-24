mkdir -p ~/.config/mango
cat << 'EOF' > ~/.config/mango/autostart.sh
#!/bin/sh
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=wlroots
waybar &
swaync &
nm-applet &
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
/usr/lib/xdg-desktop-portal-wlr &
swaybg -m fill -i /home/blanc/Downloads/wp11291027-greek-aesthetic-pc-wallpapers.jpg &
EOF
chmod +x ~/.config/mango/autostart.sh
