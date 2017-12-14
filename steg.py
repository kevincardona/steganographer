#!/usr/bin/env python

import sys, binascii, math, os
from PIL import Image

max_lsb = 1

def decode():
    global image, imagepath

    imagepath = sys.argv[2]
    image = Image.open(imagepath)


    # Available storage bits (3 (RGB) * width * height * max_lsb)
    max_bits = 3 * image.size[0] * image.size[1] * max_lsb
    image_data = image.convert("RGB").getdata()

    data = ""
    ssize = ""
    size = 0
    count = 0
    for h in range(image.height):
        for w in range(image.width):
            (r, g, b) = image_data.getpixel((w,h))
            if (h*image.height + w < 8):
                ssize += str(r & 1)
                ssize += str(g & 1)
                ssize += str(b & 1)
            else:
                if (h*image.height + w == 8):
                    size = int(ssize,2)

                if (w + image.height * h < size+8):
                    if ((count < size)):
                        data += str(r & 1)
                    if (count + 1 < size):
                        data += str(g & 1)
                    if (count + 2 < size):
                        data += str(b & 1)
                    count += 3
                else:
                    break
    # Convert lsb data back into message
    data = hex(int(data,2))[2:]
    data = data.strip('L')
    print "Message:\n%s\n" % binascii.unhexlify(data)

def encode():
    global image, imagepath

    imagepath = sys.argv[2]
    image = Image.open(imagepath)

    rawtext = sys.argv[3]
    bintext = bin(int(binascii.hexlify(rawtext),16))
    bintext = bintext[:1] + bintext[2:]
    binsize = bin(len(bintext))
    binsize = binsize[:1] + binsize[2:]
    # Appends 0 to fill the storage space
    while (len(binsize) < 8 * 3):
        binsize = "0" + binsize


    # Available storage bits (3 (RGB) * width * height * max_lsb)
    max_bits = 3 * image.size[0] * image.size[1] * max_lsb
    image_data = image.convert("RGB").getdata()

    new_image = Image.new('RGB', (image.width, image.height));
    new_image_data = new_image.getdata()

    data_iterator = 0
    for h in range(image.height):
        for w in range(image.width):
            (r, g, b) = image_data.getpixel((w,h))
            r = r >> 2
            r = r << 2
            g = g >> 2
            g = g << 2
            b = b >> 2
            b = b << 2
            if (h * image.height + w < 8):
                if (w + h < len(binsize)):
                    r += int (binsize[(w+h) * 3])
                    g += int (binsize[(w+h) * 3 + 1])
                    b += int(binsize[(w+h) * 3 + 2])
            if ((h * image.height + w >= 8) & (data_iterator < len(bintext))):
                r += int(bintext[data_iterator])
                if (data_iterator + 1 < len(bintext)):
                    g += int(bintext[data_iterator + 1])
                if (data_iterator + 2 < len(bintext)):
                    b += int(bintext[data_iterator + 2])
                data_iterator += 3
            
            new_image_data.putpixel((w,h), (r, g, b))

    print "Saving image in steg-images/"
    new_image.save( "steg-images/" + os.path.splitext(os.path.basename(sys.argv[2]))[0] + ".png" , "PNG")


def usage():
    print 'Usage: ' + sys.argv[0] + ' <encode or decode> <file> <text>'
    sys.exit(2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    if (len(sys.argv) != 4) & (sys.argv[1] != "decode"):
        usage()
    option = sys.argv[1]

    if (option == "encode"):
        encode()
        sys.exit(1)
    else:
        decode()
        sys.exit(1)
