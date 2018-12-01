import numpy as np
from handencoder import HandEncoder as HE
from sklearn.neural_network import MLPClassifier
import pickle
import os
import cv2

class GestureClassifier:
	"""This class trains a classifier that can prdict
		hand gestures giving hand encodings"""
	def __init__(self):
		self.he = HE()
		self.model = MLPClassifier(hidden_layer_sizes=(10, 10, 10, 10), random_state=1)
		self.train_data = None
		self.train_labels = None


	def saveModel(self, path="model.sl"):
		file = open(path, 'wb')
		pickle.dump(self.model, file)
		file.close()


	def loadModel(self, path="model.sl"):
		file = open(path, 'rb')
		self.model = pickle.load(file)
		file.close()


	def loadData(self, path="Dataset/Train"):
		folders = ["OpenHand", "Fist", "Zero", "Knife"]
		self.train_data = np.zeros((1, 4), dtype=float)
		self.train_labels = np.zeros((1, 4))
		for i in range(len(folders)):
			imgs = os.listdir("{}/{}".format(path, folders[i]))
			np.random.shuffle(imgs)
			for im in imgs:
				img = cv2.imread("{}/{}/{}".format(path, folders[i], im), cv2.IMREAD_GRAYSCALE)
				encoding = self.he.encode(img).reshape(1, -1)
				self.train_data = np.concatenate((self.train_data, encoding), axis=0)
				label = np.array([0, 0, 0, 0])
				label[i] = 1
				label = label.reshape(1, -1)
				self.train_labels = np.concatenate((self.train_labels, label), axis=0)
		self.train_data = self.train_data[1:, :]
		self.train_labels = self.train_labels[1:, :]


	def fit(self):
		self.model.fit(self.train_data, self.train_labels)


	def predict(self, binary_img):
		encoding = self.he.encode(binary_img).reshape(1, -1)
		prediction = self.model.predict(encoding)
		return np.argmax(prediction[0])


	def train(self):
		self.loadData()
		self.fit()

	def getAccuracy(self):
		self.model.score(self.train_data, self.train_labels)



if __name__ == "__main__":
	classifier = GestureClassifier()
	classifier.train()
	classifier.saveModel()
	classifier = GestureClassifier()
	classifier.loadModel()
	img = cv2.imread('Dataset/Test/Fist/678.jpg', cv2.IMREAD_GRAYSCALE)
	print (classifier.predict(img))