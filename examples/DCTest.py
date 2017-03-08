#!/usr/bin/python
from FriendlyELEC_NanoHatMotor import FriendlyELEC_NanoHatMotor, FriendlyELEC_DCMotor

import time
import atexit
import sys

if len(sys.argv) <= 1:
    print "Usage: python DCTest.py <Motor port>"
    print "\tMotor port: 1~4"
    exit()

motorPort=int(sys.argv[1])
if motorPort<1 or motorPort>4:
    print "Wrong motor port, it must be 1~4."
    exit()

# create a default object, no changes to I2C address or frequency
mh = FriendlyELEC_NanoHatMotor(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(FriendlyELEC_NanoHatMotor.RELEASE)
    mh.getMotor(2).run(FriendlyELEC_NanoHatMotor.RELEASE)
    mh.getMotor(3).run(FriendlyELEC_NanoHatMotor.RELEASE)
    mh.getMotor(4).run(FriendlyELEC_NanoHatMotor.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
myMotor = mh.getMotor(motorPort)

# set the speed to start, from 0 (off) to 255 (max speed)
myMotor.setSpeed(150)
myMotor.run(FriendlyELEC_NanoHatMotor.FORWARD);
# turn on motor
myMotor.run(FriendlyELEC_NanoHatMotor.RELEASE);


while (True):
    print "Forward! "
    myMotor.run(FriendlyELEC_NanoHatMotor.FORWARD)

    print "\tSpeed up..."
    for i in range(255):
        myMotor.setSpeed(i)
        time.sleep(0.01)

    print "\tSlow down..."
    for i in reversed(range(255)):
        myMotor.setSpeed(i)
        time.sleep(0.01)

    print "Backward! "
    myMotor.run(FriendlyELEC_NanoHatMotor.BACKWARD)

    print "\tSpeed up..."
    for i in range(255):
        myMotor.setSpeed(i)
        time.sleep(0.01)

    print "\tSlow down..."
    for i in reversed(range(255)):
        myMotor.setSpeed(i)
        time.sleep(0.01)

    print "Release"
    myMotor.run(FriendlyELEC_NanoHatMotor.RELEASE)
    time.sleep(1.0)
