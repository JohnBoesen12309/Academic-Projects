#!/bin/bash

# Filename: ex15.sh
#
# Problem: Design an awk script that counts how many lines are in the ex15.sh
# file. Do not edit ex15.sh, only edit ex15.awk.

cat $0 | awk -f ex15.awk
