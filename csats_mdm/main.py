#!/usr/bin/env python3

import json
import os
import pkg_resources
import socket
import sys

# Pull screen saver settings from user configuration. I don't love these blind
# fallbacks, but they appear to be robust. I tested it on four different
# systems, two 18.04 LTS and one 16.04 LTS. I didn't dig into GNOME-land far
# enough to understand why sometimes gsettings has valid configuration
# information and other times dconf does.

# Descriptions below are from gsettings.
# For example: `gsettings describe org.gnome.desktop.session idle-delay`

# The number of seconds of inactivity before the session is considered idle.
# example: 'uint32 300'
idleDelayRaw = os.popen('gsettings get org.gnome.desktop.session idle-delay').read()
if len(idleDelayRaw) < 1:
    idleDelayRaw = os.popen('dconf read /org/gnome/desktop/session/idle-delay').read()
idleDelay = int(idleDelayRaw.split()[1])

# The number of seconds after screensaver activation before locking the screen.
# example: 'uint32 0'
lockDelayRaw = os.popen('gsettings get org.gnome.desktop.screensaver lock-delay').read()
if len(lockDelayRaw) < 1:
    lockDelayRaw = os.popen('dconf read /org/gnome/desktop/screensaver/lock-delay').read()
lockDelay = int(lockDelayRaw.split()[1])

# Set this to TRUE to lock the screen when the screensaver goes active.
# example: 'true'
lockEnabledString = os.popen('gsettings get org.gnome.desktop.screensaver lock-enabled').read().rstrip()
if len(lockEnabledString) < 1:
    lockEnabledString = os.popen('dconf read /org/gnome/desktop/screensaver/lock-enabled').read().rstrip()
lockEnabled = (True if lockEnabledString == 'true' else False)

# example: 'E3PDCG001T3K'
machineId = os.popen('sudo dmidecode --string system-serial-number').read().rstrip()

# compute compliance of above values
compliant = idleDelay <= 300 and lockDelay == 0 and lockEnabled

# assemble and output machine info
machineInfo = {
    'mdmVersion': pkg_resources.get_distribution('csats_mdm').version,
    'idleDelay': idleDelay,
    'lockDelay': lockDelay,
    'lockEnabled': lockEnabled,
    'machineId': machineId,
    'compliant': compliant,
}
machineInfoJson = json.dumps(machineInfo, separators=(',', ':'))

message = 'cyberaudit {}\n'.format(machineInfoJson).encode()

if len(sys.argv) > 1 and sys.argv[1] == '--dry-run':
    print('DRY RUN - will not send to papertail')
    print(message)
else:
    # here's a socket-based implementation of something like this shell code →
    # echo "cyberaudit - $USER upgraded sea-hq.csats.pizza UniFi controller to version 5.12.35-12979-1 on $(date)" | nc -w0 -v localhost 12004
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 12004))
        s.sendall(message)
