#Topic: Social Distancing Project using Computer Vision and deep Learning
#Team Nmae: Tech Enigma

import numpy as np
import time
import cv2
import math

labelsPath = "./coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

weightsPath = "./yolov3.weights"
configPath = "./yolov3.cfg"
#Loading YOLO model
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

#Accepting input image
image =cv2.imread('./first_image.jpg')
(H, W) = image.shape[:2]
#Recovering output layer names
ln = net.getLayerNames()
ln = [ln[idx - 1] for idx in net.getUnconnectedOutLayers()]
#conerting to blob
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),swapRB=True, crop=False)
#passing blob
net.setInput(blob)
start = time.time()
layerOutputs = net.forward(ln)
end = time.time()
print("Frame Prediction Time : {:.6f} seconds".format(end - start))
boxes = []
confidences = []
classIDs = []
#actual processing logic
for output in layerOutputs:
    for detection in output:
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]
        if confidence > 0.5 and classID == 0:
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY, width, height) = box.astype("int")
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)
            
idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5,0.3)
ind = []
for i in range(0,len(classIDs)):
    if(classIDs[i]==0):
        ind.append(i)
a = []
b = []
color = (0,255,0) 
if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            a.append(x)
            b.append(y)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            

distance=[] 
nsd = []
for i in range(0,len(a)-1):
    for k in range(1,len(a)):
        if(k==i):
            break
        else:
            x_dist = (a[k] - a[i])
            y_dist = (b[k] - b[i])
            d = math.sqrt(x_dist * x_dist + y_dist * y_dist)
            distance.append(d)
            if(d<=100.0):
                nsd.append(i)
                nsd.append(k)
            nsd = list(dict.fromkeys(nsd))
   
color = (0, 0, 255)
text=""
for i in nsd:
    (x, y) = (boxes[i][0], boxes[i][1])
    (w, h) = (boxes[i][2], boxes[i][3])
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    text = "Alert"
    cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
           
cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)
cv2.imshow("Social Distancing Detector", image)
cv2.imwrite('output.jpg', image)
cv2.waitKey()
