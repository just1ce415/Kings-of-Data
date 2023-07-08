import numpy as np
import cv2


DISR_THRESHOLD = 0.2
FEAT_THRESHOLD = 5
K = 3

def clasify(img1, img2):

    img1 = cv2.resize(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), (256, 256))
    img2 = cv2.resize(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), (256, 256))

    best_matches = sift_compute(img1, img2, DISR_THRESHOLD, K)

    if len(best_matches) < FEAT_THRESHOLD or best_matches is None:
        return 0
    else:
        return 1

def sift_compute(img1, img2, threshold, k):
    sift = cv2.SIFT_create()

    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    try:
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=k)

    except Exception as e:
        return []
    
    try:
      if k == 3:
          ft, sd, th = zip(*matches)
          mask = np.array([ft[i].distance < threshold * sd[i].distance and ft[i].distance < threshold * th[i].distance for i in range(len(ft))])
          good = np.array([ft[i] for i, m in enumerate(mask) if m])
      else:
          ft, sd = zip(*matches)
          mask = np.array([ft[i].distance < threshold * sd[i].distance for i in range(len(ft))])
          good = np.array([ft[i] for i, m in enumerate(mask) if m])

    except Exception as e:
        return []

    return good
