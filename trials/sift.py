import cv2
import numpy as np
from skimage.feature import hog
from skimage.filters import gaussian
from featureextraction import FeatureExtraction

class MiniSIFT:
	def __init__(self, num_scale_levels=5, k=1.4142135623730951, sigma=0.707107):
		self.num_scale_levels = num_scale_levels
		self.sigma = sigma
		self.k = k
		self.Gaussians = []
		self.DoGs = []


	def buildDoGPyramid(self, img):
		sigma = self.sigma

		self.Gaussians = []
		self.DoGs = []

		#gaussian_img = cv2.GaussianBlur(img,(5,5), sigma)
		gaussian_img = gaussian(img, sigma)
		self.Gaussians.append(gaussian_img)


		for i in range(1, self.num_scale_levels):
			sigma *= self.k
			gaussian_img = gaussian(img, sigma)
			self.Gaussians.append(gaussian_img)
			self.DoGs.append(self.Gaussians[i] - self.Gaussians[i - 1])


	def getSmoothedfromPoint(self, point):
		x = point[0]
		y = point[1]
		sigma = None
		smoothed_image = None
		for i in range(1, len(self.DoGs) -1):
			val = self.DoGs[i][x, y]
			x_after = min(x + 1, self.DoGs[i].shape[0] - 1)
			x_before = max(x - 1, 0)
			y_after = min(y + 1, self.DoGs[i].shape[1] - 1)
			y_before = max(y - 1, 0)
			if ((val > 0 and val >= self.DoGs[i][x_after, y] and val >= self.DoGs[i][x_before, y] and val >= self.DoGs[i][x, y_after] and val >= self.DoGs[i][x, y_before]
				and val >= self.DoGs[i][x_after, y_after] and val >= self.DoGs[i][x_after, y_before] and val >= self.DoGs[i][x_before, y_after] and val >= self.DoGs[i][x_before, y_before]
				and val >= self.DoGs[i-1][x_after, y] and val >= self.DoGs[i-1][x_before, y] and val >= self.DoGs[i-1][x, y_after] and val >= self.DoGs[i-1][x, y_before]
				and val >= self.DoGs[i-1][x_after, y_after] and val >= self.DoGs[i-1][x_after, y_before] and val >= self.DoGs[i-1][x_before, y_after] and val >= self.DoGs[i-1][x_before, y_before]
				and val >= self.DoGs[i-1][x, y] and val >= self.DoGs[i-1][x, y] and val >= self.DoGs[i+1][x_after, y] and val >= self.DoGs[i+1][x_before, y] 
				and val >= self.DoGs[i+1][x, y_after] and val >= self.DoGs[i+1][x, y_before]
				and val >= self.DoGs[i+1][x_after, y_after] and val >= self.DoGs[i+1][x_after, y_before] and val >= self.DoGs[i+1][x_before, y_after] and val >= self.DoGs[i+1][x_before, y_before]
				and val >= self.DoGs[i+1][x, y] and val >= self.DoGs[i+1][x, y])
				or
				(val < 0 and val <= self.DoGs[i][x_after, y] and val <= self.DoGs[i][x_before, y] and val <= self.DoGs[i][x, y_after] and val <= self.DoGs[i][x, y_before]
				and val <= self.DoGs[i][x_after, y_after] and val <= self.DoGs[i][x_after, y_before] and val <= self.DoGs[i][x_before, y_after] and val <= self.DoGs[i][x_before, y_before]
				and val <= self.DoGs[i-1][x_after, y] and val <= self.DoGs[i-1][x_before, y] and val <= self.DoGs[i-1][x, y_after] and val <= self.DoGs[i-1][x, y_before]
				and val <= self.DoGs[i-1][x_after, y_after] and val <= self.DoGs[i-1][x_after, y_before] and val <= self.DoGs[i-1][x_before, y_after] and val <= self.DoGs[i-1][x_before, y_before]
				and val <= self.DoGs[i-1][x, y] and val <= self.DoGs[i-1][x, y] and val <= self.DoGs[i+1][x_after, y] and val <= self.DoGs[i+1][x_before, y] 
				and val <= self.DoGs[i+1][x, y_after] and val <= self.DoGs[i+1][x, y_before]
				and val <= self.DoGs[i+1][x_after, y_after] and val <= self.DoGs[i+1][x_after, y_before] and val <= self.DoGs[i+1][x_before, y_after] and val <= self.DoGs[i+1][x_before, y_before]
				and val <= self.DoGs[i+1][x, y] and val <= self.DoGs[i+1][x, y])):
				sigma = np.power(self.k, i) * self.sigma
				smoothed_image = self.Gaussians[i]
		return sigma, smoothed_image



	def computeDescriptors(self, img, points):
		self.buildDoGPyramid(img)
		feature_vectors = []
		for point in points:
			sigma, smoothed_image = self.getSmoothedfromPoint(point)
			if smoothed_image is not None:
				print(smoothed_image[point[0]-8: point[0]+8, point[1]-8:point[1]+8].shape)
				feature_vector, hog_image = hog(smoothed_image[point[0]-8: point[0]+8, point[1]-8:point[1]+8], orientations=36, pixels_per_cell=(4, 4), cells_per_block=(1, 1))
				feature_vectors.append(feature_vector)
			else:
				feature_vectors.append(None)
		return feature_vectors




if __name__ == "__main__":
	f = FeatureExtraction()
	imgrgb = cv2.imread('image2.jpg')
	img = cv2.cvtColor(imgrgb, cv2.COLOR_BGR2GRAY)
	defects, contour = f.convexDefects(img)
	my_sift = MiniSIFT()
	points = []
	for defect in defects:
		points.append(tuple(defect[0]))
		points.append(tuple(defect[1]))
		points.append(tuple(defect[2]))
	feature_vectors = my_sift.computeDescriptors(img, points)