
import getopt
import sys
import os
import subprocess
import re
from VAD import *

version = '1.0'
verbose = False

print ('ARGV      :', sys.argv[1:])

#default values
tolerance = 2
frame_duration = 10
stutter_length = 48

options, remainder = getopt.getopt(sys.argv[1:], 'i:o:f:t:s:', ['inputfile=', 
                                                            'outputfile='
                                                            'frame_duration'
                                                            'tolerance'
                                                            'stutter_length',
                                                            ])
print ('OPTIONS   :', options)

for opt, arg in options:
    if opt in ('-i', '--inputfile'):
        inpfile = arg
    elif opt in ('-o', '--outputfile'):
        outfile = arg
    elif opt in ('-t', '--tolerance'):
        tolerance = arg
    elif opt in ('-f', '--frame_duration'):
        frame_duration = arg
    elif opt in ('-s', '--stutter_length'):
        stutter_length = int(arg)

try:
    fsrc = open (inpfile,'rb')
except IOError:
    print("Failed to open" + inpfile)
    exit()

try:
    fdest = open (outfile,'wb')
except IOError:
    print("Failed to open" + outfile)
    exit()

# retrieve sample rate
string_mp3_file_attributes = "C:\\Users\\Pranav\\Documents\\ffmpeg\\ffmpeg-2.1.1-win64-static\\ffmpeg-2.1.1-win64-static\\bin\\ffprobe.exe " + inpfile + " -show_streams"
output = subprocess.getoutput(string_mp3_file_attributes)
print(output)

sSampleRate = re.search('sample_rate=(.+?)\n', output).group(1)
sample_rate = int(sSampleRate)

if "stereo" in output:
    print('ERROR - FILE MUST HAVE ONLY ONE AUDIO CHANNEL')
    sys.exit()
if ( (sample_rate != 48000) and (sample_rate != 32000) and (sample_rate != 16000) and (sample_rate != 8000) ):
    print('ERROR - FILE MUST HAVE 48k, 32k, 16k, or 8k sample rate')
    sys.exit()

# decode mp3
string_decode_cmd = "C:\\Users\\Pranav\\Documents\\ffmpeg\\ffmpeg-2.1.1-win64-static\\ffmpeg-2.1.1-win64-static\\bin\\ffmpeg.exe -i " + inpfile + " -f s16le -c:a pcm_s16le decoded.raw"
os.system(string_decode_cmd)

fsrc.close
#----------file has been decoded, call VAD subroutine which uses intermediate subroutines

ProcessVAD(tolerance, frame_duration, stutter_length, sample_rate)

#----VAD is done, encode mp3
string_encode_cmd = "C:\\Users\\Pranav\\Documents\\ffmpeg\\ffmpeg-2.1.1-win64-static\\ffmpeg-2.1.1-win64-static\\bin\\ffmpeg.exe -f s16le -ar " + sSampleRate + " -ac 1 -i processed.raw " + outfile
print(string_encode_cmd)
os.system(string_encode_cmd)

fdest.close


