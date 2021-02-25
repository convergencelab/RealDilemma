import RPi.GPIO as GPIO
import time
import numpy as np
"""
Abstract actions from algorithm:
"""

TESTING = True


class PiBot:

    def __init__(self,
                 GPIO_SERVO: int = 11,
                 GPIO_TRIGGER: int = 12,
                 GPIO_ECHO: int = 24,
                 GPIO_LEFT_FORWARD: int = 16,
                 GPIO_LEFT_BACKWARD: int = 18,
                 GPIO_LEFT_PWM: int = 22,
                 GPIO_RIGHT_FORWARD: int = 29,
                 GPIO_RIGHT_BACKWARD: int = 31,
                 GPIO_RIGHT_PWM: int = 26):

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
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

        # setup GPIO
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)  # output
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)  # input
        GPIO.setup(self.GPIO_SERVO, GPIO.OUT)
        GPIO.setup(self.GPIO_LEFT_PWM, GPIO.OUT)  # en1
        GPIO.setup(self.GPIO_LEFT_FORWARD, GPIO.OUT)  # IN1
        GPIO.setup(self.GPIO_LEFT_BACKWARD, GPIO.OUT)  # IN2
        GPIO.setup(self.GPIO_RIGHT_PWM, GPIO.OUT)  # EN2
        GPIO.setup(self.GPIO_RIGHT_FORWARD, GPIO.OUT)  # IN4
        GPIO.setup(self.GPIO_RIGHT_BACKWARD, GPIO.OUT)  # IN3
        self.servo = GPIO.PWM(self.GPIO_SERVO, 100)  # 11 = pin, 50 = 50hz

        # motors
        self.l_pwm = GPIO.PWM(self.GPIO_LEFT_PWM, 100)
        self.r_pwm = GPIO.PWM(self.GPIO_RIGHT_PWM, 100)

        # start PWM
        self.servo.start(0)  # 0 -> pulse off
        self.l_pwm.start(0)  # 0 -> pulse off
        self.r_pwm.start(0)  # 0 -> pulse off

        # [forwards, backwards, cw, ccw, turn servo], Ultrasound sensor]
        self._total_actions = np.zeros(5)
        self._state = np.zeros(2, dtype=np.int32)
        self.testing = TESTING

    def read_ultrasound(self):
        """
        Function to get distance from ultrasound sensor
        """
        if self.testing:
            print("read us")
            return 0
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



    def forward(self, d):
        # r or l
        GPIO.output(self.GPIO_RIGHT_FORWARD, True)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, False)
        # r or l
        GPIO.output(self.GPIO_LEFT_FORWARD, True)
        GPIO.output(self.GPIO_LEFT_BACKWARD, False)
        # set duty for both motors
        self.l_pwm.ChangeDutyCycle(100)
        self.r_pwm.ChangeDutyCycle(100)
        GPIO.output(self.GPIO_RIGHT_PWM, True)
        GPIO.output(self.GPIO_LEFT_PWM, True)
        time.sleep(d)
        # set duty for both motors
        self.l_pwm.ChangeDutyCycle(0)
        self.r_pwm.ChangeDutyCycle(0)
        # update state, set last action taken and read ultrasound sensor
        self._state[0] = 0
        self._state[1] = min(self.read_ultrasound(), 1000)
        self._total_actions[0]+=d
        if self.testing:
            print(f"forwards: {d}")

    def backward(self, d):
        # r or l
        GPIO.output(self.GPIO_RIGHT_FORWARD, False)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, True)
        # r or l
        GPIO.output(self.GPIO_LEFT_FORWARD, False)
        GPIO.output(self.GPIO_LEFT_BACKWARD, True)
        # set duty for both motors
        self.l_pwm.ChangeDutyCycle(100)
        self.r_pwm.ChangeDutyCycle(100)
        GPIO.output(self.GPIO_RIGHT_PWM, True)
        GPIO.output(self.GPIO_LEFT_PWM, True)
        time.sleep(d)
        # set duty for both motors
        self.l_pwm.ChangeDutyCycle(0)
        self.r_pwm.ChangeDutyCycle(0)
        # update state, set last action taken and read ultrasound sensor
        self._state[0] = 1
        self._state[1] = min(self.read_ultrasound(), 1000)
        self._total_actions[1] += d
        if self.testing:
            print(f"backwards: {d}")


    def turn_cw(self, d):
        # r or l
        GPIO.output(self.GPIO_RIGHT_FORWARD, True)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, False)
        # r or l
        GPIO.output(self.GPIO_LEFT_FORWARD, False)
        GPIO.output(self.GPIO_LEFT_BACKWARD, True)
        # set duty for both motors
        self.l_pwm.ChangeDutyCycle(100)
        self.r_pwm.ChangeDutyCycle(100)
        GPIO.output(self.GPIO_RIGHT_PWM, True)
        GPIO.output(self.GPIO_LEFT_PWM, True)
        time.sleep(d)
        # set duty for both motors
        self.l_pwm.ChangeDutyCycle(0)
        self.r_pwm.ChangeDutyCycle(0)
        # update state, set last action taken and read ultrasound sensor
        self._state[0] = 2
        self._state[1] = min(self.read_ultrasound(), 1000)
        self._total_actions[2] += d
        if self.testing:
            print(f"cw: {d}")

    def turn_ccw(self, d):
        # r or l
        GPIO.output(self.GPIO_RIGHT_FORWARD, False)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, True)
        # r or l
        GPIO.output(self.GPIO_LEFT_FORWARD, True)
        GPIO.output(self.GPIO_LEFT_BACKWARD, False)
        # set duty for both motors
        self.l_pwm.ChangeDutyCycle(100)
        self.r_pwm.ChangeDutyCycle(100)
        GPIO.output(self.GPIO_RIGHT_PWM, True)
        GPIO.output(self.GPIO_LEFT_PWM, True)
        time.sleep(d)
        # set duty for both motors
        self.l_pwm.ChangeDutyCycle(0)
        self.r_pwm.ChangeDutyCycle(0)
        # update state, set last action taken and read ultrasound sensor
        self._state[0] = 3
        self._state[1] = min(self.read_ultrasound(), 1000)
        self._total_actions[3] += d
        if self.testing:
            print(f"ccw: {d}")

    def turn_servo(self, d):
        """
        turn servo, range between 0 - 12
        """
        self.servo.ChangeDutyCycle(d)
        # update state, set last action taken and read ultrasound sensor
        self._state[0] = 4
        self._state[1] = int(min(self.read_ultrasound(), 1000))
        self._total_actions[4] += d
        if self.testing:
            print(f"servo: {d}")

    def get_state(self):
        return self._state

    def get_total_actions(self):
        return self._total_actions

    def reset(self):
        self.l_pwm.stop()
        self.r_pwm.stop()
        self.servo.stop()
        GPIO.cleanup()
        self.__init__()


    def test(self):
        """
        test physical components
        """
        self.forward(1)
        self.backward(1)
        self.turn_ccw(1)
        self.turn_cw(1)
        self.l_pwm.ChangeDutyCycle(0)
        self.r_pwm.ChangeDutyCycle(0)
        GPIO.cleanup()

    def run(self):
        while True:
            cmd = input()
            if cmd == "f":
                self.forward(1)
            elif cmd == "b":
                self.backward(1)
            elif cmd == "l":
                self.turn_ccw(1)
            elif cmd == "r":
                self.turn_cw(1)
            else:
                print("incorrect cmd")

    def __del__(self):
        GPIO.cleanup()


if __name__ == "__main__":
    pibot = PiBot()
    pibot.run()


