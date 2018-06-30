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

def crosscor_square(T,length):
    i=0
    Tlen=len(T)
    Clen=Tlen-length+1
    C=np.zeros(Clen,dtype=float)
    while i<length:
        C[0]=C[0]+T[i]
        i += 1
    i=1
    while i<Clen:
        C[i]=C[i-1]-T[i-1]+T[i+length-1]
        i+=1
    return C/length

def peak_lorenz(width,length):
    P=np.zeros(length)
    mid=length/2
    for i in range(length):
        P[i]=1/(1+((i+1/2-mid)/width)**2)
    return P/np.sum(P)

def peak_gauss(width,length):
    P=np.zeros(length)
    mid=length/2
    for i in range(length):
        P[i]=np.exp(-((i+1/2-mid)/width)**2)
    return P/np.sum(P)



data = sio.loadmat('R033_00015.mat',appendmat = False)


t = np.array(data['t'][0])
dataPmt = np.array(data['dataPmt'][0])



#filtr pasmowo-zaporowy na sieć 50 Hz i harmoniczne
dataPmt_filt=dataPmt
for i in range(1,11):
	[b, a] = ss.butter(1, [i*49.0/(Fs/2), i*51.0/(Fs/2)], btype = 'bandstop')
	dataPmt_filt = ss.filtfilt(b, a, dataPmt_filt)

dataPmt_low = dataPmt_filt
[b2,a2] = ss.butter(1, 20/(Fs/2), btype = 'lowpass')
dataPmt_low = ss.filtfilt(b2, a2, dataPmt_filt)
dataPmt_filt -= dataPmt_low

dataPmt_new=crosscor_square(dataPmt_filt,400)


#widmoMocy, freq = widmo_dB(dataPmt_filt, len(dataPmt_filt), Fs)

#print(len(t))
#print(len(dataPmt))
#print(len(freq))
#print(len(widmoMocy))

fig,ax = plt.subplots()
ax.plot(t,dataPmt)
ax.plot(t,dataPmt_filt)
plt.show()
#plt.plot(freq, widmoMocy)
#plt.show()