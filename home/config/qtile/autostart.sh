#! /bin/bash
 
#daemon swaync
swayosd-server &
kanshi &
swaync &
# pw-metadata -n settings 0 clock.force-rate 96000
# pw-metadata -n settings 0 clock force-quantum 256

#systemctl --user start xdg-desktop-portal
#systemctl --user start xdg-desktop-portal-wlr
. /home/presi300/.config/qtile/env.sh
. /home/presi300/.config/qtile/desktop-portal.sh

# . /home/presi300/.config/qtile/alt_release &


dbus-update-activation-environment WAYLAND_DISPLAY
dbus-update-activation-environmen XDG_CURRENT_DESKTOP=qtile
dbus-update-activation-environmen DISPLAY

#daemon /usr/lib/kdeconnectd
