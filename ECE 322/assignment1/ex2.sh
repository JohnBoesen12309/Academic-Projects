#!/bin/bash

# Filename: ex2.sh
#
# Problem: Make a script to print out the first and third arguments to 
# the script. Then combine the two arguments in var and print var out.

echo The first argument is $1
echo The third argument is $3
var=$1$3
echo The combined first and third argument in var is $var
