#!/bin/bash

export XDG_CURRENT_DESKTOP=qtile
export XDG_SESSION_TYPE=wayland
export GDK_BACKEND=wayland,x11
export MOZ_ENABLE_WAYLAND=1
export ELECTRON_OZONE_PLATFORM_HINT=wayland
export QT_QPA_PLATFORM=wayland
export _JAVA_AWT_WM_NONREPARENTING=1
export SDL_VIDEODRIVER="wayland,x11"

dbus-run-session qtile start -b wayland
