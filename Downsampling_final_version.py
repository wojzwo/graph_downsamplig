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
 
def peak_gauss(width,length):
	P=np.zeros(length)
	mid=length/2
	for i in range(length):
		P[i]=np.exp(-2*((i+1/2-mid)/width)**2)
	return P/np.sum(P)

def dec_function(x, th=-50):
	'''th - treshhold; wartość graniczna, od której uznajemy, że zaszło zdarzenie'''
	if x<th:
		return True
	return False

def downsampleTable(Dec, downsampling_rate = 2000, excess = 200, skipIterator = 10):
	'''Dec - decision table; 
	downsampling_rate, excess - liczba punktów dookoła zdarzenia
	'''
	i=0
	keep=np.zeros(len(Dec),dtype=bool)
	keep[::downsampling_rate] = True
	while i<len(Dec):
		if dec_function(Dec[i]):
			keep[i-excess:i+excess]=True
			i +=skipIterator-1
		i +=1
	return keep

parser = agp.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()
data = sio.loadmat(args.file,appendmat = False)

t = np.array(data['t'][0])
dataPmt = np.array(data['dataPmt'][0])


#filtr pasmowo-zaporowy na sieć 50 Hz i harmoniczne
dataPmt_filt=dataPmt
#for i in range(1,5):
#	[b, a] = ss.butter(1, [i*49.0/(Fs/2), i*51.0/(Fs/2)], btype = 'bandstop')
#	dataPmt_filt = ss.filtfilt(b, a, dataPmt_filt)

#filtr górnoprzepustowy (filtrowanie dolnoprzepustowe i odjęcie od sygnału)

cutoff_freq = 4000 #częstotliwość odcięcia
[b2,a2] = ss.butter(1, cutoff_freq/(Fs/2), btype = 'lowpass')
dataPmt_low = ss.filtfilt(b2, a2, dataPmt_filt)
dataPmt_filt = dataPmt_filt.astype(float) - dataPmt_low #przefiltrowany sygnał - można go użyć do analizy danych

dataPmt_corr = ss.correlate(dataPmt_filt, peak_gauss(3.7,15), mode = 'same')

keepT=downsampleTable(dataPmt_corr)

WF=np.zeros((2,len(t)))
WF[0]=np.array(data['t'][0])
WF[1]=dataPmt
WF=np.transpose(WF)
dataPmt_DS=WF[keepT]

WF=np.zeros((2,len(t)))
WF[0]=np.array(data['t'][0])
WF[1]=dataPmt_corr
WF=np.transpose(WF)
dataPmt_corr_DS=WF[keepT]


#plt.plot(t, dataPmt, 'c') #wykres danych bez filtrów i downsamplingu
plt.plot(dataPmt_DS[:,0], dataPmt_DS[:,1] , color = '#00FF00') #wykres po downsamplingu danych bez filtrowania
plt.title('Wykres po downsamplingu danych bez filtrowania')
plt.show()
plt.plot(dataPmt_corr_DS[:,0], dataPmt_corr_DS[:,1] , color = '#00FF00') #wykres po downsamplingu i po filtrowaniu
plt.title('Wykres po downsamplingu i po filtrowaniu')
plt.show()

print('''Długość sygnału zredukowano z {} do {} próbek,
czyli {:.0f}-krotnie.'''.format(len(t), len(dataPmt_DS[:,0]), len(t)/len(dataPmt_DS[:,0])))


# do oglądania widm:

#widmoMocy, freq = widmo_dB(dataPmt, len(dataPmt_filt), Fs)
#widmoMocy2, freq2 = widmo_dB(dataPmt_filt, len(dataPmt_filt), Fs)
#widmoMocy3, freq3 = widmo_dB(dataPmt_corr, len(dataPmt_corr), Fs)

#plt.plot(freq, widmoMocy)
#plt.plot(freq, widmoMocy2)
#plt.plot(freq, widmoMocy3)
#plt.show()