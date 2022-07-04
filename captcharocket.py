from PIL import Image, ImageOps
import easyocr
def redact_stock_img(mode,img_src):
    img = Image.open(img_src)
    img = ImageOps.grayscale(img)
    pixels = img.load()
    if mode =='b':
        colors = [x for x in range(0, 60)]
        for i in range(img.width):
            for j in range(img.height):

                if pixels[i, j] in colors:
                    continue
                else:
                    pixels[i, j] = (255)
        img.save("tmp.jpg")
        reader = easyocr.Reader(['en'])
        result = reader.readtext('tmp.jpg')
        str_r = ''
        for el in result:
            str_r += el[1]

        return str_r.replace(' ','')
    if mode =='w':
        colors = [x for x in range(110,255)]
        for i in range(img.width):
            for j in range(img.height):

                if pixels[i,j] in colors:
                    continue
                else:
                    pixels[i, j] = (0)
        img.save("tmp.jpg")
        reader = easyocr.Reader(['en'])
        result = reader.readtext('tmp.jpg')
        str_r = ''
        for el in result:
            str_r += el[1]
        return str_r.replace(' ','')

