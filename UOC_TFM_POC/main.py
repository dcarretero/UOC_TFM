from datapreparation.imagehelper import ImageHelper

# Constantes
IMAGES_WIDTH = 500
IMAGES_WEIGHT = 500
OUTPUT_SUBDIR ='resized'

if __name__ == '__main__':
    ###### UNIFICACIÓN DE RESOLUCIONES
    #Se unifican las imagenes a 500x500 para las imagenes de copas
    input_dir_path = r'C:\\Users\\dcsj\\Repositorios\\UOC_TFM/UOC_TFM_POC/Imagenes/vasos_copas'
    imagehelper = ImageHelper()
    imagehelper.resize_images(input_dir_path,OUTPUT_SUBDIR, IMAGES_WIDTH,IMAGES_WEIGHT)

    print('Fin de proceso')



