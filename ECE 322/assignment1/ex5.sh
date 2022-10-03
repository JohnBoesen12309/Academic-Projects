#!/bin/bash

# Filename: ex5.sh
#
# Problem: Use a case statement to give a different answer depending on whether
# a "y" or a "n" is entered.

read -p "Do you wish to open the pod bay doors?" inputVar

case $inputVar in
	y) echo "I'm sorry, Dave. I'm afraid I can't do that." ;;
	n) echo "That is good. I wouldn't open them anyway." ;;
esac


