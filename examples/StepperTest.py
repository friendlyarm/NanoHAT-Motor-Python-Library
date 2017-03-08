#!/usr/bin/python
#import FriendlyELEC_NanoHatMotor, FriendlyELEC_DCMotor, FriendlyELEC_Stepper
from FriendlyELEC_NanoHatMotor import FriendlyELEC_NanoHatMotor, FriendlyELEC_DCMotor, FriendlyELEC_StepperMotor

import time
import atexit
import sys

if len(sys.argv) <= 1:
    print "Usage: python StepperTest.py <Motor port>"
    print "\tMotor port: 1~2"
    exit()

motorPort=int(sys.argv[1])
if motorPort<1 or motorPort>2:
    print "Wrong motor port, it must be 1~2."
    exit()

# create a default object, no changes to I2C address or frequency
mh = FriendlyELEC_NanoHatMotor()

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(FriendlyELEC_NanoHatMotor.RELEASE)
    mh.getMotor(2).run(FriendlyELEC_NanoHatMotor.RELEASE)
    mh.getMotor(3).run(FriendlyELEC_NanoHatMotor.RELEASE)
    mh.getMotor(4).run(FriendlyELEC_NanoHatMotor.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, motorPort)      # 200 steps/rev, motor port #1
myStepper.setSpeed(30)          # 30 RPM

while (True):
    print("Single coil steps")
    myStepper.step(100, FriendlyELEC_NanoHatMotor.FORWARD, FriendlyELEC_NanoHatMotor.SINGLE)
    myStepper.step(100, FriendlyELEC_NanoHatMotor.BACKWARD, FriendlyELEC_NanoHatMotor.SINGLE)

    print("Double coil steps")
    myStepper.step(100, FriendlyELEC_NanoHatMotor.FORWARD, FriendlyELEC_NanoHatMotor.DOUBLE)
    myStepper.step(100, FriendlyELEC_NanoHatMotor.BACKWARD, FriendlyELEC_NanoHatMotor.DOUBLE)

    print("Interleaved coil steps")
    myStepper.step(100, FriendlyELEC_NanoHatMotor.FORWARD, FriendlyELEC_NanoHatMotor.INTERLEAVE)
    myStepper.step(100, FriendlyELEC_NanoHatMotor.BACKWARD, FriendlyELEC_NanoHatMotor.INTERLEAVE)

    print("Microsteps")
    myStepper.step(100, FriendlyELEC_NanoHatMotor.FORWARD, FriendlyELEC_NanoHatMotor.MICROSTEP)
    myStepper.step(100, FriendlyELEC_NanoHatMotor.BACKWARD, FriendlyELEC_NanoHatMotor.MICROSTEP)
