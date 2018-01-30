import pyaudio
import numpy as np


def record_wav(stream, time, fs):
    buffer_size = 1000
    save_buffer = b""
    read_time_per_second = fs / buffer_size
    cnt = 0
    print("Start Record")
    while cnt < time * read_time_per_second:
        str_data = stream.read(buffer_size)
        print(str_data)
        save_buffer += str_data
        cnt += 1
    wave_data = np.frombuffer(save_buffer, dtype=np.float32)
    return wave_data


def open_stream(fs):
    pa = pyaudio.PyAudio()
    buffer_size = 1000
    stream = pa.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=fs,
        input=True,
        frames_per_buffer=buffer_size)
    return stream
