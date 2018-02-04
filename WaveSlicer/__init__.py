import WaveSlicer.import_file
import WaveSlicer.import_stream
import WaveSlicer.segmentation
import WaveSlicer.save
import numpy as np
import threading
import librosa
from WaveSlicer.config import configs

sampling_rate = configs['stream']['sampling_rate']
buffer_size = configs['stream']['buffer_size']
buffer_time = configs['stream']['buffer_time']
frame_size = configs['segmentation']['frame_size']
frame_shift = configs['segmentation']['frame_shift']
save_path = ""
save_name = ""
__streamsavepath = ""
__streamsavename = ""
__isfirst = True
__filenum = 0
__y = np.ndarray


def cut_audio_fromfile(filepath: str, savepath=save_path, savename=save_name):
    global frame_size, frame_shift
    if savepath == "" or savename == "":
        raise IOError("Undefined filepath and filename.")
    y, sr, d = import_file.load_audio_file(filepath)
    segpoint = segmentation.multi_segmentation(y=y, sr=sr, frame_size=frame_size, frame_shift=frame_shift,
                                               is_only_have_voice=True)
    save.save_wav_sequence(raw_y=y, sr=sr, segpoint=segpoint, path=savepath, name=savename)
    return


def cut_audio_fromstream(savepath=save_path, savename=save_name):
    global sampling_rate, buffer_size, buffer_time
    global __isfirst, temp, istempchanged, __streamsavepath, __streamsavename
    __streamsavepath = savepath
    __streamsavename = savename
    stream = import_stream.open_stream(samplingrate=sampling_rate, buffersize=buffer_size)
    while True:
        temp = import_stream.record_wav(stream, buffer_time)
        tread = threading.Thread(target=__cutstream(temp))
        tread.start()
        # savename += "a"


def __cutstream(temp):
    global __isfirst, __filenum
    global __y, sampling_rate, save_path, save_name
    global frame_size, frame_shift
    # print("temp" + str(len(temp)))
    if __isfirst:
        __y = temp
        __isfirst = False
    else:
        __y = np.append(__y, temp)
    # print("B" + str(len(y)))
    # pt = savepath + str(__filenum) + ".wav"
    # librosa.output.write_wav(path=pt, y=__y, sr=sr)
    segpoint = segmentation.multi_segmentation(y=__y, sr=sampling_rate, frame_size=frame_size, frame_shift=frame_shift,
                                               is_only_have_voice=True)
    # print(str(segpoint))
    if len(segpoint) != 0:
        save.save_wav_sequence(raw_y=__y, sr=sampling_rate, segpoint=segpoint[:-1], path=save_path, name=save_name,
                               startnum=__filenum)
        # print(segpoint[-1][0])
        yt = int(segpoint[-1][0] * sampling_rate)
        __y = __y[yt:]
        # print("A" + str(len(y)))
        __filenum += len(segpoint) - 1
