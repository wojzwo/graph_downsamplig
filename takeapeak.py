import argparse as agp
import matplotlib.pyplot as plt	
import numpy as np
import scipy.io as sio
import os


data = sio.loadmat('R033_00015.mat',appendmat = False)

t = np.array(data['t'][0])
dataPmt = np.array(data['dataPmt'][0])

plt.figure(figsize=(30, 20))
fig,ax = plt.subplots()
ax.plot(t,dataPmt)
plt.show()