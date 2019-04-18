# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:29:43 2019

@author: Administrator
"""
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 

#定义LCD类 ，
class LCD1604:
  #lcd类的初始化函数，有6个参数，分别是lcd6个引脚对应树莓派的6个引脚，并且设置为输出引脚
    def __init__(self,LCD_RS,LCD_E,LCD_D4,LCD_D5,LCD_D6,LCD_D7,LCD_D8):
        self.LCD_RS = LCD_RS
        self.LCD_E  = LCD_E
        self.LCD_D4 = LCD_D4
        self.LCD_D5 = LCD_D5
        self.LCD_D6 = LCD_D6
        self.LCD_D7 = LCD_D8
        GPIO.setup(LCD_E, GPIO.OUT)  
        GPIO.setup(LCD_RS, GPIO.OUT) 
        GPIO.setup(LCD_D4, GPIO.OUT) 
        GPIO.setup(LCD_D5, GPIO.OUT) 
        GPIO.setup(LCD_D6, GPIO.OUT) 
        GPIO.setup(LCD_D7, GPIO.OUT) 
        self.LCD_WIDTH = 16 #行长度
        self.LCD_CHR = True #写数据标志位
        self.LCD_CMD = False #写命令标志位
        self.LCD_LINE_1 = 0x80 # lcd屏幕第一行初始地址
        self.LCD_LINE_2 = 0xC0 # lcd屏幕第二行初始地址
        self.E_PULSE = 0.0005  #使能上升时间
        self.E_DELAY = 0.0005  #使能延时时间
        self.lcd_init() #lcd初始化
        
    #执行触发使能函数
    def lcd_toggle_enable(self):
        time.sleep(self.E_DELAY)
        GPIO.output(self.LCD_E, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)
        time.sleep(self.E_DELAY) 

    '''lcd的写操作函数，有两个参数，第一个为数据，第二个为标志为，
    为True时写数据，False时为写命令'''
    def lcd_byte(self,bits, mode):
        GPIO.output(self.LCD_RS, mode) 
        #低4位数据
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.LCD_D4, True)
        if bits&0x20==0x20:
            GPIO.output(self.LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(self.LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(self.LCD_D7, True)
        
        self.lcd_toggle_enable() #触发执行  
        #高4位数据
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x10==0x01:
            GPIO.output(self.LCD_D4, True)
        if bits&0x20==0x02:
            GPIO.output(self.LCD_D5, True)
        if bits&0x40==0x04:
            GPIO.output(self.LCD_D6, True)
        if bits&0x80==0x08:
            GPIO.output(self.LCD_D7, True)

        self.lcd_toggle_enable()#触发执行
 
    #lcd初始化函数
    def lcd_init(self):
      self.lcd_byte(0x33,self.LCD_CMD) # 初始化
      self.lcd_byte(0x32,self.LCD_CMD) # 初始化
      self.lcd_byte(0x06,self.LCD_CMD) # 设置光标
      self.lcd_byte(0x0C,self.LCD_CMD) # 打开LCD显示，光标不显示，光标字符不闪烁
      self.lcd_byte(0x28,self.LCD_CMD) # 设置数据位为4位，2行显示，5*7点阵字符
      self.lcd_byte(0x01,self.LCD_CMD) # 清屏
      time.sleep(self.E_DELAY)    
    
    #显示数据函数，一个有两个参数，第一个是要显示的内容，第二个是要显示所在的地址
    def lcd_string(self,message,line):
        message = message.ljust(self.LCD_WIDTH," ")
        self.lcd_byte(line, self.LCD_CMD) 
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]),self.LCD_CHR)
 
 
    
'''    
def main():
  # Main program block
        # Use BCM GPIO numbers
  
 
  # Initialise display
  lcd_init()
 
  while True:
 
    # Send some test
    lcd_string("Rasbperry Pi",LCD_LINE_1)
    lcd_string("16x2 LCD Test",LCD_LINE_2)
 
    time.sleep(3) # 3 second delay
 
    # Send some text
    lcd_string("1234567890123456",LCD_LINE_1)
    lcd_string("abcdefghijklmnop",LCD_LINE_2)
 
    time.sleep(3) # 3 second delay
 
    # Send some text
    lcd_string("Basemu.com",LCD_LINE_1)
    lcd_string("Welcome",LCD_LINE_2)
 
    time.sleep(3)
 
    # Send some text
    lcd_string("Welcome to",LCD_LINE_1)
    lcd_string("Basemu.com",LCD_LINE_2)
 
    time.sleep(3)
 

 


 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()
    '''