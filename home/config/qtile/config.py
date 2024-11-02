# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtile_extras import widget as ewgt
from libqtile import hook
from libqtile.log_utils import logger

@hook.subscribe.startup_once
async def autostart():
   # lazy.spawn("/usr/bin/swaync")
    start = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.run([start])
    
class NotificationButton(widget.TextBox):
    def __init__(self, *args, **config):
        widget.TextBox.__init__(self, *args, text=' 󰍜 ', background='#00332F', fontsize=14)
        self.add_callbacks(
            {
                "Button1": lazy.spawn('swaync-client -t')
            }
        )


mod = "mod4"
alt = "mod1"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "e", lazy.spawn("thunar"), desc="Spawn file manager"),

      #Volume control
    Key([], "XF86AudioRaiseVolume", lazy.spawn("swayosd-client --output-volume 5")), #vol up
    Key([], "XF86AudioLowerVolume", lazy.spawn("swayosd-client --output-volume -5")), #vol down
    Key([], "XF86AudioMute", lazy.spawn("swayosd-client --output-volume mute-toggle")), #vol mute
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")), #next
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")), #prev
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    
    Key([mod], "F11", lazy.spawn("ddccontrol -r 0x10 -W +20 dev:/dev/i2c-17")),
    Key([mod], "F10", lazy.spawn("ddccontrol -r 0x10 -W -20 dev:/dev/i2c-17")),

    
    Key([alt], "Space", lazy.spawn("fuzzel")),
    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panesgtk theme qtile
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window",),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    
    Key([], "Print", lazy.spawn("bash /home/presi300/.config/qtile/screenshot.sh"), desc="Take screenshot"),
    Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard(),   desc="Next keyboard layout"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)

groups = [Group(i) for i in "12345678"]


for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

def go_to_group_and_move_window(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.current_window.togroup(name, switch_group=True)
            return

        if name in "1234":
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()
        else:
            qtile.current_window.togroup(name, switch_group=False)
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()

    return _inner

def go_to_group(name: str):
    def _inner(qtile):
        if len(qtile.screens) == 1:
            qtile.groups_map[name].toscreen()
            return

        if name in '1234':
            qtile.focus_screen(1)
            qtile.groups_map[name].toscreen()
        else:
            qtile.focus_screen(0)
            qtile.groups_map[name].toscreen()

    return _inner



for i in groups:
    if i.name in "1234":
        keys.append(Key([mod], i.name, lazy.function(go_to_group(i.name)))),
        keys.append(Key([mod, "shift"], i.name, lazy.function(go_to_group_and_move_window(i.name)))),
        keys.extend([Key([mod, "control"], i.name, lazy.window.togroup(i.name),desc="move focused window to group {}".format(i.name))]
    )
    elif i.name in "5678":
        keys.append(Key([alt],  str(int(i.name) - 4), lazy.function(go_to_group(i.name)))),
        keys.append(Key([alt, "shift"], str(int(i.name) - 4), lazy.function(go_to_group_and_move_window(i.name)))),
        keys.extend([Key([alt, "control"], str(int(i.name) - 4), lazy.window.togroup(i.name),desc="move focused window to group {}".format(i.name))]),

    

layouts = [
    layout.Columns(border_focus_stack=["#ffffff", "#ffffff"], border_width=2, border_normal="#57635B", border_focus="#C3DBCB", margin=2),
    layout.Max(border_focus_stack=["#ffffff", "#ffffff"], border_width=0, border_normal="#2C5552", border_focus="#2E7671"),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="RobotoMono Nerd Font Mono",
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

keyboard = widget.KeyboardLayout(configured_keyboards=['us', 'bg phonetic'], background="00443F")

screens = [
   
    Screen(
        top=bar.Bar(
            [
                ewgt.CurrentLayoutIcon(),
                widget.Spacer(length=5),
                widget.GroupBox(highlight_method='line', use_mouse_wheel=False, disable_drag=True),
                #widget.Prompt
                widget.WidgetBox(text_closed="󰇙", text_open="󰇙", fontsize=12,  widgets=[
                    widget.WindowName(),
                ]),
                widget.Spacer(),

                widget.Clock(format="%H:%M "),
                widget.Spacer(),
                
                                
                widget.TextBox(text="\ue0ba", padding=-1, foreground="#00332F", fontsize=30),
                widget.Net(background="#00332F", interface="enp6s0", format='{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}'),
                widget.TextBox(text="\ue0bc" , padding=-1, foreground="#00332F", fontsize=30),
                
                widget.TextBox(text="\ue0ba", padding=-1, foreground="#00332F", fontsize=30),
                widget.CPU(background="#00332F"),
                widget.TextBox(text="\ue0bc" , padding=-1, foreground="#00332F", fontsize=30),
                
                widget.TextBox(text="\ue0ba", padding=-1, foreground="#00332F", fontsize=30),
                widget.Memory(background="#00332F", measure_mem='G'),
                widget.TextBox(text="\ue0bc" , padding=-1, foreground="#00332F", fontsize=30),
                
              

                widget.WidgetBox(close_button_location='right', text_closed='\ue0ba', text_open='\ue0b2', padding=-1, foreground="00443F", fontsize=30, widgets=[
                    widget.StatusNotifier(padding_x=10, padding=10),    
                    
                ]),
                keyboard,
            
                #widget.TextBox(text="", fontsize=14),

                #ewgt.WiFiIcon(interface='wlp0s20f3', padding_y=5.8, background="00443F"),
                # widget.Spacer(length=7, background="00443F"),

                #widget.Backlight(background="00443F", backlight_name='intel_backlight', fmt=' {}'),
                # widget.Spacer(length=7, background="00443F"),

                #widget.GenPollText(fontsize=14, update_interval=5, background="00443F", func=lambda: subprocess.check_output("/home/presi300/.config/qtile/battery").decode()), #battery indicator
                # widget.Spacer(length=7, background="00443F"),

                # widget.TextBox(text="󰖀", fontsize=14, background="00443F"),
                # widget.Volume(emoji=False, background="00443F", fmt="{}"),
                #this is a dirty hack, because the textbox has some sort of padding around it for some reason
                widget.TextBox(text="\ue0bc" , padding=-1, foreground="00443F", fontsize=30),

                # widget.Spacer(length=15),
                #same thing here
                widget.TextBox(text="\ue0ba", padding=-1, foreground="#00332F", fontsize=30),
                NotificationButton(text='p'),
            ],
            23,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
     Screen(
        wallpaper="/home/presi300/.config/qtile/wallpaper_miku.png",
        wallpaper_mode="fill")
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = True
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_width=2,
    border_normal="#57635B",
    border_focus="#C3DBCB",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
