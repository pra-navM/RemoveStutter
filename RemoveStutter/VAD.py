import getopt
import sys
import math
import os
import webrtcvad

# decode mp3 file specified in the cmdline
# write the decoded file as input.raw
# get attributes of mp3 file -> sample rate and put it in variable sample_rate

def ProcessVAD(tolerance, frame_duration, stutter_length, sample_rate):
    file = open("decoded.raw", "rb")
    file_write = open("processed.raw", "wb")
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0,0)

    vad = webrtcvad.Vad(int(tolerance))

    #take from other program later
    frame_size_bytes = 2*sample_rate * int(frame_duration)
    frame_size_bytes = int(2*(int(sample_rate) * int(frame_duration) / 1000))

    total_num_frames = math.floor(file_size / frame_size_bytes)
    n = 0
    ctr = 0     # how big the voiced island is
    templist = [0] * stutter_length # temporary list to hold voiced frames that you are unsure to write or not

    for num_frames in range(total_num_frames):
        file.seek(n * frame_size_bytes, 0)
        frame = file.read (frame_size_bytes)
        n += 1

        # if all zeroes, just write and go to the next frame; dont even do VAD-processing
        if CheckIfAllZeroes(frame, frame_size_bytes):
            print("All zeroes, so write")
            file_write.write(frame)
            ctr = 0
        else:
            if vad.is_speech(frame, sample_rate) == False:   # checking if speech is there in the frame
                 print("(not all_zeros and) vad_false, so dont write")
    #            file_write.write(frame)
                 ctr = 0                                      # set ctr to 0
            else:
                if ctr < stutter_length:
                    print("ctr <= " + str(stutter_length-1) + ", ctr=" + str(ctr))
                    templist[ctr] = frame
                    ctr += 1

                elif ctr == stutter_length:
                    print("ctr == " + str(stutter_length) + ", ctr=" + str(ctr))
                    for item in range(stutter_length):
                        print("write items 0-(stutter_length-1) item #=" + str(item))
                        print(str(item))
                        file_write.write(templist[item])
                        ctr += 1

                else:
                    print("ctr >= " + str(stutter_length) + ", so just write")
                    file_write.write(frame)    
        continue

    file_write.close()
    file.close()

def CheckIfAllZeroes(frame, frame_size_bytes):
    for item in range(frame_size_bytes):
        if frame[item] != 0:
            return False
    return True

