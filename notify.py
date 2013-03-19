#!/usr/bin/env python

import logging
import time
import daemon

# mac notification center
import Foundation
import objc

# dbus
import dbus.mainloop.glib
import dbus.service
import dbus

NSUserNotification = objc.lookUpClass('NSUserNotification')
NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')

def notifycenter(title, subtitle, info_text, delay=0, sound=False, userInfo={}):
    notification = NSUserNotification.alloc().init()
    notification.setTitle_(title)
    notification.setSubtitle_(subtitle)
    notification.setInformativeText_(info_text)
    notification.setUserInfo_(userInfo)
    if sound:
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
    notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(delay, Foundation.NSDate.date()))
    NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)

class NotificationDaemon(dbus.service.Object):
    def __init__(self, objectPath):
        bus_name = dbus.service.BusName(
            "org.freedesktop.Notifications", dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, objectPath)

    @dbus.service.method(
        dbus_interface="org.freedesktop.Notifications",
        in_signature="",
        out_signature="as")
    def GetCapabilities(self):
        return ["body", "body-markup", "persistence", "icon-static"]

    @dbus.service.method(
        dbus_interface="org.freedesktop.Notifications",
        in_signature="susssava{sv}i",
        out_signature="u")
    def Notify(
        self, app_name, replaces_id, app_icon, summary,
        body, actions, hints, expire_timeout):
        notifycenter(summary, app_name, body)
        return 0

    @dbus.service.method(
        dbus_interface="org.freedesktop.Notifications",
        in_signature="u",
        out_signature="")
    def CloseNotification(self, id):
        pass

    @dbus.service.method(
        dbus_interface="org.freedesktop.Notifications",
        in_signature="",
        out_signature="ssss")
    def GetServerInformation(self):
        return ("Notifications", "freedesktop.org", "0.1", "0.7.1")

    # Signals

    @dbus.service.signal(
        dbus_interface="org.freedesktop.Notifications",
        signature="uu")
    def NotificationClosed(self, id, reason):
        pass

    @dbus.service.signal(
        dbus_interface="org.freedesktop.Notifications",
        signature="us")
    def ActionInvoked(self, id, action_key):
        pass

def main():
    logging.basicConfig(level=logging.DEBUG)

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    notifyDaemon = NotificationDaemon("/org/freedesktop/Notifications")
    daemon.daemonize("/tmp/notication-daemon-mac-py.pid")
    while True:
        time.sleep(1000)

if __name__ == '__main__':
    main()

