# pyano #

press key on midi keyboard, makes led strip colorful

I am pretty sure the script needs some adjustments by you (name of midi device, length of led strip, offset of led strip,...)

The script stops because of an error from time to time.

I use this in crontab for now. It re-runs the script at every boot and reboots when it detects that it does not run.

```
@reboot /home/pi/pyano/pyano.py >/tmp/pyano 2>&1
* * * * * ps x | grep pyano | grep -v grep || /usr/sbin/reboo
```
