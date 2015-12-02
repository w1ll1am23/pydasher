#!/bin/bash

TEST=$(ps aux | grep "python2 /var/opt/pydasher/pydasher.py" | grep -v "grep")
if [ -z "$TEST" ]
then
  /usr/bin/python2 /var/opt/pydasher/pydasher.py&
fi
exit
