A Simple Notification Daemon in python for mac osx
===

Register dbus notification service by python, show in mountain lion notification center.

dependency:
  brew install dbus
  pip install dbus-python
  pip install daemon

Usage:
  python notify.py
  
  I wrote this for run WeCase on osx, to run WeCase, use notify2 replace pynotify
  pip install notify2
  import notify2 as pynotify
  
