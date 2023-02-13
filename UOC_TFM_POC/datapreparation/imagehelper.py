from PIL import Image
import os

class ImageHelper:
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
