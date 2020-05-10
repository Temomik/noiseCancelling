import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import numpy as np

fs = 44100  # Sample rate
seconds = 3  # Duration of recording
windowSize = 1024
halfWindowSize = windowSize//2
globalRecord = []
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
    return np.hanning(windowSize) * outArray

def getParticles(record):
    outArray = []
    for i in range(0,len(record)//windowSize*windowSize-halfWindowSize,halfWindowSize):
        outArray.append(record[i:int(i + windowSize)])
    return outArray

def restore(arr):
    out = np.zeros(len(arr) * halfWindowSize + halfWindowSize)
    index = 0
    for i in range(0,len(out) - halfWindowSize ,halfWindowSize):
        out[i:int(i + windowSize)] += arr[index]
        index +=1
    return out

out = getWidnowVoice()
print(len(out))
newOut = restore(out)
print(len(newOut))
print(len(globalRecord))

# s = range(44100)
# p = getParticles(s)
# p = np.hanning(windowSize) * p 
# r = restore(p)

# print(len(s))
# print(len(p[0]))
# print(len(r))


# plt.subplot(311)
# plt.plot(s[0:len(r)]-r)
# plt.subplot(312)
# plt.plot(r)
# plt.subplot(313)
# plt.plot(s[0:len(r)])
# plt.show()

# plt.plot(globalRecord[0:len(newOut)]-newOut)
# plt.subplot(311)
# plt.plot(globalRecord[0:len(newOut)]-newOut)
# plt.subplot(312)
# plt.plot(newOut)
# plt.subplot(313)
# plt.plot(globalRecord[0:len(newOut)])
# plt.show()
write('input.wav', fs, globalRecord)  # Save as WAV file 
write('output.wav', fs, np.array(newOut))  # Save as WAV file 

# kek = np.hanning(13)
# [print(i[2]) for i in out]
# print("start")
# noice = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
# sd.wait()  # Wait until recording is finished
# print("stop")

# print("start")
# myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
# sd.wait()  # Wait until recording is finished
# print("stop")
# write('iput.wav', fs, myrecording)  # Save as WAV file 
# toSingleList(noice)
# toSingleList(myrecording)

# plt.subplot(311)
# plt.plot(np.fft.fft(noice))
# plt.subplot(312)
# plt.plot(np.fft.fft(myrecording))
# plt.subplot(313)
# plt.plot(np.fft.ifft(np.fft.fft(myrecording) - np.fft.fft(noice)))
# plt.show()

# write('output.wav', fs, np.abs(np.fft.ifft(np.fft.fft(myrecording).real - np.fft.fft(noice).real)))  # Save as WAV file 