import WaveSlicer.import_file
import WaveSlicer.segmentation
import WaveSlicer.save


def cut_audio_fromfile(path, outpath, name):
    y, sr, d = import_file.load_audio_file(path)
    segpoint = segmentation.multi_segmentation(y=y, sr=sr, frame_size=256, frame_shift=128, iscut_head_and_tail=True)
    save.save_wav_sequence(raw_y=y,sr=sr,segpoint=segpoint,path=outpath,name=name)
    return
