import cv2
import numpy as np
import os

def findMainColor(image):

	path = os.path.dirname(os.path.abspath(__file__)) + '/static/'

	print image

	imageUrl = path + image

	print os.path.isfile(imageUrl)

	print imageUrl

	img = cv2.imread('static/' + str(image))

	print len(img)

	if img == None:

		img = cv2.imread('static/'+ image)

		if img == None:

			print "Entra in default"
			imageUrl = path + 'ano.jpg'
			img = cv2.imread(imageUrl)

	print "Dopo %s" % img

	imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	histH = cv2.calcHist([imgHsv],[0], None, [180],[0,180])
	histS = cv2.calcHist([imgHsv], [1], None, [256], [0,256])
	histV = cv2.calcHist([imgHsv], [2], None, [256], [0,256])

	maxTuple = ( [i for i,j in enumerate(histH) if j == max(histH)][0],
				 [i for i,j in enumerate(histS) if j == max(histS)][0],
				 [i for i,j in enumerate(histV) if j == max(histV)][0])

	color = np.uint8([[[maxTuple[0],maxTuple[1],maxTuple[2]]]])
	mainColor = cv2.cvtColor(color, cv2.COLOR_HSV2RGB)
	mainColor = (list(mainColor)[0][0][0], list(mainColor)[0][0][1], list(mainColor)[0][0][2])

	print "Alla fine: %s" % os.path.isfile(imageUrl)
	return mainColor

def findSURFMatch(sourceUrl, queryUrl):

	path = os.path.dirname(os.path.abspath(__file__)) + "/static/"

	source = cv2.imread(path + sourceUrl, 0)
	query = cv2.imread(path + queryUrl, 0)

	if source == None or query == None:
		# Non trovo le immagini
		print "Non trovo le immagini!"
		print sourceUrl
		print source
		print "***********"
		print queryUrl
		print query
		return -1

	surf = cv2.SURF(400)

	# Detect delle feature
	sKp, sDes = surf.detectAndCompute(source, None)
	qKp, qDes = surf.detectAndCompute(query, None)

	if len(sKp) < 7 or len(qKp) < 7:
		# Troppo pochi kp
		return -1
		
	FLANN_INDEX_KDTREE = 0	
	index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
	search_params = dict(checks=50)
	
	flann = cv2.FlannBasedMatcher(index_params, search_params)
	
	matches = flann.knnMatch(sDes, qDes, k = 2)

	good_match = 0

	for i, (m,n) in enumerate(matches):
		if m.distance < 0.7 * n.distance:
			good_match = good_match + 1
	
	return (float(good_match) / float(len(matches)) * 100)


