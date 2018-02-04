import WaveSlicer

raw = input("Input raw file name:")
WaveSlicer.cut_audio_fromfile(raw,savepath="/output",savename="test")
