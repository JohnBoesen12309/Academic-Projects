 #!/bin/bash

# Filename: ex18.sh
#
# Problem: Find the highest number for each line and print it. 
cat ex18.input | awk '{max=0; for (ii=1;ii<=NF; ii++) { if ($ii>max) {max=$ii}}; print max
	
	}'
