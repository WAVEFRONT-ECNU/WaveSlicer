import librosa


def save_wav_sequence(raw_y, sr, segpoint, path:str, name:str):
    # segpoint = []
    # for sp in segpointtime:
        # segpoint.append(int(sp * sr))
    rangeloop = range(len(segpoint))
    for i in rangeloop:
        temp_y = raw_y[int(segpoint[i][0]*sr):int(segpoint[i][1]*sr)]
        sp = path + name + "_" + str(i) + ".wav"
        librosa.output.write_wav(path=sp, y=temp_y, sr=sr)
    return
