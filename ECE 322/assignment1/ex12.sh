#!/bin/bash

# Filename: ex12.sh
#
# Problem: Make the code into a function and call function using cat, dog 
# and frog as an argument.

function functionName {
	
	echo The $1 chased it tail.
	echo Then the $1 sat on a $2.

}

functionName cat mat
functionName dog kennel
functionName frog lily  

