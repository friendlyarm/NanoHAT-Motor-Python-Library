#!/usr/bin/python
from FriendlyELEC_NanoHatMotor import FriendlyELEC_NanoHatMotor, FriendlyELEC_DCMotor, FriendlyELEC_StepperMotor
import time
import atexit
import threading
import random

# create a default object, no changes to I2C address or frequency
mh = FriendlyELEC_NanoHatMotor()

# create empty threads (these will hold the stepper 1 and 2 threads)
st1 = threading.Thread()
st2 = threading.Thread()


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(FriendlyELEC_NanoHatMotor.RELEASE)
    mh.getMotor(2).run(FriendlyELEC_NanoHatMotor.RELEASE)
    mh.getMotor(3).run(FriendlyELEC_NanoHatMotor.RELEASE)
    mh.getMotor(4).run(FriendlyELEC_NanoHatMotor.RELEASE)

atexit.register(turnOffMotors)

myStepper1 = mh.getStepper(200, 1)      # 200 steps/rev, motor port #1
myStepper2 = mh.getStepper(200, 2)      # 200 steps/rev, motor port #2
myStepper1.setSpeed(60)          # 30 RPM
myStepper2.setSpeed(60)          # 30 RPM


stepstyles = [FriendlyELEC_NanoHatMotor.SINGLE, FriendlyELEC_NanoHatMotor.DOUBLE, FriendlyELEC_NanoHatMotor.INTERLEAVE, FriendlyELEC_NanoHatMotor.MICROSTEP]

def stepper_worker(stepper, numsteps, direction, style):
    #print("Steppin!")
    stepper.step(numsteps, direction, style)
    #print("Done")

while (True):
    if not st1.isAlive():
        randomdir = random.randint(0, 1)
        print("Stepper 1"),
        if (randomdir == 0):
            dir = FriendlyELEC_NanoHatMotor.FORWARD
            print("forward"),
        else:
            dir = FriendlyELEC_NanoHatMotor.BACKWARD
            print("backward"),
        randomsteps = random.randint(10,50)
        print("%d steps" % randomsteps)
        st1 = threading.Thread(target=stepper_worker, args=(myStepper1, randomsteps, dir, stepstyles[random.randint(0,3)],))
        st1.start()

    if not st2.isAlive():
        print("Stepper 2"),
        randomdir = random.randint(0, 1)
        if (randomdir == 0):
            dir = FriendlyELEC_NanoHatMotor.FORWARD
            print("forward"),
        else:
            dir = FriendlyELEC_NanoHatMotor.BACKWARD
            print("backward"),

        randomsteps = random.randint(10,50)
        print("%d steps" % randomsteps)

        st2 = threading.Thread(target=stepper_worker, args=(myStepper2, randomsteps, dir, stepstyles[random.randint(0,3)],))
        st2.start()
