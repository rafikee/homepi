#!/bin/bash -l
cd $shoorbapi_path
/usr/bin/python3 sched_athan.py > /dev/null 2>&1
/usr/bin/python3 change_athan.py > /dev/null 2>&1