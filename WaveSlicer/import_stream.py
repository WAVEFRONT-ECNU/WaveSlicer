import pyaudio
import numpy as np
from WaveSlicer.config import configs

buffer_size = configs['stream']['buffer_size']
buffer_time = configs['stream']['buffer_time']

def record_wav(stream, time):
    global buffer_size, sampling_rate
    save_buffer = b""
    read_time_per_second = sampling_rate / buffer_size
    cnt = 0
    # print("Start Record")
    while cnt < time * read_time_per_second:
        str_data = stream.read(buffer_size)
        # print(str_data)
        save_buffer += str_data
        cnt += 1
    wave_data = np.frombuffer(save_buffer, dtype=np.float32)
    return wave_data


def open_stream(samplingrate=44100, buffersize=11025):
    pa = pyaudio.PyAudio()
    global buffer_size, sampling_rate
    buffer_size = buffersize
    sampling_rate = samplingrate
    stream = pa.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=samplingrate,
        input=True,
        frames_per_buffer=buffersize)
    return stream
