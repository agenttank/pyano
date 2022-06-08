program stops because of error from time to time

I use this in crontab for now l, it re-runs the script when it detects that it does not run.


@reboot /home/pi/pyano/pyano.py >/tmp/pyano 2>&1 
* * * * * ps aux | grep pyano | grep -v grep || /home/pi/pyano/pyano.py >/tmp/pyano 2>&1
