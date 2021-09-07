import numpy as np

# def centroid(*arrays):
#     min_dist = None
#     for a in arrays:
#         sum = 0
#         for b in arrays:
#             sum += np.linalg.norm(a-b)
#         if min_dist == None or sum < min_dist:
#             min_dist = sum
#             centroid = a

#     return centroid

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