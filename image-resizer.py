from PIL import Image

def resizeImage(oldPath,newPath,width,height):
    image = Image.open(oldPath)
    new_image = image.resize((width, height))
    new_image.save(newPath)

op = 'gallery/sprites/other/welcome-screen.png'
np = 'gallery/sprites/other/welcome-screen2.png'
w = 1100
h = 600

resizeImage(op, np, w, h)