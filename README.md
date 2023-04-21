# 3D-WLAN-QR-code
Generate a 3D representation of a QR code of a WLAN and also written on in humanreadable form 
# Script to generate 3-D QR-codes for access to wireless networks

## Usage

* run python3 generate_3D_WLAN_QR_object.py 

### mandatory parameters
* SSID
* password
* security 

* incase of unsecure network set security to nopass and password to '' 
* options for security are nopass, WEP and WPA 
    * WPA includes WPA2

### optional parameters
   * Scaling factor for the QR code 
   * fontsize
   * font

## Requirements 
   * [solidPython2](https://github.com/jeff-dh/SolidPython)
   * [Pillow](https://pillow.readthedocs.io/en/stable/)
   * [numpy](https://numpy.org/)
   * [pyqrcode](https://pyqrcode.readthedocs.io/en/latest/)

You can install them by running
pip3 install -r requirements.txt

## The result of the code is a SCAD file. 

* This can be processed with openSCAD to an stl file.
* It can be included as an opject in an FreeCAD project.

