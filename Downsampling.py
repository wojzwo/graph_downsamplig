import argparse as agp
import matplotlib.pyplot as plt	
import numpy as np
import scipy.io as sio
import os
import scipy.signal as ss
import time

Fs = 50000000

def widmo_dB(s, N_fft , F_samp):
    S = np.fft.rfft(s,N_fft)/np.sqrt(N_fft)
    S_dB = 20*np.log10(np.abs(S))
    F = np.fft.rfftfreq(N_fft, 1/F_samp)
    return S_dB,F
	
def crosscor_square(T,length):
	# T (table) - sygnał, length - długość okna
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
        P[i]=np.exp(-2*((i+1/2-mid)/width)**2)
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
[b2,a2] = ss.butter(1, 4000/(Fs/2), btype = 'lowpass')
dataPmt_low = ss.filtfilt(b2, a2, dataPmt_filt)
dataPmt_filt -= dataPmt_low

#dataPmt_80 = crosscor_square(dataPmt_filt, 80)
#dataPmt_10 = crosscor_square(dataPmt_filt, 10)

czas_start = time.time()
dataPmt_corr = ss.correlate(dataPmt_filt, peak_gauss(3.7,15), mode = 'same')
print(time.time() - czas_start)
#widmoMocy, freq = widmo_dB(dataPmt_filt, len(dataPmt_filt), Fs)

#np.save('sygnal_po_filtrach.dat', dataPmt_corr)


fig,ax = plt.subplots()
ax.plot(dataPmt_filt, 'c')
ax.plot(dataPmt_corr, 'pink')
plt.show()
#plt.plot(freq, widmoMocy)
#plt.show()

WF=np.zeros((2,len(t)))
WF[0]=np.array(data['t'][0])
WF[1]=dataPmt
WF=np.transpose(WF)

th=-50
def dec_function(x):
    if x<th:
        return True
    return False


dsr=2000
excess=200
skipIterator=10
def downsample(T,Dec):
    i=0
    keep=np.zeros(len(T),dtype=bool)
    while i<len(T):
        if i%dsr==0:
            keep[i]=True
        if dec_function(Dec[i]):
            keep[i-excess:i+excess]=True
            i +=skipIterator-1
        i +=1
    return T[keep]

downsampled=downsample(WF,dataPmt_corr)

