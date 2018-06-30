import argparse as agp
import matplotlib.pyplot as plt	
import numpy as np
import scipy.io as sio
import os


parser = agp.ArgumentParser()
parser.add_argument('file')

args = parser.parse_args()


data = sio.loadmat(args.file,appendmat = False)
t = np.array(data['t'][0])
dataPmt = np.array(data['dataPmt'][0])

fig,ax = plt.subplots()
ax.plot(t,dataPmt)
ax.set_title(args.file)
plt.show()