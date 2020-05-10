import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import matplotlib.pyplot as plt

#pip install -r req.txt

fs = 44100  # Sample rate
seconds = 4  # Duration of recording
windowSize = 1023
halfWindowSize = windowSize//2
globalRecord = []
trashHold = 0.03

def toSingleList(doubleList):
    tmpRecord = doubleList
    out = []
    [out.append(i[0]) for i in tmpRecord]
    return out

def getWidnowVoice():
    global globalRecord
    record = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished
    record = toSingleList(record)
    globalRecord = np.array(record)
    outArray = []
    for i in range(0,len(record)//windowSize*windowSize-halfWindowSize,halfWindowSize):
        outArray.append(record[i:int(i + windowSize)])
    hanning = np.hanning(windowSize)
    outArray = outArray[:-1]
    for i in range(len(outArray)):
        outArray[i] *= hanning
    return outArray

def getParticles(record):
    outArray = []
    for i in range(0,len(record)//windowSize*windowSize-halfWindowSize,halfWindowSize):
        outArray.append(record[i:int(i + windowSize)])
    return outArray

def restore(arr):
    out = np.zeros(len(arr) * halfWindowSize + halfWindowSize)
    index = 0
    for i in range(0,len(out) - windowSize  ,halfWindowSize):
        out[i:int(i + windowSize)] += arr[index]
        index +=1
    return out

out = getWidnowVoice()
newOut = restore(out)
fftArr = []
[fftArr.append(np.fft.fft(i)) for i in out]
fftArrAbs = np.abs(fftArr)
fftArrPhase = np.angle(fftArr)

energy = []
[energy.append(np.mean(i)) for i in fftArrAbs]

noiseFftAbs = np.zeros(windowSize)
for i in range(len(fftArrAbs)):
    if energy[i] <= trashHold:
        noiseFftAbs = (noiseFftAbs + fftArrAbs[i])/2
    fftArrAbs[i] -= noiseFftAbs


fftArr = fftArrAbs * np.exp(1j * fftArrPhase)

write('input.wav', fs, globalRecord)  # Save as WAV file 
write('output.wav', fs, restore(np.real(np.fft.ifft(fftArr))))  # Save as WAV file 

plt.subplot(211)
plt.title("orig")
plt.plot(globalRecord)
plt.subplot(212)
plt.plot((restore(np.real(np.fft.ifft(fftArr)))))
plt.show()

