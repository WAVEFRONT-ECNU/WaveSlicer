import WaveSlicer

raw = input("Input raw file name:")
WaveSlicer.cut_audio_fromfile(raw, sp="output/", sn="test")
