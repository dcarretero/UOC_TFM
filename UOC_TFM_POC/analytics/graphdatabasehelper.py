import os
import pandas as pd
class ImageAnalyzed:
    def __init__(self,filename):
        self.filename= filename
        self.classes ={}

    def add_classes(self,cs):
        if cs in self.classes.keys():
            self.classes[cs] = self.classes[cs] + 1
        else:
            self.classes[cs] = 1


class ImagesAnalyzedLoader:
    def __init__(self,txt_files_dir,labels_file):
        self.txt_files_dir = txt_files_dir
        self.images_analyzed =[]
        self.labels = pd.read_csv(labels_file, header=None, names=['label']).label.tolist()

    def get_label_from_id(self,id):
        return self.labels[id]

    def add_image_analyzed(self,image_analyzed):
        self.images_analyzed.append(image_analyzed)
    def load_txt_files(self):
        for file_txt in os.listdir(self.txt_files_dir):
            if os.path.isfile(os.path.join(self.txt_files_dir, file_txt)):
                with open(os.path.join(self.txt_files_dir, file_txt)) as f:
                    lines = f.readlines()
                    imageAnalyzed = ImageAnalyzed(file_txt)
                    for line in lines:
                        line= line.replace('\n','')
                        line_splitted = line.split(' ')
                        imageAnalyzed.add_classes(self.get_label_from_id(int(line_splitted[0])))
                    self.add_image_analyzed(imageAnalyzed)

# Ejecución de pruebas

txt_files_dir ='c:/Users/dcsj/Repositorios/UOC_TFM/runs/detect/predict/labels/'
labels_file ='c:/Users/dcsj/Repositorios/UOC_TFM/UOC_TFM_POC/labels.txt'
imageAnalyzedLoader = ImagesAnalyzedLoader(txt_files_dir,labels_file)
imageAnalyzedLoader.load_txt_files()
print(imageAnalyzedLoader.images_analyzed[0].classes)
print(imageAnalyzedLoader.images_analyzed[0].filename)


