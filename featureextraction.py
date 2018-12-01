import cv2
import numpy as np

class FeatureExtraction:
	def __init__(self):
		pass

	def __convexHull__(self, contour):
		hull = cv2.convexHull(contour, returnPoints=False)
		return hull

	def __convexityDefects__(self, contour, convex_hull):
		defects = cv2.convexityDefects(contour, convex_hull)
		return defects

	#finds the contours in a binary image
	#and returns the biggest one assuming
	#it is the hand contour
	def MaxContour(self, binary_img):
		im, contours, hierarchy = cv2.findContours(binary_img,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
		if len(contours) == 0:
			return None
		return max(contours, key=lambda x: x.shape[0])


	#return list of numpy arrays
	#each np array is 3*2 and has
	#start end and middle points
	def convexDefects(self, binary_img):
		contour = self.MaxContour(binary_img)
		if contour is None:
			return None, None
		contour = contour
		hull = self.__convexHull__(contour)
		defects = self.__convexityDefects__(contour, hull)

		if defects is None:
			return None, None

		convex_defects = []

		for i in range(defects.shape[0]):
			s,e,f,d = defects[i,0]
			start = np.array(contour[s][0])
			end = np.array(contour[e][0])
			middle = np.array(contour[f][0])
			defect = np.empty((3, 2), dtype=int)
			defect[0] = start
			defect[1] = end
			defect[2] = middle
			convex_defects.append(defect)

		return convex_defects, contour


	def plotDefects(self, imgRGB, defects):
		if defects is not None:
			for defect in defects:
				cv2.circle(imgRGB,tuple(defect[0]),5,[0,0,255],-1)
				cv2.circle(imgRGB,tuple(defect[1]),5,[0,0,255],-1)
				cv2.circle(imgRGB,tuple(defect[2]),5,[255,0,0],-1)
		cv2.imshow('contours', imgRGB)




if __name__ == "__main__":
	f = FeatureExtraction()
	imgrgb = cv2.imread('image2.jpg')
	img = cv2.cvtColor(imgrgb, cv2.COLOR_BGR2GRAY)
	defects, contour = f.convexDefects(img)
	for defect in defects:
		cv2.circle(imgrgb,tuple(defect[0]),5,[0,0,255],-1)
		cv2.circle(imgrgb,tuple(defect[1]),5,[0,0,255],-1)
		cv2.circle(imgrgb,tuple(defect[2]),5,[255,0,0],-1)

		cv2.imshow('con', imgrgb)
		cv2.waitKey(1000)