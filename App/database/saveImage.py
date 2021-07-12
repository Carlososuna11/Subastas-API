import os

def saveImage(image,model,id):
    _,file_extension = os.path.splitext(str(image))
    with open(f'media/img/{model}{id}{file_extension}', 'wb+') as f:
        for chunk in image.chunks():
            f.write(chunk)