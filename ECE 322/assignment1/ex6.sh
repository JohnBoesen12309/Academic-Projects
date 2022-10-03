#!/bin/bash

# Filename: ex6.sh
#
# Problem: Modify the case statement so it uses a regular expression 
# (also known as Regexp) so that any response starting with y or n, both
# capital or lower case works.

read -p "Do you wish to open the pod bay doors?" inputVar

case $inputVar in
	[Yy]+ ) echo "I'm sorry, Dave. I'm afraid I can't do that.";;
	[Nn]+ ) echo "That is good. I wouldn't open them anyway.";;
	* ) echo "Please answer yes or no.";;
esac


