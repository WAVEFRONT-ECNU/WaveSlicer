import librosa


def save_wav_sequence(raw_y, sr, segpointtime, path:str, name:str):
    segpoint = []
    for sp in segpointtime:
        segpoint.append(int(sp * sr))
    rangeloop = range(len(segpoint) - 1)
    for i in rangeloop:
        temp_y = raw_y[segpoint[i]:segpoint[i + 1]]
        sp = path + name + "_" + str(i) + ".wav"
        librosa.output.write_wav(path=sp, y=temp_y, sr=sr)
    return
