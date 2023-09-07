from pdf2image import convert_from_path
import os

def to_prevent_unnecessary():
    pass

def pdf_converter(file_path):
    # os.makedirs('input')
    images=convert_from_path(file_path,poppler_path=r"D:\Python\Air_Canvas\aircanvas\final_project\poppler-0.68.0_x86 (1)\poppler-0.68.0\bin")
    x=1
    for image in images:

        file_name = 'image'+str(x)+'.jpeg'
        file_path = os.path.join('input', file_name)
        image.save(file_path)
        # image.save('output'+str(x)+'.png',"PNG")
        x+=1











