import cv2,math,os
import numpy as np
from PIL import Image
import time,datetime
import RPi.GPIO as GPIO
from Image_preprocessing import Distance,CropFace, takeSecond,yuchuli
from lcd import LCD1602
from  motor import Step_motor
from keyboard import keypad
from recognition import recognition


if __name__=="__main__":
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eyeCascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    recognizer = cv2.face.EigenFaceRecognizer_create()
    recognizer.read('trainer.yml')
    HC_SR505 = 11
    DX_206 = 4
    LED = 23
    Ring = 17
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(HC_SR505, GPIO.IN, pull_up_down=GPIO.PID_DOWN)
    GPIO.setup(DX_206, GPIO.IN, pull_up_down=GPIO.PID_DOWN)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(Ring, GPIO.OUT)
    GPIO.add_event_detect(HC_SR505, GPIO.RISING, callback=my_callbak, bouncetime=1000 * 50)
    password='1234567'#z设置密码
    motor=Step_motor(2,3,14,15)
    keyboard=(12,16,20,21,6,13,19,26)
    lcd=LCD1602(7,8,25,24,23,18)
    lcd_line1=0x80
    lcd_line2=0xC0
    Out_password=''
    try:
        while(True):
            if GPIO.input(DX_206):
                lcd.lcd_string('', lcd_line2)
                word = keyboard.get_key()
                time.sleep(0.2)
                word = keyboard.get_key()
                if word:
                    Out_password +=str(word)
                    lcd.lcd_string(Out_password,lcd_line1)
                    time.sleep(0.1)
                    if Out_password == password:
                        lcd.lcd_string('success', lcd_line2)
                        motor.back(3,500)
                        time.sleep(2)
                        lcd.lcd_string('', lcd_line1)
                        Out_password=''
                    elif Outpassword != password and len(Out_password)>=6:
                        lcd.lcd_string('wrong',lcd_line2)
                        Out_password = ''
                        GPIO.output(Ring,1)
                        time.sleep(3)
            else:
                pass
    finally:
        GPIO.cleanup()

def my_callback(channel):
    if GPIO.input(DX_206):
        GPIO.output(LED,1)
        name,confidence=recognition()
        if name== 'Marcelo' and confidence >=0.5:
            lcd.lcd_string('face_right',lcd_line1)
            motor.back(3,500)
        else:
            lcd.lcd_string('face_wrong',lcd_line1)
            GPIO.output(Ring,1)
            time.sleep(2)
            GPIO.output(Ring,0)
            GPIO.output(LED,0)




