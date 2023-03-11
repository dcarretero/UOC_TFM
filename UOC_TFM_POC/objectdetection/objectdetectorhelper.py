from ultralytics import YOLO
import pandas as pd
import os


class ObjectDetector:

    def __init__(self):
        self.labels = pd.read_csv('./labels.txt',header=None,names=['label'])
    def detectionPretrained(self,yolo_model,images_source):

        model = YOLO(yolo_model)
        entries = os.listdir(images_source)
        for entry in entries:
            file_path = images_source + '/' + entry
            results = model.predict(source=file_path, conf= 0.5, save=True, save_txt=True, exist_ok=True)  # save predictions as labels


