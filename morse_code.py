#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import argparse

class MorseCode:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        
        GPIO.setup(7, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT)

        GPIO.output(11, True)
        
        self.timeUnit = 0.2

    def __del__(self):
        GPIO.output(11, False)
        GPIO.cleanup()
        
    def gpioOutput(self, value):
        valueUnitMultiplier = 1
        
        if value:
            valueUnitMultiplier = 3
            
        GPIO.output(7, True)
        time.sleep(self.timeUnit * valueUnitMultiplier)
        GPIO.output(7, False)

    def translateCharacter(self, char):
        def codeToBool(ditdah):
            if ditdah == "-":
                return True
            return False
        
        morseCodeDict = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-', '!':'-.-.--'}
        
        charCode = morseCodeDict[char.upper()]
        boolCode = [codeToBool(c) for c in charCode]
        return boolCode

    def ledOutputText(self, text):
        for char in text:
            if char == " ":
                time.sleep(self.timeUnit * 2)
            else:
                ditdahs = self.translateCharacter(char)

                for dotordash in ditdahs:
                    self.gpioOutput(dotordash)
                    time.sleep(self.timeUnit * 1)

    def outputCode(self, text):
        translatedCode = ""
        for char in text:
            if char == " ":
                translatedCode += "  "
            else:
                ditdahs = self.translateCharacter(char)

                for dotordash in ditdahs:
                    if dotordash:
                        translatedCode += '-'
                    else:
                        translatedCode += '.'
                translatedCode += " "
        print (translatedCode)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Basic morse code translator with ability to output code via LED through GPIOs on Raspberry Pi")
    parser.add_argument("input", metavar="S", help="Input to translate")

    args = parser.parse_args()
    stringToTranslate = args.input

    myMorse = MorseCode()

    myMorse.outputCode(stringToTranslate)
    myMorse.ledOutputText(stringToTranslate)

    print("Complete!")
    
