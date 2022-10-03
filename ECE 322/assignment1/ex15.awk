BEGIN {
	count=0;
}
{
	count++;
}
END {
print "Number of Lines in file: " count
}

