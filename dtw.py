import numpy as np
import librosa

def extract_features_from_file(audio_file_path):
    y, sr = librosa.load(audio_file_path)

    return extract_features(y)

def extract_features(array):
    return librosa.lpc(array, 2)

def centroid(*arrays):
    min_d = None
    for i in range(arrays):
        distance = 0
        for j in range(arrays):
            if j != i:
                distance += dtw(arrays[i], arrays[j])
        if min_d == None or distance < min_d:
            min_d = distance
            centroid = arrays[i]

    return centroid

def d(a,b):
    return np.linalg.norm(a-b)

def D(i, j, a, b):
    if i == 0 and j == 0:
        return d(a[i],b[j])
    if i == 0:
        return D(i,j-1,a,b) + d(a[i],b[j])
    if j == 0:
        return D(i-1,j,a,b) + d(a[i],b[j])
    return min(D(i-1,j,a,b), D(i,j-1,a,b), D(i-1,j-1,a,b)) + d(a[i],b[j])

def dtw(a, b):
    return D(len(a)-1, len(b)-1, a, b)