import os
import pandas as pd
import networkx as nx

class ImageAnalyzed:
    def __init__(self,name):
        self.name= name
        self.objects ={}

    def add_objects(self,object_class):
        if object_class in self.objects.keys():
            self.objects[object_class] = self.objects[object_class] + 1
        else:
            self.objects[object_class] = 1


class ImagesAnalyzedLoader:
    def __init__(self,txt_files_dir,labels_file):
        self.txt_files_dir = txt_files_dir
        self.images_analyzed =[]
        self.labels = pd.read_csv(labels_file, header=None, names=['label']).label.tolist()
        self.graph = nx.Graph()

    def get_label_from_id(self,id):
        return self.labels[id]

    def add_image_analyzed(self,image_analyzed):
        self.images_analyzed.append(image_analyzed)
    def load_txt_files(self):
        for file_txt in os.listdir(self.txt_files_dir):
            if os.path.isfile(os.path.join(self.txt_files_dir, file_txt)):
                with open(os.path.join(self.txt_files_dir, file_txt)) as f:
                    lines = f.readlines()
                    image_name = file_txt.split('.')[0]
                    imageAnalyzed = ImageAnalyzed(file_txt)
                    for line in lines:
                        line= line.replace('\n','')
                        line_splitted = line.split(' ')
                        imageAnalyzed.add_objects(self.get_label_from_id(int(line_splitted[0])))
                    self.add_image_analyzed(imageAnalyzed)
    def load_graphdatabases(self):
        for image in self.images_analyzed:
            atrib_image_node = {}
            atrib_image_node['type'] = 'image_name'
            self.graph.add_nodes_from([(image.name,atrib_image_node)])
            for object_class in image.objects.keys():
                if not self.graph.has_node(object_class):
                    atrib_class_node = {}
                    atrib_class_node['type'] = 'object_class'
                    self.graph.add_nodes_from([(object_class,atrib_class_node)])
                self.graph.add_edges_from([(image.name,object_class)],weight=image.objects[object_class])




# Ejecución de pruebas

txt_files_dir ='c:/Users/dcsj/Repositorios/UOC_TFM/runs/detect/predict/labels/'
labels_file ='c:/Users/dcsj/Repositorios/UOC_TFM/UOC_TFM_POC/labels.txt'
imageAnalyzedLoader = ImagesAnalyzedLoader(txt_files_dir,labels_file)
imageAnalyzedLoader.load_txt_files()
imageAnalyzedLoader.load_graphdatabases()
print(imageAnalyzedLoader.graph)


