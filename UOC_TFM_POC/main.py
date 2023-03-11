import os.path
import pandas as pd
from datapreparation.imagehelper import ImageHelper
from objectdetection.objectdetectorhelper import ObjectDetector


if __name__ == '__main__':

    objectdetector = ObjectDetector()
    print(objectdetector.coco_labels.loc[0].label)
    objectdetector.detectionPretrained("./models/yolov8m.pt","./images")



