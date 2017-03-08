#!/usr/bin/python

from FriendlyELEC_NanoHatMotor import FriendlyELEC_PWM_Servo_Driver
import time
import sys

if len(sys.argv) <= 1:
    print "Usage: python ServoTest.py <PWM port>"
    print "\tPWM port: 6~9"
    exit()

servonum=int(sys.argv[1])
if servonum<6 or servonum>9:
    print "Wrong PWM port, it must be 6~9."
    exit()

SERVOMIN=150
SERVOMAX=600

pwm=FriendlyELEC_PWM_Servo_Driver.PWM(0x60, debug=False)
pwm.setPWMFreq(60)

while (True):
	for pulselen in range(SERVOMIN,SERVOMAX):
		pwm.setPWM(servonum, 0, pulselen)

	time.sleep(0.5)

	for pulselen in reversed(range(SERVOMIN,SERVOMAX)):
        	pwm.setPWM(servonum, 0, pulselen)

	time.sleep(0.5)
