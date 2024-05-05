import pytesseract
from PIL import Image


def convert_image_bw(img):
    thresh = 125
    fn_w = lambda x : 255 if x > thresh else 0
    fn_b = lambda x : 0 if x > thresh else 255

    #image_convert = image_file.convert('1') # convert image to black and white
    rw = img.convert('L').point(fn_w, mode='1')
    rb = img.convert('L').point(fn_b, mode='1')

    rw.save('img/result_w.png')
    rb.save('img/result_B.png')

    return (rw,rb)


def img_to_tags():
    image_file = Image.open("img/test.png") # open colour image

    resutls = convert_image_bw(image_file)
    print(pytesseract.image_to_string(resutls[0]))
    print(pytesseract.image_to_string(resutls[1]))

    



if __name__ == "__main__":
    img_to_tags()