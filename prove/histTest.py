import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('prova.jpg')
imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

histH = cv2.calcHist([imgHsv],[0], None, [180],[0,180])
histS = cv2.calcHist([imgHsv], [1], None, [256], [0,256])
histV = cv2.calcHist([imgHsv], [2], None, [256], [0,256])

max = ( [i for i,j in enumerate(histH) if j == max(histH)][0],
		[i for i,j in enumerate(histS) if j == max(histS)][0],
		[i for i,j in enumerate(histV) if j == max(histV)][0])

color = np.uint8([[[max[0],max[1],max[2]]]])

print color

mainColor = cv2.cvtColor(color, cv2.COLOR_HSV2RGB)

return mainColor
