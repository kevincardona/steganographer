#!/usr/bin/env python

import sys
from PIL import Image

imagepath = sys.argv[1];

image = Image.open(imagepath)

print image.bits
