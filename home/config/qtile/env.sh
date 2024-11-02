#!/bin/bash


systemctl --user import-environment DISPLAY WAYLAND_DISPLAY &
dbus-update-activation-environment 2>/dev/null && dbus-update-activation-environment --systemd DISPLAY WAYLAND_DISPLAY &
