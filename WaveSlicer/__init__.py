import WaveSlicer.import_file
import WaveSlicer.import_stream
import WaveSlicer.segmentation
import WaveSlicer.save
import numpy as np
import threading
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
__isCFSrun = True


def cut_audio_fromfile(filepath: str, sp=save_path, sn=save_name):
    global frame_size, frame_shift
    if sp == "" or sn == "":
        raise IOError("Undefined filepath and filename.")
    y, sr, d = import_file.load_audio_file(filepath)
    segpoint = segmentation.multi_segmentation(y=y, sr=sr, frame_size=frame_size, frame_shift=frame_shift,
                                               is_only_have_voice=True)
    save.save_wav_sequence(raw_y=y, sr=sr, segpoint=segpoint, path=sp, name=sn)
    return


def cut_audio_fromstream_in_new_thread(sp=save_path, sn=save_name):
    global __isCFSrun
    __isCFSrun = True
    thread = threading.Thread(target=cut_audio_fromstream(sp=sp, sn=sn))
    thread.start()


def stop_cut_audio_fromstream():
    global __isCFSrun
    __isCFSrun = False


def cut_audio_fromstream(sp=save_path, sn=save_name):
    global sampling_rate, buffer_size, buffer_time
    global __isfirst, temp, istempchanged, save_path, save_name
    global __isCFSrun
    save_path = sp
    save_name = sn
    if save_path == "" or save_name == "":
        raise IOError("Undefined filepath and filename.")
    stream = import_stream.open_stream(samplingrate=sampling_rate, buffersize=buffer_size)
    while __isCFSrun:
        temp = import_stream.record_wav(stream, buffer_time)
        thread = threading.Thread(target=__cutstream(temp))
        thread.start()


def __cutstream(temp):
    global __isfirst, __filenum
    global __y, sampling_rate, save_path, save_name
    global frame_size, frame_shift
    if __isfirst:
        __y = temp
        __isfirst = False
    else:
        __y = np.append(__y, temp)
    segpoint = segmentation.multi_segmentation(y=__y, sr=sampling_rate, frame_size=frame_size, frame_shift=frame_shift,
                                               is_only_have_voice=True)
    if len(segpoint) != 0:
        save.save_wav_sequence(raw_y=__y, sr=sampling_rate, segpoint=segpoint[:-1], path=save_path, name=save_name,
                               startnum=__filenum)
        yt = int(segpoint[-1][0] * sampling_rate)
        __y = __y[yt:]
        __filenum += len(segpoint) - 1
