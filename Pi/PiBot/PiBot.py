import RPi.GPIO as GPIO
import time
import numpy as np
"""
Abstract actions from algorithm:
"""

TESTING = True


class PiBot:
    """
    Standard PiBot
    No PWM control only time control on motors
    """
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
        self.l_pwm.stop()
        self.r_pwm.stop()
        self.servo.stop()
        GPIO.cleanup()


class PiBot2(PiBot):
    """
    more complexity added,
    improvements on resolution of ultrasound resolution
    change nature of turning

    """
    # variables for
    TURN_PWM_CCW = 100, 100
    TURN_PWM_CW = 100, 100
    US_RES = 0
    US_THRES = 0
    MIN_SCORE = 0
    def __init__(self, us_res=US_RES,
                 us_thres=US_THRES,
                 min_score=MIN_SCORE,
                 turn_pwm_ccw = TURN_PWM_CCW,
                 turn_pwm_cw = TURN_PWM_CW):
        super(PiBot2, self).__init__()
        # hyperparams for action #
        self._us_res = us_res # resolution for ultrasound reading (# of readings per action)
        self._us_thres = us_thres # threshold for a "bad distance" in the reading
        self._min_score = min_score # the minimum score for considering an series of actions bad
        self._turn_pwm_ccw = turn_pwm_ccw
        self._turn_pwm_cw = turn_pwm_cw
        # redefine the total actions as a int score #
        self._total_actions = 0

    def forward(self, duty, n):
        """
        move forward: action = 0
        :param duty: the duty to put on the servo
        :param n: number of seconds
        :return: outcome
        """

        # set motor control
        GPIO.output(self.GPIO_RIGHT_FORWARD, True)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, False)
        GPIO.output(self.GPIO_LEFT_FORWARD, True)
        GPIO.output(self.GPIO_LEFT_BACKWARD, False)
        # move robot in designated direction
        return travel(duty, n)

    def backward(self, duty, n):
        """
        move forward: action = 0
        :param duty: the duty to put on the servo
        :param n: number of seconds
        :return: outcome
        """
        # set motor control
        GPIO.output(self.GPIO_RIGHT_FORWARD, False)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, True)
        GPIO.output(self.GPIO_LEFT_FORWARD, False)
        GPIO.output(self.GPIO_LEFT_BACKWARD, True)
        # move robot in designated direction
        return travel(duty, n)

    def turn_cw(self, duty, n):
        """
        problem with PiBot 1 turning is that it spins to hard
        and does not really act how we want it to.
        we will adjust these settings with the global variables
        TURN_PWM_*
        :param duty:
        :param n:
        :return:
        """
        GPIO.output(self.GPIO_RIGHT_FORWARD, True)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, False)
        GPIO.output(self.GPIO_LEFT_FORWARD, False)
        GPIO.output(self.GPIO_LEFT_BACKWARD, True)
        return travel(duty, n, self._turn_pwm_cw)

    def turn_ccw(self, duty, n):
        """
        problem with PiBot 1 turning is that it spins to hard
        and does not really act how we want it to.
        we will adjust these settings with the global variables
        TURN_PWM_*
        :param duty:
        :param n:
        :return:
        """
        GPIO.output(self.GPIO_RIGHT_FORWARD, False)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, True)
        GPIO.output(self.GPIO_LEFT_FORWARD, True)
        GPIO.output(self.GPIO_LEFT_BACKWARD, False)
        return travel(duty, n, self._turn_pwm_ccw)


    def travel(self, duty, n, turning=None):
        """
        helper function for forwards and backwards, left and right motion
        :param n:
        :param turning: contains amount of duty for l and right motor for turning
        :param duty:
        :return:
        """
        output = []
        output.append(self.read_ultrasound())
        score = []
        t = n / self._us_res  # time to sleep per ultrasound reading
        for i in range(self._us_res):
            # set duty for both motors
            if not turning:
                self.l_pwm.ChangeDutyCycle(duty)
                self.r_pwm.ChangeDutyCycle(duty)
            else:
                self.l_pwm.ChangeDutyCycle(duty*turning[0])
                self.r_pwm.ChangeDutyCycle(duty*turning[1])

            GPIO.output(self.GPIO_RIGHT_PWM, True)
            GPIO.output(self.GPIO_LEFT_PWM, True)
            time.sleep(t)
            output.append(self.read_ultrasound())
            if output[i + 1] >= self._us_thres:  # if reading is greater than or equal to the thres
                score[k] += 1
            total_score = sum(score[k])
            if total_score <= self._min_score:
                # if there is not a significant amount of good, make it bad
                total_score = -total_score

        # set duty for both motors
        self.l_pwm.ChangeDutyCycle(0)
        self.r_pwm.ChangeDutyCycle(0)
        # update state, set last action taken and read ultrasound sensor
        self._state[0] = 0
        self._state[1] = output, score
        self._total_actions += total_score
        if self.testing:
            print(f"forwards: {d}")

        return total_score, output, score

if __name__ == "__main__":
    pibot = PiBot()
    pibot.run()


