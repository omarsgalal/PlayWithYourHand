import numpy as np
import cv2
import skimage.io as io
import os 
from skimage.color import rgb2gray,rgb2hsv,hsv2rgb


class TrainSkinModel():
    # train for both datasets and save the model
    def train(self):
        skinHisto,nonskinHisto = trainPratheepan()
        skinHisto,nonskinHisto = trainWIDER(skinHisto,nonskinHisto)
        saveModel(skinHisto,nonskinHisto)
        return skinHisto,nonskinHisto

    # train Pratheepan Dataset
    def trainPratheepan (self,skinHisto=np.zeros((256,256,256)),nonskinHisto=np.zeros((256,256,256)), imgPath = "Face_Dataset/Pratheepan_Dataset/", grPath = "Face_Dataset/Ground_Truth/"):
        for name in os.listdir(grPath):
            if name[-4:] == '.png':
                    grI = io.imread(grPath+name)[:,:,:3] #3 to delete the fourth dimention on png files
                    img = io.imread(imgPath+name[:-4]+'.jpg') 
                    
                    skinImg = rgb2hsv((grI/255)*img)*255
                    nonSkinImg = rgb2hsv((1-(grI/255))*img)*255
                    
                    skinHisto += cv2.calcHist([skinImg.astype(np.uint8)],[0,1,2],None,[256,256,256],[0,256,0,256,0,256])
                    nonskinHisto += cv2.calcHist([nonSkinImg.astype(np.uint8)],[0,1,2],None,[256,256,256],[0,256,0,256,0,256])
        return skinHisto,nonskinHisto


    # train WIDER dataset
    def trainWIDER (self,skinHisto=np.zeros((256,256,256)),nonskinHisto=np.zeros((256,256,256)), filePath = "wider_face_train_bbx_gt.txt", grPath = "WIDER_train/images"):
        file = open(filePath)
        lines = file.readlines()
        file.close

        img = io.imread("{}/{}".format(grPath,lines[0][:-1]))
        a = np.zeros_like(img)
        factor = 1
        for factor in [1,0.9]:
            b = True

            img = np.array( rgb2hsv(io.imread("{}/{}".format(grPath,lines[0][:-1]))) *255,dtype=np.uint8)
            a = np.zeros(shape=img.shape)
                            
            for line in progressbar.progressbar(lines):
                elem = line.split(" ")
                if len(elem) == 11:
                    start = (int(int(elem[0])*(2-factor)),int(int(elem[1])*(2-factor)))
                    end = (int(elem[0])+int(int(elem[2])*factor),int(elem[1])+int(int(elem[3])*factor))
                    cv2.rectangle(a,start,end,(1,1,1),cv2.FILLED)

                else:
                    if b:
                        skin = img*a
                        skinHisto += cv2.calcHist([skin.astype('uint8')],[0,1,2],None,[256,256,256],[0,256,0,256,0,256])

                        nonSkin = (1 - a) * img
                        nonskinHisto += cv2.calcHist([nonSkin.astype('uint8')],[0,1,2],None,[256,256,256],[0,256,0,256,0,256])

                        img = np.array( rgb2hsv(io.imread("{}/{}".format(grPath,line[:-1]))) *255,dtype=np.uint8)
                        a = np.zeros(shape=img.shape)
                    
                    b= not b    
        return skinHisto,nonskinHisto  


    def saveModel(self,skinHisto,nonskinHisto):
        np.save("AllModel-skin.npy",skinHisto)
        np.save("AllModel-nonskin.npy",nonskinHisto)

    




    # work only on google colab
    def downloadWIDER (self):
        os.system("pip install -U -q PyDrive")
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive
        from google.colab import auth
        from oauth2client.client import GoogleCredentials

        auth.authenticate_user()
        gauth = GoogleAuth()
        gauth.credentials = GoogleCredentials.get_application_default()
        drive = GoogleDrive(gauth)

        file_id = '0B6eKvaijfFUDQUUwd21EckhUbWs'
        downloaded = drive.CreateFile({'id': file_id})
        downloaded.GetContentFile('WIDER_train.zip')
        os.system("unzip WIDER_train.zip &> abdo.txt")
        os.system("pip install progressbar2 &> abdo.txt")
        import progressbar
        os.system("wget 'https://transfer.sh/P2pwS/wider_face_train_bbx_gt.txt' &> abdo.txt")



def loadModel():
    try:
        skinHisto = np.load("AllModel-skin.npy")
        nonskinHisto = np.load("AllModel-nonskin.npy")

    except:
        os.system("wget https://transfer.sh/12sP3e/AllModel-skin.npy")
        os.system("wget https://transfer.sh/TMCm2/AllModel-nonskin.npy")
        skinHisto = np.load("AllModel-skin.npy")
        nonskinHisto = np.load("AllModel-nonskin.npy")

    # to be removed if the new model come
    skinHisto[0,0,0] = 0
    nonskinHisto[0,0,0] = 0

    return skinHisto,nonskinHisto