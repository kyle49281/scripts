import numpy as np
import statistics as stats

filename = "stars4.data"

with open(filename, "r") as infile, open("output.txt", "w") as outfile:
    for line in infile:
        modified_line = line.replace('"', '')
        outfile.write(modified_line)

data = np.genfromtxt("output.txt", delimiter=',',dtype= None)

app_mag= data[1:, 3]
BVcolor_index=data[1:,5]
VIcolor_index=data[1:,6]
parallax=data[1:, 4] #milli-arcsec to arsec
parallax=[float(i)/1000 for i in parallax]
spectral_type=data[1:,7]

tuples = [(float(appmag)+5*(np.log(para)+1),BV ,VI ,spec) for appmag, spec, para, BV, VI in zip(app_mag, spectral_type ,parallax, BVcolor_index, VIcolor_index) 
          if spec.lower().startswith('f') and spec.lower().endswith('v') and spec[-2].isdigit() ]

abs_mag_main=[]
bv_main=[]
vi_main=[]
spec_main=[]
for i in range(len(tuples)):
    abs, bv, vi, spec = tuples[i]
    abs_mag_main.append(abs)
    bv_main.append(float(bv))
    vi_main.append(float(vi))
    spec_main.append(spec)


print(f'''statistic values of F-type main-sequence stars:\nabsolute magnitude: mean = {stats.mean(abs_mag_main):.3f}, standard deviation = {stats.stdev(abs_mag_main):.3f}.''')
print(f'(B-V) color index: mean = {stats.mean(bv_main):.3f}, standard deviation = {stats.stdev(bv_main):.3f}')
print(f'(V-I) color index: mean = {stats.mean(vi_main):.3f}, standard deviation = {stats.stdev(vi_main):.3f}')
print(data.shape)