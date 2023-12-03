
def CheckIfAllZeroes(frame, frame_size_bytes):
    for item in range(frame_size_bytes):
        if frame[item] != 0:
            return False
    return True

