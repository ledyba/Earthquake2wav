#! python

import struct
import wave
import csv
import functools

def conv(csvfname, outfname, factor):
	with open(csvfname, 'r') as f:
		c = csv.reader(f)
		for _ in range(0,7):
			next(c)
		dat = []
		for row in c:
			dat.append(float(row[0]))
			dat.append(float(row[1]))
		def max_f(x,y):
			if abs(x) >= abs(y):
				return abs(x)
			else:
				return abs(y)
		max = functools.reduce(max_f, dat, 0)
		dat = [(int(x/max * (65535/2) * 0.5)) for x in dat]
		dat = sum([ [x]*factor for x in dat ], [])
		d = struct.pack('<'+('h'*len(dat)), *dat);
		wav = wave.open(outfname, "w")
		wav.setparams( (2, 2, 44100, len(dat)*2, 'NONE', 'not compressed') )
		wav.writeframesraw(d)
		wav.close()

conv("L3114BF1.csv", "out.wav", 5)
