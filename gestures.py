from numpy.random import choice
import time


class Vision:
    def __init__(self):
        pass

    
    def cnnForEmotionRecognition(self, image):
        classes = ["Neutral", "Happy", "Sad", "Surprise"]

        prediction = self.forward(image)

        return classes[prediction]


    def forward(self, image):
        list_of_candidates = [0, 1, 2, 3]

        if image == "happyImage":
            weights = [0.1, 0.5, 0.05, 0.35]
        elif image == "neutralImage":
            weights = [0.7, 0.1, 0.1, 0.1]  
        elif image == "sadImage":
            weights = [0.1, 0.05, 0.8, 0.05]  
        elif image == "surpriseImage":
            weights = [0.1, 0.35, 0.05, 0.5]  
        
        output = choice(list_of_candidates, 1, p=weights)[0]

        return output


class Gesture:
    def __init__(self, ALMotion, doGesture, vision, tts_service, typeImage = "happyImage", favourite=None):
        self.ALMotion = ALMotion
        self.doGesture = doGesture
        self.vision = vision
        self.tts_service = tts_service
        self.typeImage = typeImage
        self.favourite = favourite


    def doHello(self):
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch"]
        angles = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07]
        times  = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
        isAbsolute = True
        self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

        for i in range(10):
            jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
            angles = [1.7, -0.07, -0.07]
            times  = [0.8, 0.8, 0.8]
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)

            jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
            angles = [1.3, -0.07, -0.07]
            times  = [0.8, 0.8, 0.8]
            isAbsolute = True
            self.ALMotion.angleInterpolation(jointNames, angles, times, isAbsolute)


        return

    def look_hand(self):
        for item in range(5):
            joints = ["HeadYaw", "HeadPitch", 'RElbowRoll', 'LElbowRoll']
            times = [0.8, 0.8, 0.8, 0.4]
            angles = [0.05, -0.1, 2.9, -1.2]
            self.ALMotion.angleInterpolation(joints, angles, times, True)
            
            angles = [-0.04, 0.2, 0, 0]
            self.ALMotion.angleInterpolation(joints, angles, times, True)


    def dance_0(self):
        joints = ['HeadPitch', 'HeadYaw', 
                  'RElbowYaw', 'RElbowRoll', 'RShoulderPitch', 
                  'LElbowYaw', 'LElbowRoll', 'LShoulderPitch',
                  "RHand", "LHand",
                  "HipRoll", "HipPitch"]
        times = [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
        for i in range(50):
            # angles = [0, 0.5, 1, 2, 0.1, -1.9, -2, 0.2, 0, 0]
            # self.ALMotion.angleInterpolation(joints, angles, times, True)
            angles = [-0.5, 0, 0.48, 2, 0.1, -2.53, -2, 0.2, 0, 0, -0.15, -0.17] 
            self.ALMotion.angleInterpolation(joints, angles, times, True)
            # angles = [0, 0.5, 1, 2, 0.1, -1.9, -2, 0.2, 0, 0] 
            # self.ALMotion.angleInterpolation(joints, angles, times, True)

            angles = [0.5, 0, 1.9, 2, 0.1, -1.03, -2, 0.2, 0, 0, 0.15, -0.17] 
            self.ALMotion.angleInterpolation(joints, angles, times, True)
            # angles = [0.5, 0, 1, 2, 0.1, -1.9, -2, 0.2, 0, 0] 
            # self.ALMotion.angleInterpolation(joints, angles, times, True)

    def touch_head(self):
            joints = ["HeadPitch", 'RElbowRoll', 'RElbowYaw', 'RShoulderPitch']
            times = [1, 1, 1, 1]
            angles = [0.5, 4, 0.9, -0.5]
            self.ALMotion.angleInterpolation(joints, angles, times, True)
            angles = [0, 0, 1.47, 1.6]
            self.ALMotion.angleInterpolation(joints, angles, times, True)

    def touch_hand(self):
            #for item in range(10):
            joints = ["HeadYaw", "HeadPitch", 'RElbowRoll', 'LElbowRoll']
            times = [0.8, 0.8, 0.8, 0.4]
            angles = [0.05, -0.1, 2.9, -1.2]
            self.ALMotion.angleInterpolation(joints, angles, times, True)
            
            angles = [-0.04, 0.2, 0, 0]
            self.ALMotion.angleInterpolation(joints, angles, times, True)



    