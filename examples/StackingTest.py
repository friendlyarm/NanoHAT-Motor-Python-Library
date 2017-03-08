#!/usr/bin/python
from FriendlyELEC_NanoHatMotor import FriendlyELEC_NanoHatMotor, FriendlyELEC_DCMotor, FriendlyELEC_StepperMotor
import time
import atexit
import threading
import random

# bottom hat is default address 0x60
bottomhat = FriendlyELEC_NanoHatMotor(addr=0x60)
# top hat has A0 jumper closed, so its address 0x61
tophat = FriendlyELEC_NanoHatMotor(addr=0x61)

# create empty threads (these will hold the stepper 1, 2 & 3 threads)
stepperThreads = [threading.Thread(), threading.Thread(), threading.Thread()]

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    tophat.getMotor(1).run(FriendlyELEC_NanoHatMotor.RELEASE)
    tophat.getMotor(2).run(FriendlyELEC_NanoHatMotor.RELEASE)
    tophat.getMotor(3).run(FriendlyELEC_NanoHatMotor.RELEASE)
    tophat.getMotor(4).run(FriendlyELEC_NanoHatMotor.RELEASE)
    bottomhat.getMotor(1).run(FriendlyELEC_NanoHatMotor.RELEASE)
    bottomhat.getMotor(2).run(FriendlyELEC_NanoHatMotor.RELEASE)
    bottomhat.getMotor(3).run(FriendlyELEC_NanoHatMotor.RELEASE)
    bottomhat.getMotor(4).run(FriendlyELEC_NanoHatMotor.RELEASE)

atexit.register(turnOffMotors)

myStepper1 = bottomhat.getStepper(200, 1)      # 200 steps/rev, motor port #1
myStepper2 = bottomhat.getStepper(200, 2)      # 200 steps/rev, motor port #2
myStepper3 = tophat.getStepper(200, 1)      # 200 steps/rev, motor port #1

myStepper1.setSpeed(60)          # 60 RPM
myStepper2.setSpeed(30)          # 30 RPM
myStepper3.setSpeed(15)          # 15 RPM

# get a DC motor!
myMotor = tophat.getMotor(3)
# set the speed to start, from 0 (off) to 255 (max speed)
myMotor.setSpeed(150)
# turn on motor
myMotor.run(FriendlyELEC_NanoHatMotor.FORWARD);


stepstyles = [FriendlyELEC_NanoHatMotor.SINGLE, FriendlyELEC_NanoHatMotor.DOUBLE, FriendlyELEC_NanoHatMotor.INTERLEAVE]
steppers = [myStepper1, myStepper2, myStepper3]

def stepper_worker(stepper, numsteps, direction, style):
    #print("Steppin!")
    stepper.step(numsteps, direction, style)
    #print("Done")

while (True):
    for i in range(3):
        if not stepperThreads[i].isAlive():
            randomdir = random.randint(0, 1)
            print("Stepper %d" % i),
            if (randomdir == 0):
                            dir = FriendlyELEC_NanoHatMotor.FORWARD
                            print("forward"),
            else:
                            dir = FriendlyELEC_NanoHatMotor.BACKWARD
                print("backward"),
            randomsteps = random.randint(10,50)
            print("%d steps" % randomsteps)
            stepperThreads[i] = threading.Thread(target=stepper_worker, args=(steppers[i], randomsteps, dir, stepstyles[random.randint(0,len(stepstyles)-1)],))
            stepperThreads[i].start()

            # also, lets switch around the DC motor!
            myMotor.setSpeed(random.randint(0,255))  # random speed
            #myMotor.run(random.randint(0,1)) # random forward/back
