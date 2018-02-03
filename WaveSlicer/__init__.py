import WaveSlicer.import_file
import WaveSlicer.import_stream
import WaveSlicer.segmentation
import WaveSlicer.save
import numpy as np
import threading
import librosa


def cut_audio_fromfile(path, outpath, name):
    y, sr, d = import_file.load_audio_file(path)
    segpoint = segmentation.multi_segmentation(y=y, sr=sr, frame_size=256, frame_shift=128, is_only_have_voice=True)
    save.save_wav_sequence(raw_y=y, sr=sr, segpoint=segpoint, path=outpath, name=name)
    return


def cut_audio_fromstream(outpath, name):
    global sr
    global __isfirst, temp, istempchanged, savepath, savename
    savepath = outpath
    savename = name
    stream = import_stream.open_stream(sr)
    while True:
        temp = import_stream.record_wav(stream, 5, sr)
        tread = threading.Thread(target=__cutstream(temp))
        tread.start()
        savename += "a"


__isfirst = True
__filenum = 0
y = np.ndarray
sr = 44100
savepath = ""
savename = ""


def __cutstream(temp):
    global __isfirst, __filenum
    global y, sr, savepath, savename
    # print("temp" + str(len(temp)))
    if __isfirst:
        y = temp
        __isfirst = False
    else:
        y = np.append(y, temp)
    # print("B" + str(len(y)))
    pt = savepath + str(__filenum) + ".wav"
    librosa.output.write_wav(path=pt, y=y, sr=sr)
    segpoint = segmentation.multi_segmentation(y=y, sr=sr, frame_size=1200, frame_shift=600,
                                               is_only_have_voice=True)
    # print(str(segpoint))
    if len(segpoint) != 0:
        save.save_wav_sequence(raw_y=y, sr=sr, segpoint=segpoint[:-1], path=savepath, name=savename, startnum=__filenum)
        # print(segpoint[-1][0])
        yt = int(segpoint[-1][0] * sr)
        y = y[yt:]
        # print("A" + str(len(y)))
        __filenum += len(segpoint) - 1
