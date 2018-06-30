import argparse as agp
import matplotlib.pyplot as plt	
import numpy as np
import scipy.io as sio
import os
import scipy.signal as ss

Fs = 50000000

def widmo_dB(s, N_fft , F_samp):
    S = np.fft.rfft(s,N_fft)/np.sqrt(N_fft)
    S_dB = 20*np.log10(np.abs(S))
    F = np.fft.rfftfreq(N_fft, 1/F_samp)
    return S_dB,F

parser = agp.ArgumentParser()
parser.add_argument('file')

args = parser.parse_args()


data = sio.loadmat(args.file,appendmat = False)


t = np.array(data['t'][0])
dataPmt = np.array(data['dataPmt'][0])



#filtr pasmowo-zaporowy na sieć 50 Hz i harmoniczne
dataPmt_filt=dataPmt
for i in range(1,11):
	[b, a] = ss.butter(1, [i*49.0/(Fs/2), i*51.0/(Fs/2)], btype = 'bandstop')
	dataPmt_filt = ss.filtfilt(b, a, dataPmt_filt)


widmoMocy, freq = widmo_dB(dataPmt_filt, len(dataPmt_filt), Fs)

print(len(t))
print(len(dataPmt))
print(len(freq))
print(len(widmoMocy))

fig,ax = plt.subplots()
ax.plot(t,dataPmt_filt)
ax.set_title(args.file)
plt.show()
plt.plot(freq, widmoMocy)
plt.show()