import WaveSlicer

def fileDemo():
    raw = input("Input raw file name:")
    WaveSlicer.cut_audio_fromfile(raw, sp="output/", sn="test")

def streamDemo():
    WaveSlicer.cut_audio_fromstream("output/", "1")

if __name__ == "__main__" :
    print("Choose mode: \n1.From File \n2.From Stream \n")
    mode = input()
    if mode == 1:
        fileDemo()
    elif mode == 2:
        streamDemo()