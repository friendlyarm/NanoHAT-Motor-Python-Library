#!/usr/bin/python

from FriendlyELEC_PWM_Servo_Driver import PWM
import time

class FriendlyELEC_StepperMotor:
    MICROSTEPS = 8
    MICROSTEP_CURVE = [0, 50, 98, 142, 180, 212, 236, 250, 255]

    #MICROSTEPS = 16
    # a sinusoidal curve NOT LINEAR!
    #MICROSTEP_CURVE = [0, 25, 50, 74, 98, 120, 141, 162, 180, 197, 212, 225, 236, 244, 250, 253, 255]

    def __init__(self, controller, num, steps=200):
        self.MC = controller
        self.revsteps = steps
        self.motornum = num
        self.sec_per_step = 0.1
        self.steppingcounter = 0
        self.currentstep = 0

        num -= 1

        if (num == 0):
            self.PWMA = 0
            self.AIN2 = 1
            self.AIN1 = 2
            self.PWMB = 5
            self.BIN2 = 4
            self.BIN1 = 3
        elif (num == 1):
            self.PWMA = 15
            self.AIN2 = 14
            self.AIN1 = 13
            self.PWMB = 10
            self.BIN2 = 11
            self.BIN1 = 12
        else:
            raise NameError('NanoHat Stepper must be between 1 and 2 inclusive')

    def setSpeed(self, rpm):
        self.sec_per_step = 60.0 / (self.revsteps * rpm)
        self.steppingcounter = 0

    def oneStep(self, dir, style):
        pwm_a = pwm_b = 255

        # first determine what sort of stepping procedure we're up to
        if (style == FriendlyELEC_NanoHatMotor.SINGLE):
            if ((self.currentstep/(self.MICROSTEPS/2)) % 2):
                # we're at an odd step, weird
                if (dir == FriendlyELEC_NanoHatMotor.FORWARD):
                    self.currentstep += self.MICROSTEPS/2
                else:
                    self.currentstep -= self.MICROSTEPS/2
            else:
                # go to next even step
                if (dir == FriendlyELEC_NanoHatMotor.FORWARD):
                    self.currentstep += self.MICROSTEPS
                else:
                    self.currentstep -= self.MICROSTEPS
        if (style == FriendlyELEC_NanoHatMotor.DOUBLE):
            if not (self.currentstep/(self.MICROSTEPS/2) % 2):
                # we're at an even step, weird
                if (dir == FriendlyELEC_NanoHatMotor.FORWARD):
                    self.currentstep += self.MICROSTEPS/2
                else:
                    self.currentstep -= self.MICROSTEPS/2
            else:
                # go to next odd step
                if (dir == FriendlyELEC_NanoHatMotor.FORWARD):
                    self.currentstep += self.MICROSTEPS
                else:
                    self.currentstep -= self.MICROSTEPS
        if (style == FriendlyELEC_NanoHatMotor.INTERLEAVE):
            if (dir == FriendlyELEC_NanoHatMotor.FORWARD):
                self.currentstep += self.MICROSTEPS/2
            else:
                self.currentstep -= self.MICROSTEPS/2

        if (style == FriendlyELEC_NanoHatMotor.MICROSTEP):
            if (dir == FriendlyELEC_NanoHatMotor.FORWARD):
                self.currentstep += 1
            else:
                self.currentstep -= 1

                # go to next 'step' and wrap around
                self.currentstep += self.MICROSTEPS * 4
                self.currentstep %= self.MICROSTEPS * 4

            pwm_a = pwm_b = 0
            if (self.currentstep >= 0) and (self.currentstep < self.MICROSTEPS):
                pwm_a = self.MICROSTEP_CURVE[self.MICROSTEPS - self.currentstep]
                pwm_b = self.MICROSTEP_CURVE[self.currentstep]
            elif (self.currentstep >= self.MICROSTEPS) and (self.currentstep < self.MICROSTEPS*2):
                pwm_a = self.MICROSTEP_CURVE[self.currentstep - self.MICROSTEPS]
                pwm_b = self.MICROSTEP_CURVE[self.MICROSTEPS*2 - self.currentstep]
            elif (self.currentstep >= self.MICROSTEPS*2) and (self.currentstep < self.MICROSTEPS*3):
                pwm_a = self.MICROSTEP_CURVE[self.MICROSTEPS*3 - self.currentstep]
                pwm_b = self.MICROSTEP_CURVE[self.currentstep - self.MICROSTEPS*2]
            elif (self.currentstep >= self.MICROSTEPS*3) and (self.currentstep < self.MICROSTEPS*4):
                pwm_a = self.MICROSTEP_CURVE[self.currentstep - self.MICROSTEPS*3]
                pwm_b = self.MICROSTEP_CURVE[self.MICROSTEPS*4 - self.currentstep]


        # go to next 'step' and wrap around
        self.currentstep += self.MICROSTEPS * 4
        self.currentstep %= self.MICROSTEPS * 4

        # only really used for microstepping, otherwise always on!
        self.MC._pwm.setPWM(self.PWMA, 0, pwm_a*16)
        self.MC._pwm.setPWM(self.PWMB, 0, pwm_b*16)

        # set up coil energizing!
        coils = [0, 0, 0, 0]

        if (style == FriendlyELEC_NanoHatMotor.MICROSTEP):
            if (self.currentstep >= 0) and (self.currentstep < self.MICROSTEPS):
                coils = [1, 1, 0, 0]
            elif (self.currentstep >= self.MICROSTEPS) and (self.currentstep < self.MICROSTEPS*2):
                coils = [0, 1, 1, 0]
            elif (self.currentstep >= self.MICROSTEPS*2) and (self.currentstep < self.MICROSTEPS*3):
                coils = [0, 0, 1, 1]
            elif (self.currentstep >= self.MICROSTEPS*3) and (self.currentstep < self.MICROSTEPS*4):
                coils = [1, 0, 0, 1]
        else:
            step2coils = [     [1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1] ]
            coils = step2coils[self.currentstep/(self.MICROSTEPS/2)]

        #print "coils state = " + str(coils)
        self.MC.setPin(self.AIN2, coils[0])
        self.MC.setPin(self.BIN1, coils[1])
        self.MC.setPin(self.AIN1, coils[2])
        self.MC.setPin(self.BIN2, coils[3])

        return self.currentstep

    def step(self, steps, direction, stepstyle):
        s_per_s = self.sec_per_step
        lateststep = 0

        if (stepstyle == FriendlyELEC_NanoHatMotor.INTERLEAVE):
            s_per_s = s_per_s / 2.0
        if (stepstyle == FriendlyELEC_NanoHatMotor.MICROSTEP):
            s_per_s /= self.MICROSTEPS
            steps *= self.MICROSTEPS

        print s_per_s, " sec per step"

        for s in range(steps):
            lateststep = self.oneStep(direction, stepstyle)
            time.sleep(s_per_s)

        if (stepstyle == FriendlyELEC_NanoHatMotor.MICROSTEP):
            # this is an edge case, if we are in between full steps, lets just keep going
            # so we end on a full step
            while (lateststep != 0) and (lateststep != self.MICROSTEPS):
                lateststep = self.oneStep(dir, stepstyle)
                time.sleep(s_per_s)

class FriendlyELEC_DCMotor:
    def __init__(self, controller, num):
        self.MC = controller
        self.motornum = num
        pwm = in1 = in2 = 0

        if (num == 0):
            pwm = 0     #8
            in2 = 1     #9
            in1 = 2     #10
        elif (num == 1):
            pwm = 5     #13
            in2 = 4     #12
            in1 = 3     #11
        elif (num == 2):
            pwm = 15    #2
            in2 = 14    #3
            in1 = 13    #4
        elif (num == 3):
            pwm = 10    #7
            in2 = 11    #6
            in1 = 12    #5
        else:
            raise NameError('NanoHat Motor must be between 1 and 4 inclusive')
        self.PWMpin = pwm
        self.IN1pin = in1
        self.IN2pin = in2

    def run(self, command):
        if not self.MC:
            return
        if (command == FriendlyELEC_NanoHatMotor.FORWARD):
            self.MC.setPin(self.IN2pin, 0)
            self.MC.setPin(self.IN1pin, 1)
        if (command == FriendlyELEC_NanoHatMotor.BACKWARD):
            self.MC.setPin(self.IN1pin, 0)
            self.MC.setPin(self.IN2pin, 1)
        if (command == FriendlyELEC_NanoHatMotor.RELEASE):
            self.MC.setPin(self.IN1pin, 0)
            self.MC.setPin(self.IN2pin, 0)
    def setSpeed(self, speed):
        if (speed < 0):
            speed = 0
        if (speed > 255):
            speed = 255
        self.MC._pwm.setPWM(self.PWMpin, 0, speed*16)

class FriendlyELEC_NanoHatMotor:
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3
    RELEASE = 4

    SINGLE = 1
    DOUBLE = 2
    INTERLEAVE = 3
    MICROSTEP = 4

    def __init__(self, addr = 0x60, freq = 1600):
        self._i2caddr = addr            # default addr on HAT
        self._frequency = freq        # default @1600Hz PWM freq
        self.motors = [FriendlyELEC_DCMotor(self, m) for m in range(4)]
        self.steppers = [FriendlyELEC_StepperMotor(self, 1), FriendlyELEC_StepperMotor(self, 2)]
        self._pwm =  PWM(addr, debug=False)
        self._pwm.setPWMFreq(self._frequency)

    def setPin(self, pin, value):
        if (pin < 0) or (pin > 15):
            raise NameError('PWM pin must be between 0 and 15 inclusive')
        if (value != 0) and (value != 1):
            raise NameError('Pin value must be 0 or 1!')
        if (value == 0):
            self._pwm.setPWM(pin, 0, 4096)
        if (value == 1):
            self._pwm.setPWM(pin, 4096, 0)

    def getStepper(self, steps, num):
        if (num < 1) or (num > 2):
            raise NameError('NanoHat Stepper must be between 1 and 2 inclusive')
        return self.steppers[num-1]

    def getMotor(self, num):
        if (num < 1) or (num > 4):
            raise NameError('NanoHat Motor must be between 1 and 4 inclusive')
        return self.motors[num-1]
