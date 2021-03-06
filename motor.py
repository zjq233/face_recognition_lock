import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#将5V步进电机模块写成类
class Step_motor:
    #初始化函数，设置了4个参数，分别为IN4到IN1对应树莓派的引脚
    def __init__(self,IN4A,IN3B,IN2C,IN1D):
        self.forward_seq=['1100','0110','0011','1001']  #电机正转的一个脉冲，4步
        self.back_seq=['1100','1001','0011','0110']      #电机反转的一个脉冲，4步
        #设置4个引脚口为输出口
        self.IN4A=IN4A
        GPIO.setup(self.IN4A,GPIO.OUT)
        self.IN3B=IN3B
        GPIO.setup(self.IN3B,GPIO.OUT)
        self.IN2C=IN2C
        GPIO.setup(self.IN2C,GPIO.OUT)
        self.IN1D=IN1D
        GPIO.setup(self.IN1D,GPIO.OUT)
   #电机正转
    def forward(self,delay,steps):
        for i in range(steps):
            for step in self.forward_seq:
                self.set_step(step)
                time.sleep(int(delay)/1000.0)
        self.stop()
    #电机反转
    def back(self,delay,steps):
        for i in range(steps):
            for step in self.back_seq:
                self.set_step(step)
                time.sleep(int(delay)/1000.0)
        self.stop()
    #给电机一个脉冲
    def set_step(self,step):
        GPIO.output(self.IN4A,step[0]=='1')
        GPIO.output(self.IN3B,step[1]=='1')
        GPIO.output(self.IN2C,step[2]=='1')
        GPIO.output(self.IN1D,step[3]=='1')
    #电机停转
    def stop(self):
        GPIO.output(self.IN4A,False)
        GPIO.output(self.IN3B,False)
        GPIO.output(self.IN2C,False)
        GPIO.output(self.IN1D,False)
'''
if __name__=="__main__":
    HRC505=18
    i=0
    GPIO.setup(HRC505,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    motor=Step_motor(7,8,14,15)
    def my_callback(channel):
        motor.forward(5,10)
    GPIO.add_event_detect(18,GPIO.FALLING,callback=my_callback)
    try:
        while (True):
            time.sleep(1)
            i=i+1
    finally:
        print('clean')
        GPIO.cleanup()
            
    #GPIO.add_event_detect(18,GPIO.RISING,callback=motor.forward(5,640*2))
'''