# steganographer
<div width="50%" margin="auto" align="center" style="float: left;">
  <br>
  <b>Python program used to hide data inside of images using LSB Steganography.</b>
  <br><br>
</div>



<img width="49%" src="https://raw.githubusercontent.com/kevincardona/steganographer/master/images/car.png?token=AK4Wl2FOfr2aWwpaB29ovBloCd5QOvkkks5aO-ZuwA%3D%3D"></img>
<img width="49%" src="https://raw.githubusercontent.com/kevincardona/steganographer/master/steg-images/car.png?token=AK4Wl4knEEVoR6FrkLsCLiCnxoBHLc2Wks5aO-ZDwA%3D%3D"></img>
<div width="50%" margin="auto" align="center" style="float: left;">
  <b>The image on the left is the original image and the one on the right has a secret message in it.</b>
  
  By using the LSB of each pixel in the image to store data the human eye cannot detect any image abnormalities.
</div>


usage
-----
```bash
steg.py

Usage: 
  encode <image> <message>
  decode <image>
```
