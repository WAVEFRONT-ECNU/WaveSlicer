import numpy as np
import WaveSlicer.activity_detect as vad
import librosa


def compute_bic(mfcc_v, delta):
    m, n = mfcc_v.shape
    # print(m, n)

    sigma0 = np.cov(mfcc_v).diagonal()
    eps = np.spacing(1)
    realmin = np.finfo(np.double).tiny
    det0 = max(np.prod(np.maximum(sigma0, eps)), realmin)

    flat_start = 5

    range_loop = range(flat_start, n, delta)
    x = np.zeros(len(range_loop))
    iter = 0
    for index in range_loop:
        part1 = mfcc_v[:, 0:index]
        part2 = mfcc_v[:, index:n]

        sigma1 = np.cov(part1).diagonal()
        sigma2 = np.cov(part2).diagonal()

        det1 = max(np.prod(np.maximum(sigma1, eps)), realmin)
        det2 = max(np.prod(np.maximum(sigma2, eps)), realmin)

        BIC = 0.5 * (n * np.log(det0) - index * np.log(det1) - (n - index) * np.log(det2)) - 0.5 * (
                    m + 0.5 * m * (m + 1)) * np.log(n)
        x[iter] = BIC
        iter = iter + 1

    maxBIC = x.max()
    maxIndex = x.argmax()
    if maxBIC > 0:
        return range_loop[maxIndex] - 1
    else:
        return -1


def speech_segmentation(mfccs):
    wStart = 0
    wEnd = 200
    wGrow = 200
    delta = 25

    m, n = mfccs.shape

    store_cp = []
    index = 0
    while wEnd < n:
        featureSeg = mfccs[:, wStart:wEnd]
        detBIC = compute_bic(featureSeg, delta)
        index = index + 1
        if detBIC > 0:
            temp = wStart + detBIC
            store_cp.append(temp)
            wStart = wStart + detBIC + 200
            wEnd = wStart + wGrow
        else:
            wEnd = wEnd + wGrow

    return np.array(store_cp)


def multi_segmentation(y, sr, frame_size=256, frame_shift=128, iscut_head_and_tail=True):

    mfccs = librosa.feature.mfcc(y, sr, n_mfcc=12, hop_length=frame_shift, n_fft=frame_size)
    seg_point = speech_segmentation(mfccs / mfccs.max())

    seg_point = seg_point * frame_shift
    seg_point = np.insert(seg_point, 0, 0)
    seg_point = np.append(seg_point, len(y))
    rangeLoop = range(len(seg_point) - 1)

    output_segpoint = []

    if iscut_head_and_tail:
        cut_segpoint = [0]
        for i in rangeLoop:
            temp = y[seg_point[i]:seg_point[i + 1]]
            x1, x2 = vad.vad(temp, sr=sr, framelen=frame_size, frameshift=frame_shift)
            if len(x1) == 0 or len(x2) == 0:
                continue
            elif seg_point[i + 1] == len(y):
                continue
            else:
                cut_segpoint.append(seg_point[i + 1])
        cut_segpoint.append(len(y))
        output_segpoint = cut_segpoint
    else:
        output_segpoint = seg_point

    return (np.asarray(output_segpoint) / float(sr))