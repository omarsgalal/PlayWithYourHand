import cv2
import numpy as np
from matplotlib import pyplot as plt
class GestureDetector:
	def __init__(self):
		self.sift = cv2.xfeatures2d.SIFT_create(400)
		#self.surf = cv2.xfeatures2d.SURF_create(400)
	def matchOpenHand(self,desInput):
		openHand = cv2.imread('openhand.jpg',0)
		kpOpenHand, desOpenHand = self.sift.detectAndCompute(openHand,None)
		matchesOpenHand=0
		if type(desInput) is np.ndarray and type(desOpenHand) is np.ndarray:
			for i in range(len(desInput)):
				dist1=9999
				dist2=9999
				temp=0
				for j in range(len(desOpenHand)):
					temp=min(np.linalg.norm(desInput[i]-desOpenHand[j]),dist1)
					
					if temp<dist1:
						dist2=dist1
						dist1=temp
						
						#print("dist1 ",dist1,"dist2",dist2)
				#print(dist1/dist2)
				if((dist1/dist2)<0.45):
					matchesOpenHand+=1
					#print(dist," in openHand")	
		print(matchesOpenHand,"Open hand matches")
		if(matchesOpenHand>25):
			return True
	def matchFist(self,desInput):
		fist = cv2.imread('fist.jpg',0)
		kpFist, desFist = self.sift.detectAndCompute(fist,None)
		matchesFist=0
		if type(desInput) is np.ndarray and type(desFist) is np.ndarray:
			for i in range(len(desInput)):
				dist1=9999
				dist2=9999
				temp=0
				for j in range(len(desFist)):
					temp=min(np.linalg.norm(desInput[i]-desFist[j]),dist1)
					
					if  temp<dist1:
						dist2=dist1
						dist1=temp
						
						#print("dist1 ",dist1,"dist2",dist2)
				#print(dist1/dist2)
				if((dist1/dist2)<0.45):

					matchesFist+=1
					#print(dist," in openHand")	
		print(matchesFist,"Fist matches")
		if(matchesFist>25):
			return True
	def matchZeroShaped(self,desInput):
		zeroShaped = cv2.imread('zeroshaped.jpg',0)
		kpZeroShaped, desZeroShaped = self.sift.detectAndCompute(zeroShaped,None)
		matches=0
		if type(desInput) is np.ndarray and type(desZeroShaped) is np.ndarray:
			for i in range(len(desInput)):
				dist1=9999
				dist2=9999
				temp=0
				for j in range(len(desZeroShaped)):
					temp=min(np.linalg.norm(desInput[i]-desZeroShaped[j]),dist1)
					
					if  temp<dist1:
						dist2=dist1
						dist1=temp
						
						#print("dist1 ",dist1,"dist2",dist2)
				#print(dist1/dist2)
				if((dist1/dist2)<0.45):

					matches+=1
					#print(dist," in openHand")	
		print(matches,"zero matches")
		if(matches>25):
			return True	
	def matchKnife(self,desInput):
		knife = cv2.imread('knife.jpg',0)
		kpKnife, desKnife = self.sift.detectAndCompute(knife,None)
		matches=0
		if type(desInput) is np.ndarray and type(desKnife) is np.ndarray:
			for i in range(len(desInput)):
				dist1=9999
				dist2=9999
				temp=0
				for j in range(len(desKnife)):
					temp=min(np.linalg.norm(desInput[i]-desKnife[j]),dist1)
					
					if  temp<dist1:
						dist2=dist1
						dist1=temp
						
						#print("dist1 ",dist1,"dist2",dist2)
				#print(dist1/dist2)
				if((dist1/dist2)<0.45):

					matches+=1
					#print(dist," in openHand")	
		print(matches,"knife matches")
		if(matches>25):
			return True		
	def match(self, img1):
		kp1, des1 = self.sift.detectAndCompute(img1,None)
		img2 = cv2.imread('openhand.jpg',0)
		kp2, des2 = self.sift.detectAndCompute(img2,None)
		'''print("\n\n\n\n\n")
		if(self.matchOpenHand(desInput)):
			print("openHand")
			return
		if(self.matchFist(desInput)):
			print("Fist")
			return
		if(self.matchZeroShaped(desInput)):
			print("zero shaped")
			return
		if(self.matchKnife(desInput)):
			print("Knife")
			return	
		#print("No Match")	'''		
		'''OpenHand = cv2.imread('openhand.jpg',0) # trainImage
		fist=cv2.imread('fist.jpg',0)
		knife=cv2.imread('knife.jpg',0)
		zeroShaped=cv2.imread('zeroshaped.jpg',0)

		

		# find the keypoints and descriptors with SIFT
		#kp1, des1 = self.sift.detectAndCompute(img1,None)
		#kp2, des2 =self. sift.detectAndCompute(img2,None)
		kpInput, desInput = self.sift.detectAndCompute(img1,None)
		kpOpenHand, desOpenHand = self.sift.detectAndCompute(OpenHand,None)
		matchesOpenHand=0
		if type(desInput) is np.ndarray and type(desOpenHand) is np.ndarray:
			for i in range(len(desInput)):
				dist1=9999
				dist2=9999
				temp=0
				for j in range(len(desOpenHand)):
					temp=min(np.linalg.norm(desInput[i]-desOpenHand[j]),dist1)
					
					if  temp<dist1:
						dist2=dist1
						dist1=temp
						
						#print("dist1 ",dist1,"dist2",dist2)
				#print(dist1/dist2)
				if((dist1/dist2)<0.5):

					matchesOpenHand+=1
					#print(dist," in openHand")	
		#print(matchesOpenHand,"Open hand matches")
		if(matchesOpenHand>20):
			print("OpenHand",matchesOpenHand)
			return	
		#it's not openhand try fist
		kpFist, desFist = self.sift.detectAndCompute(OpenHand,None)
		matchesFist=0
		if type(desInput) is np.ndarray and type(desFist) is np.ndarray:
			for i in range(len(desInput)):
				dist1=9999
				dist2=9999
				temp=0
				for j in range(len(desFist)):
					temp=min(np.linalg.norm(desInput[i]-desFist[j]),dist1)
					if temp<dist1:
						dist2=dist1
						dist1=temp
				if((dist1/dist2)<0.7):
					matchesFist+=1
					#print(dist)
		#print("matches Fist",matchesFist)				
		if(matchesFist>20):
			print("Fist",matchesFist)
			#print(matchesFist)
			return	
		'''	
		#print(matchesOpenHand,matchesFist)	
		#print(len(des2[0]),len(kp1))
		#for i in des1:
		#	for j in des2:


		# BFMatcher with default params
		bf = cv2.BFMatcher()
		matches = bf.match(des1,des2)
		matches = sorted(matches, key=lambda x:x.distance)
		matching_result = cv2.drawMatches(img1, kp1, img2, kp2, matches[:5], None, flags=2)
		cv2.imshow("image", matching_result)
		#print((des1[0].shape))

		# FLANN parameters
		'''FLANN_INDEX_KDTREE = 0
		index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
		search_params = dict(checks=50)   # or pass empty dictionary

		flann = cv2.FlannBasedMatcher(index_params,search_params)

		matches = flann.knnMatch(des1,des2,k=2)

		# Need to draw only good matches, so create a mask
		matchesMask = [[0,0] for i in range(len(matches))]

		# ratio test as per Lowe's paper
		for i,(m,n) in enumerate(matches):
		    if m.distance < 0.6*n.distance:
		        matchesMask[i]=[1,0]

		draw_params = dict(matchColor = (0,255,0),
		                   singlePointColor = (255,0,0),
		                   matchesMask = matchesMask,
		                   flags = 0)

		img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)

		'''#plt.imshow(img3,),plt.show()
		
		#return (img3,"SIFTS")
		#return (img3,"SIFT")




	def matchReady(self, img):
		kp_img, des_img = self.sift.detectAndCompute(img,None)
		
		open_hand = cv2.imread('openhand.jpg',0)
		kp_openhand, des_openhand = self.sift.detectAndCompute(open_hand,None)
		
		fist = cv2.imread('fist.jpg',0)
		kp_fist, des_fist = self.sift.detectAndCompute(fist,None)
		
		knife = cv2.imread('knife.jpg',0)
		kp_knife, des_knife = self.sift.detectAndCompute(knife,None)
		
		zero = cv2.imread('zeroshaped.jpg',0)
		kp_zero, des_zero = self.sift.detectAndCompute(zero,None)


		bf = cv2.BFMatcher()

		num_points = 20
		
		matches_openhand = bf.match(des_img, des_openhand)
		matches_openhand = sorted(matches_openhand, key=lambda x:x.distance)
		for i  in range(len(matches_openhand)):
			if matches_openhand[i].distance	>0.5:
				matches_openhand[i].erase() 

		matches_fist = bf.match(des_img, des_fist)
		matches_fist = sorted(matches_fist, key=lambda x:x.distance)[:num_points]

		matches_knife = bf.match(des_img, des_knife)
		matches_knife = sorted(matches_knife, key=lambda x:x.distance)[:num_points]

		matches_zero = bf.match(des_img, des_zero)
		matches_zero = sorted(matches_zero, key=lambda x:x.distance)[:num_points]

		sum_openhand = sum(x.distance for x in matches_openhand)
		sum_fist = sum(x.distance for x in matches_fist)
		sum_zero = sum(x.distance for x in matches_zero)
		sum_knife = sum(x.distance for x in matches_knife)


		sums = np.array([sum_openhand, sum_fist, sum_zero, sum_knife])
		gestures = ["openhand", "fist", "zero", "knife"]

		max_sum = np.argmin(sums)

		print(gestures[max_sum])
		print (sums)