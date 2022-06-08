# pyano #

press key on midi keyboard, makes led strip colorful

I am pretty sure the script needs some adjustments by you (name of midi device, length of led strip, offset of led strip,...)

The script stops because of an error from time to time.

I use this in crontab for now. It re-runs the script when it detects that it does not run.

```
* * * * * ps aux | grep pyano | grep -v grep || /home/pi/pyano/pyano.py >/dev/null 2>&1
```
