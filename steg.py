#!/usr/bin/env python

import sys, binascii, math
from PIL import Image

max_lsb = 1

def decode():
    global image, imagepath

    imagepath = sys.argv[2]
    image = Image.open(imagepath)


    # Available storage bits (3 (RGB) * width * height * max_lsb)
    max_bits = 3 * image.size[0] * image.size[1] * max_lsb
    image_data = list(image.convert("RGBA").getdata())

    size = ""
    # Gets the size of the hidden message
    for i in range(8):
        size += str(image_data[i][0] & 1)
        size += str(image_data[i][1] & 1)
        size += str(image_data[i][2] & 1)
    size = int(size,2)

    data = ""
    for i in range(size/3 + 1):
        data += str(image_data[i + 8][0] & 1)
        if (i * 3 + 2 <= size):
            data += str(image_data[i + 8][1] & 1)
        if (i * 3 + 3 <= size):
            data += str(image_data[i + 8][2] & 1)

    # Convert lsb data back into message
    data = hex(int(data,2))[2:]
    data = data[:len(data)-1]
    print "Message: %s" % binascii.unhexlify(data)

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
    image_data = list(image.getdata())

    new_image = Image.new('RGB', (image.width, image.height));
    new_image_data = new_image.getdata()

    data_iterator = 0
    for i in range(image.height * image.width):
            r = image_data[i][0]
            g = image_data[i][1]
            b = image_data[i][2]
            r = r >> 2
            r = r << 2
            g = g >> 2
            g = g << 2
            b = b >> 2
            b = b << 2
            if (i < 8):
                if (i * 3 < len(binsize)):
                    r += int (binsize[i * 3])
                    g += int (binsize[i * 3 + 1])
                    b += int(binsize[i * 3 + 2])
            if ((i >= 8) & (data_iterator < len(bintext))):
                r += int(bintext[data_iterator])
                if (data_iterator + 1 < len(bintext)):
                    g += int(bintext[data_iterator + 1])
                if (data_iterator + 2 < len(bintext)):
                    b += int(bintext[data_iterator + 2])
                data_iterator += 3

            new_image_data.putpixel((i % image.height, int (math.floor(i/image.height)) ), (r, g, b))

#    for i in range(image.width * image.height):
#        print new_image_data[i]
    print "Saving image"
    new_image.save( "test" + "-hidden.png", "PNG")








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

    #imagepath = sys.argv[2]
    #image = Image.open(imagepath)
