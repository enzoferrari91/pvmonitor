#!/bin/bash
ps cax | grep python2.7 > /dev/null
if [ $? -eq 0 ]; then
  echo "Process is running."
else
  echo "Process is not running."
fi
