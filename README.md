
# 🐧 NitroGen-AI Linux Port

This repository contains the necessary patches and instructions to run the NitroGen AI model on **Manjaro/Arch Linux (KDE Plasma)**. This port replaces Windows-specific dependencies (DXCam, Win32API) with Linux-native alternatives.

## 🛠 Prerequisites

### Session Requirement
NitroGen's screen capture requires an **X11 Session**. Wayland is currently unsupported due to security restrictions on screen scraping.
1. Log out of your current session.
2. Select **Plasma (X11)** from the login screen menu.
3. Verify by running: `echo $XDG_SESSION_TYPE` (should return `x11`).

### System Dependencies
Install the required X11 tools and virtual controller support:
```bash
sudo pacman -S --needed xorg-xset xorg-xrandr plasma-x11-session

This guide compiles the steps required to run the NitroGen AI model on Manjaro/Arch Linux using KDE Plasma.
1. Prerequisites

NitroGen requires an X11 Session to capture the screen. Wayland is not supported as it blocks screen scraping.

    Install Dependencies:
    Bash

    sudo pacman -S --needed xorg-xset xorg-xrandr plasma-x11-session

    Switch to X11: Log out, select Plasma (X11) from the session menu, and log back in.

    Verify Session: Run echo $XDG_SESSION_TYPE. It must say x11.

2. Core Linux Patch (nitrogen/game_env.py)

3. Launching the AI

Open three terminals and run the following:
Terminal 1: AI Inference Server
Bash

cd ~/NitroGen && source venv/bin/activate.fish
python scripts/serve.py ng.pt

Terminal 2: The Game
Bash

# Disable PRIME offload if using NVIDIA/Intel hybrid to avoid capture lag
__NV_PRIME_RENDER_OFFLOAD=0 supertux2

Terminal 3: Input Bridge
Bash

sudo chmod 0666 /dev/uinput
cd ~/NitroGen && source venv/bin/activate.fish
python scripts/play.py --process supertux2 --port 5555
