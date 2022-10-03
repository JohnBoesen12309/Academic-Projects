#!/usr/bin/awk -f
BEGIN {
	# This occurs at the begining of a script
	print "Fix and run the following awk script in the command line."
	print "awk '{print \"Hello\"}' > test/ex14.sol"
	# This exit is only needed if other parts of the script are defined, but
	# we don't actually want to run them. The exit is not needed if we don't
	# define the other parts of the script.
	exit
}
{
	# This occurs for each line input into awk
}
END {
	# This occurs at the end of a script after all lines
}

