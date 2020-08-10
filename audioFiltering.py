# -*- coding: utf-8 -*-
"""
realizovano u Spyder Editoru

naziv skripte: audioFiltering.py
autor: Nebojsa Jovanovic, student
mesto: Elektrotehnicki fakultet, Univerziteta u Beogradu
datum: 18. decembar 2019. godine

"""
# biblioteke koje se koriste
import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
import math

# ucitavanje song.wav signala
fs, dat = wavfile.read('song.wav', mmap = False)

# izdvajanje signala [u sekundama] u odabranom opsegu
poc_trenutak = 140
kraj_trenutak = 150

poc_odbirci = poc_trenutak * fs
kraj_odbirci = kraj_trenutak * fs

data_dec1 = list(dat[poc_odbirci:kraj_odbirci, 0])
vreme = np.linspace(0., (kraj_odbirci - poc_odbirci)/fs, len(data_dec1))

# prikaz audio signala u vremenskom domenu
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(vreme, data_dec1, color = 'royalblue', linewidth = 2)
plt.xlabel('Vreme [s]')
plt.ylabel('amplituda [a.u.]')
plt.grid(True)
plt.title('Audio signal')
plt.show()

# prikaz FFT-a audio signala
sigF = np.fft.fft(data_dec1)
freq = np.fft.fftfreq( len(data_dec1) )
freq = freq * fs

plt.plot(freq, abs(sigF.real))
plt.xlabel('frekvencija [Hz]')
plt.xlim(0, fs/2)
plt.ylabel('a.u.')
plt.grid(True)
plt.title('FFT audio signala')
plt.show()

# filtriranje audio signala filtrom propusnikom opsega

low_freq = 500.0 # u Hz
high_freq = 1000.0

wn1 = (low_freq*2) / fs
wn2 = (high_freq*2) / fs

b, a = signal.butter(3, [wn1, wn2], btype = 'band')
dataFilt = signal.filtfilt(b, a, data_dec1)

sigFF = np.fft.fft(dataFilt)
freq = np.fft.fftfreq( len(dataFilt) )
freq = freq * fs

# prikaz Furijeove transformacije filtriranog signala
plt.plot(freq, abs(sigFF.real))
plt.xlabel('frekvencija [Hz]')
plt.xlim(0, 2500)
plt.ylabel('a.u.')
plt.grid(True)
plt.title('FFT filtriranog audio signala')
plt.show()

# NAPOMENA:
# Potrebno je rezultujuci fajl konvertovati u .mp3
# pomocu nekog od online konvertera kako bi ga
# Windows media player uspesno pustio

# snimanje signala u .wav fajl
wavfile.write('Filtriran.wav', fs, dataFilt)
