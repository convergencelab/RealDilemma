import RPi.GPIO as GPIO
import time
import numpy as np
from threading import Thread
from src.Pi.PiBot.PiBot import PiBot
import socket

class PiBot2(PiBot):
    """
    more complexity added,
    improvements on resolution of ultrasound resolution
    change nature of turning

    UPDATE ultrasound as seperate thread
    """
    # variables for actions #
    # left and right motors, we can adjust this as we please #
    # set to 0.75 0.75 by default to prevent too intense of movement #
    TURN_PWM_CCW = 1.0, 1.0
    TURN_PWM_CW = 1.0, 1.0
    BACKWARDS_MOTOR_PWM = 1.0, 1.0
    FORWARDS_MOTOR_PWM = 1.0, 1.0
    STARTING_FACTOR = 100
    STOPPING_FACTOR = 5 # how slow to stop bot
    US_RES = 5
    US_THRES = 5
    MIN_SCORE = 5
    def __init__(self, us_res=US_RES,
                 us_thres=US_THRES,
                 min_score=MIN_SCORE,
                 turn_pwm_ccw = TURN_PWM_CCW,
                 turn_pwm_cw = TURN_PWM_CW,
                 backwards_motor_pwm = BACKWARDS_MOTOR_PWM,
                 forwards_motor_pwm = FORWARDS_MOTOR_PWM,
                 starting_factor=STARTING_FACTOR,
                 stopping_factor = STOPPING_FACTOR):
        super(PiBot2, self).__init__()
        # hyperparams for action #
        self._us_res = us_res # resolution for ultrasound reading (# of readings per action)
        self._us_thres = us_thres # threshold for a "bad distance" in the reading
        self._min_score = min_score # the minimum score for considering an series of actions bad
        self._turn_pwm_ccw = turn_pwm_ccw
        self._turn_pwm_cw = turn_pwm_cw
        self._backwards_motor_pwm = backwards_motor_pwm
        self._forwards_motor_pwm = forwards_motor_pwm
        self._starting_factor = starting_factor
        self._stopping_factor = stopping_factor
        # redefine the total actions as a int score #
        self._total_actions = 0
        # state is now just a 3-tuple
        self._state = np.zeros(3)
        self._ultrasound = 0
        self._start_ultrasound()
        # oh camera info #
        self.host = '192.168.2.43'  # Server ip
        self.port = 4000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.host, self.port))


    def reset(self):
        self._total_actions = 0
        # state is now just a 3-tuple
        self._state = np.zeros(3)
        self._ultrasound = 0

    def _start_ultrasound(self):
        """
        start thread for ultrasound
        :return: none
        """
        self.stop_us = False
        Thread(target=self._update_us, args=()).start()
        return self

    def _update_us(self):
        while True:
            if self.stop_us:
                return
            self._ultrasound = self.read_ultrasound()

    def _start_comm(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def _update_comm(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            data, addr = self.s.recvfrom(1024)
            data = data.decode('utf-8')
            print("Message from: " + str(addr))
            print("From connected user: " + data)
            data = data.upper()
            print("Sending: " + data)
            self.s.sendto(data.encode('utf-8'), addr)

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
        return self._travel(duty, n, self._forwards_motor_pwm, 0)

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
        return self._travel(duty, n, self._backwards_motor_pwm, 1)

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
        return self._travel(duty, n, self._turn_pwm_cw, 2)

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
        return self._travel(duty, n, self._turn_pwm_ccw, 3)

    def stop(self, duty, n):
        GPIO.output(self.GPIO_RIGHT_FORWARD, False)
        GPIO.output(self.GPIO_RIGHT_BACKWARD, False)
        GPIO.output(self.GPIO_LEFT_FORWARD, False)
        GPIO.output(self.GPIO_LEFT_BACKWARD, False)
        # time.sleep(n)
        self._travel(duty=0, n=n, pwm_thres=[0,0], action=4)


    def _travel(self, duty, n, pwm_thres, action):
        """
        helper function for forwards and backwards, left and right motion
        :param n:
        :param turning: contains amount of duty for l and right motor for turning
        :param duty:
        :param move_x: allow for smoother stopping in x travel
        :return:
        """
        us_readings = []
        us_readings.append(self.get_ultrasound())
        score = []
        if us_readings[0] >= self._us_thres:  # if reading is greater than or equal to the thres
            score.append(1)
        else:
            score.append(0)
        t = n / self._us_res  # time to sleep per ultrasound reading
        # actual travel time #
        for i in range(self._us_res-1):
            # set duty for both motors
            # pwm thres is hyper param that varies for each direction
            self.l_pwm.ChangeDutyCycle(duty*pwm_thres[0])
            self.r_pwm.ChangeDutyCycle(duty*pwm_thres[1])
            GPIO.output(self.GPIO_RIGHT_PWM, True)
            GPIO.output(self.GPIO_LEFT_PWM, True)
            time.sleep(t)
            GPIO.output(self.GPIO_RIGHT_PWM, False)
            GPIO.output(self.GPIO_LEFT_PWM, False)
            us = self.get_ultrasound()
            us_readings.append(us)
            if us >= self._us_thres:  # if reading is greater than or equal to the thres
                score.append(1)
            else:
                score.append(0)
            total_score = sum(score)
            #if total_score <= self._min_score:
                # if there is not a significant amount of good, make it bad
             #   total_score = -total_score

        # set duty for both motors
        self.l_pwm.ChangeDutyCycle(0)
        self.r_pwm.ChangeDutyCycle(0)
        self._total_actions+=total_score
        #self._total_actions = max(0, total_score+self._total_actions)
        # update state, set last action taken and read ultrasound sensor
        #self._state = 0, us_readings, score, total_score
        # self._state = {
        #     "action": np.int64(action),
        #     "us_readings": np.array(us_readings, dtype=np.float32),
        #     "score": np.array(score, dtype=np.float32),
        #     "total_score": np.array([total_score], dtype=np.float32)
        # }
        self._state[0] = action # action taken
        self._state[1] = sum(np.diff(us_readings)) # dx
        self._state[2] = sum(score)# sum of score for movement
        # return total_score, output, score

    def get_ultrasound(self):
        return self._ultrasound

    def _manually_calibrate_turn(self):
        #self.testing = True
        try:
            while True:
                cmd = input()
                cmd = cmd.split(" ")
                dir = cmd[0]
                duty = int(cmd[1])
                n = float(cmd[2])
                l = float(cmd[3])
                r = float(cmd[4])

                if dir == "cw":
                    self._turn_pwm_cw = l, r
                    self.turn_cw(duty, n)
                elif dir == "ccw":
                    self._turn_pwm_ccw = l, r
                    self.turn_ccw(duty, n)
                else:
                    print("incorrect cmd")

        except KeyboardInterrupt:
            self.testing = False
            exit()

    def _manually_calibrate_translation(self):

        while True:
            cmd = input()
            cmd = cmd.split(" ")
            dir = cmd[0]
            duty = int(cmd[1])
            n = float(cmd[2])
            l = float(cmd[3])
            r = float(cmd[4])


            if dir == "f":
                self._forwards_motor_pwm = l, r
                self.forward(duty, n)
            elif dir == "b":
                b = int(cmd[5])
                self._starting_factor = b
                self._backwards_motor_pwm = l, r
                self.backward(duty, n)
            else:
                print("incorrect cmd")
    def _autonomous_simple(self):
        while True:
            print(self.get_ultrasound())
            if self.get_ultrasound() <= 20:
                self.stop(1)
                self.backward(100, 1)
                self.turn_ccw(100, 0.5)
            else:
                self.forward(100, 0.1)

    def _test_ultrasound(self):
        while True:
            distance = self.get_ultrasound()
            print(f"US: {distance}")

    def _test(self):
        try:
            while True:
                cmd = input()
                cmd = cmd.split(" ")
                dir = cmd[0]
                n = int(cmd[1])
                duty = 100
                if dir == "f":
                    self.forward(duty, n)
                elif dir == "b":
                    self.backward(duty, n)
                elif dir == "cw":
                    self.turn_cw(duty, n)
                elif dir == "ccw":
                    self.turn_ccw(duty, n)
                else:
                    print("incorrect cmd")

        except KeyboardInterrupt:
            self.testing = False
            exit()