from morphology import calcMorphology
import motionDetection as md
import cv2
import numpy as np
from SkinModel.SkinModel import SkinModel as pm
from utils import *

models = pm.loadModel()

def readFrame():
    frame = cap.read()[1]
    return frame


cap = cv2.VideoCapture(0)

INITIAL_BACKGROUND = readFrame()
backgroundModel = INITIAL_BACKGROUND

md.setInitialBackground(INITIAL_BACKGROUND)



def combination(MD, SCD, morphW, sB):
    # params = MD, SCD, morphW, sB
    # r = [(img.shape, img.dtype) for img in params]
    # print(r)

    rate_img = (MD + SCD + morphW - sB) / 3

    # rate_img *= (255.0/rate_img.max())
    rate_img = 255*(rate_img - np.min(rate_img))/np.ptp(rate_img).astype(np.uint8)
    
    final_img = cv2.threshold(rate_img.astype(np.uint8),0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[0]
    return (final_img - np.min(final_img))/np.ptp(final_img)


def getSkinBackgroundModel(backgroundModel):
    print(backgroundModel.shape)
    return pm.colorSkin(backgroundModel,models[0], models[1])

def main():
    global backgroundModel
    beforeLastFrame = INITIAL_BACKGROUND
    beforeLastFrameGray = toGray(beforeLastFrame)

    cv2.waitKey(20)
    lastFrame = readFrame()
    lastFrameGray = toGray(lastFrame)
    cv2.waitKey(20)
    while(True):
        currFrame = readFrame()
        currFrameGray = toGray(currFrame)
        
        skinBackgroundModel = getSkinBackgroundModel(backgroundModel) #optimize

        roi, backgroundSubtraction, backgroundModel = md.motionDetection(beforeLastFrameGray, lastFrameGray, currFrameGray, currFrame, backgroundModel, skinBackgroundModel)
        backgroundSubtraction = (backgroundSubtraction - np.min(backgroundSubtraction))/np.ptp(backgroundSubtraction)

        skinColorDetection = pm.colorSkin(currFrame,models[0],models[1])
        morphologyWeight = calcMorphology(backgroundSubtraction)

        showImages([backgroundSubtraction,backgroundModel,skinColorDetection,morphologyWeight], ["bgS","bgm","skinD","morphW"])
        # showImages([backgroundSubtraction,backgroundModel,skinColorDetection,morphologyWeight])

        res = combination(backgroundSubtraction, skinColorDetection, morphologyWeight, skinBackgroundModel)
        cv2.imshow("res", res)

        beforeLastFrame = lastFrame
        lastFrame = currFrame
        beforeLastFrameGray = lastFrameGray
        lastFrameGray = currFrameGray

        key = cv2.waitKey(30)
        if key==27:
            break
            





if __name__ == "__main__":
    main()