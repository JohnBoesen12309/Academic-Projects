#!/bin/bash

# Filename: ex7.sh
#
# Problem: The first part of the script kills the script after 3 seconds.
# The second part of the script tries to print out Finished Nap, but is already
# killed. Change the sleep time of the kill so it is finished after the echo.

# sleep = delay
# kill = terminate process
# $$ = the PID of this script
# >& = redirect standard output and standard error to /dev/null
# /dev/null = trashcan
# (    )& = run these commands separately without blocking further commands
(sleep 5;kill $$ >& /dev/null) &

sleep 1
echo Finished Nap.



