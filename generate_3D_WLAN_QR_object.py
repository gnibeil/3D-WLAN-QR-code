'''
This is a python programm to generate WLAN QR codes.
They contain additionally the information in a human readable form
The output of this programm is a picture of the QR code and a scad file that has to be run in OpenSCAD to get an stl file and to proceed from there.
Either to a 3d printer or Lasercutter or what ever you like
Author Simon Liebing 2020-2023
This programm is free software under BSD-3-CLause-license.
Some hints can be found under the following link:
* https://www.kite.com/blog/python/creating-3d-printed-wifi-access-qr-codes-with-python/
'''

import pyqrcode as pq
import numpy as np
# actually the python package is not called solid but solidpython
from solid2 import *
from PIL import ImageFont

def create_wifi_qr(ssid: str, security: str, password: str):
   '''
   Function to generate the image of an QR code with the WLAN credentials encoded into
   Input
      ssid .. string of the SSID 
      security ...  string encoding to encryption methods 
      password ... string representing the password
   Output
      qr   .... image of the QR code   
   '''
   qr = pq.create(f'WIFI:S:{ssid};T:{security};P:{password};;')
   return qr


#With that, we can create an array version of our QR code above:
def qr2array(qr):
   '''
   Function converting the QR code image to an nummerical array 
   Input
      qr   .... image of the QR code   
   Output
      arr  ... numpy array
   '''
   arr = []
   for line in qr.text().split('\n'):
      if len(line) != 0:
         arr.append([int(bit) for bit in line])
   return np.vstack(arr)

# define the parameters
# all are given as keyword argument
## ssid is self explainatory
ssid = 'SSID'
## security defines encryption
## possible are WEP, WPA (includes WPA2) or  nopass
security ='WPA'
## password gives the password in case of none give empty string
password = 'password'

## Incase of a nework without encryption use the following
#security='nopass'
#password=''

SCALE = 2  # output defaults to 1 mm per unit; this lets us increase the size of objects proportionally.
HEIGHT=2*SCALE
# The function in the Pillow package delivers text length supposingly in pixels. For our openSCAD code we need mm. I found the following number experimentally. I am very open to other numbers or an explenation why this is the correct number.
pix2mm=1.254

font='arial'
fontsize=9
fonta = ImageFont.truetype(font, fontsize)

fullpasswordline='PW: '+password

qr = create_wifi_qr(ssid, security, password)
qr.png('QRcode_wifi_'+ssid+'.png')
arr = qr2array(qr)

## now we have to determine the size of the base plate.
if (arr.shape[0]*SCALE+2*fontsize) >= max(fonta.getlength(fullpasswordline)*pix2mm,fonta.getlength(ssid)*pix2mm): 
   shift = 2*fontsize
else: 
   if fonta.getlength(ssid) >= fonta.getlength(fullpasswordline):
      shift=(fonta.getlength(ssid)*pix2mm-arr.shape[0]*SCALE)+2*fontsize
   else: 
      if fonta.getlength(password) > fonta.getlength(ssid):
         shift =(fonta.getlength(password)*pix2mm-arr.shape[0]*SCALE + 3*fontsize)
      else:
         shift =(fonta.getlength(ssid)*pix2mm-arr.shape[0]*SCALE + 3*fontsize)

# get the cubes of the QR code
cubes=[]
for i in range(arr.shape[0]):
   for j in range(arr.shape[1]):
      if arr[i,j] == 1:
         cubes.append(translate([i*SCALE+shift/2, j*SCALE+shift/2, 0])(color('black')(cube(size=[SCALE, SCALE, HEIGHT]))))
base_plate = color('white')(cube(size=(arr.shape[0] * SCALE + shift, arr.shape[1] * SCALE+shift, HEIGHT / 2)))
text_ssid= [translate(v=[(arr.shape[0] * SCALE+shift)/2, (arr.shape[1]*SCALE+shift-fontsize-2), HEIGHT/2]) (color('black')(linear_extrude(height=2) ( text(text=ssid, size=fontsize, font=font, halign = "center"))))]
# Deternmine the distribution of the password text
# Variante with PW and password on two lines
if shift > (fonta.getlength(ssid)*pix2mm -arr.shape[0]*SCALE+2*fontsize) and (fonta.getlength(ssid)*pix2mm -arr.shape[0]*SCALE+2*fontsize ) > 0:
   text_password= [translate(v=[(arr.shape[0] * SCALE+shift)/2, 1.5, HEIGHT/2]) (color('black')(linear_extrude(height=2) ( text(text=password, size=fontsize, font=font, halign = "center"))))]
   text_PW= [translate(v=[(arr.shape[0] * SCALE+shift)/2, 3+fontsize, HEIGHT/2]) (color('black')(linear_extrude(height=2) ( text(text='PW:', size=fontsize, font=font, halign = "center"))))]
   qrobj = union()(*cubes, base_plate,text_ssid,text_password,text_PW)
# Variante with PW and password on one line
else:   
   text_fullpassword= [translate(v=[(arr.shape[0] * SCALE+shift)/2, 2, HEIGHT/2]) (color('black')(linear_extrude(height=2) ( text(text=fullpasswordline, size=fontsize, font=font, halign = "center"))))]
   qrobj = union()(*cubes, base_plate,text_ssid,text_fullpassword)
# save the result
f=open('wlan_'+ssid+'_QRcode.scad','w')
f.write(scad_render(qrobj))
f.close()
