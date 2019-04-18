import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#将4*4键盘写成一个类
class keypad:
    '''类初始化函数，8个参数，分别是键盘行和列的GPIO口'''
    def __init__(self,row1,row2,row3,row4,col1,col2,col3,col4):
        self.rows=[row1,row2,row3,row4]#按顺序记录每一行的GPIO口
        self.cols=[col1,col2,col3,col4]#按顺序记录每一列的GPIO口
        #保存行和列组合对应的键盘信息
        self.keys=[['1','2','3','A'],
               ['4','5','6','B'],
               ['7','8','9','C'],
               ['*','0','#','D']]
        #设置每一行对应的引脚为输入端口，并且常态为低电平，每一列对应的引脚为输出引脚
        for row_pin in self.rows:
            GPIO.setup(row_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

        for col_pin in self.cols:
            GPIO.setup(col_pin,GPIO.OUT)
#读取键盘按下的按键
    def get_key(self):
        key = 0 #用于保存按下的键盘信息
        #扫描每一列
        for col_num,col_pin in enumerate(self.cols):
            GPIO.output(col_pin,1) #设置高电平
            for row_num,row_pin in enumerate(self.rows):
                if GPIO.input(row_pin):    #读取行引脚状态，若为高，取行和列序列号，
                    key=self.keys[row_num][col_num] #得出按键的信息
            GPIO.output(col_pin,0)
        return key

'''
if __name__=="__main__":
    #Inpassword=input("please set a 6-digit password for the lock")
    Inpassword='123456'
    motor=Step_motor(2,3,14,15)
    keyboard=keypad(12,16,20,21,6,13,19,26)
    Outpassword=''
    try:
        while(True):
            word =keyboard.get_key()
            time.sleep(0.2)
            word =keyboard.get_key()   
            if word:
                print(word)
                Outpassword += str(word)
                time.sleep(0.1)
                if len(Outpassword) == 6:
                    if Outpassword == Inpassword:
                        print('success to open the lock')
                        motor.forward(5,500)
                        
                        Outpassword=''
                        
                    else :
                        print('password wrong')
    finally:
        print('clean')
        GPIO.cleanup()
'''

           

