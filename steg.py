#!/usr/bin/env python

import sys, binascii
from PIL import Image

max_lsb = 2

def encode():
    global image, imagepath
    rawtext = sys.argv[3]
    bintext = bin(int(binascii.hexlify(rawtext),16))
    bintext = bintext[:1] + bintext[2:]
    print bintext
    imagepath = sys.argv[2]
    image = Image.open(imagepath)


    # Available storage bits (3 (RGB) * width * height * max_lsb)
    max_bits = 3 * image.size[0] * image.size[1] * max_lsb
    image_data = list(image.getdata())
    data_iterator = 0

    working = True
    x = 5;
    print "x : %d" % x
    x = x >> 2
    x = x << 2
    print "x2 : %d" % x
#        while (working):
#            rgb = list(image_data[data_iterator])
#            for i in range(3):
    






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
        print "TODO: Implement decode"
        sys.exit(1)

    #imagepath = sys.argv[2]
    #image = Image.open(imagepath)
