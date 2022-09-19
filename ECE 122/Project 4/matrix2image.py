import numpy as np
import matplotlib.pyplot as plt

#file name
name=input("Enter full matrix file name: ")
#load entire matrix
A = np.loadtxt(name)


#print image of A
plt.imshow(A,cmap="binary")
plt.show()



