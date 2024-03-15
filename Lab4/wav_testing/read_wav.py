import wave
import struct
import scipy.fft
import matplotlib.pyplot as plt


INPUT = "WAVs/trumpet.wav"
OUTPUT = "DATA/train.csv"
LEN = 100

def wav_to_floats(wave_file):
    w = wave.open(wave_file)
    astr = w.readframes(w.getnframes())
    # convert binary chunks to short 
    a = struct.unpack("%ih" % (w.getnframes()* w.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    return a


signal = wav_to_floats(INPUT)


x = [0.0 for i in range(LEN)]
rows = []

for i in range(len(signal)):
    y = signal[i]
    
    row = x.copy() + [y]
    rows.append(row)
    
    x = x[1:] + [y]
    
headers = [f"x{i}" for i in range(LEN)] + ["y"]

with open(OUTPUT, "w") as f:
    f.write(",".join(headers) + "\n")
    for row in rows:
        f.write(",".join(map(str, row)) + "\n")