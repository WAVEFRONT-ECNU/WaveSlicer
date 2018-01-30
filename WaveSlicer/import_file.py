# coding=utf-8
"""
This is the module to import media files;
"""

import librosa


def load_audio_file(filename: str):
    """
    Open audio file.
    :param filename: The file path to open.
    :return:    y: audio time series
                sr: sampling rate of y
                d: Duration (in seconds)
    """
    y, sr = librosa.load(path=filename, mono=True)
    d = librosa.get_duration(y=y, sr=sr)
    return y, sr, d
