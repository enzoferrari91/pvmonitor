#!/bin/bash
ps cax | grep python2.7 > /dev/null
if [ $? -eq 0 ]; then
  echo "$(date) -- Process is running." >> /home/pi/pvmonitor-logs/log_process.txt
else
  echo "$(date) -- Process is not running." >> /home/pi/pvmonitor-logs/log_process.txt
fi
