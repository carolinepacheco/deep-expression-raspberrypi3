# -*- coding: utf-8 -*-
# This are german umlauts äöü
# Author: Caroline Pacheco do E. Silva
# Date: 15/03/2018

from neopixel import *
import _rpi_ws281x as ws
import curses
import os
import math
import time

# screen setting variables
LED_COUNT      = 64
LED_LINE       = int(math.sqrt(LED_COUNT))
LED_PIN        = 18
LED_FREQ_HZ    = 800000
LED_DMA        = 5
LED_BRIGHTNESS = 8
LED_INVERT     = False
CHANNEL        = 0
STRIP_TYPE     = ws.WS2811_STRIP_GRB

# clean screen
def clearScreen(leds):
    for i in range(LED_COUNT):
        leds[i] = Color(0, 0, 0)

# screen display
def displayScreen(strip, leds):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, leds[i])
    strip.show()

# generic activation of leds
def addElement(elt, leds, color):
    for (x, y) in elt:
        leds[x + y * LED_LINE] = color

# activation of the leds of the emotions
def addEmotion(face, leds, result):
    if result == 'happy':
        addElement(face, leds, Color(128, 255, 0))   
    if result== 'angry':
        addElement(face, leds, Color(255, 0, 0))
    if result == 'neutral':
        addElement(face, leds, Color(51, 51, 255))
    if result == 'sad':
        addElement(face, leds, Color(102, 102, 0))  
    if result == 'disgust':
        addElement(face, leds, Color(153, 51, 255))  
    if result == 'fear':
        addElement(face, leds, Color(255, 153, 255))  # read emotions (.txt)
    if result == 'surprise':
        addElement(face, leds, Color(255, 102, 51))  # read emotions (.txt)
                
def readEmotion(filename):
    face = []
    try:
        with open(filename, 'r') as fic:
            level = fic.readlines()
    except:
        exit(1)

    for y in range(LED_LINE):
        for x, symbol in enumerate(level[y]):
            if symbol == 'X':
                face.append((x, y))
    return (face)
 
# beginning animation
def newAnimation(leds):
    for y in range(LED_LINE):
        for x in range(LED_LINE): 
            leds[x + y * LED_LINE] = Color(255, 0, 127)
        displayScreen(strip, leds)
        time.sleep(0.2)
        for x in range(LED_LINE): 
            leds[x + y * LED_LINE] = Color(0, 0, 0)

def led_emotions(result):

    # creation of an element allowing to "manipulate" the leds screen
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, CHANNEL, STRIP_TYPE)
     
    # initializing the screen
    strip.begin()

    # initializing the black leds
    leds = [Color(0, 0, 0)] * 64   

    # find all emotions (.txt)
    listeFichiers = os.listdir('emotions')
    for fichier in listeFichiers:
        if fichier == 'sad.txt' and result == 'sad':
             # reading emotion data
             expression = readEmotion('emotions/' + fichier)
              # add face expression 
             addEmotion(expression, leds, 'sad')
             # screen display
             displayScreen(strip, leds)
             # waiting for 3.1s
             time.sleep(3.1)
             # clean screen
             clearScreen(leds)
        if fichier == 'angry.txt' and result == 'angry':
              # reading emotion data
             expression = readEmotion('emotions/' + fichier)
             # add face expression 
             addEmotion(expression, leds, 'angry')
             # screen display
             displayScreen(strip, leds)
             # waiting for 3.1s
             time.sleep(3.1)
             # clean screen
             clearScreen(leds)             
        if fichier == 'happy.txt' and result == 'happy':
             # reading emotion data
             expression = readEmotion('emotions/' + fichier)
             # add face expression 
             addEmotion(expression, leds, 'happy')
             # screen display
             displayScreen(strip, leds)
             # waiting for 3.1s
             time.sleep(3.1)
             # clean screen
             clearScreen(leds)
        if fichier == 'neutral.txt' and result == 'neutral':
             # reading emotion data
             expression = readEmotion('emotions/' + fichier)
             # add face expression 
             addEmotion(expression, leds, 'neutral')
             # screen display
             displayScreen(strip, leds)
             # waiting for 3.1s
             time.sleep(3.1)
             # clean screen
             clearScreen(leds)             
        if fichier == 'disgust.txt' and result == 'disgust':
             # reading emotion data
             expression = readEmotion('emotions/' + fichier)
             # add face expression 
             addEmotion(expression, leds, 'disgust')
             # screen display
             displayScreen(strip, leds)
             # waiting for 3.1s
             time.sleep(3.1)
             # clean screen
             clearScreen(leds)    
        if fichier == 'fear.txt' and result == 'fear':
             # reading emotion data
             expression = readEmotion('emotions/' + fichier)
             # add face expression 
             addEmotion(expression, leds, 'fear')
             # screen display
             displayScreen(strip, leds)
             # waiting for 3.1s
             time.sleep(3.1)
             # clean screen
             clearScreen(leds)     
        if fichier == 'surprise.txt' and result == 'surprise':
             # reading emotion data
             expression = readEmotion('emotions/' + fichier)
             # add face expression 
             addEmotion(expression, leds, 'surprise')
             # screen display
             displayScreen(strip, leds)
             # waiting for 3.1s
             time.sleep(3.1)
             # clean screen
             clearScreen(leds)                                      
    
    # clearing the screen
    clearScreen(leds)
    displayScreen(strip, leds)