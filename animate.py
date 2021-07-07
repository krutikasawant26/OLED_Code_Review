# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import math
import time

#import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json
import os.path
from os import path

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Get display width and height.
width = disp.width
height = disp.height

# Clear display.
disp.clear()
disp.display()

# Create image buffer.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (width, height))

# Load default font.
#font = ImageFont.load_default();

font = ImageFont.truetype("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf", 12);
JSON_FILE_PATH ="/dev/shm/mjpeg/fd_output.json" 
# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as this python script!
# Some nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)
# Create drawing object.
draw = ImageDraw.Draw(image)
draw.text((40, 2), '6th SENSE',  font=(font), fill=255)
draw.text((40, 17),'   DMS', font=(font), fill=255)
disp.image(image)
disp.display()

time.sleep(5)
disp.clear()
disp.display()
PrevTimestamp = 0
Timestamp = 0
#open JSON file and read the tag
while os.path.isfile(JSON_FILE_PATH) == 0 :
    #print("File not present")
    PrevTimestamp = 0
    prev_modificationTime = 0
    modificationTime = 1;
#file is at /dev/shm/mjpeg

    while True:
        
        if os.path.isfile(JSON_FILE_PATH):

             file_status_Obj = os.stat(JSON_FILE_PATH)
             modificationTime = time.ctime(file_status_Obj[stat.ST_MTIME])

             if modificationTime == prev_modificationTime:
         
                prev_modificationTime = modificationTime
                 #else if os.path.isfile(JSON_FILE_PATH):
                #print("File present")
             else:
                prev_modificationTime = modificationTime
                try:
                    with open(JSON_FILE_PATH) as file:
                    
                        try:
                            data = json.load(file)
                            file.close
                
                            Alert_Type = data["faces"][0]["alert_type"]
                            Timestamp = data["timestamp"]
                            
                        except :
                            PrevTimestamp = Timestamp 
                except :
                    PrevTimestamp = Timestamp      

            
            #print(Timestamp)

                if Timestamp == PrevTimestamp:
                
                #time.sleep(1)
                    PrevTimestamp = Timestamp 
                else :
                #print(Alert_Type)
                    PrevTimestamp = Timestamp            
                #print("\r\n 1 sec sleep \r\n")
                    image2 = Image.new('1', (width, height))
                    draw = ImageDraw.Draw(image2)
                    if Alert_Type == "DROWSINESS":
                        draw.text((40, 1),  'DRIVER',  font=(font), fill=255)
                        draw.text((40, 20), 'DROWSY', font=(font), fill=255)
                        disp.image(image2)
                        disp.display()
                        time.sleep(5)
                        disp.clear()
                        disp.display()
                    elif Alert_Type == "DISTRACTED":
                        draw.text((40, 1),  'DRIVER',  font=(font), fill=255)
                        draw.text((40, 20), 'DISTRACTED', font=(font), fill=255)
                        disp.image(image2)
                        disp.display()
                        time.sleep(5)
                        disp.clear()
                        disp.display()

                    elif Alert_Type == "NO_DRIVER":
                        draw.text((40, 1),  'DRIVER',  font=(font), fill=255)
                        draw.text((40, 20), 'ABSENT', font=(font), fill=255)
                        disp.image(image2)
                        disp.display()
                        time.sleep(5)
                        disp.clear()
                        disp.display()
                    

                    elif Alert_Type == "":
                        draw.text((40, 1),  'DRIVER',  font=(font), fill=255)
                        draw.text((30, 20), 'DISTRACTED',font=(font),fill=255)
                        disp.image(image2)
                        disp.display()
                        time.sleep(5)
                        disp.clear()
                        disp.display()
                    
                
            
        else :
    #print("file absent")
            image1 = Image.new('1', (width, height))
            draw = ImageDraw.Draw(image1)
            draw.text((40, 1),'***Error***',  font=(font), fill=255)
            draw.text((40, 20),'***********', font=(font), fill=255)
            disp.image(image1)
            disp.display()
            time.sleep(5)
            disp.clear()
            disp.display()

