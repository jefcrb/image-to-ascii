from PIL import Image, ImageOps
import numpy as np
import sys


def check_img(args):
    if len(args) > 1 and args[1] != "-h":
        try:
            image = Image.open(args[1])
            return image
        except:
            print("This is not a valid image")
            exit()
    else:
        help()
        exit()


def check_args(args):
    idx = 0
    res = 0
    charset = ""
    out_file = ""
    for arg in args:
        if arg == "-r":
            try:
                res = int(args[idx+1])
            except:
                print("Invalid argument")
                exit()

        if arg == "-c":
            charset = args[idx+1]
        
        if arg == "-o":
            out_file = args[idx+1]

        idx += 1
    
    return res or 2, charset or "Ñ@#W$9810?!abc;:+=_-, ", out_file or None


def help():
    print("""
No image given!
Usage: image_to_ascii <image> [resolution] [charset] [output file]
-r  Resolution, default 2, meaning: e.g. entering 5 would mean that a 5x5 pixel area turns into one ASCII character
-c  Enter a customized list of ASCII characters in decreasing density, e.g. \"Ñ@#W$9810?!abc;:+=_-, \"
-o  Specify output file
-h  Show this help message""")

def success():
    print("Program finished successfully")

image = check_img(sys.argv)
sqrt_pixels_per_char, CHARS, output_file = check_args(sys.argv)
width = image.size[0]
height = image.size[1]
image = ImageOps.grayscale(image)
ascii_img = ""

chars_per_row = int(width/sqrt_pixels_per_char)
chars_per_column = int(height/sqrt_pixels_per_char)

def opt_img(img, ppc): #Crop image so the amount of pixels are a product of the amount of ascii characters
    new_width = int(len(img[0])/ppc)*ppc
    new_height = int(len(img)/ppc)*ppc
    new_img = img[0:new_height, 0:new_width]
    return new_img

npImage = np.asarray(image)

npImage = opt_img(npImage, sqrt_pixels_per_char)

width = len(npImage[0])
height = len(npImage)

chars_per_row = int(width/sqrt_pixels_per_char)
chars_per_column = int(height/sqrt_pixels_per_char)

pixels = []

for r in range(chars_per_column):
    for c in range(chars_per_row):
        for i in range(sqrt_pixels_per_char):
            pixels_in_chunk = []
            for j in range(sqrt_pixels_per_char):
                try: 
                    pixels_in_chunk.append(npImage[(r*sqrt_pixels_per_char)+i][(c*sqrt_pixels_per_char)+j])
                except:
                    print(f"error, r: {r}, c: {c}, i: {i}, j: {j}")
            avg_in_chunk = int(sum(pixels_in_chunk)/len(pixels_in_chunk)) if len(pixels_in_chunk) > 0 else 0
        pixels.append(avg_in_chunk)


idx = 0
for val in pixels:
    val = int((val/255)*len(CHARS))
    ascii_img += CHARS[val%len(CHARS)]
    ascii_img += CHARS[val%len(CHARS)]

    if idx%(width/sqrt_pixels_per_char) == 0:
        ascii_img += "\n"

    idx += 1

if output_file:
    f = open(output_file, "a+")

    f.truncate(0)
    f.write(ascii_img)
    f.close()
    success()
else:
    print(ascii_img)
    success()