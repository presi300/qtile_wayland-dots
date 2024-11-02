#! /bin/bash
 
#daemon swaync
swayosd-server &
kanshi &
swaync &



. /home/presi300/.config/qtile/env.sh
. /home/presi300/.config/qtile/desktop-portal.sh

dbus-update-activation-environment WAYLAND_DISPLAY
dbus-update-activation-environmen XDG_CURRENT_DESKTOP=qtile
dbus-update-activation-environmen DISPLAY

