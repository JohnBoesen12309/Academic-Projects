#!/bin/bash

# Filename: ex9.sh
#
# Problem: Add two input numbers together.

echo -n Input a number:
read val
echo -n Input a second number:
read val2
total=$((val+val2))
echo Result is $total.
