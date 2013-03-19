A Simple Notification Daemon in python for mac osx
===

Register dbus notification service by python, show in mountain lion notification center.

dependency:

    brew install dbus
    pip install dbus-python
    pip install daemon

Usage:

    #start dbus first
    launchctl load -w /usr/local/opt/d-bus/org.freedesktop.dbus-session.plist

    python notify.py
