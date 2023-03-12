from PIL import Image
import os
from glob import glob
import pandas as pd
from functools import reduce
from xml.etree import ElementTree as et

class ImageHelper:

    def __init__(self, labels):
        self.labels = labels
    def _save_txt(self, df_grouped,output_path):
        for filename, data in df_grouped:
            txt_filename = os.path.splitext(filename)[0]
            path_txt_filename = output_path + '/' + txt_filename +'.txt'
            df_grouped.get_group(filename).set_index('filename').to_csv(path_txt_filename,sep=' ',index= False, header= False)

    def resize_images(self,input_dir_path,output_subdir,width,height):
        #Se crea el subdirectorio si no existe
        os.makedirs(os.path.join(input_dir_path, output_subdir), exist_ok=True)
        for path in os.listdir(input_dir_path):
            if os.path.isfile(os.path.join(input_dir_path, path)):
                split_tup = os.path.splitext(path)
                file_extension = split_tup[1]
                file_name = split_tup[0]
                if file_extension.find('xml') == -1:
                    image = Image.open(os.path.join(input_dir_path, path))
                    if image.size[0] > width and image.size[1] > height:
                        new_image = image.resize((width, height))
                        new_file_name = file_name + '_'+ str(width) + '.' + file_extension
                        new_image.save(os.path.join(input_dir_path,output_subdir, new_file_name))

    def generate_txt_label_files(self,input_dir_path,output_subdir):
        # Se fija el criterio de busqueda de ficheros con *.xml en el directorio de imagenes redimensionadas
        search_criteria =str(os.path.join(input_dir_path,output_subdir)).replace('\\','/')+'/*.xml'
        # Se obtienen los nombres de los ficheros
        xml_list = glob(search_criteria)
        # Se cambian los separadores de ruta
        xml_list = list(map(lambda x:x.replace('\\','/'),xml_list))
        parser = []
        for xml in xml_list:

            tree = et.parse(xml)    # Se obtiene el árbol xml
            root = tree.getroot()   # Se obtiene el nodo raiz
            image_name = root.find('filename').text  # Se obtiene el nombre de la imagen informado en el fichero
            width = root.find('size').find('width').text # Se obtiene el ancho de la imagen en pixels
            height = root.find('size').find('height').text # Se obtiene el alto de la imagen en pixels
            objs = root.findall('object') # Se encuentran todos los objetos etiquetados en la imagen
            for obj in objs: # Se recorren los objetos para obtener el nombre y las dimensiones del bounding box
                name = obj.find('name').text
                bndbox = obj.find('bndbox')
                xmin= bndbox.find('xmin').text
                xmax= bndbox.find('xmax').text
                ymin= bndbox.find('ymin').text
                ymax= bndbox.find('ymax').text
                parser.append([image_name,width,height,name,xmin,xmax,ymin,ymax])
        # Se crea un pandas dataframe a partir de la información en la lista parser
        df = pd.DataFrame(parser, columns=['filename', 'width', 'height', 'name', 'xmin', 'xmax', 'ymin', 'ymax'])
        # Se calculan las columnas necesarias en etiquetas utilizables por la libreria Yolo
        cols = ['width', 'height', 'xmin', 'xmax', 'ymin', 'ymax']
        df[cols] = df[cols].astype(int)
        df['center_x'] = ((df['xmax'] + df['xmin']) / 2) / df['width']
        df['center_y'] = ((df['ymax'] + df['ymin']) / 2) / df['height']
        df['w'] = (df['xmax'] - df['xmin']) / df['width']
        df['h'] = (df['ymax'] - df['ymin']) / df['height']
        df['id'] = df['name'].apply(lambda x: self.labels[x])
        cols =['filename','id','center_x','center_y','w','h']
        # Se agrupan por fichero
        df_yolo = df[cols].groupby('filename')
        self._save_txt(df_yolo,os.path.join(input_dir_path,output_subdir))


