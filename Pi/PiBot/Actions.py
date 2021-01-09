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
                 GPIO_ECHO: int = 24):
        
        # pins
        self.GPIO_SERVO: int = GPIO_SERVO
        self.GPIO_TRIGGER: int = GPIO_TRIGGER
        self.GPIO_ECHO: int = GPIO_ECHO
                 
                 
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT) # output
        GPIO.setup(self.GPIO_ECHO, GPIO.IN) # input
        GPIO.setup(self.GPIO_SERVO, GPIO.OUT)
        self.servo = GPIO.PWM(11,50) # 11 = pin, 50 = 50hz
        # start PWM
        self.servo.start(0) # 0 -> pulse off
        time.sleep(2)
        # duty for pwm
        self.duty = 2


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
        
    def motor_left(self):
        raise NotImplementedError
    
    def motor_right(self):
        raise NotImplementedError
    
    def test(self):
        """
        test physical components
        """
        for i in range(12):
            self.turn_servo(i)
            us = self.read_ultrasound()
            print(f"ultrasound: {us}")
        
    
    def __del__(self):
        GPIO.cleanup()
        
