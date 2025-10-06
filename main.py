#!/usr/bin/env python3
import socket
import getpass
import platform
import os
import psutil
import subprocess

# Get distro name
def get_distro_name():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.strip().split("=")[1].strip('"')
    except FileNotFoundError:
        return None

# Find amount of packages
def get_package_count():
    managers = {
        "pacman": "pacman -Q",
        "dpkg": "dpkg -l | grep '^ii'",
        "rpm": "rpm -qa",
        "apk": "apk info",
        "xbps-query": "xbps-query -l",
        "pkg": "pkg info"
    }

    for cmd, query in managers.items():
        if subprocess.call(f"which {cmd}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            try:
                output = subprocess.check_output(query + " | wc -l", shell=True)
                return int(output.strip())
            except Exception:
                return None
    return None

pkg_count = get_package_count()


print(f"Distro: {get_distro_name()}")
print(f"Hostname: {socket.gethostname()}")
print(f"User: {getpass.getuser()}")
print(f"Kernel: {platform.system()} {platform.release()}")
if pkg_count is not None:
    print(f"Packages: {pkg_count}")
else:
    print("Packages: Unknown")
print(f"PyFetch Version: 1.0.0 Lite")
print(f"CPU: {os.uname().machine}")
print(f"RAM: {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
