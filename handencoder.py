import cv2
import numpy as np
from featureextraction import FeatureExtraction as FE

class HandEncoder:
	""" This class encodes a hand in a binary image to a vector
		of 4 components the physical area in the image,  the area of the hand contour
		, sum of convex defect distances and sum of their dot product as a measure of the angle"""
	def __init__(self):
		self.fe = FE()


	#this function the binary image and encodes it
	def encode(self, binary_img):
		defects, contour = self.fe.convexDefects(binary_img)
		physical_area = np.sum(binary_img)
		area = 0
		sum_distance = 0
		sum_angels = 0
		if contour is not None:
			area = cv2.contourArea(contour)
			if defects is not None:
				for defect in defects:
					vector1 = defect[2] - defect[0]
					vector2 = defect[2] - defect[1]
					sum_distance += np.linalg.norm(vector1) + np.linalg.norm(vector2)
					sum_angels += np.dot(vector1.T, vector2)
		return np.array([physical_area, area, sum_distance, sum_angels])