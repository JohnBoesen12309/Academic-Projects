#!/bin/bash

# Filename: ex3.sh
#
# Problem: Make a script to check if a file exists. The filename is the first 
# argument passed to the script. Print that the file exists if it does, and 
# file doesn't exist if it doesn't.

if [ -e \"$1\" ]; then

	echo The file \"$1\" exists.
else

	echo The file \"$1\" does not exist.
fi
