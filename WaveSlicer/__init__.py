import WaveSlicer.import_file
import WaveSlicer.import_stream
import WaveSlicer.segmentation
import WaveSlicer.save
import numpy as np


def cut_audio_fromfile(path, outpath, name):
    y, sr, d = import_file.load_audio_file(path)
    segpoint = segmentation.multi_segmentation(y=y, sr=sr, frame_size=256, frame_shift=128, is_only_have_voice=True)
    save.save_wav_sequence(raw_y=y, sr=sr, segpoint=segpoint, path=outpath, name=name)
    return


def cut_audio_fromstream(outpath, name):
    sr = 16000
    filenum = 0
    isfirst = True
    stream = import_stream.open_stream(sr)
    while True:
        temp = import_stream.record_wav(stream, 5, sr)
        if isfirst:
            y = temp
            isfirst = False
        else:
            y = np.append(y, temp)
        segpoint = segmentation.multi_segmentation(y=y, sr=sr, frame_size=256, frame_shift=128,
                                                   is_only_have_voice=True)
        if len(segpoint) != 0:
            save.save_wav_sequence(raw_y=y, sr=sr, segpoint=segpoint[:-1], path=outpath, name=name, startnum=filenum)
            yt = int(segpoint[-1][0] * sr)
            y = temp[yt:]
        filenum += len(segpoint) - 1
