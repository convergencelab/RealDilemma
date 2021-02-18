import RPi.GPIO as GPIO
import time
"""
Abstract actions from algorithm:
"""
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Actions:
    def __init__(self,
                 GPIO_SERVO: int = 11,
                 GPIO_TRIGGER: int = 12,
                 GPIO_ECHO: int = 24,
                 GPIO_LEFT_FORWARD: int = 18,
                 GPIO_LEFT_BACKWARD: int = 16,
                 GPIO_LEFT_PWM: int = 22,
                 GPIO_RIGHT_FORWARD: int = 31,
                 GPIO_RIGHT_BACKWARD: int = 29,
                 GPIO_RIGHT_PWM: int = 37):
        
        # pins
        self.GPIO_SERVO: int = GPIO_SERVO
        self.GPIO_TRIGGER: int = GPIO_TRIGGER
        self.GPIO_ECHO: int = GPIO_ECHO
        self.GPIO_LEFT_FORWARD: int = GPIO_LEFT_FORWARD
        self.GPIO_LEFT_BACKWARD: int = GPIO_LEFT_BACKWARD
        self.GPIO_LEFT_PWM: int = GPIO_LEFT_PWM
        self.GPIO_RIGHT_FORWARD: int = GPIO_RIGHT_FORWARD
        self.GPIO_RIGHT_BACKWARD: int = GPIO_RIGHT_BACKWARD
        self.GPIO_RIGHT_PWM: int = GPIO_RIGHT_PWM
        
        
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT) # output
        GPIO.setup(self.GPIO_ECHO, GPIO.IN) # input
        GPIO.setup(self.GPIO_SERVO, GPIO.OUT)
        GPIO.setup(self.GPIO_LEFT_PWM, GPIO.OUT)
        GPIO.setup(self.GPIO_LEFT_FORWARD, GPIO.OUT)
        GPIO.setup(self.GPIO_LEFT_BACKWARD, GPIO.OUT)
        GPIO.setup(self.GPIO_RIGHT_PWM, GPIO.OUT)
        GPIO.setup(self.GPIO_RIGHT_FORWARD, GPIO.OUT)
        GPIO.setup(self.GPIO_RIGHT_BACKWARD, GPIO.OUT)
        self.servo = GPIO.PWM(self.GPIO_SERVO,50) # 11 = pin, 50 = 50hz
        
       
        
        # motors
        self.l_pwm = GPIO.PWM(self.GPIO_LEFT_PWM,100)
        self.r_pwm = GPIO.PWM(self.GPIO_RIGHT_PWM,100)
        
        # start PWM
        self.servo.start(0) # 0 -> pulse off
        self.l_pwm.start(0) # 0 -> pulse off
        self.r_pwm.start(0) # 0 -> pulse off
        self.l_pwm.ChangeDutyCycle(0)
        self.r_pwm.ChangeDutyCycle(0)
        GPIO.output(self.GPIO_LEFT_FORWARD, GPIO.LOW)
        GPIO.output(self.GPIO_RIGHT_FORWARD, GPIO.LOW)
        GPIO.output(self.GPIO_LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, GPIO.LOW)
        time.sleep(2)
        


    def read_ultrasound(self):
        """
        Function to get distance from ultrasound sensor
        """
        # trig set to high
        GPIO.output(self.GPIO_TRIGGER, True)
        
        # set trig to low after 0.01ms
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
        StartTime = time.time()
        StopTime = time.time()
        
        while GPIO.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
            
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()

        del_time = StopTime - StartTime
        # mult with sonic speed and dive by 2 (back and fourth)
        distance = (del_time * 34300) / 2
        return distance
    
    def turn_servo(self, duty):
        """
        turn servo, range between 0 - 12
        """
        self.servo.ChangeDutyCycle(duty)
        
    def forward(self, d):
        
        # set motors pwm to designated duty
        self.l_pwm.ChangeDutyCycle(d)
        self.r_pwm.ChangeDutyCycle(d)
        GPIO.output(self.GPIO_LEFT_FORWARD, GPIO.HIGH)
        GPIO.output(self.GPIO_RIGHT_FORWARD, GPIO.HIGH)
        print("Moving Forward")
        #time.sleep(5)
        # set back to zero
        #GPIO.output(self.GPIO_LEFT_FORWARD, GPIO.LOW)
        #GPIO.output(self.GPIO_RIGHT_FORWARD, GPIO.LOW)
        #self.l_pwm.ChangeDutyCycle(0)
        #self.r_pwm.ChangeDutyCycle(0)
    
    def backward(self, d):
        GPIO.output(self.GPIO_LEFT_BACKWARD, GPIO.LOW)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, GPIO.LOW)
        self.l_pwm.ChangeDutyCycle(0)
        self.r_pwm.ChangeDutyCycle(0)
        # set motors pwm to designated duty
        self.l_pwm.ChangeDutyCycle(d)
        self.r_pwm.ChangeDutyCycle(d)
        GPIO.output(self.GPIO_LEFT_BACKWARD, GPIO.HIGH)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, GPIO.HIGH)
        print("Moving Backward")
        # time.sleep(5)
        # set back to zero
        #GPIO.output(self.GPIO_LEFT_BACKWARD, GPIO.LOW)
        #GPIO.output(self.GPIO_RIGHT_BACKWARD, GPIO.LOW)
        #self.l_pwm.ChangeDutyCycle(0)
        #self.r_pwm.ChangeDutyCycle(0)
        
    def motor_left(self):
        raise NotImplementedError
    
    def motor_right(self):
        raise NotImplementedError
    
    def test(self):
        """
        test physical components
        """
        #while True:
          #  self.forward(100)
          #  self.backward(100)
        for i in range(12):
            self.forward(100)
            self.backward(100)
            #self.turn_servo(i)
            #us = self.read_ultrasound()
            #print(f"ultrasound: {us}")
            time.sleep(1)
        
    
    def __del__(self):
        GPIO.cleanup()
        
